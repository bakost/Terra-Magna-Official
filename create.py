import discord

from discord.ext import commands
from numpy import random

from gspread_formatting import *
from connectmysql import connection, cursor
from numpy.core.defchararray import title, isdigit
from config import *

class create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['reg'], pass_context=True)
    async def __create(self, ctx, *,  args=None):
        #cash = str(worksheet.get('A1')[0])[2:-2]
        #await ctx.send(cash)
        #worksheet.update("A1", "=A2+B2", raw = False)
        connection.connect()
        member = ctx.message.author

        cursor.execute(f"SELECT globaltime FROM {ctx.author.guild.id}_time WHERE id = 2")
        reco0 = int(cursor.fetchone()[0])

        if reco0 > 1:
            await ctx.send(f"**{member.mention}** время ожидания ещё не прошло, попробуйте выполнить команду позднее!")
            return

        if args is None:
            #await ctx.send(f"**{member.mention}** отсутствуют аргументы! Пример команды: !claim [Название государства] [Название столицы] [Название морской провинции]")
            await ctx.send(f"**{member.mention}**, отсутствуют аргументы! Пример команды: !reg [Название государства] [Название столицы] [Тип местности] [С какими городами граничит(писать через ; без пробелов), если не граничит то -] [С какими морскими провинциями граничит(писать через ; без пробелов), если не граничит то -]")
            return

        cursor.execute(f"UPDATE {ctx.author.guild.id}_time SET globaltime = 60 WHERE id = 2")

        connection.commit()

        cursor.execute(f"SELECT colony FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        reco2 = cursor.fetchone()[0]

        cursor.execute(f"SELECT colony FROM `{ctx.author.guild.id}`")
        reco4 = cursor.fetchall()

        cursor.execute(f"SELECT capital FROM `{ctx.author.guild.id}`")
        reco5 = cursor.fetchall()

        #await ctx.send(f"met1")

        cursor.execute(f"SELECT first_town FROM {ctx.author.guild.id}_towns")
        first_towns = cursor.fetchall()

        #await ctx.send(f"met2")

        cursor.execute(f"SELECT second_town FROM {ctx.author.guild.id}_towns")
        second_towns = cursor.fetchall()

        cursor.execute(f"SELECT town FROM {ctx.author.guild.id}_maritimes")
        town_mar = cursor.fetchall()

        cursor.execute(f"SELECT maritime FROM {ctx.author.guild.id}_maritimes")
        maritime_mar = cursor.fetchall()

        #await ctx.send(f"met3")

        name = str(title(str(args.split()[0])))
        namecapital = str(title(str(args.split()[1])))
        type_of_locality = str(args.split()[2])

        border_of_city = str(title(str(args.split()[3])))
        if ";" in border_of_city:
            border_of_city_massive = border_of_city.split(";")
            border_of_city_massive = title(border_of_city_massive)

        border_of_maritime = str(title(str(args.split()[4])))
        if ";" in border_of_maritime:
            border_of_maritime_massive = border_of_maritime.split(";")
            border_of_maritime_massive = title(border_of_maritime_massive)

        #await ctx.send(f"met4")

        name = str(name)
        namecapital = str(namecapital)
        type_of_locality = str(type_of_locality)

        towns = sh.worksheet("Города").get(f"{town_towns}:{town_towns}")
        towns = str(towns)[1:-1]
        towns = towns.replace("[", "")
        towns = towns.replace("]", "")
        towns = towns.replace(" \'", "")
        towns = towns.replace("\'", "")
        towns = towns.split(",")

        resources = sh.worksheet("Ресурсы").get(f"{resources_state}:{resources_state}")
        resources = str(resources)[1:-1]
        resources = resources.replace("[", "")
        resources = resources.replace("]", "")
        resources = resources.replace(" \'", "")
        resources = resources.replace("\'", "")
        resources = resources.split(",")

        countries = sh.worksheet("Доходы/Расходы").get(f"{income_expenses_state}:{income_expenses_state}")
        countries = str(countries)[1:-1]
        countries = countries.replace("[", "")
        countries = countries.replace("]", "")
        countries = countries.replace(" \'", "")
        countries = countries.replace("\'", "")
        countries = countries.split(",")

        dompol = sh.worksheet("Внутренняя политика").get(f"{domestic_policy_state}:{domestic_policy_state}")
        dompol = str(dompol)[1:-1]
        dompol = dompol.replace("[", "")
        dompol = dompol.replace("]", "")
        dompol = dompol.replace(" \'", "")
        dompol = dompol.replace("\'", "")
        dompol = dompol.split(",")

        buildings = sh.worksheet("Постройки").get(f"{building_state}:{building_state}")
        buildings = str(buildings)[1:-1]
        buildings = buildings.replace("[", "")
        buildings = buildings.replace("]", "")
        buildings = buildings.replace(" \'", "")
        buildings = buildings.replace("\'", "")
        buildings = buildings.split(",")

        laws = sh.worksheet("Законы").get(f"{laws_state}:{laws_state}")
        laws = str(laws)[1:-1]
        laws = laws.replace("[", "")
        laws = laws.replace("]", "")
        laws = laws.replace(" \'", "")
        laws = laws.replace("\'", "")
        laws = laws.split(",")

        #await ctx.send(f"met5")

        if reco2 is not None:
            await ctx.send(f"**{member.mention}** у вас уже есть государство!")
            return

        for i in range(0, len(reco4)):
            temp = str(reco4[i])[2:-3]
            if temp == name:
                await ctx.send(f"**{member.mention}** такое государство уже существует!")
                return

        #await ctx.send(f"met6")

        for i in range(0, len(reco5)):
            temp = str(reco5[i])[2:-3]
            if temp == namecapital:
                await ctx.send(f"**{member.mention}** такая столица уже существует!")
                return

        await ctx.send(f"**{member.mention}**, создание государства занимает несколько минут, по окончании вы будете уведомлены.")

        if ";" in border_of_city:
            for k in range(len(border_of_city_massive)):
                temp = str(border_of_city_massive[k])

                if (temp != "-") and not(temp in towns):
                    await ctx.send(f"**{member.mention}** города, с которым граничит ваш город, не существует!")
                    return

        #await ctx.send(f"met7")



        #await ctx.send(f"met8")

        #await ctx.send(f"{border_of_city}")

        #if ";" in border_of_city:
        #    await ctx.send(f"meta 8.0")

        if (";" in border_of_city) and (border_of_city != "-"):
            #await ctx.send(f"met8.1")
            for k in range(0, len(border_of_city_massive)):
                border_of_city = str(border_of_city_massive[k])

                counter_countries_temp = 1

                #await ctx.send(f"met9.{k}")

                while str(towns[counter_countries_temp]) != "Город":
                    counter_countries_temp += 1

                #await ctx.send(f"met10.{k}")

                while str(towns[counter_countries_temp]) != border_of_city:
                    counter_countries_temp += 1

                #await ctx.send(f"met11.{k}")

                counter_countries_temp += 1

                colony = str(sh.worksheet("Города").get(f"{town_state}{counter_countries_temp}"))[3:-3]

                #await ctx.send(f"met12.{k}")

                cursor.execute(f"SELECT iduser FROM `{ctx.author.guild.id}` WHERE colony = '{colony}'")
                iduser_second_player = int(cursor.fetchone()[0])

                temp_k = 0

                #await ctx.send(f"met13.{k}")

                cursor.execute(f"SELECT type_of_locality FROM `{ctx.author.guild.id}` WHERE iduser = {iduser_second_player}")
                second_type_of_locality = str(cursor.fetchone()[0])

                #await ctx.send(f"met14.{k}")

                for j in range(len(first_towns)):
                    if ((first_towns[j] == namecapital) and (second_towns[j] == border_of_city)) or ((first_towns[j] == border_of_city) and (second_towns[j] == namecapital)):
                        temp_k += 1

                #await ctx.send(f"met15.{k}")

                if temp_k == len(first_towns):
                    cursor.execute(f"INSERT INTO {ctx.author.guild.id}_towns(first_town, second_town, first_type_of_locality, second_type_of_locality) VALUES ('{namecapital}','{border_of_city}','{type_of_locality}','{second_type_of_locality}')")

                #await ctx.send(f"met16.{k}")

                connection.commit()

        elif border_of_city != "-":
            #await ctx.send(f"met9")
            counter_countries_temp = 1

            while str(towns[counter_countries_temp]) != "Город":
                counter_countries_temp += 1

            #await ctx.send(f"met10")

            while str(towns[counter_countries_temp]) != border_of_city:
                counter_countries_temp += 1

            counter_countries_temp += 1

            #await ctx.send(f"met11")

            colony = str(sh.worksheet("Города").get(f"{town_state}{counter_countries_temp}"))[3:-3]

            #await ctx.send(f"met12")

            cursor.execute(f"SELECT iduser FROM `{ctx.author.guild.id}` WHERE colony = '{colony}'")
            iduser_second_player = int(cursor.fetchone()[0])

            #await ctx.send(f"met13")

            temp_k = 0

            cursor.execute(f"SELECT type_of_locality FROM `{ctx.author.guild.id}` WHERE iduser = {iduser_second_player}")
            second_type_of_locality = str(cursor.fetchone()[0])

            #await ctx.send(f"met14")

            for j in range(len(first_towns)):
                if ((first_towns[j] == namecapital) and (second_towns[j] == border_of_city)) or ((first_towns[j] == border_of_city) and (second_towns[j] == namecapital)):
                    temp_k += 1

            #await ctx.send(f"met15")

            if temp_k == len(first_towns):
                cursor.execute(f"INSERT INTO {ctx.author.guild.id}_towns(first_town, second_town, first_type_of_locality, second_type_of_locality) VALUES ('{namecapital}','{border_of_city}','{type_of_locality}','{second_type_of_locality}')")

            connection.commit()

        #await ctx.send(f"metka100")

        if (";" in border_of_maritime) and (border_of_maritime != "-"):
            for k in range(0, len(border_of_maritime_massive)):
                border_of_maritime = str(border_of_maritime_massive[k])

                if not((border_of_maritime in maritime_mar) and (namecapital in town_mar)):
                    cursor.execute(f"INSERT INTO {ctx.author.guild.id}_maritimes(town, maritime) VALUES ('{namecapital}','{border_of_maritime}')")

                connection.commit()

        elif border_of_maritime != "-":

            if not((border_of_maritime in maritime_mar) and (namecapital in town_mar)):
                cursor.execute(f"INSERT INTO {ctx.author.guild.id}_maritimes(town, maritime) VALUES ('{namecapital}','{border_of_maritime}')")

            connection.commit()

        '''
        counter_countries_temp = 1

        iduser_second_player = 0

        if border_of_city != "-":
            while str(towns[counter_countries_temp]) != "Город":
                counter_countries_temp += 1

            while str(towns[counter_countries_temp]) != border_of_city:
                counter_countries_temp += 1

            counter_countries_temp += 1

            colony = str(sh.worksheet("Города").get(f"B{counter_countries_temp}"))[3:-3]

            cursor.execute(f"SELECT iduser FROM `{ctx.author.guild.id}` WHERE colony = '{colony}'")
            iduser_second_player = int(cursor.fetchone()[0])

        cursor.execute(f"SELECT border_of_city FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        border_of_city_temp = str(cursor.fetchone()[0])

        if border_of_city != "-":
            if border_of_city_temp != "None":
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_city = CONCAT(border_of_city, '{namecapital} ') WHERE iduser = {iduser_second_player}")
            else:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_city = '{namecapital} ' WHERE iduser = {iduser_second_player}")

        connection.commit()

        counter_countries_temp = 1

        iduser_second_player = 0

        if border_of_maritime != "-":
            while str(towns[counter_countries_temp]) != "Город":
                counter_countries_temp += 1

            while str(towns[counter_countries_temp]) != border_of_maritime:
                counter_countries_temp += 1

            counter_countries_temp += 1

            colony = str(sh.worksheet("Города").get(f"B{counter_countries_temp}"))[3:-3]

            cursor.execute(f"SELECT iduser FROM `{ctx.author.guild.id}` WHERE colony = '{colony}'")
            iduser_second_player = int(cursor.fetchone()[0])

        cursor.execute(f"SELECT border_of_maritime FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        border_of_maritime_temp = str(cursor.fetchone()[0])

        if border_of_maritime != "-":
            if border_of_maritime_temp != "None":
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_maritime = CONCAT(border_of_maritime, '{namecapital} ') WHERE iduser = {iduser_second_player}")
            else:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_maritime = '{namecapital} ' WHERE iduser = {iduser_second_player}")

        connection.commit()

        for k in range(len(border_of_city_massive)):
            border_of_city = str(border_of_city_massive[k])

            cursor.execute(f"SELECT border_of_city FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            border_of_city_temp = str(cursor.fetchone()[0])

            if border_of_city != "-":
                if border_of_city_temp != "None":
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_city = CONCAT(border_of_city, '{border_of_city} ') WHERE iduser = {ctx.author.id}")
                else:
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_city = '{border_of_city} ' WHERE iduser = {ctx.author.id}")

            connection.commit()

        for k in range(len(border_of_maritime_massive)):
            border_of_maritime = str(border_of_maritime_massive[k])

            cursor.execute(f"SELECT border_of_maritime FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            border_of_maritime_temp = str(cursor.fetchone()[0])

            if border_of_maritime != "-":
                if border_of_maritime_temp != "None":
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_maritime = CONCAT(border_of_maritime, '{border_of_maritime} ') WHERE iduser = {ctx.author.id}")
                else:
                    cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_maritime = '{border_of_maritime} ' WHERE iduser = {ctx.author.id}")

            connection.commit()
        '''
        counter_countries = 1
        counter_towns = 1
        counter_internal_policy = 1
        counter_resources = 1
        counter_buildings = 1
        counter_laws = 1

        while str(countries[counter_countries]) != "Государство":
            counter_countries += 1

        while counter_countries != len(countries):
            counter_countries += 1

        counter_countries += 1

        while str(towns[counter_towns]) != "Город":
            counter_towns += 1

        while counter_towns != len(towns):
            counter_towns += 1

        counter_towns += 2

        while str(dompol[counter_internal_policy]) != "Государство":
            counter_internal_policy += 1

        while counter_internal_policy != len(dompol):
            counter_internal_policy += 1

        counter_internal_policy += 1

        while str(resources[counter_resources]) != "Государство":
            counter_resources += 1

        while counter_resources != len(resources):
            counter_resources += 1

        counter_resources += 2

        while str(buildings[counter_buildings]) != "Государство":
            counter_buildings += 1

        while counter_buildings != len(buildings):
            counter_buildings += 1

        counter_buildings += 2

        while str(laws[counter_laws]) != "Государство":
            counter_laws += 1

        while counter_laws != len(laws):
            counter_laws += 1

        counter_laws += 1


        wood = 0
        stone = 0
        prodo = 0

        if type_of_locality == "Равнины":
            wood = random.randint(1,3)
            stone = random.randint(1,2)
            prodo = random.randint(1,3)

        if type_of_locality == "Лес":
            wood = random.randint(1,5)
            stone = random.randint(1,2)
            prodo = random.randint(1,4)

        if type_of_locality == "Побережье":
            wood = random.randint(1,2)
            stone = 0
            prodo = random.randint(1,2)

        if type_of_locality == "Саванна":
            wood = random.randint(1,3)
            stone = 0
            prodo = random.randint(1,2)

        if type_of_locality == "Горы":
            wood = random.randint(1,2)
            stone = random.randint(1,5)
            prodo = 0


        sh.worksheet("Ресурсы").batch_update([
            {
                "range" : f"{resources_frame_1}{counter_resources}:{resources_frame_2}{counter_resources}",
                "values" : [[
                    name,
                    namecapital,
                    f"='Постройки'!{building_sawmill}{counter_buildings}",
                    f"='Постройки'!{building_quarry}{counter_buildings}",
                    f"='Постройки'!{building_farm}{counter_buildings}",
                    f"='Постройки'!{building_scientific_center}{counter_buildings}",
                    f"='Постройки'!{building_paper_workshop}{counter_buildings}",
                    f"='Постройки'!{building_foundry_workshop}{counter_buildings}",
                    f"='Постройки'!{building_textile_workshop}{counter_buildings}",
                    f"='Постройки'!{building_rope_yard}{counter_buildings}",
                    f"='Постройки'!{building_plantation}{counter_buildings}",
                    f"='Постройки'!{building_gold_deposit}{counter_buildings}",
                    f"={resources_income_paper}{counter_resources}*2+{resources_income_grocery}{counter_resources}*2",
                    f"={resources_income_metall}{counter_resources}*2",
                    f"=0",
                    f"=0",
                    f"=0",
                    f"={resources_income_mechanisms}{counter_resources}*2",
                    f"=0",
                    f"=0",
                    f"={resources_income_cloth}{counter_resources}*2+{resources_income_gear}{counter_resources}*2",
                    f"=0"
                ]]
            }
        ], raw = False)

        sh.worksheet("Доходы/Расходы").batch_update([
            {
                "range" : f"{income_expenses_frame_1}{counter_countries}:{income_expenses_frame_2}{counter_countries}",
                "values" : [[
                    name,
                    f"=СУММ('Города'!{town_population}{counter_towns}:{town_population}{counter_towns+1})",
                    f"=0",
                    f"=СУММ('Города'!{town_income_resources}{counter_towns}:{town_income_resources}{counter_towns+1})",
                    f"=ЕСЛИ(СУММ('Ресурсы'!{resources_income_wood}{counter_resources}:{resources_income_wood}{counter_resources+1})>0,\"Дерево x\"&СУММ('Ресурсы'!{resources_income_wood}{counter_resources}:{resources_income_wood}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_income_stone}{counter_resources}:{resources_income_stone}{counter_resources+1})>0,\"Камень x\"&СУММ('Ресурсы'!{resources_income_stone}{counter_resources}:{resources_income_stone}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_income_mechanisms}{counter_resources}:{resources_income_mechanisms}{counter_resources+1})>0,\"Механизмы x\"&СУММ('Ресурсы'!{resources_income_mechanisms}{counter_resources}:{resources_income_mechanisms}{counter_resources}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_income_paper}{counter_resources}:{resources_income_paper}{counter_resources+1})>0,\"Бумага x\"&СУММ('Ресурсы'!{resources_income_paper}{counter_resources}:{resources_income_paper}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_income_metall}{counter_resources}:{resources_income_metall}{counter_resources+1})>0,\"Металл x\"&СУММ('Ресурсы'!{resources_income_metall}{counter_resources}:{resources_income_metall}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_income_cloth}{counter_resources}:{resources_income_cloth}{counter_resources+1})>0,\"Ткань x\"&СУММ('Ресурсы'!{resources_income_cloth}{counter_resources}:{resources_income_cloth}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_income_gear}{counter_resources}:{resources_income_gear}{counter_resources+1})>0,\"Снасти x\"&СУММ('Ресурсы'!{resources_income_gear}{counter_resources}:{resources_income_gear}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_income_grocery}{counter_resources}:{resources_income_grocery}{counter_resources+1})>0,\"Бакалея x\"&СУММ('Ресурсы'!{resources_income_grocery}{counter_resources}:{resources_income_grocery}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_income_gold}{counter_resources}:{resources_income_gold}{counter_resources+1})>0,\"Золото x\"&СУММ('Ресурсы'!{resources_income_gold}{counter_resources}:{resources_income_gold}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_income_prodo}{counter_resources}:{resources_income_prodo}{counter_resources+1})>0,\"Провизия x\"&СУММ('Ресурсы'!{resources_income_prodo}{counter_resources}:{resources_income_prodo}{counter_resources+1}),)",
                    f"=СУММ('Города'!{town_expenses_money}{counter_towns}:{town_expenses_money}{counter_towns+1})",
                    f"=ЕСЛИ(СУММ('Ресурсы'!{resources_expenses_wood}{counter_resources}:{resources_income_wood}{counter_resources+1})>0,\"Дерево x\"&СУММ('Ресурсы'!{resources_expenses_wood}{counter_resources}:{resources_expenses_wood}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_expenses_stone}{counter_resources}:{resources_expenses_stone}{counter_resources+1})>0,\"Камень x\"&СУММ('Ресурсы'!{resources_expenses_stone}{counter_resources}:{resources_expenses_stone}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_expenses_mechanisms}{counter_resources}:{resources_expenses_mechanisms}{counter_resources+1})>0,\"Механизмы x\"&СУММ('Ресурсы'!{resources_expenses_mechanisms}{counter_resources}:{resources_expenses_mechanisms}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_expenses_paper}{counter_resources}:{resources_expenses_paper}{counter_resources+1})>0,\"Бумага x\"&СУММ('Ресурсы'!{resources_expenses_paper}{counter_resources}:{resources_expenses_paper}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_expenses_metall}{counter_resources}:{resources_expenses_metall}{counter_resources+1})>0,\"Металл x\"&СУММ('Ресурсы'!{resources_expenses_metall}{counter_resources}:{resources_expenses_metall}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_expenses_cloth}{counter_resources}:{resources_expenses_cloth}{counter_resources+1})>0,\"Ткань x\"&СУММ('Ресурсы'!{resources_expenses_cloth}{counter_resources}:{resources_expenses_cloth}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_expenses_gear}{counter_resources}:{resources_expenses_gear}{counter_resources+1})>0,\"Канаты x\"&СУММ('Ресурсы'!{resources_expenses_gear}{counter_resources}:{resources_expenses_gear}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_expenses_grocery}{counter_resources}:{resources_expenses_grocery}{counter_resources+1})>0,\"Бакалея x\"&СУММ('Ресурсы'!{resources_expenses_grocery}{counter_resources}:{resources_expenses_grocery}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Ресурсы'!{resources_expenses_gold}{counter_resources}:{resources_expenses_gold}{counter_resources+1})>0,\"Золото x\"&СУММ('Ресурсы'!{resources_expenses_gold}{counter_resources}:{resources_expenses_gold}{counter_resources+1}),)&\" \"&ЕСЛИ(СУММ('Города'!{town_requirement_prodo}{counter_towns}:{town_requirement_prodo}{counter_towns+1})>0,\"Провизия x\"&СУММ('Города'!{town_requirement_prodo}{counter_towns}:{town_requirement_prodo}{counter_towns+1}),)",
                    f"={income_expenses_income_taxes}{counter_countries}-{income_expenses_expenses_armyflot}{counter_countries}",
                    f"=ЕСЛИ(СУММ('Ресурсы'!{resources_income_wood}{counter_resources}:{resources_income_wood}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_wood}{counter_resources}:{resources_expenses_wood}{counter_resources+1})<>0,\" Дерево x \"&СУММ('Ресурсы'!{resources_income_wood}{counter_resources}:{resources_income_wood}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_wood}{counter_resources}:{resources_expenses_wood}{counter_resources+1}),)&ЕСЛИ(СУММ('Ресурсы'!{resources_income_stone}{counter_resources}:{resources_income_stone}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_stone}{counter_resources}:{resources_expenses_stone}{counter_resources+1})<>0,\" Камень x \"&СУММ('Ресурсы'!{resources_income_stone}{counter_resources}:{resources_income_stone}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_stone}{counter_resources}:{resources_expenses_stone}{counter_resources+1}),)&ЕСЛИ(СУММ('Ресурсы'!{resources_income_mechanisms}{counter_resources}:{resources_income_mechanisms}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_mechanisms}{counter_resources}:{resources_expenses_mechanisms}{counter_resources+1})<>0,\" Механизмы x \"&СУММ('Ресурсы'!{resources_income_mechanisms}{counter_resources}:{resources_income_mechanisms}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_mechanisms}{counter_resources}:{resources_expenses_mechanisms}{counter_resources+1}),)&ЕСЛИ(СУММ('Ресурсы'!{resources_income_paper}{counter_resources}:{resources_income_paper}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_paper}{counter_resources}:{resources_expenses_paper}{counter_resources+1})<>0,\" Бумага x \"&СУММ('Ресурсы'!{resources_income_paper}{counter_resources}:{resources_income_paper}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_paper}{counter_resources}:{resources_expenses_paper}{counter_resources+1}),)&ЕСЛИ(СУММ('Ресурсы'!{resources_income_metall}{counter_resources}:{resources_income_metall}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_metall}{counter_resources}:{resources_expenses_metall}{counter_resources+1})<>0,\" Металл x \"&СУММ('Ресурсы'!{resources_income_metall}{counter_resources}:{resources_income_metall}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_metall}{counter_resources}:{resources_expenses_metall}{counter_resources+1}),)&ЕСЛИ(СУММ('Ресурсы'!{resources_income_cloth}{counter_resources}:{resources_income_cloth}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_cloth}{counter_resources}:{resources_expenses_cloth}{counter_resources+1})<>0,\" Ткань x \"&СУММ('Ресурсы'!{resources_income_cloth}{counter_resources}:{resources_income_cloth}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_cloth}{counter_resources}:{resources_expenses_cloth}{counter_resources+1}),)&ЕСЛИ(СУММ('Ресурсы'!{resources_income_gear}{counter_resources}:{resources_income_gear}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_gear}{counter_resources}:{resources_expenses_gear}{counter_resources+1})<>0,\" Снасти x \"&СУММ('Ресурсы'!{resources_income_gear}{counter_resources}:{resources_income_gear}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_gear}{counter_resources}:{resources_expenses_gear}{counter_resources+1}),)&ЕСЛИ(СУММ('Ресурсы'!{resources_income_grocery}{counter_resources}:{resources_income_grocery}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_grocery}{counter_resources}:{resources_expenses_grocery}{counter_resources+1})<>0,\" Бакалея x \"&СУММ('Ресурсы'!{resources_income_grocery}{counter_resources}:{resources_income_grocery}{counter_resources+1})-СУММ('Ресурсы'!{resources_expenses_grocery}{counter_resources}:{resources_expenses_grocery}{counter_resources+1}),)&ЕСЛИ((СУММ('Ресурсы'!{resources_income_prodo}{counter_resources}:{resources_income_prodo}{counter_resources+1})-СУММ('Города'!{town_requirement_prodo}{counter_towns}:{town_requirement_prodo}{counter_towns+1}))<>0,\" Провизия x \"&(СУММ('Ресурсы'!{resources_income_prodo}{counter_resources}:{resources_income_prodo}{counter_resources+1})-СУММ('Города'!{town_requirement_prodo}{counter_towns}:{town_requirement_prodo}{counter_towns+1})),)",
                    f"=СУММ('Города'!{town_recruits}{counter_towns}:{town_recruits}{counter_towns+1})"
                ]]
            }
        ], raw = False)

        sh.worksheet("Города").batch_update([
            {
                "range" : f"{town_frame_1}{counter_towns}:{town_frame_2}{counter_towns}",
                "values" : [[
                    name,
                    namecapital,
                    f"=ЕСЛИ('Постройки'!{building_sawmill}{counter_buildings}>0,\"Лесопилка x\"&'Постройки'!{building_sawmill}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_quarry}{counter_buildings}>0,\"Каменоломня x\"&'Постройки'!{building_quarry}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_farm}{counter_buildings}>0,\"Ферма x\"&'Постройки'!{building_farm}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_scientific_center}{counter_buildings}>0,\"Научный центр x\"&'Постройки'!{building_scientific_center}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_paper_workshop}{counter_resources}>0,\"Бумажная мастерская x\"&'Постройки'!{building_paper_workshop}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_foundry_workshop}{counter_buildings}>0,\"Литейная мастерская x\"&'Постройки'!{building_foundry_workshop}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_textile_workshop}{counter_buildings}>0,\"Текстильная мастерская x\"&'Постройки'!{building_textile_workshop}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_rope_yard}{counter_buildings}>0,\"Канатный ярд x\"&'Постройки'!{building_rope_yard}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_plantation}{counter_buildings}>0,\"Плантация x\"&'Постройки'!{building_plantation}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_home}{counter_buildings}>0,\"Жилой дом x\"&'Постройки'!{building_home}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_church}{counter_buildings}>0,\"Церковь x\"&'Постройки'!{building_church}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_palace}{counter_buildings}>0,\"Дворец x\"&'Постройки'!{building_palace}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_barracks}{counter_buildings}>0,\"Казармы x\"&'Постройки'!{building_barracks}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_fortress}{counter_buildings}>0,\"Крепость x\"&'Постройки'!{building_fortress}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_capital_fortress}{counter_buildings}>0,\"Столичная крепость x\"&'Постройки'!{building_capital_fortress}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_port}{counter_buildings}>0,\"Порт x\"&'Постройки'!{building_port}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_shipyard}{counter_buildings}>0,\"Верфь x\"&'Постройки'!{building_shipyard}{counter_buildings},)",
                    f"Дерево x{wood}, Камень x{stone}, Провизия x{prodo}",
                    f"=(((({town_estates_citizens}{counter_towns}/100*'Внутренняя политика'!{domestic_policy_taxes_citizens}{counter_internal_policy})))+((({town_estates_clergy}{counter_towns}/100*'Внутренняя политика'!{domestic_policy_taxes_clergy}{counter_internal_policy})))+((({town_estates_nobility}{counter_towns}/100*'Внутренняя политика'!{domestic_policy_taxes_nobility}{counter_internal_policy}))))*ЕСЛИ('Законы'!{laws_equality}{counter_laws}=\"Принято\",1.1,1)*ЕСЛИ('Законы'!{laws_significant_privileges}{counter_laws}=\"Принято\",0.8,1)*ЕСЛИ('Законы'!{laws_religion_doesnt_matter}{counter_laws}=\"Принято\",0.95,1)*ЕСЛИ('Законы'!{laws_fanaticism}{counter_laws}=\"Принято\",1.05,1)*ЕСЛИ('Законы'!{laws_natives_oppression}{counter_laws}=\"Принято\",1.1,1)*ЕСЛИ('Законы'!{laws_conditional_slavery}{counter_laws}=\"Принято\",1.1,1)*ЕСЛИ('Внутренняя политика'!{domestic_policy_loyality_clergy}{counter_internal_policy}>=60,1.1,1)",
                    f"=ЕСЛИ('Постройки'!{building_sawmill}{counter_buildings}>0,\"Дерево x\"&'Ресурсы'!{resources_income_wood}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_quarry}{counter_buildings}>0,\"Камень x\"&'Ресурсы'!{resources_income_stone}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_farm}{counter_buildings}>0,\"Провизия x\"&'Ресурсы'!{resources_income_prodo}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_scientific_center}{counter_buildings}>0,\"Механизмы x\"&'Ресурсы'!{resources_income_mechanisms}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_paper_workshop}{counter_buildings}>0,\"Бумага x\"&'Ресурсы'!{resources_income_paper}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_foundry_workshop}{counter_buildings}>0,\"Металл x\"&'Ресурсы'!{resources_income_metall}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_textile_workshop}{counter_buildings}>0,\"Ткань x\"&'Ресурсы'!{resources_income_cloth}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_rope_yard}{counter_buildings}>0,\"Снасти x\"&'Ресурсы'!{resources_income_gear}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_plantation}{counter_buildings}>0,\"Бакалея x\"&'Ресурсы'!{resources_income_grocery}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_gold_deposit}{counter_buildings}>0,\"Золото x\"&'Ресурсы'!{resources_income_gold}{counter_resources},\"\")",
                    f"=ЕСЛИ('Постройки'!{building_fortress}{counter_buildings}>0,'Постройки'!{building_fortress}{counter_buildings}*50,0)",
                    f"=ЕСЛИ('Ресурсы'!{resources_expenses_wood}{counter_resources}>0,\"Дерево x\"&'Ресурсы'!{resources_expenses_wood}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_stone}{counter_resources}>0,\"Камень x\"&'Ресурсы'!{resources_expenses_stone}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_prodo}{counter_resources}>0,\"Провизия x\"&'Ресурсы'!{resources_expenses_prodo}{counter_resources},\"\")&\" \"&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_mechanisms}{counter_resources}>0,\"Механизмы x\"&'Ресурсы'!{resources_expenses_mechanisms}{counter_resources},\"\")&\" \"&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_paper}{counter_resources}>0,\"Бумага x\"&'Ресурсы'!{resources_expenses_paper}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_metall}{counter_resources}>0,\"Металл x\"&'Ресурсы'!{resources_expenses_metall}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_cloth}{counter_resources}>0,\"Ткань x\"&'Ресурсы'!{resources_expenses_cloth}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_gear}{counter_resources}>0,\"Снасти x\"&'Ресурсы'!{resources_expenses_gear}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_grocery}{counter_resources}>0,\"Бакалея x\"&'Ресурсы'!{resources_expenses_grocery}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_gold}{counter_resources}>0,\"Золото x\"&'Ресурсы'!{resources_expenses_gold}{counter_resources},\"\")&\" \"",
                    f"=1000",
                    f"=0",
                    f"=0",
                    f"={town_unoccupied_population}{counter_towns}+{town_occupied_population}{counter_towns}+{town_slaves}{counter_towns}",
                    f"=(({town_estates_citizens}{counter_towns}/100*5)+(ЕСЛИ('Доходы/Расходы'!{income_expenses_prestige}{counter_countries}>0,({town_estates_citizens}{counter_towns}/100*5)/100*'Доходы/Расходы'!{income_expenses_prestige}{counter_countries},({town_estates_citizens}{counter_towns}/100*5)/100*'Доходы/Расходы'!{income_expenses_prestige}{counter_countries}*2)+(ЕСЛИ('Постройки'!{building_home}{counter_buildings}>0,{town_estates_citizens}{counter_towns}/100*1.5,0))+(ЕСЛИ('Законы'!{laws_democracy}{counter_laws}=\"Принято\",({town_estates_citizens}{counter_towns}/100*5)/100*20,0))-(ЕСЛИ('Законы'!{laws_dictatorship}{counter_laws}=\"Принято\",({town_estates_citizens}{counter_towns}/100*5)/100*20,0))+(ЕСЛИ('Законы'!{laws_open_doors}{counter_laws}=\"Принято\",({town_estates_citizens}{counter_towns}/100*5)/100*20,0))-(ЕСЛИ('Законы'!{laws_isolation}{counter_laws}=\"Принято\",({town_estates_citizens}{counter_towns}/100*5)/100*20,0))-(ЕСЛИ('Законы'!{laws_natives_peaceful}{counter_laws}=\"Принято\",({town_estates_citizens}{counter_towns}/100*5)/100*10,0))+(ЕСЛИ('Законы'!{laws_natives_oppression}{counter_laws}=\"Принято\",({town_estates_citizens}{counter_towns}/100*5)/100*10,0))+(ЕСЛИ('Законы'!{laws_emphasis_fleet}{counter_laws}=\"Принято\",({town_estates_citizens}{counter_towns}/100*5)/100*10,0))-({town_estates_citizens}{counter_towns}/100*5)/100*'Внутренняя политика'!{domestic_policy_taxes_citizens}{counter_internal_policy}*2))*ЕСЛИ('Постройки'!{building_home}{counter_buildings}>0,1.1,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Равнины\",1,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Лес\",0.95,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Побережье\",1.1,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Саванна\",0.9,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Горы\",0.85,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Пустыня\",0.7,1)",
                    f"=({town_estates_clergy}{counter_towns}/100*5+(({town_estates_clergy}{counter_towns}/100*5)/100*'Доходы/Расходы'!{income_expenses_prestige}{counter_countries})+(ЕСЛИ('Постройки'!{building_church}{counter_buildings}>0,{town_estates_clergy}{counter_towns}/100*1.5,0))+(ЕСЛИ('Законы'!{laws_democracy}{counter_laws}=\"Принято\",({town_estates_clergy}{counter_towns}/100*5)/100*20,0))-(ЕСЛИ('Законы'!{laws_dictatorship}{counter_laws}=\"Принято\",({town_estates_clergy}{counter_towns}/100*5)/100*20,0))+(ЕСЛИ('Законы'!{laws_open_doors}{counter_laws}=\"Принято\",({town_estates_clergy}{counter_laws}/100*5)/100*20,0))-(ЕСЛИ('Законы'!{laws_isolation}{counter_laws}=\"Принято\",({town_estates_clergy}{counter_towns}/100*5)/100*20,0))-(ЕСЛИ('Законы'!{laws_natives_peaceful}{counter_laws}=\"Принято\",({town_estates_clergy}{counter_towns}/100*5)/100*10,0))+(ЕСЛИ('Законы'!{laws_natives_oppression}{counter_laws}=\"Принято\",({town_estates_clergy}{counter_towns}/100*5)/100*10,0))+(ЕСЛИ('Законы'!{laws_emphasis_fleet}{counter_laws}=\"Принято\",({town_estates_clergy}{counter_towns}/100*5)/100*10,0))-({town_estates_clergy}{counter_towns}/100*5)/100*'Внутренняя политика'!{domestic_policy_taxes_clergy}{counter_internal_policy}*2)*ЕСЛИ('Постройки'!{building_church}{counter_buildings}>0,1.1,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Равнины\",1,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Лес\",0.95,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Побережье\",1.1,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Саванна\",0.9,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Горы\",0.85,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Пустыня\",0.7,1)",
                    f"=({town_estates_nobility}{counter_towns}/100*5+(({town_estates_nobility}{counter_towns}/100*5)/100*'Доходы/Расходы'!{income_expenses_prestige}{counter_countries})+ЕСЛИ('Постройки'!{building_church}{counter_buildings}>0,{town_estates_nobility}{counter_towns}/100*1.5,0)+(ЕСЛИ('Законы'!{laws_democracy}{counter_laws}=\"Принято\",({town_estates_nobility}{counter_towns}/100*5)/100*20,0))-(ЕСЛИ('Законы'!{laws_dictatorship}{counter_laws}=\"Принято\",({town_estates_nobility}{counter_towns}/100*5)/100*20,0))+(ЕСЛИ('Законы'!{laws_open_doors}{counter_laws}=\"Принято\",({town_estates_nobility}{counter_laws}/100*5)/100*20,0))-(ЕСЛИ('Законы'!{laws_isolation}{counter_laws}=\"Принято\",({town_estates_nobility}{counter_towns}/100*5)/100*20,0))-(ЕСЛИ('Законы'!{laws_natives_peaceful}{counter_laws}=\"Принято\",({town_estates_nobility}{counter_towns}/100*5)/100*10,0))+(ЕСЛИ('Законы'!{laws_natives_oppression}{counter_laws}=\"Принято\",({town_estates_nobility}{counter_towns}/100*5)/100*10,0))+(ЕСЛИ('Законы'!{laws_emphasis_fleet}{counter_laws}=\"Принято\",({town_estates_nobility}{counter_towns}/100*5)/100*10,0))-({town_estates_nobility}{counter_towns}/100*5)/100*'Внутренняя политика'!{domestic_policy_taxes_nobility}{counter_internal_policy}*2)*ЕСЛИ('Постройки'!{building_palace}{counter_buildings}>0,1.1,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Равнины\",1,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Лес\",0.95,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Побережье\",1.1,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Саванна\",0.9,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Горы\",0.85,1)*ЕСЛИ({town_type_of_locality}{counter_towns}=\"Пустыня\",0.7,1)",
                    f"={town_population}{counter_towns}/100*80",
                    f"={town_population}{counter_towns}/100*10",
                    f"={town_population}{counter_towns}/100*10",
                    f"=(({town_unoccupied_population}{counter_towns}/100*'Внутренняя политика'!{domestic_policy_recruitment_call}{counter_internal_policy})*ЕСЛИ('Законы'!{laws_dictatorship}{counter_laws}=\"Принято\",1.2,1)*ЕСЛИ('Законы'!{laws_emphasis_fleet}{counter_laws}=\"Принято\",1.1,1)*ЕСЛИ('Законы'!{laws_emphasis_army}{counter_laws}=\"Принято\",1.2,1)+ЕСЛИ('Доходы/Расходы'!{income_expenses_prestige}{counter_countries}>0,({town_unoccupied_population}{counter_towns}/100*'Внутренняя политика'!{domestic_policy_recruitment_call}{counter_internal_policy})/100*'Доходы/Расходы'!{income_expenses_prestige}{counter_countries},({town_unoccupied_population}{counter_towns}/100*'Внутренняя политика'!{domestic_policy_recruitment_call}{counter_internal_policy})/100*'Доходы/Расходы'!{income_expenses_prestige}{counter_countries}*2))*ЕСЛИ('Постройки'!{building_barracks}{counter_buildings}>0,1.15,1)",
                    f"=(({town_unoccupied_population}{counter_towns}/1000)+({town_occupied_population}{counter_towns}/1000))*ЕСЛИ('Внутренняя политика'!{domestic_policy_loyality_citizens}{counter_internal_policy}>=60,0.8,1)+(({town_slaves}{counter_towns}/1000)*0.5)",
                    type_of_locality
                ]]
            }
        ], raw = False)

        sh.worksheet("Внутренняя политика").batch_update([
            {
                "range" : f"{domestic_policy_frame_1}{counter_internal_policy}:{domestic_policy_frame_2}{counter_internal_policy}",
                "values" : [[
                    name,
                    f"=СУММ('Города'!{town_unoccupied_population}{counter_towns}:{town_unoccupied_population}{counter_towns+1})+СУММ('Города'!{town_occupied_population}{counter_towns}:{town_occupied_population}{counter_towns+1})-СУММ('Города'!{town_estates_clergy}{counter_towns}:{town_estates_clergy}{counter_towns+1})-СУММ('Города'!{town_estates_nobility}{counter_towns}:{town_estates_nobility}{counter_towns+1})-СУММ('Города'!{town_slaves}{counter_towns}:{town_slaves}{counter_towns+1})",
                    f"=СУММ('Города'!{town_estates_clergy}{counter_towns}:{town_estates_clergy}{counter_towns+1})",
                    f"=СУММ('Города'!{town_estates_nobility}{counter_towns}:{town_estates_nobility}{counter_towns+1})",
                    f"=СУММ('Города'!{town_slaves}{counter_towns}:{town_slaves}{counter_towns+1})",
                    f"=50",
                    f"=50",
                    f"=50",
                    f"=ЕСЛИ('Законы'!{laws_democracy}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_dictatorship}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_equality}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_minor_inequality}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_significant_privileges}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_open_doors}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_isolation}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_religion_doesnt_matter}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_spirituality}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_fanaticism}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_natives_peaceful}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_natives_oppression}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_emphasis_fleet}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_balance_armyflot}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_emphasis_army}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_limited_slavery}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_slave_owning_society}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}<=15,0.1,)+ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}<=10,0.1,)+ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}<=5,0.1)-ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}>15,0.1)-ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}>=20,0.1)-ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}>=25,0.1)-ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}>=30,0.15)-ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}>=35,0.15)-ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}>=40,0.15)-ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}>=45,0.15)-ЕСЛИ({domestic_policy_taxes_citizens}{counter_internal_policy}=50,0.15)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=0,0.2,)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=1,0.1,)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=2,0.05,)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=3,0.025,)-ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=4,0.05,)-ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=5,0.1,)",
                    f"=ЕСЛИ('Законы'!{laws_equality}{counter_laws}=\"Принято\",-0.1,)+ЕСЛИ('Законы'!{laws_significant_privileges}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_open_doors}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_average_openness}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_isolation}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_religion_doesnt_matter}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{domestic_policy_taxes_clergy}{counter_internal_policy}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_natives_peaceful}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_natives_oppression}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_conditional_slavery}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_slave_owning_society}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}<=15,0.1,)+ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}<=10,0.1,)+ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}<=5,0.1)-ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}>15,0.1)-ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}>=20,0.1)-ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}>=25,0.1)-ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}>=30,0.15)-ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}>=35,0.15)-ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}>=40,0.15)-ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}>=45,0.15)-ЕСЛИ({domestic_policy_taxes_clergy}{counter_internal_policy}=50,0.15)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=0,0.2,)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=1,0.1,)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=2,0.05,)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=3,0.025,)-ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=4,0.05,)-ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=5,0.1,)",
                    f"=-ЕСЛИ('Законы'!{laws_democracy}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_oligarchy}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_dictatorship}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_equality}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_significant_privileges}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_natives_peaceful}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_neutrality}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_natives_oppression}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_emphasis_fleet}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_balance_armyflot}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_emphasis_army}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_conditional_slavery}{counter_laws}=\"Принято\",0.1,)-ЕСЛИ('Законы'!{laws_limited_slavery}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ('Законы'!{laws_slave_owning_society}{counter_laws}=\"Принято\",0.1,)+ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}<=15,0.1,)+ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}<=10,0.1,)+ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}<=5,0.1)-ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}>15,0.1)-ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}>=20,0.1)-ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}>=25,0.1)-ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}>=30,0.15)-ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}>=35,0.15)-ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}>=40,0.15)-ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}>=45,0.15)-ЕСЛИ({domestic_policy_taxes_nobility}{counter_internal_policy}=50,0.15)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=0,0.2,)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=1,0.1,)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=2,0.05,)+ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=3,0.025,)-ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=4,0.05,)-ЕСЛИ({domestic_policy_recruitment_call}{counter_internal_policy}=5,0.1,)",
                    f"=10",
                    f"=10",
                    f"=10",
                    f"=3"
                ]]
            }
        ], raw = False)

        sh.worksheet("Постройки").batch_update([
            {
                "range" : f"{building_frame_1}{counter_buildings}:{building_frame_2}{counter_buildings}",
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
                    f"=1",
                    f"=0",
                    f"=0",
                    f"=0"
                ]]
            }
        ], raw = False)

        sh.worksheet("Законы").batch_update([
            {
                "range" : f"{laws_frame_1}{counter_laws}:{laws_frame_2}{counter_laws}",
                "values" : [[
                    name,
                    f"",
                    f"Принято",
                    f"",
                    f"",
                    f"Принято",
                    f"",
                    f"",
                    f"Принято",
                    f"",
                    f"",
                    f"Принято",
                    f"",
                    f"",
                    f"Принято",
                    f"",
                    f"",
                    f"Принято",
                    f"",
                    f"",
                    f"Принято",
                    f""
                ]]
            }
        ], raw = False)

        worksheettown = sh.worksheet('Города')
        worksheetbuilding = sh.worksheet('Постройки')
        worksheetresources = sh.worksheet('Ресурсы')

        set_row_height(worksheettown, f"{counter_towns}", 50)
        set_row_height(worksheettown, f"{counter_towns+1}", 11)

        set_row_height(worksheetbuilding, f"{counter_buildings}", 50)
        set_row_height(worksheetbuilding, f"{counter_buildings+1}", 11)

        set_row_height(worksheetresources, f"{counter_resources}", 50)
        set_row_height(worksheetresources, f"{counter_resources+1}", 11)

        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET colony = '{name}' WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET capital = '{namecapital}' WHERE iduser = {ctx.author.id}")
        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET type_of_locality = '{type_of_locality}' WHERE iduser = {ctx.author.id}")

        '''
        cursor.execute(f"INSERT INTO {ctx.author.guild.id}_economy(name, type, res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11) VALUES ('{name}','Продажа', 50, 50, 70, 80, 80, 80, 40, 60, 40, 0.15, 200)")
        cursor.execute(f"INSERT INTO {ctx.author.guild.id}_economy(name, type, res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11) VALUES ('{name}','Покупка', 50, 50, 70, 80, 80, 80, 40, 60, 40, 0.15, 200)")
        cursor.execute(f"INSERT INTO {ctx.author.guild.id}_economy(name, type, res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11) VALUES ('{name}','Количество', 10, 10, 10, 10, 10, 10, 10, 10, 10, 3000, 10)")
        '''

        connection.commit()
        await ctx.send(f"**{member.mention}**, ваше государство \"{name}\" со столицей \"{namecapital}\" занесено в таблицу!")


async def setup(bot):
    await bot.add_cog(create(bot))