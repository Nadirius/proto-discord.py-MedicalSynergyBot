import discord
from discord import Embed
from discord.ext.commands import Cog, command
from discord_components import Button, ButtonStyle, InteractionType


# menu_features : {
#     1 : creer_cas()
#     2 : ouvrir_cas()
#     3 : fermer_cas()
#
#     5: Chercher_medecin()
#     6: Chercher_domaine()
#     7: Chercher_hopital()
#
# }


class Menu(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("menu")

    @command(name="menu2")
    async def menu(self, ctx):

        case_button_1 = Button(style=ButtonStyle.blue, label="1", id="embed1")
        case_button_2 = Button(style=ButtonStyle.blue, label="2", id="embed2")
        case_button_3 = Button(style=ButtonStyle.blue, label="3", id="embed3")
        case_button_4 = Button(style=ButtonStyle.blue, label="4", id="embed4")
        invite = Button(style=ButtonStyle.URL, label="Invite here", url="https://discord.gg/NGMk8MkWSU")

        embed1 = Embed(title="Menu 1", Description="", colour=discord.Colour.greyple())
        embed2 = Embed(title="Menu 2", Description="", colour=discord.Colour.greyple())
        embed3 = Embed(title="Menu 3", Description="", colour=discord.Colour.greyple())
        embed4 = Embed(title="Menu 4", Description="", colour=discord.Colour.greyple())

        await ctx.send(
            """```diff
+ Selectionez votre métier :
         ```""",
            components=[
                [case_button_1, case_button_2],
                [case_button_4, case_button_3],
                [invite]

            ])

        buttons = {
            "embed1": embed1,
            "embed2": embed2,
            "embed3": embed3,
            "embed4": embed4,
        }

        while True:
            event = await self.bot.wait_for("button_click")
            response = buttons.get(event.component.id)
            if response is None:
                await event.channel.send("Something went wrong. Please Try again")
            if event.channel == ctx.channel:
                await event.response(
                    type=InteractionType.ChannelMessageWithSource,
                    embed=response
                )


@command(name="menu")
async def menu(self, ctx):
    await ctx.send(
        """```diff
+ Click :
        ```""",
        components=[
            [
                Button(style=ButtonStyle.blue,
                       label="1"),
                Button(style=ButtonStyle.blue, label="2"),
                Button(style=ButtonStyle.blue, label="3"),
                Button(style=ButtonStyle.blue, label="4"),
            ],
            [
                Button(style=ButtonStyle.green, label="BLUE"),
                Button(style=ButtonStyle.green, label="URL", url="https://www.example.com"),
            ]

        ]

    )

    while True:
        interaction = await self.bot.wait_for("button_click")
        await interaction.respond(content=f"{interaction.component.label} clicked!")


def setup(bot):
    bot.add_cog(Menu(bot))
