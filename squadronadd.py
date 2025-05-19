import discord

from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor

class squadronadd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['squadronadd'], pass_context=True)
    async def __squadronadd(self, ctx, *, args=None):
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}**, введите номер эскадры, тип и количество кораблей!")
            return

        connection.connect()

        squadronnumber = int(args.split()[0])
        typeship = title(str(args.split()[1]))
        kolvoship = int(args.split()[2])


        if (typeship != "Каравелла") and (typeship != "Галеон"):
            await ctx.send(f"**{ctx.message.author.mention}**, указан неверный тип корабля.")
            return

        if kolvoship <= 0:
            await ctx.send(f"**{ctx.message.author.mention}**, количество кораблей меньше 1.")
            return

        if squadronnumber < 0:
            await ctx.send(f"**{ctx.message.author.mention}**, указанная эскадра меньше 0.")
            return

        cursor.execute(f"SELECT squadron FROM {ctx.author.guild.id}_squadron WHERE iduser = {ctx.author.id}")
        squadron = cursor.fetchall()

        squadron.sort()

        cursor.execute(f"SELECT type FROM {ctx.author.guild.id}_squadron WHERE squadron = {squadronnumber} and iduser = {ctx.author.id}")
        ships = cursor.fetchall()

        k1 = 0
        k2 = 0
        max = 0

        for i in squadron:
            temper = str(i)[1:-2]
            temper = int(temper)
            if temper > max:
                max = temper
                k1 += 1
            if temper == squadronnumber:
                k2 += 1

        if (k1 >= 5) and (k2 == 0):
            await ctx.send(f"**{ctx.message.author.mention}**, у Вас максимальное количество эскадр.")
            return

        if len(ships)+kolvoship >= 11:
            await ctx.send(f"**{ctx.message.author.mention}**, у Вас максимальное количество кораблей в эскадре.")
            return


        for i in range(kolvoship):
            cursor.execute(f"INSERT INTO {ctx.author.guild.id}_squadron(name, iduser, type, squadron, hp) VALUES ('{ctx.author}',{ctx.author.id},'{typeship}',{squadronnumber},100)")


        connection.commit()
        await ctx.send(f"**{ctx.message.author.mention}**, Вы добавили в эскадру №{squadronnumber} корабль типа {typeship} в количестве {kolvoship}.")



async def setup(bot):
    await bot.add_cog(squadronadd(bot))