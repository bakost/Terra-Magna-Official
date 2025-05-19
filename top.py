import discord

from discord.ext import commands
from connectmysql import connection, cursor
from config import smile

class top(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['top'], pass_context=True)
    async def __top(self, ctx):
        connection.connect()
        embed = discord.Embed(
            title="Terra Magna | ВПИ (Топ игроков по количеству монет)",
            description=f"Это топ игроков по количеству монет на сервере Terra Magna",
            color = 0x00BFFF,
        )
        cursor.execute(f"SELECT name, cash FROM `{ctx.author.guild.id}` ORDER BY cash DESC")
        reco = cursor.fetchall()
        for row in reco:
            if row[1] > 0:
                embed.add_field(name=f"{row[0]}", value=f"{row[1]}{smile}", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(top(bot))