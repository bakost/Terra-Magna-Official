import discord

from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor
from config import adminrole

class additem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['add-item'], pass_context=True)
    async def __additem(self, ctx, *, args=None):
        role = discord.utils.get(ctx.guild.roles, id=adminrole)
        if role in ctx.author.roles:
            connection.connect()
            if args is None:
                await ctx.send(f"Введите упоминание игрока, название и количество предметов, которые вы хотите выдать!")
                return



            a = args.split()[0]

            vladiok1 = a.replace("<","")
            vladiok1 = vladiok1.replace(">","")
            vladiok1 = vladiok1.replace("@","")

            namer = title(args.split()[1])
            kolvor = int(args.split()[2])

            if kolvor < 0:
                await ctx.send(f"**{ctx.message.author.mention}**, указанное количество меньше 0.")
                return





            cursor.execute(f"SELECT inventory FROM `{ctx.author.guild.id}` WHERE iduser = {vladiok1}")
            reco1 = cursor.fetchone()

            cursor.execute(f"SELECT inventory_amount FROM `{ctx.author.guild.id}` WHERE iduser = {vladiok1}")
            reco2 = cursor.fetchone()

            cursor.execute(f"SELECT name FROM {ctx.author.guild.id}_shop WHERE name = '{namer}'")
            reco3 = cursor.fetchone()[0]

            cursor.execute(f"SELECT name FROM {ctx.author.guild.id}_shop WHERE name = '{namer}'")
            reco5 = cursor.fetchone()







            if reco5 is None:
                await ctx.send(f"Предмет не найден!")
                return





            cursor.execute(f"SELECT inventory FROM `{ctx.author.guild.id}` WHERE iduser = {vladiok1}")
            reco8 = cursor.fetchone()[0]

            cursor.execute(f"SELECT inventory_amount FROM `{ctx.author.guild.id}` WHERE iduser = {vladiok1}")
            reco9 = cursor.fetchone()[0]

            if reco8 is None:
                if reco9 is None:
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = '{reco3} ' WHERE iduser = {vladiok1}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{kolvor} ' WHERE iduser = {vladiok1}")
                    connection.commit()
                    await ctx.send(f"Вы выдали предмет {reco3} {kolvor} раз игроку {a}!")
                    return


            keklik = ' '.join(reco1).find(reco3)



            if keklik == -1:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = CONCAT(inventory, '{reco3} ') WHERE iduser = {vladiok1}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = CONCAT(inventory_amount, '{kolvor} ') WHERE iduser = {vladiok1}")
                connection.commit()
                await ctx.send(f"Вы выдали предмет {reco3} {kolvor} раз игроку {a}!")
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


            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{itogo} ' WHERE iduser = {vladiok1}")
            connection.commit()
            await ctx.send(f"Вы выдали предмет {reco3} {kolvor} раз игроку {a}!")
        else:
            await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор.")

async def setup(bot):
    await bot.add_cog(additem(bot))