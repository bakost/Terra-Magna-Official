import discord

from config import texrole, admins, idserver
from discord import app_commands
from discord.ext import commands

class pingSC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx) -> None:
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send(f"Synced {len(fmt)} commands.")

    @app_commands.command(name="test1", description="test command")
    async def test(self, interaction: discord.Interaction, question: str):
        await interaction.response.send_message(f"test command: {question}")


async def setup(bot):
    await bot.add_cog(pingSC(bot), guilds=[discord.Object(id=idserver)])