import discord

from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor
from config import adminrole, texrole

class removeitem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['remove-item-all'], pass_context=True)
    async def __removeitemall(self, ctx, *, args=None):
        role = discord.utils.get(ctx.guild.roles, id=texrole)
        if role in ctx.author.roles:
            connection.connect()
            user = args.split()[0]
            userid = user.replace("<","")
            userid = userid.replace(">","")
            userid = userid.replace("@","")
            cursor.execute(f"SELECT inventory FROM `{ctx.author.guild.id}` WHERE iduser = {userid}")
            reco1 = cursor.fetchone()[0]
            if reco1 is None:
                await ctx.send(f"Инвентарь {user} уже пуст!")
                return
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = Null WHERE iduser = {userid}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = Null WHERE iduser = {userid}")

            connection.commit()
            await ctx.send(f"Администратор **{ctx.message.author.mention}** полностью очистил инвентарь игрока {user}!")
        else:
            await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор.")


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['remove-item'], pass_context=True)
    async def __removeitem(self, ctx, *, args=None):
        role = discord.utils.get(ctx.guild.roles, id=adminrole)
        if role in ctx.author.roles:
            connection.connect()
            if args is None:
                await ctx.send(f"Введите упоминание игрока, название и количество предметов, которые вы хотите удалить!")
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
            reco1 = cursor.fetchone()[0]

            cursor.execute(f"SELECT name FROM {ctx.author.guild.id}_shop WHERE name = '{namer}'")
            reco2 = cursor.fetchone()[0]

            cursor.execute(f"SELECT inventory_amount FROM `{ctx.author.guild.id}` WHERE iduser = {vladiok1}")
            reco3 = cursor.fetchone()[0]

            if reco2 is None:
                await ctx.send(f"Предмет не найден!")
                return

            if reco1.find(reco2) == -1:
                await ctx.send(f"У {a} нет {reco2} в инвентаре!")
                return



            inventory = reco1
            inventoryamo = reco3

            allslovo = inventory.replace(f'{reco2}', '',1)



            natsl = 0




            for temp in range(0, inventory.find(reco2)):
                if inventory[temp] == " ":
                    natsl = natsl + 1



            slovonat = ""
            probels = 0
            konsl = 0
            slovonat2 = ""
            probels2 = 0
            konsl2 = 0


            for konsl in range(0,len(inventoryamo)):
                if inventoryamo[konsl] == " ":
                    probels = probels + 1
                if probels == natsl:
                    break
                slovonat = slovonat + inventoryamo[konsl]

            for konsl2 in range(0,len(inventory)):
                if inventory[konsl2] == " ":
                    probels2 = probels2 + 1
                if probels2 == natsl:
                    break
                slovonat2 = slovonat2 + inventory[konsl2]



            slovogl = ""
            testo = 0

            if natsl > 0:
                for testo in range(konsl+1, len(inventoryamo)-1):
                    if inventoryamo[testo] == " ":
                        break
                    slovogl = slovogl + inventoryamo[testo]

            if natsl == 0:
                for testo in range(konsl, len(inventoryamo)):
                    if inventoryamo[testo] == " ":
                        break
                    slovogl = slovogl + inventoryamo[testo]

            slovogl2 = ""
            testo2 = 0

            if natsl > 0:
                for testo2 in range(konsl2+1, len(inventory)-1):
                    if inventory[testo2] == " ":
                        break
                    slovogl2 = slovogl2 + inventory[testo2]

            if natsl == 0:
                for testo2 in range(konsl2, len(inventory)):
                    if inventory[testo2] == " ":
                        break
                    slovogl2 = slovogl2 + inventory[testo2]




            slovokon = ""
            slovokon2 = ""

            if natsl > 0:
                for testa in range(testo+1,len(inventoryamo)-1):
                    slovokon = slovokon + inventoryamo[testa]

            if natsl == 0:
                for testa in range(testo+1,len(inventoryamo)-1):
                    slovokon = slovokon + inventoryamo[testa]


            if natsl > 0:
                for testa2 in range(testo2+1,len(inventory)-1):
                    slovokon2 = slovokon2 + inventory[testa2]

            if natsl == 0:
                for testa2 in range(testo2+1,len(inventory)-1):
                    slovokon2 = slovokon2 + inventory[testa2]


            itogo = int(slovogl)-kolvor

            if itogo < 0:
                await ctx.send(f"Не достаточно предметов в инвентаре {a} для удаления!")
                return

            if itogo == 0:
                if allslovo == " ":
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = Null WHERE iduser = {vladiok1}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = Null WHERE iduser = {vladiok1}")
                elif konsl == 0:
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{slovokon} ' WHERE iduser = {vladiok1}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = '{slovokon2} ' WHERE iduser = {vladiok1}")
                elif slovokon == "":
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{slovonat} ' WHERE iduser = {vladiok1}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = '{slovonat2} ' WHERE iduser = {vladiok1}")
                else:
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{slovonat} {slovokon} ' WHERE iduser = {vladiok1}")
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = '{slovonat2} {slovokon2} ' WHERE iduser = {vladiok1}")



            else:
                if allslovo == " ":
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{itogo} ' WHERE iduser = {vladiok1}")
                elif konsl == 0:
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{itogo} {slovokon} ' WHERE iduser = {vladiok1}")
                elif slovokon == "":
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{slovonat} {itogo}' WHERE iduser = {vladiok1}")
                else:
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = '{slovonat} {itogo} {slovokon} ' WHERE iduser = {vladiok1}")

            connection.commit()
            await ctx.send(f"Вы удалили предмет {reco2} {kolvor} раз у игрока {a}!")


        else:
            await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор.")

async def setup(bot):
    await bot.add_cog(removeitem(bot))