import discord
import asyncio

from fractions import Fraction
from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor
from config import sh, res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, town_towns, building_towns, town_unoccupied_population, town_occupied_population, town_possible_mining

class building(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['building', 'build'], pass_context=True)
    async def __building(self, ctx, *,  args=None):
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}** отсутствуют аргументы! Пример команды: !building [Название города] [Название постройки] [Количество построек]")
            return

        connection.connect()

        nametown = title(str(args.split()[0]))
        namebuilding = title(str(args.split()[1]))
        buildingkolvo = int(args.split()[2])

        nametown = str(nametown)
        namebuilding = str(namebuilding)


        if buildingkolvo < 1:
            await ctx.send(f"**{member.mention}** количество построек, не может быть меньше нуля!")
            return

        cursor.execute(f"SELECT count_building FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        count_building = str(cursor.fetchone()[0])

        cursor.execute(f"SELECT count_building_max FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        count_building_max = int(cursor.fetchone()[0])

        cursor.execute(f"SELECT cash FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        cash = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res1 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres1 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res2 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres2 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res3 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres3 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res4 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres4 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res5 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres5 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res6 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres6 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res7 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres7 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res8 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres8 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res9 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres9 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res10 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres10 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res11 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        tres11 = float(cursor.fetchone()[0])



        cursor.execute(f"SELECT ares1 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares1 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares2 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares2 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares3 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares3 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares4 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares4 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares5 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares5 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares6 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares6 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares7 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares7 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares8 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares8 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares9 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares9 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares10 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares10 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT ares11 FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        ares11 = float(cursor.fetchone()[0])




        cursor.execute(f"SELECT cash FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        minecash = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res1 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres1 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res2 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres2 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res3 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres3 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res4 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres4 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res5 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres5 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res6 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres6 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res7 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres7 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res8 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres8 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res9 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres9 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res10 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres10 = float(cursor.fetchone()[0])

        cursor.execute(f"SELECT res11 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        mineres11 = float(cursor.fetchone()[0])


        buildingkolvofinalcash = buildingkolvo * cash
        buildingkolvofinalres1 = buildingkolvo * tres1
        buildingkolvofinalres2 = buildingkolvo * tres2
        buildingkolvofinalres3 = buildingkolvo * tres3
        buildingkolvofinalres4 = buildingkolvo * tres4
        buildingkolvofinalres5 = buildingkolvo * tres5
        buildingkolvofinalres6 = buildingkolvo * tres6
        buildingkolvofinalres7 = buildingkolvo * tres7
        buildingkolvofinalres8 = buildingkolvo * tres8
        buildingkolvofinalres9 = buildingkolvo * tres9
        buildingkolvofinalres10 = buildingkolvo * tres10
        buildingkolvofinalres11 = buildingkolvo * tres11






        if buildingkolvofinalcash > minecash:
            await ctx.send(f"**{member.mention}** недостаточно денег!")
            return

        if buildingkolvofinalres1 > mineres1:
            await ctx.send(f"**{member.mention}** недостаточно {res1}!")
            return

        if buildingkolvofinalres2 > mineres2:
            await ctx.send(f"**{member.mention}** недостаточно {res2}!")
            return

        if buildingkolvofinalres3 > mineres3:
            await ctx.send(f"**{member.mention}** недостаточно {res3}!")
            return

        if buildingkolvofinalres4 > mineres4:
            await ctx.send(f"**{member.mention}** недостаточно {res4}!")
            return

        if buildingkolvofinalres5 > mineres5:
            await ctx.send(f"**{member.mention}** недостаточно {res5}!")
            return

        if buildingkolvofinalres6 > mineres6:
            await ctx.send(f"**{member.mention}** недостаточно {res6}!")
            return

        if buildingkolvofinalres7 > mineres7:
            await ctx.send(f"**{member.mention}** недостаточно {res7}!")
            return

        if buildingkolvofinalres8 > mineres8:
            await ctx.send(f"**{member.mention}** недостаточно {res8}!")
            return

        if buildingkolvofinalres9 > mineres9:
            await ctx.send(f"**{member.mention}** недостаточно {res9}!")
            return

        if buildingkolvofinalres10 > mineres10:
            await ctx.send(f"**{member.mention}** недостаточно {res10}!")
            return

        if buildingkolvofinalres11 > mineres11:
            await ctx.send(f"**{member.mention}** недостаточно {res11}!")
            return


        #await ctx.send(f"m1")

        k1 = 1
        k2 = 1

        #await ctx.send(str(sh.worksheet("Города").get(f"C4"))[3:-3])

        while str(sh.worksheet("Города").get(f"{town_towns}{k1}"))[3:-3] != nametown:
            k1 += 1

        #await ctx.send(f"m2")

        while str(sh.worksheet("Постройки").get(f"{building_towns}{k2}"))[3:-3] != nametown:
            k2 += 1

        #await ctx.send(f"m3")

        arbeitertownkolvo = str(sh.worksheet("Города").get(f"{town_unoccupied_population}{k1}"))[3:-3]#незанятое население
        arbeiterkolvo = str(sh.worksheet("Города").get(f"{town_occupied_population}{k1}"))[3:-3]#занятое население
        count_building_builded = str(sh.worksheet("Постройки").get(f"{count_building}{k2}"))[3:-3]#постройка

        #await ctx.send(f"m4")

        arbeitertownkolvo = int(arbeitertownkolvo)
        arbeiterkolvo = int(arbeiterkolvo)
        count_building_builded = int(count_building_builded)

        if (count_building_builded >= count_building_max) and (count_building_max != 0):
            await ctx.send(f"**{member.mention}** лимит построек в городе превышен!")
            return

        #await ctx.send(f"m5")
        #await ctx.send(f"count_building_builded: {count_building_builded}")

        cursor.execute(f"SELECT arbeiter FROM {ctx.author.guild.id}_buildings WHERE building = '{namebuilding}'")
        arbeiter = int(cursor.fetchone()[0])

        if arbeitertownkolvo < (arbeiter*buildingkolvo):
            await ctx.send(f"**{member.mention}** для постройки не хватает рабочих!")
            return

        await asyncio.sleep(15)

        #await ctx.send(f"m1")

        possible_mining = str(sh.worksheet("Города").get(f"{town_possible_mining}{k1}"))[3:-3]
        possible_mining_mass = possible_mining.split(", ")

        #await ctx.send(f"m2")

        wood_material = 0
        stone_material = 0
        metall_material = 0

        for i in possible_mining_mass:
            if (i.split("x"))[0] == "Дерево ":
                wood_material = int((i.split("x"))[1])
            if (i.split("x"))[0] == "Камень ":
                stone_material = int((i.split("x"))[1])
            if (i.split("x"))[0] == "Металл ":
                metall_material = int((i.split("x"))[1])

        postroika_wood_material = 0
        postroika_stone_material = 0
        postroika_prov_material = 0

        #await ctx.send(f"m3")

        if ares1 != 0:
            postroika_wood_material = wood_material / ares1
        else:
            postroika_wood_material = 1000000

        if ares2 != 0:
            postroika_stone_material = stone_material / ares2
        else:
            postroika_stone_material = 1000000

        if ares3 != 0:
            postroika_prov_material = metall_material / ares3
        else:
            postroika_prov_material = 1000000

        minpostroika = min(postroika_wood_material,postroika_stone_material,postroika_prov_material)

        #await ctx.send(f"minpostroika: {minpostroika}")

        minpostroika = Fraction(minpostroika)

        #await ctx.send(f"minpostroika: {minpostroika}")

        #await ctx.send(f"minpostroika: {minpostroika}")
        #await ctx.send(f"{minpostroika - count_building_builded}")

        if (minpostroika - count_building_builded) < buildingkolvo:
            await ctx.send(f"**{member.mention}** в городе уже добываются все ресурсы этого вида!")
            return

        #buildings = str(sh.worksheet("Города").get(f"D{k}"))[3:-3]
        #prodincomeprom = str(sh.worksheet("Города").get(f"G{k}"))[3:-3]
        #prodincome = int(prodincomeprom)

        #await ctx.send(f"m7")

        #sh.worksheet("Города").update(f"G{k1}", prodincome + buildingkolvofinalcash)
        sh.worksheet("Города").update(f"{town_unoccupied_population}{k1}", arbeitertownkolvo - (arbeiter*buildingkolvo))
        sh.worksheet("Города").update(f"{town_occupied_population}{k1}", arbeiterkolvo + (arbeiter*buildingkolvo))
        sh.worksheet("Постройки").update(f"{count_building}{k2}", count_building_builded + buildingkolvo)

        #await ctx.send(f"m8")

        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash - {buildingkolvofinalcash} WHERE iduser = {ctx.author.id}")

        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res1 = res1 - {buildingkolvofinalres1} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res2 = res2 - {buildingkolvofinalres2} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res3 = res3 - {buildingkolvofinalres3} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res4 = res4 - {buildingkolvofinalres4} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res5 = res5 - {buildingkolvofinalres5} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res6 = res6 - {buildingkolvofinalres6} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res7 = res7 - {buildingkolvofinalres7} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res8 = res8 - {buildingkolvofinalres8} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res9 = res9 - {buildingkolvofinalres9} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res10 = res10 - {buildingkolvofinalres10} WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res11 = res11 - {buildingkolvofinalres11} WHERE iduser = {ctx.author.id}")


        connection.commit()
        await ctx.send(f"**{member.mention}** построил \"{namebuilding}\" в количестве \"{buildingkolvo}\" штук в городе \"{nametown}\"!")

async def setup(bot):
    await bot.add_cog(building(bot))