from datetime import datetime
from typing import Optional

from aiohttp import request
from discord import Forbidden, Embed, File, Member
from discord.ext.commands import Cog, command, has_permissions, CheckFailure, cooldown, BucketType
from discord_components import ButtonStyle, Button, InteractionType, SelectOption, Select

from lib.db import db

from lib.utils.codeGenerator import get_password
from lib.utils.mailto import mailto


class HaveFun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("haveFun")

    @command(name="def")
    @cooldown(1, 60, BucketType.user)
    async def get_def(self, ctx, word: str, lg: str = "en"):
        try:
            URL = f"https://api.dictionaryapi.dev/api/v2/entries/{lg}/{word}"
            async with request("GET", URL, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = Embed(title=f"{word.capitalize().title()}",
                                  description=f"{data[0]['meanings'][0]['definitions'][0]['definition']}",
                                  colour=ctx.author.colour, timestamp=datetime.utcnow())
                    embed.set_footer(text="Powered from Free Dictionary API")
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"No definition found for {word.capitalize()}.")
        except Exception as ex:
            pass

    @command(name="slap", aliases=["hit"])
    @cooldown(1, 15, BucketType.guild)
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        await ctx.send(f"{ctx.author.mention} slapped {member.display_name} {reason} !")


def setup(bot):
    bot.add_cog(HaveFun(bot))
