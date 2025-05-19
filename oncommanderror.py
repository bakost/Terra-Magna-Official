import discord
import datetime

from discord.ext import commands

class oncommanderror(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        member = ctx.message.author
        if isinstance(error, commands.CommandOnCooldown):
            retry_after = str(datetime.timedelta(seconds=error.retry_after)).split('.')[0]
            await ctx.send(f"{member.mention}, не так быстро! Попробуйте использовать команду повторно через {retry_after}")

async def setup(bot):
    await bot.add_cog(oncommanderror(bot))