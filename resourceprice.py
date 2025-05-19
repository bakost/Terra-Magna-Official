import discord

from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor
from config import res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, res12, res13, res14, smile1, smile2, smile3, smile4, smile5, smile6, smile7, smile8, smile9, smile10, smile11, smile12, smile13, smile14

class resourceprice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['market'], pass_context=True)
    async def __market(self, ctx, *, args=None):
        connection.connect()
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}**, введите название государства, у которого хотите посмотреть экономику!")
            return

        namer = title(args.split()[0])

        cursor.execute(f"SELECT res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, res12, res13, res14 FROM {ctx.author.guild.id}_economy WHERE name = '{namer}' and type = 'Покупка'")
        reco = cursor.fetchall()[0]
        cursor.execute(f"SELECT res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, res12, res13, res14 FROM {ctx.author.guild.id}_economy WHERE name = '{namer}' and type = 'Продажа'")
        reco1 = cursor.fetchall()[0]
        cursor.execute(f"SELECT res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, res12, res13, res14 FROM {ctx.author.guild.id}_economy WHERE name = '{namer}' and type = 'Количество'")
        reco2 = cursor.fetchall()[0]
        embed = discord.Embed(
            title=f"""Terra Magna | ВПИ (Ресурсы)""",
            description = f"""""",
            color = 0x00BFFF
        )
        embed.add_field(name=f"""Ресурс:""", value=f"""
        {res1} {smile1}:  
        {res2} {smile2}: 
        {res3} {smile3}: 
        {res4} {smile4}: 
        {res5} {smile5}: 
        {res6} {smile6}: 
        {res7} {smile7}: 
        {res8} {smile8}: 
        {res9} {smile9}: 
        {res10} {smile10}: 
        {res11} {smile11}: 
        {res12} {smile12}: 
        {res13} {smile13}: 
        {res14} {smile14}:
        """, inline=True)
        embed.add_field(name=f"""Цена:""", value=f"""
    {reco[0]} 
    {reco[1]} 
    {reco[2]}
    {reco[3]} 
    {reco[4]}
    {reco[5]} 
    {reco[6]}
    {reco[7]} 
    {reco[8]} 
    {reco[9]} 
    {reco[10]} 
    {reco[11]} 
    {reco[12]} 
    {reco[13]} 
        """, inline=True)
        embed.add_field(name=f"""Количество:""", value=f"""
    {reco2[0]} 
    {reco2[1]} 
    {reco2[2]}
    {reco2[3]}
    {reco2[4]}
    {reco2[5]} 
    {reco2[6]} 
    {reco2[7]} 
    {reco2[8]} 
    {reco2[9]} 
    {reco2[10]} 
    {reco2[11]} 
    {reco2[12]}
    {reco2[13]}
        """, inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(resourceprice(bot))