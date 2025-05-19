import discord

from discord.ext import commands
from connectmysql import connection, cursor
from config import smile, sh

class rsell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['rsell'], pass_context=True)
    async def __rsell(self, ctx, *, args=None):
        connection.connect()
        if args is None:
            await ctx.send(f"Введите id и количество ресурса, которые вы хотите продать!")
            return

        namer = str(args.split()[0])
        kolvor = float(args.split()[1])

        namer = int(namer)

        if kolvor < 1:
            await ctx.send(f"**{ctx.message.author.mention}**, указанное количество меньше 0.")
            return

        if kolvor > 100:
            await ctx.send(f"**{ctx.message.author.mention}**, указанное количество больше 100.")
            return

        cursor.execute(f"SELECT res{namer} FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco1 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res{namer} FROM {ctx.author.guild.id}_economy WHERE id = 2")
        reco = float(cursor.fetchone()[0])

        sumtrat = kolvor*reco
        procent = kolvor*0.25

        if kolvor > reco1:
            await ctx.send(f"У вас не достаточно ресурсов!")
            return

        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash + {sumtrat} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res{namer} = res{namer} - {kolvor} WHERE iduser = {ctx.author.id}")

        cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{namer} = res{namer} - {procent} WHERE id = 1")
        cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{namer} = res{namer} - {procent} WHERE id = 2")

        cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{namer} = res{namer} + {kolvor} WHERE id = 3")
        await ctx.send(f"Вы продали предмет с id {namer} {kolvor} раз за {sumtrat}{smile}!")

        connection.commit()



async def setup(bot):
    await bot.add_cog(rsell(bot))