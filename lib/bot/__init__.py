from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.triggers.cron import CronTrigger
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase, NotOwner
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
                                  CommandOnCooldown)
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import when_mentioned_or
from discord import Embed, File

from discord.ext.commands import Bot
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType, Select, SelectOption
from asyncio import TimeoutError

from ..db import db

PREFIX = "+"
OWNER_IDS = [494435090084921346]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


#
# def get_prefix(bot, message):
#     prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
#     return when_mentioned_or(prefix)(bot, message)


# Cog loading handller (tous les cog doivent etre charger avant de rendre le bot ready
class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.VERSION = None
        self.TOKEN = None

        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.stdout = None

        self.scheduler = AsyncIOScheduler()
        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=self.PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all())

    def setup_cogs(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")
        print("setup cogs complete")

    def run(self, version):
        self.VERSION = version

        print("running setup cogs...")
        self.setup_cogs()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def rules_reminder(self):
        await self.stdout.send("Rember to adhere to the rules")

    async def on_connect(self):
        print(" bot connected")

    async def on_disconnect(self):
        print(" bot disconnected")

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(863522945514209281)
            self.stdout = self.get_channel(864618749944791051)
            # Rappelle 4 fois par secondes
            # self.scheduler.add_job(self.rules_reminder, CronTrigger(second="0,15,30,45"))
            # Rappel chaque semaine
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()
            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            await self.stdout.send("Now online !")

            print(" bot ready")

            message = """
            _
            Bonjour,

            Je m'appelle Medina, je suis votre assistante de premier niveau sur la plateforme **Hospital Synergy**.

            Hospital Synergy permet au personnel hospitalier du monde entier d'analyser et de collaborer sur les cas complexes de manière asynchrone et organisée.

            Bien que je parle du monde entier, je ne sors pas du cadre. En effet, je pars du principe d'ouvrir le monde entier au personnel de l'hôpital du valais, l'objet de ma raison d'être.

            Afin de vous ouvrir l'accés, je dois procéder à votre inscription. Pour ce faire, je vous ai contacté à travers un message privé.

            Je vous attends !

            A tout de suite.
            _
            """
            embed = Embed(title="Bienvenu dans la plateforme Hospital Synergy", description=message,
                          colour=0xFF0000)
            embed.set_author(name="Medina", icon_url=self.user.avatar_url)
            embed.set_footer(text="Devellopée au sein de la HES-VS - Lifecycle management des SI.")
            #await self.get_channel(863522946496725055).send(embed=embed)

        else:
            print(" bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is not None:  # and ctx.guild is not None:
            if self.ready:
                # await self.invoke(ctx)
                await super().process_commands(message)
            else:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds")

    async def on_error(self, event_method, *args, **kwargs):
        if event_method == "on_command_error":
            channel = args[0]
            await channel.send("Something went wrong.")

        await self.stdout.send("An error occured.!")

        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, err) for err in IGNORE_EXCEPTIONS]):
            pass
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required  arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs.")

        elif isinstance(exc, NotOwner):
            await ctx.send('Reserved command. Sorry!')

        elif hasattr(exc, "original"):
            if isinstance(exc.original, HTTPException):
                await ctx.send("Unable to send message.")

            elif isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permission to do that")

            elif isinstance(exc.original, ValueError):
                await ctx.send("Invalid argument of command.")

            else:
                raise exc.original
        else:
            raise exc


bot = Bot()



