from datetime import datetime
from typing import Optional

from aiohttp import request
from discord import Forbidden, Embed, File, Member
from discord.ext import commands
from discord.ext.commands import Cog, command, has_permissions, CheckFailure, cooldown, BucketType
from discord_components import ButtonStyle, Button, InteractionType, SelectOption, Select

from lib.db import db

from lib.utils.codeGenerator import get_password
from lib.utils.mailto import mailto


class Cockpit(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("cockpit")

    @command(name="clear_db")
    @commands.is_owner()
    async def _(self, ctx):
        for i in ("STAFF", "CAS", "CAS_STAFF", "SPE_STAFF"):
            db.execute_(f"DELETE FROM {i}")

    @command(name="do_test")  # open plateform
    @commands.is_owner()
    async def test(self, ctx, *arg):
        print("hello")
        print(db.records_("SELECT * FROM STAFF"))
        print(db.records_("SELECT * FROM SPE_STAFF"))
        print(db.column_("SELECT st_id FROM SPE_STAFF"))
        print(db.field("SELECT st_code FROM STAFF WHERE st_id = ?", ctx.author.id))

    @command(name="clear")
    @commands.is_owner()
    async def vide_salon(self, ctx):
        async for msg in ctx.channel.history(limit=1000):
            await msg.delete()

    @command(name="user_test")
    async def _(self, ctx):
        member = await self.bot.guild.fetch_member(ctx.author.id)
        await member.edit(nick="Nadir Zemrani")


def setup(bot):
    bot.add_cog(Cockpit(bot))
