import discord

from discord.ext import commands
from connectmysql import connection, cursor
from config import smile

class pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['pay'], pass_context=True)
    async def __pay(self, ctx, *, args=None):
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}**, введите упоминание игрока, id предмета (или деньги) и количество передаваемого!")
            return

        connection.connect()

        namer = args.split()[0]#имя
        predm = str(args.split()[1])#предмет
        kolvor = float(args.split()[2])#колво

        a = namer.replace("<","")
        a = a.replace(">","")
        a = a.replace("@","")

        if (predm == "Деньги") or (predm == "деньги"):
            cursor.execute(f"SELECT cash FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco = cursor.fetchone()[0]
            if float(reco) < float(kolvor):
                await ctx.send(f"**{ctx.message.author.mention}**, у вас недостаточно монет для передачи!")
                return
            elif float(kolvor) < 0:
                await ctx.send(f"**{ctx.message.author.mention}**, указанное количество меньше 0.")
                return
            else:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash + {float(kolvor)} WHERE iduser = {a}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash - {float(kolvor)} WHERE iduser = {ctx.author.id}")
                connection.commit()
                await ctx.send(f"Игрок **{ctx.message.author.mention}** передал {kolvor}{smile} игроку **{namer}**!")

        else:
            predm = int(predm)
            cursor.execute(f"SELECT res{predm} FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco = cursor.fetchone()[0]
            if float(reco) < float(kolvor):
                await ctx.send(f"**{ctx.message.author.mention}**, у вас недостаточно ресурса для передачи!")
                return
            elif float(kolvor) < 0:
                await ctx.send(f"**{ctx.message.author.mention}**, указанное количество меньше 0.")
                return
            else:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res{predm} = res{predm} + {float(kolvor)} WHERE iduser = {a}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res{predm} = res{predm} - {float(kolvor)} WHERE iduser = {ctx.author.id}")
                connection.commit()
                await ctx.send(f"Игрок **{ctx.message.author.mention}** передал {kolvor} ресурса игроку **{namer}**!")



async def setup(bot):
    await bot.add_cog(pay(bot))