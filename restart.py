import discord
import asyncio

from discord.ext import commands
from numpy.core.defchararray import title
from config import texrole, admins

class restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['restart'], pass_context=True)
    async def __restart(self, ctx):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            try:
                await ctx.send(f"**{ctx.message.author.mention}**, вы уверены, что нужно перезапустить бота? (P.S. перезапуск 2 раза подряд = выключение бота)")
                message = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id and m.channel == ctx.channel, timeout=30.0)

            except asyncio.TimeoutError:
                await ctx.send(f"**{ctx.message.author.mention}**, вы слишком долго отвечали.")

            otvet = title(message.content.lower())

            if otvet == "Да":
                await ctx.send(f"**{ctx.message.author.mention}**, перезапуск бота.")
                await self.bot.close()
        else:
            await ctx.send(f"**{ctx.message.author.mention}**, перезапуск бота доступен только <@{admin0}>, <@{admin1}>, <@{admin2}>, <@{admin3}>!")

async def setup(bot):
    await bot.add_cog(restart(bot))