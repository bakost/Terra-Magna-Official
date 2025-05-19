import discord

from discord.ext import commands
from connectmysql import connection
from config import adminrole

class bdrestart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['bd'], pass_context=True)
    async def __bd(self, ctx):
        role = discord.utils.get(ctx.guild.roles, id=adminrole)
        if role in ctx.author.roles:
            connection.connect()
            await ctx.send(f"Соединение восстановлено!")
        else:
            await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор!")

async def setup(bot):
    await bot.add_cog(bdrestart(bot))