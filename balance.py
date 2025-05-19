import discord

from discord.ext import commands
from connectmysql import connection, cursor
from config import res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, smile, smile1, smile2, smile3, smile4, smile5, smile6, smile7, smile8, smile9, smile10, smile11

class balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['balance','cash','bal', 'money'], pass_context=True)
    async def __balance(self, ctx, member: discord.Member = None):
        connection.connect()
        if member is None:
            cursor.execute(f"SELECT cash FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row1 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res1 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row2 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res2 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row3 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res3 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row4 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res4 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row5 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res5 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row6 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res6 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row7 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res7 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row8 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res8 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row9 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res9 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row10 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res10 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row11 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res11 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            row12 = cursor.fetchone()[0]


            embed = discord.Embed(
                description = f"""Монеты: {row1} {smile} 
                {res1}: {row2} {smile1} 
                {res2}: {row3} {smile2} 
                {res3}: {row4} {smile3} 
                {res4}: {row5} {smile4} 
                {res5}: {row6} {smile5} 
                {res6}: {row7} {smile6} 
                {res7}: {row8} {smile7} 
                {res8}: {row9} {smile8} 
                {res9}: {row10} {smile9}
                {res10}: {row11} {smile10}
                {res11}: {row12} {smile11}""",
                color = 0x00BFFF
            )
            #embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            cursor.execute(f"SELECT cash FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row1 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res1 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row2 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res2 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row3 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res3 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row4 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res4 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row5 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res5 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row6 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res6 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row7 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res7 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row8 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res8 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row9 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res9 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row10 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res10 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row11 = cursor.fetchone()[0]
            cursor.execute(f"SELECT res11 FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
            row12 = cursor.fetchone()[0]


            embed = discord.Embed(
                description = f"""Монеты: {row1} {smile} 
                {res1}: {row2} {smile1} 
                {res2}: {row3} {smile2} 
                {res3}: {row4} {smile3} 
                {res4}: {row5} {smile4} 
                {res5}: {row6} {smile5} 
                {res6}: {row7} {smile6} 
                {res7}: {row8} {smile7} 
                {res8}: {row9} {smile8} 
                {res9}: {row10} {smile9}
                {res10}: {row11} {smile10}
                {res11}: {row12} {smile11}""",
                color = 0x00BFFF
            )
            #embed.set_author(name=member.display_name, icon_url=member.avatar_url)
            await ctx.send(embed = embed)


async def setup(bot):
    await bot.add_cog(balance(bot))