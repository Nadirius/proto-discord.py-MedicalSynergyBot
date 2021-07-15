from typing import Optional

from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext.commands import command


def syntax(command):
    # retournera example|alias <required> [optional]
    #print(command.aliases)
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []
    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            #print(key)
            # declarer un param Optional[str, autreType] est convertit en Union[str, NoneType]
            # Pour pouvoir détecter les param optional on les track avec le NoneType ajouté par Optional
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)
    #return f"`{cmd_and_aliases} {params}`"
    return f"```{cmd_and_aliases} {params}```"
    # return f"```{command}{f'|{cmd_and_aliases}' if len(cmd_and_aliases) > 0 else ''}{f' {params}' if len(params) > 0 else ''}```"


class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
       # print("1 " +  str(data))
        self.ctx = ctx

        super().__init__(data, per_page=3)

    #called automatiquement
    async def write_page(self, menu, fields=[]):
        print(self.ctx)
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(title="Help",
                      description="Welcome to the Diana help dialog!",
                      colour=self.ctx.author.colour)
        embed.set_thumbnail(url=self.ctx.me.avatar_url)
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset + self.per_page - 1):,} of {len_data:,} commands.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, commands):

        fields = []
        for entry in commands:
            fields.append((entry.help or "No description", syntax(entry)))

        return await self.write_page(menu, fields)


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with `{command}`",
                      # description=syntax(command),
                      colour=ctx.author.color)
        embed.add_field(name="Syntax", value=syntax(command))
        embed.add_field(name="Command description", value=command.help)
        await ctx.send(embed=embed)

    @command(name="help", brief="Brief")
    async def show_help(self, ctx, cmd: Optional[str]):
        """Shows this message."""
        if cmd is None:
            menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),
                             clear_reactions_after=True,
                             delete_message_after=True,
                             timeout=60.0)

            await menu.start(ctx)
        else:
            if command := get(self.bot.commands, name=cmd):
                await self.cmd_help(ctx, command)
            else:
                await ctx.send("That command does not exist.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot):
    bot.add_cog(Help(bot))
