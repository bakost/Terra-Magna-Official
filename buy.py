import discord

from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor

class buy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['buy'], pass_context=True)
    async def __buy(self, ctx, *, args=None):
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}**, введите название и количество предметов, которые вы хотите купить!")
            return

        connection.connect()

        namer = title(args.split()[0])
        kolvor = int(args.split()[1])

        if kolvor < 0:
            await ctx.send(f"**{ctx.message.author.mention}**, указанное количество меньше 0.")
            return



        cursor.execute(f"SELECT name FROM {ctx.author.guild.id}_shop WHERE name = '{namer}'")
        reco3 = cursor.fetchone()[0]

        cursor.execute(f"SELECT name FROM {ctx.author.guild.id}_shop WHERE name = '{namer}'")
        reco5 = cursor.fetchone()

        cursor.execute(f"SELECT type FROM {ctx.author.guild.id}_shop WHERE name = '{namer}'")
        type = str(cursor.fetchone()[0])
        type = int(type)

        if type == 1:
            cursor.execute(f"SELECT inventory FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco1 = cursor.fetchone()

            cursor.execute(f"SELECT inventory_amount FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco2 = cursor.fetchone()

        if type == 2:
            cursor.execute(f"SELECT fleet FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco1 = cursor.fetchone()

            cursor.execute(f"SELECT fleet_amount FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco2 = cursor.fetchone()


        cursor.execute(f"SELECT cash FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco200 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res1 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco201 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res2 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco202 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res3 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco203 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res4 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco204 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res5 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco205 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res6 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco206 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res7 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco207 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res8 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco208 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res9 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco209 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res10 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco210 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res11 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco211 = cursor.fetchone()[0]








        cursor.execute(f"SELECT cash FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco100 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res1 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco101 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res2 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco102 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res3 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco103 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res4 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco104 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res5 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco105 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res6 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco106 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res7 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco107 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res8 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco108 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res9 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco109 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res10 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco110 = cursor.fetchone()[0]

        cursor.execute(f"SELECT res11 FROM {ctx.author.guild.id}_shop WHERE name = '{reco3}'")
        reco111 = cursor.fetchone()[0]






        kolcash = int(reco100)*int(kolvor)
        kolres1 = int(reco101)*int(kolvor)
        kolres2 = int(reco102)*int(kolvor)
        kolres3 = int(reco103)*int(kolvor)
        kolres4 = int(reco104)*int(kolvor)
        kolres5 = int(reco105)*int(kolvor)
        kolres6 = int(reco106)*int(kolvor)
        kolres7 = int(reco107)*int(kolvor)
        kolres8 = int(reco108)*int(kolvor)
        kolres9 = int(reco109)*int(kolvor)
        kolres10 = int(reco110)*int(kolvor)
        kolres11 = int(reco111)*int(kolvor)






        if reco5 is None:
            await ctx.send(f"Предмет не найден!")
            return

        if int(reco200) < kolcash:
            await ctx.send(f"У вас не достаточно монет!")
            return

        if int(reco201) < kolres1:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco202) < kolres2:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco203) < kolres3:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco204) < kolres4:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco205) < kolres5:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco206) < kolres6:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco207) < kolres7:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco208) < kolres8:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco209) < kolres9:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco210) < kolres10:
            await ctx.send(f"У вас не достаточно ресурса!")
            return

        if int(reco211) < kolres11:
            await ctx.send(f"У вас не достаточно ресурса!")
            return





        if type == 1:
            cursor.execute(f"SELECT inventory FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco8 = cursor.fetchone()[0]

            cursor.execute(f"SELECT inventory_amount FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco9 = cursor.fetchone()[0]

            if reco8 is None:
                if reco9 is None:
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash - {kolcash} WHERE iduser = {ctx.author.id}")

                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res1 = res1 - {kolres1} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res2 = res2 - {kolres2} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res3 = res3 - {kolres3} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res4 = res4 - {kolres4} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res5 = res5 - {kolres5} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res6 = res6 - {kolres6} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res7 = res7 - {kolres7} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res8 = res8 - {kolres8} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res9 = res9 - {kolres9} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res10 = res10 - {kolres10} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res11 = res11 - {kolres11} WHERE iduser = {ctx.author.id}")



                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = '{reco3} ' WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{kolvor} ' WHERE iduser = {ctx.author.id}")

                    connection.commit()
                    await ctx.send(f"Вы купили предмет {reco3} {kolvor} раз!")
                    return

        if type == 2:
            cursor.execute(f"SELECT fleet FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco8 = cursor.fetchone()[0]

            cursor.execute(f"SELECT fleet_amount FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco9 = cursor.fetchone()[0]

            if reco8 is None:
                if reco9 is None:
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash - {kolcash} WHERE iduser = {ctx.author.id}")

                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res1 = res1 - {kolres1} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res2 = res2 - {kolres2} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res3 = res3 - {kolres3} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res4 = res4 - {kolres4} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res5 = res5 - {kolres5} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res6 = res6 - {kolres6} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res7 = res7 - {kolres7} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res8 = res8 - {kolres8} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res9 = res9 - {kolres9} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res10 = res10 - {kolres10} WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res11 = res11 - {kolres11} WHERE iduser = {ctx.author.id}")



                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet = '{reco3} ' WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet_amount = '{kolvor} ' WHERE iduser = {ctx.author.id}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet_amount_usable = '0 ' WHERE iduser = {ctx.author.id}")

                    connection.commit()
                    await ctx.send(f"Вы купили корабль {reco3} {kolvor} раз!")
                    return


        keklik = ' '.join(reco1).find(reco3)


        if type == 1:
            if keklik == -1:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash - {kolcash} WHERE iduser = {ctx.author.id}")

                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res1 = res1 - {kolres1} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res2 = res2 - {kolres2} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res3 = res3 - {kolres3} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res4 = res4 - {kolres4} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res5 = res5 - {kolres5} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res6 = res6 - {kolres6} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res7 = res7 - {kolres7} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res8 = res8 - {kolres8} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res9 = res9 - {kolres9} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res10 = res10 - {kolres10} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res11 = res11 - {kolres11} WHERE iduser = {ctx.author.id}")


                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = CONCAT(inventory, '{reco3} ') WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = CONCAT(inventory_amount, '{kolvor} ') WHERE iduser = {ctx.author.id}")

                connection.commit()
                await ctx.send(f"Вы купили предмет {reco3} {kolvor} раз!")
                return

        if type == 2:
            if keklik == -1:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash - {kolcash} WHERE iduser = {ctx.author.id}")

                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res1 = res1 - {kolres1} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res2 = res2 - {kolres2} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res3 = res3 - {kolres3} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res4 = res4 - {kolres4} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res5 = res5 - {kolres5} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res6 = res6 - {kolres6} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res7 = res7 - {kolres7} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res8 = res8 - {kolres8} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res9 = res9 - {kolres9} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res10 = res10 - {kolres10} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res11 = res11 - {kolres11} WHERE iduser = {ctx.author.id}")


                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet = CONCAT(fleet, '{reco3} ') WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet_amount = CONCAT(fleet_amount, '{kolvor} ') WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet_amount_usable = CONCAT(fleet_amount_usable, '0 ') WHERE iduser = {ctx.author.id}")

                connection.commit()
                await ctx.send(f"Вы купили корабль {reco3} {kolvor} раз!")
                return

        natsl = 0

        inventory = ' '.join(reco1)
        inventoryamo = ' '.join(reco2)


        for temp in range(0, inventory.find(reco3)):
            if inventory[temp] == " ":
                natsl = natsl + 1

        slovonat = ""
        probels = 0

        konsl = 0

        if natsl != 0:
            for konsl in range(0,len(inventoryamo)):
                slovonat = slovonat + inventoryamo[konsl]
                if inventoryamo[konsl] == " ":
                    probels = probels + 1
                if probels == natsl:
                    break

        slovogl = ""

        konsl2 = 0

        if natsl != 0:
            for konsl2 in range(int(konsl)+1, len(inventoryamo)):
                if inventoryamo[konsl2] == " ":
                    break
                slovogl = slovogl + inventoryamo[konsl2]

        if natsl == 0:
            for konsl2 in range(int(konsl), len(inventoryamo)):
                if inventoryamo[konsl2] == " ":
                    break
                slovogl = slovogl + inventoryamo[konsl2]

        slovokon = ""

        if len(inventoryamo) == konsl2+1:
            slovokon = " "

        if len(inventoryamo) != konsl2+1:
            for temp in range(konsl2,len(inventoryamo)):
                slovokon = slovokon + inventoryamo[temp]

        itogosum = int(slovogl)+int(kolvor)

        itogo = ""

        if natsl != 0:
            itogo = f"{slovonat}{itogosum}{slovokon}"

        if natsl == 0:
            itogo = f"{itogosum}{slovokon}"


        if type == 1:
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash - {kolcash} WHERE iduser = {ctx.author.id}")

            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res1 = res1 - {kolres1} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res2 = res2 - {kolres2} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res3 = res3 - {kolres3} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res4 = res4 - {kolres4} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res5 = res5 - {kolres5} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res6 = res6 - {kolres6} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res7 = res7 - {kolres7} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res8 = res8 - {kolres8} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res9 = res9 - {kolres9} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res10 = res10 - {kolres10} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res11 = res11 - {kolres11} WHERE iduser = {ctx.author.id}")


            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{itogo}' WHERE iduser = {ctx.author.id}")

            connection.commit()
            await ctx.send(f"Вы купили предмет {reco3} {kolvor} раз!")


        if type == 2:
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash - {kolcash} WHERE iduser = {ctx.author.id}")

            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res1 = res1 - {kolres1} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res2 = res2 - {kolres2} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res3 = res3 - {kolres3} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res4 = res4 - {kolres4} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res5 = res5 - {kolres5} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res6 = res6 - {kolres6} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res7 = res7 - {kolres7} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res8 = res8 - {kolres8} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res9 = res9 - {kolres9} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res10 = res10 - {kolres10} WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res11 = res11 - {kolres11} WHERE iduser = {ctx.author.id}")


            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET fleet_amount = '{itogo}' WHERE iduser = {ctx.author.id}")

            connection.commit()
            await ctx.send(f"Вы купили флот {reco3} {kolvor} раз!")



        connection.commit()

async def setup(bot):
    await bot.add_cog(buy(bot))