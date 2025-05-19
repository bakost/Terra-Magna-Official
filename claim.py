import discord

from discord.ext import commands
from connectmysql import connection, cursor
from numpy.core.defchararray import title, isdigit
from config import sh

class claim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['claim'], pass_context=True)
    async def __claim(self, ctx, *,  args=None):
        #cash = str(worksheet.get('A1')[0])[2:-2]
        #await ctx.send(cash)
        #worksheet.update("A1", "=A2+B2", raw = False)
        connection.connect()
        member = ctx.message.author

        cursor.execute(f"SELECT globaltime FROM {ctx.author.guild.id}_time WHERE id = 2")
        reco0 = int(cursor.fetchone()[0])

        if reco0 >= 30:
            await ctx.send(f"**{member.mention}** время ожидания ещё не прошло, попробуйте выполнить команду позднее!")
            return

        if args is None:
            await ctx.send(f"**{member.mention}** отсутствуют аргументы! Пример команды: !claim [Название государства] [Название столицы] [Название морской провинции]")
            return

        name = title(str(args.split()[0]))
        namecapital = title(str(args.split()[1]))
        maritime = str(args.split()[2])

        name = str(name)
        namecapital = str(namecapital)


        if isdigit(maritime) == False:
            await ctx.send(f"**{member.mention}** морская провинция должна быть цифрой!")
            return

        maritime = 'S' + maritime

        k1 = 1
        k2 = 1
        k3 = 1
        k4 = 1
        k5 = 1

        #pass1 = ""
        #pass2 = ""
        #pass3 = ""



        #pass1 = "B"
        #pass2 = "E"
        #pass3 = "C"

        resources = sh.worksheet("Ресурсы").get(f"B:B")
        resources = str(resources)[1:-1]
        resources = resources.replace("[", "")
        resources = resources.replace("]", "")
        resources = resources.replace(" \'", "")
        resources = resources.replace("\'", "")
        resources = resources.split(",")

        dompol = sh.worksheet("Внутренняя политика").get(f"B:B")
        dompol = str(dompol)[1:-1]
        dompol = dompol.replace("[", "")
        dompol = dompol.replace("]", "")
        dompol = dompol.replace(" \'", "")
        dompol = dompol.replace("\'", "")
        dompol = dompol.split(",")

        countries = sh.worksheet("Доходы/Расходы").get(f"B:B")
        countries = str(countries)[1:-1]
        countries = countries.replace("[", "")
        countries = countries.replace("]", "")
        countries = countries.replace(" \'", "")
        countries = countries.replace("\'", "")
        countries = countries.split(",")

        towns = sh.worksheet("Города").get(f"C:C")
        towns = str(towns)[1:-1]
        towns = towns.replace("[", "")
        towns = towns.replace("]", "")
        towns = towns.replace(" \'", "")
        towns = towns.replace("\'", "")
        towns = towns.split(",")

        buildings = sh.worksheet("Постройки").get(f"B:B")
        buildings = str(buildings)[1:-1]
        buildings = buildings.replace("[", "")
        buildings = buildings.replace("]", "")
        buildings = buildings.replace(" \'", "")
        buildings = buildings.replace("\'", "")
        buildings = buildings.split(",")

        #await ctx.send(f"meta1")
        #await ctx.send(f"{countries}")

        #await ctx.send(f"meta2")

        cursor.execute(f"SELECT colony FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco2 = cursor.fetchone()[0]

        cursor.execute(f"SELECT capital FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco3 = cursor.fetchone()[0]

        cursor.execute(f"SELECT colony FROM `{ctx.author.guild.id}`")
        reco4 = cursor.fetchall()

        cursor.execute(f"SELECT capital FROM `{ctx.author.guild.id}`")
        reco5 = cursor.fetchall()

        cursor.execute(f"SELECT maritime FROM `{ctx.author.guild.id}`")
        reco6 = cursor.fetchall()

        #await ctx.send(f"meta3")

        if reco2 is not None:
            await ctx.send(f"**{member.mention}** у вас уже есть государство!")
            return

        #await ctx.send(f"meta4")

        for i in range(0, len(reco4)):
            temp = str(reco4[i])[2:-3]
            if temp == name:
                await ctx.send(f"**{member.mention}** такое государство уже существует!")
                return

        #await ctx.send(f"meta5")

        for i in range(0, len(reco5)):
            temp = str(reco5[i])[2:-3]
            if temp == namecapital:
                await ctx.send(f"**{member.mention}** такая столица уже существует!")
                return


        await ctx.send(f"**{member.mention}**, создание государства занимает несколько минут, по окончании вы будете уведомлены.")

        while str(countries[k1]) != "Государство":
            k1 += 1

        while k1 != len(countries):
            k1 += 1

        k1 += 1

        while str(towns[k2]) != "Город":
            k2 += 1

        while k2 != len(towns):
            k2 += 1

        k2 += 2

        while str(dompol[k3]) != "Государство":
            k3 += 1

        while k3 != len(dompol):
            k3 += 1

        k3 += 1

        while str(resources[k4]) != "Государство":
            k4 += 1

        while k4 != len(resources):
            k4 += 1

        k4 += 2

        while str(buildings[k5]) != "Государство":
            k5 += 1

        while k5 != len(buildings):
            k5 += 1

        k5 += 2

        #while str(countries[k3]) != "% Пошлин":
        #    k3 += 1

        #k3 += 1

        #nalogstavka = 10

        #naselenie = str(sh.worksheet("Страны").get(f"{pass2}4"))[3:-3]
        #naselenie = int(naselenie)

        sh.worksheet("Ресурсы").batch_update([
            {
                "range" : f"B{k4}:AG{k4}",
                "values" : [[
                    name,
                    namecapital,
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0"
                ]]
            }
        ], raw = False)

        sh.worksheet("Ресурсы").format(f"B{k4+1}:AG{k4+1}", {
            "backgroundColor": {
                "red": 39,
                "green": 39,
                "blue": 39
            }
        })

        sh.worksheet("Доходы/Расходы").batch_update([
            {
                "range" : f"B{k1}:M{k1}",
                "values" : [[
                    name,
                    f"=СУММ('Города'!Q{k2}:Q{k2+1})",
                    f"=0",
                    f"=СУММ('Города'!E{k2}:E{k2+1})",
                    f"=СУММ('Города'!F{k2}:F{k2+1})",
                    f"=ЕСЛИ('Ресурсы'!E1=1;\"Дерево x\"&СУММ('Ресурсы'!E{k4}:E{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!F1=1;\"Камень x\"&СУММ('Ресурсы'!F{k4}:F{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!G1=1;\"Металл x\"&СУММ('Ресурсы'!G{k4}:G{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!H1=1;\"Керамика x\"&СУММ('Ресурсы'!H{k4}:H{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!I1=1;\"Овощи и фрукты x\"&СУММ('Ресурсы'!I{k4}:I{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!J1=1;\"Хлопок x\"&СУММ('Ресурсы'!J{k4}:J{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!K1=1;\"Роскошь x\"&СУММ('Ресурсы'!K{k4}:K{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!L1=1;\"Алкоголь x\"&СУММ('Ресурсы'!L{k4}:L{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!M1=1;\"Одежда x\"&СУММ('Ресурсы'!M{k4}:M{k4+1});)&\" \"",
                    f"=0",
                    f"=0",
                    f"=СУММ('Города'!I{k2}:I{k2+1})",
                    f"=ЕСЛИ('Ресурсы'!N1=1;\"Дерево x\"&СУММ('Ресурсы'!N{k4}:N{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!O1=1;\"Камень x\"&СУММ('Ресурсы'!O{k4}:O{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!P1=1;\"Металл x\"&СУММ('Ресурсы'!P{k4}:P{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!Q1=1;\"Керамика x\"&СУММ('Ресурсы'!Q{k4}:Q{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!R1=1;\"Овощи и фрукты x\"&СУММ('Ресурсы'!R{k4}:R{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!S1=1;\"Хлопок x\"&СУММ('Ресурсы'!S{k4}:S{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!T1=1;\"Роскошь x\"&СУММ('Ресурсы'!T{k4}:T{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!U1=1;\"Алкоголь x\"&СУММ('Ресурсы'!U{k4}:U{k4+1});)&\" \"&ЕСЛИ('Ресурсы'!V1=1;\"Одежда x\"&СУММ('Ресурсы'!V{k4}:V{k4+1});)&\" \"",
                    f"=0",
                    f"=СУММ(E{k1};F{k1})-СУММ(I{k1};J{k1};L{k1})"
                ]]
            }
        ], raw = False)

        '''
        sh.worksheet("Доходы/Расходы").format(f"B{k1+1}:M{k1+1}", {
            "backgroundColor": {
                "red": 39,
                "green": 39,
                "blue": 39
            }
        })
        '''

        sh.worksheet("Города").batch_update([
            {
                "range" : f"B{k2}:U{k2}",
                "values" : [[
                    name,
                    namecapital,
                    "Ратуша; ",
                    f"=(((S{k2}/100*'Внутренняя политика'!M{k3})/ЕСЛИ('Внутренняя политика'!G{k3}<50;1,3;1)/ЕСЛИ('Внутренняя политика'!G{k3}<40;1,3;1)/ЕСЛИ('Внутренняя политика'!G{k3}<30;1,3;1))+((T{k2}/100*'Внутренняя политика'!N{k3})/ЕСЛИ('Внутренняя политика'!H{k3}<50;1,3;1)/ЕСЛИ('Внутренняя политика'!H{k3}<40;1,3;1)/ЕСЛИ('Внутренняя политика'!H{k3}<30;1,3;1))+(U{k2}/100*'Внутренняя политика'!O{k3})/ЕСЛИ('Внутренняя политика'!I{k3}<50;1,3;1)/ЕСЛИ('Внутренняя политика'!I{k3}<40;1,3;1)/ЕСЛИ('Внутренняя политика'!I{k3}<30;1,3;1))/2",
                    "=0",
                    f"=ЕСЛИ('Ресурсы'!E{k4}>0;\"Дерево x\"&'Ресурсы'!E{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!F{k4}>0;\"Камень x\"&'Ресурсы'!F{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!G{k4}>0;\"Металл x\"&'Ресурсы'!G{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!H{k4}>0;\"Керамика x\"&'Ресурсы'!H{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!I{k4}>0;\"Овощи и фрукты x\"&'Ресурсы'!I{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!J{k4}>0;\"Хлопок x\"&'Ресурсы'!J{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!K{k4}>0;\"Роскошь x\"&'Ресурсы'!K{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!L{k4}>0;\"Алкоголь x\"&'Ресурсы'!L{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!M{k4}>0;\"Одежда x\"&'Ресурсы'!M{k4};\"\")",
                    "=0",
                    f"=ЕСЛИ('Ресурсы'!N{k4}>0;\"Дерево x\"&'Ресурсы'!N{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!O{k4}>0;\"Камень x\"&'Ресурсы'!O{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!P{k4}>0;\"Металл x\"&'Ресурсы'!P{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!Q{k4}>0;\"Керамика x\"&'Ресурсы'!Q{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!R{k4}>0;\"Овощи и фрукты x\"&'Ресурсы'!R{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!S{k4}>0;\"Хлопок x\"&'Ресурсы'!S{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!T{k4}>0;\"Роскошь x\"&'Ресурсы'!T{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!U{k4}>0;\"Алкоголь x\"&'Ресурсы'!U{k4};\"\")&\" \"&ЕСЛИ('Ресурсы'!V{k4}>0;\"Одежда x\"&'Ресурсы'!V{k4};\"\")",
                    f"=1000",
                    f"=0",
                    f"=0",
                    f"=((J{k2}+K{k2})/100*10)-((J{k2}+K{k2})/1000*'Внутренняя политика'!M{k3})-((J{k2}+J{k2})/1000*'Внутренняя политика'!N{k3})-((J{k2}+K{k2})/1000*'Внутренняя политика'!O{k3})",
                    f"=M{k2}/100*5",
                    f"=M{k2}/100*5",
                    f"=0",
                    f"=J{k2}+K{k2}+L{k2}",
                    f"=(J{k2}+K{k2})-S{k2}-T{k2}",
                    f"=СУММ(J{k2}:K{k2})/100*5",
                    f"=СУММ(J{k2}:K{k2})/100*5",
                    f"=J{k2}/100*'Внутренняя политика'!P{k3}"
                ]]
            }
        ], raw = False)

        sh.worksheet("Города").format(f"B{k2+1}:U{k2+1}", {
            "backgroundColor": {
                "red": 39,
                "green": 39,
                "blue": 39
            }
        })

        sh.worksheet("Внутренняя политика").batch_update([
            {
                "range" : f"B{k3}:P{k3}",
                "values" : [[
                    name,
                    f"=СУММ('Города'!J{k2}:J{k2+1})+СУММ('Города'!K{k2}:K{k2+1})-СУММ('Города'!S{k2}:S{k2+1})-СУММ('Города'!T{k2}:T{k2+1})-СУММ('Города'!L{k2}:L{k2+1})",
                    f"=СУММ('Города'!S{k2}:S{k2+1})",
                    f"=СУММ('Города'!T{k2}:T{k2+1})",
                    f"=СУММ('Города'!L{k2}:L{k2+1})",
                    f"=50",
                    f"=50",
                    f"=50",
                    f"=1-(M{k3}/30)-(P{k3}/10)",
                    f"=1-(N{k3}/30)-(P{k3}/10)",
                    f"=1-(O{k3}/30)-(P{k3}/10)",
                    f"=10",
                    f"=10",
                    f"=10",
                    f"=3"
                ]]
            }
        ], raw = False)

        '''
        sh.worksheet("Внутренняя политика").format(f"B{k3+1}:P{k3+1}", {
            "backgroundColor": {
                "red": 39,
                "green": 39,
                "blue": 39
            }
        })
        '''

        sh.worksheet("Постройки").batch_update([
            {
                "range" : f"B{k5}:AG{k5}",
                "values" : [[
                    name,
                    namecapital,
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"=0"
                ]]
            }
        ], raw = False)

        sh.worksheet("Постройки").format(f"B{k5+1}:AG{k5+1}", {
            "backgroundColor": {
                "red": 39,
                "green": 39,
                "blue": 39
            }
        })

        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET colony = '{name}' WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET capital = '{namecapital}' WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET maritime = '{maritime}' WHERE iduser = {ctx.author.id}")

        cursor.execute(f"UPDATE {ctx.author.guild.id}_time SET globaltime = 60 WHERE id = 2")

        connection.commit()
        await ctx.send(f"**{member.mention}**, ваше государство \"{name}\" со столицей \"{namecapital}\" занесено в таблицу!")


async def setup(bot):
    await bot.add_cog(claim(bot))