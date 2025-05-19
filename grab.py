import discord

from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor

class grab(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['grab'], pass_context=True)
    async def __grab(self, ctx, *,  args=None):
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}**, отсутствуют аргументы! Пример команды: !grab [Название морской провинции] [Количество галеонов] [Количество каравелл]")
            return

        connection.connect()

        maritime = title(str(args.split()[0]))
        maritime = str(maritime)

        galeons = str(args.split()[1])
        galeons = int(galeons)

        karavells = str(args.split()[2])
        karavells = int(karavells)

        cursor.execute(f"SELECT maritime FROM {ctx.author.guild.id}_grab")
        reco1 = cursor.fetchall()

        cursor.execute(f"SELECT iduser FROM {ctx.author.guild.id}_grab")
        reco2 = cursor.fetchall()

        cursor.execute(f"SELECT type FROM {ctx.author.guild.id}_grab")
        reco3 = cursor.fetchall()

        for i in range(0, len(reco1)):
            temp = str(reco1[i])[2:-3]
            temp2 = str(reco2[i])[1:-2]
            temp2 = int(temp2)
            temp3 = str(reco3[i])[1:-2]
            temp3 = int(temp3)

            if (temp == maritime) and (temp2 == ctx.author.id) and (temp3 == 1):
                await ctx.send(f"**{member.mention}**, Вы уже ведете пиратство в этой морской провинции!")
                return

        cursor.execute(f"SELECT fleet FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        fleet = cursor.fetchall()

        cursor.execute(f"SELECT fleet_amount FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        fleet_amount = cursor.fetchall()

        cursor.execute(f"SELECT fleet_amount_usable FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        fleet_amount_usable = cursor.fetchall()

        fleet = str(fleet)[3:-4]
        fleet = fleet.split()

        fleet_amount = str(fleet_amount)[3:-4]
        fleet_amount = fleet_amount.split()

        fleet_amount_usable = str(fleet_amount_usable)[3:-4]
        fleet_amount_usable = fleet_amount_usable.split()

        for i in range(0, len(fleet)):
            temp = str(fleet[i])

            temp2 = str(fleet_amount[i])
            temp2 = int(temp2)

            if temp == "Галеон":
                if temp2 < galeons:
                    await ctx.send(f"**{member.mention}**, у Вас не достаточно галеонов!")
                    return
                fleet_amount[i] = temp2 - galeons
                fleet_amount_usable[i] = int(fleet_amount_usable[i]) + galeons

            if temp == "Каравелла":
                if temp2 < karavells:
                    await ctx.send(f"**{member.mention}**, у Вас не достаточно каравелл!")
                    return
                fleet_amount[i] = temp2 - karavells
                fleet_amount_usable[i] = int(fleet_amount_usable[i]) + karavells



        fleet_amount = [str(x) for x in fleet_amount]
        fleet_amount_usable = [str(x) for x in fleet_amount_usable]

        str_fleet_amount = ' '.join(fleet_amount)
        str_fleet_amount_usable = ' '.join(fleet_amount_usable)

        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet_amount = '{str_fleet_amount} ' WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet_amount_usable = '{str_fleet_amount_usable} ' WHERE iduser = {ctx.author.id}")
        cursor.execute(f"INSERT INTO {ctx.author.guild.id}_grab(name, iduser, maritime, galeons, karavells, type) VALUES ('{member}',{member.id},'{maritime}',{galeons},{karavells},1)")

        connection.commit()
        await ctx.send(f"**{member.mention}**, Вы начали пиратство в \"{maritime}\"!")


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['ungrab'], pass_context=True)
    async def __ungrab(self, ctx, *,  args=None):
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}**, отсутствуют аргументы! Пример команды: !ungrab [Название морской провинции] [Количество галеонов] [Количество каравелл]")
            return

        connection.connect()

        maritime = title(str(args.split()[0]))
        maritime = str(maritime)

        cursor.execute(f"SELECT maritime FROM {ctx.author.guild.id}_grab")
        reco1 = cursor.fetchall()

        cursor.execute(f"SELECT id FROM {ctx.author.guild.id}_grab")
        reco2 = cursor.fetchall()

        cursor.execute(f"SELECT iduser FROM {ctx.author.guild.id}_grab")
        reco3 = cursor.fetchall()

        cursor.execute(f"SELECT type FROM {ctx.author.guild.id}_grab")
        reco4 = cursor.fetchall()

        for i in range(0, len(reco1)):
            temps = str(reco1[i])[2:-3]
            temps2 = str(reco2[i])[1:-2]
            temps2 = int(temps2)
            temps3 = str(reco3[i])[1:-2]
            temps3 = int(temps3)
            temps4 = str(reco4[i])[1:-2]
            temps4 = int(temps4)

            if (temps == maritime) and (temps3 == ctx.author.id) and (temps4 == 1):
                cursor.execute(f"SELECT fleet FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
                fleet = cursor.fetchall()

                cursor.execute(f"SELECT fleet_amount FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
                fleet_amount = cursor.fetchall()

                cursor.execute(f"SELECT fleet_amount_usable FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
                fleet_amount_usable = cursor.fetchall()

                cursor.execute(f"SELECT galeons FROM {ctx.author.guild.id}_grab WHERE maritime = '{maritime}' and type = 1")
                galeons = cursor.fetchone()[0]

                cursor.execute(f"SELECT karavells FROM {ctx.author.guild.id}_grab WHERE maritime = '{maritime}' and type = 1")
                karavells = cursor.fetchone()[0]

                fleet = str(fleet)[3:-4]
                fleet = fleet.split()

                fleet_amount = str(fleet_amount)[3:-4]
                fleet_amount = fleet_amount.split()

                fleet_amount_usable = str(fleet_amount_usable)[3:-4]
                fleet_amount_usable = fleet_amount_usable.split()

                for i in range(0, len(fleet)):
                    temp = str(fleet[i])

                    temp2 = str(fleet_amount[i])
                    temp2 = int(temp2)

                    if temp == "Галеон":
                        fleet_amount[i] = temp2 + galeons
                        fleet_amount_usable[i] = int(fleet_amount_usable[i]) - galeons

                    if temp == "Каравелла":
                        fleet_amount[i] = temp2 + karavells
                        fleet_amount_usable[i] = int(fleet_amount_usable[i]) - karavells

                fleet_amount = [str(x) for x in fleet_amount]
                fleet_amount_usable = [str(x) for x in fleet_amount_usable]

                str_fleet_amount = ' '.join(fleet_amount)
                str_fleet_amount_usable = ' '.join(fleet_amount_usable)

                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet_amount = '{str_fleet_amount} ' WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet_amount_usable = '{str_fleet_amount_usable} ' WHERE iduser = {ctx.author.id}")

                cursor.execute(f"DELETE FROM {ctx.author.guild.id}_grab WHERE maritime = '{maritime}' and type = 1")

                connection.commit()
                await ctx.send(f"**{member.mention}**, Вы закончили пиратство в \"{maritime}\"!")
                return

        await ctx.send(f"**{member.mention}**, Вы не проводили пиратство в данной морской провинции!")


async def setup(bot):
    await bot.add_cog(grab(bot))