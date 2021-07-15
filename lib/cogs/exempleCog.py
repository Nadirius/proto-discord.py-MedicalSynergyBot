from discord.ext.commands import command, Cog
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)


class ExampleCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("exempleCog")

    @command(name="lol")
    async def button(self, ctx):
        await ctx.send(
            """```diff
+ Selectionez votre métier :
        ```""",
            components=[
                [
                    Button(style=ButtonStyle.grey, label="EMOJI", emoji="😂"),
                    Button(style=ButtonStyle.green, label="GREEN"),
                    Button(style=ButtonStyle.red, label="RED"),
                    Button(style=ButtonStyle.grey, label="GREY"),
                ],
                Button(style=ButtonStyle.blue, label="BLUE"),
                Button(style=ButtonStyle.URL, label="URL", url="https://www.example.com"),
            ]
        )

        while True:
            interaction = await self.bot.wait_for("button_click")
            await interaction.respond(content=f"{interaction.component.label} clicked!")

    @command(name="sel1")
    async def select_cog(self, ctx):
        await ctx.send(
            "Here is an example of a select",
            components=[
                Select(
                    placeholder="You can select up to 2",
                    max_values=2,
                    options=[
                        SelectOption(label="a", value="A"),
                        SelectOption(label="b", value="B"),
                    ],
                ),
                Select(
                    min_values=2,
                    max_values=3,
                    options=[
                        SelectOption(label="a", value="A"),
                        SelectOption(label="b", value="B"),
                        SelectOption(label="c", value="C"),
                    ],
                ),
                Select(
                    disabled=False,
                    options=[
                        SelectOption(label="a", value="A"),
                    ],
                ),
            ],
        )

        while True:
            interaction = await self.bot.wait_for("select_option")
            await interaction.respond(
                content=f"{', '.join(map(lambda x: x.label, interaction.component))} selected!"
            )


def setup(bot):
    bot.add_cog(ExampleCog(bot))
