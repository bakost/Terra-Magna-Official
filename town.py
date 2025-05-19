import asyncio

import discord
import gspread

from discord.ext import commands
from numpy import random

from gspread_formatting import *
from config import *
from connectmysql import connection, cursor
from numpy.core.defchararray import title

gs = gspread.service_account(filename='tm.json')
sh = gs.open_by_key(keygooglesheet)
worksheet = sh.sheet1

class town(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['claim'], pass_context=True)
    async def __town(self, ctx, *,  args=None):
        connection.connect()

        member = ctx.message.author

        cursor.execute(f"SELECT globaltime FROM {ctx.author.guild.id}_time WHERE id = 3")
        reco0 = int(cursor.fetchone()[0])

        cursor.execute(f"SELECT colony FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        namecolony = str(cursor.fetchone()[0])

        cursor.execute(f"SELECT first_town FROM {ctx.author.guild.id}_towns")
        first_towns = cursor.fetchall()

        cursor.execute(f"SELECT second_town FROM {ctx.author.guild.id}_towns")
        second_towns = cursor.fetchall()

        cursor.execute(f"SELECT town FROM {ctx.author.guild.id}_maritimes")
        town_mar = cursor.fetchall()

        cursor.execute(f"SELECT maritime FROM {ctx.author.guild.id}_maritimes")
        maritime_mar = cursor.fetchall()

        if reco0 > 1:
            await ctx.send(f"**{member.mention}** время ожидания ещё не прошло, попробуйте выполнить команду позднее!")
            return

        if args is None:
            #await ctx.send(f"**{member.mention}** отсутствуют аргументы! Пример команды: !town [Название города]")
            await ctx.send(f"**{member.mention}** отсутствуют аргументы! Пример команды: !claim [Название города] [Тип местности] [С какими городами граничит(писать через ; без пробелов), если не граничит то -] [С какими морскими провинциями граничит(писать через ; без пробелов), если не граничит то -] [Город, из которого прибудут переселенцы]")
            return

        if namecolony == "None":
            await ctx.send(f"**{member.mention}** у вас нет государства!")
            return

        cursor.execute(f"UPDATE {ctx.author.guild.id}_time SET globaltime = 60 WHERE id = 3")

        connection.commit()

        name = title(str(args.split()[0]))
        type_of_locality = str(args.split()[1])

        border_of_city = str(args.split()[2])
        if ";" in border_of_city:
            border_of_city_massive = border_of_city.split(";")
            border_of_city_massive = title(border_of_city_massive)

        border_of_maritime = str(args.split()[3])
        if ";" in border_of_maritime:
            border_of_maritime_massive = border_of_maritime.split(";")
            border_of_maritime_massive = title(border_of_maritime_massive)

        try:
            town_population_set = str(args.split()[4])

        except:
            cursor.execute(f"SELECT capital FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            town_population_set = str(cursor.fetchone()[0])


        name = str(name)
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

        dompol = sh.worksheet("Внутренняя политика").get(f"{domestic_policy_state}:{domestic_policy_state}")
        dompol = str(dompol)[1:-1]
        dompol = dompol.replace("[", "")
        dompol = dompol.replace("]", "")
        dompol = dompol.replace(" \'", "")
        dompol = dompol.replace("\'", "")
        dompol = dompol.split(",")

        countries = sh.worksheet("Доходы/Расходы").get(f"{income_expenses_state}:{income_expenses_state}")
        countries = str(countries)[1:-1]
        countries = countries.replace("[", "")
        countries = countries.replace("]", "")
        countries = countries.replace(" \'", "")
        countries = countries.replace("\'", "")
        countries = countries.split(",")

        towns_state = sh.worksheet("Города").get(f"{town_state}:{town_state}")
        towns_state = str(towns_state)[1:-1]
        towns_state = towns_state.replace("[", "")
        towns_state = towns_state.replace("]", "")
        towns_state = towns_state.replace(" \'", "")
        towns_state = towns_state.replace("\'", "")
        towns_state = towns_state.split(",")

        countrycheck = ""

        counter_towns_temp = 1

        for i in range(0, len(towns)):
            temp = str(towns[i])
            temp_country = str(towns_state[i])
            if temp == town_population_set:
                countrycheck = temp_country
                counter_towns_temp = i

        counter_towns_temp += 1

        if countrycheck != namecolony:
            await ctx.send(f"**{member.mention}** город, который вы хотите использовать для использования поселенцев не ваш!")
            return

        population_town = str(sh.worksheet("Города").get(f"{town_unoccupied_population}{counter_towns_temp}"))[3:-3]
        population_town = int(population_town)

        if population_town < 300:
            await ctx.send(f"**{member.mention}** в городе {town_population_set} не достаточно поселенцев!")
            return

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

        for i in range(0, len(towns)):
            temp = str(towns[i])
            if temp == name:
                await ctx.send(f"**{member.mention}** такой город уже существует!")
                return

        await ctx.send(f"**{member.mention}**, создание города занимает менее минуты, по окончании вы будете уведомлены.")

        if ";" in border_of_city:
            for k in range(len(border_of_city_massive)):
                border_of_city = str(border_of_city_massive[k])

                if (border_of_city != "-") and not(border_of_city in towns):
                    await ctx.send(f"**{member.mention}** города, с которым граничит ваш город, не существует!")
                    return
        '''
        if ";" in border_of_maritime:
            for k in range(len(border_of_maritime_massive)):
                border_of_maritime = str(border_of_maritime_massive[k])

                if (border_of_maritime != "-") and not(border_of_maritime in towns):
                    await ctx.send(f"**{member.mention}** города, с которым граничит ваш город, не существует!")
                    return
        '''

        if (";" in border_of_city) and (border_of_city != "-"):
            for k in range(0, len(border_of_city_massive)):
                border_of_city = str(border_of_city_massive[k])

                counter_countries_temp = 1

                while str(towns[counter_countries_temp]) != "Город":
                    counter_countries_temp += 1

                while str(towns[counter_countries_temp]) != border_of_city:
                    counter_countries_temp += 1

                counter_countries_temp += 1

                colony = str(sh.worksheet("Города").get(f"{towns_state}{counter_countries_temp}"))[3:-3]

                cursor.execute(f"SELECT iduser FROM `{ctx.author.guild.id}` WHERE colony = '{colony}'")
                iduser_second_player = int(cursor.fetchone()[0])

                temp_k = 0

                cursor.execute(f"SELECT type_of_locality FROM `{ctx.author.guild.id}` WHERE iduser = {iduser_second_player}")
                second_type_of_locality = str(cursor.fetchone()[0])

                for j in range(len(first_towns)):
                    if ((first_towns[j] == name) and (second_towns[j] == border_of_city)) or ((first_towns[j] == border_of_city) and (second_towns[j] == name)):
                        temp_k += 1

                if temp_k == len(first_towns):
                    cursor.execute(f"INSERT INTO {ctx.author.guild.id}_towns(first_town, second_town, first_type_of_locality, second_type_of_locality) VALUES ('{name}','{border_of_city}','{type_of_locality}','{second_type_of_locality}')")

                connection.commit()

        elif border_of_city != "-":

            counter_countries_temp = 1

            while str(towns[counter_countries_temp]) != "Город":
                counter_countries_temp += 1

            while str(towns[counter_countries_temp]) != border_of_city:
                counter_countries_temp += 1

            counter_countries_temp += 1

            colony = str(sh.worksheet("Города").get(f"{town_state}{counter_countries_temp}"))[3:-3]

            cursor.execute(f"SELECT iduser FROM `{ctx.author.guild.id}` WHERE colony = '{colony}'")
            iduser_second_player = int(cursor.fetchone()[0])

            temp_k = 0

            cursor.execute(f"SELECT type_of_locality FROM `{ctx.author.guild.id}` WHERE iduser = {iduser_second_player}")
            second_type_of_locality = str(cursor.fetchone()[0])

            for j in range(len(first_towns)):
                if ((first_towns[j] == name) and (second_towns[j] == border_of_city)) or ((first_towns[j] == border_of_city) and (second_towns[j] == name)):
                    temp_k += 1

            if temp_k == len(first_towns):
                cursor.execute(f"INSERT INTO {ctx.author.guild.id}_towns(first_town, second_town, first_type_of_locality, second_type_of_locality) VALUES ('{name}','{border_of_city}','{type_of_locality}','{second_type_of_locality}')")

            connection.commit()



        if (";" in border_of_maritime) and (border_of_maritime != "-"):
            for k in range(0, len(border_of_maritime_massive)):
                border_of_maritime = str(border_of_maritime_massive[k])

                if not((border_of_maritime in maritime_mar) and (name in town_mar)):
                    cursor.execute(f"INSERT INTO {ctx.author.guild.id}_maritimes(town, maritime) VALUES ('{name}','{border_of_maritime}')")

                connection.commit()

        elif border_of_maritime != "-":

            if not((border_of_maritime in maritime_mar) and (name in town_mar)):
                cursor.execute(f"INSERT INTO {ctx.author.guild.id}_maritimes(town, maritime) VALUES ('{name}','{border_of_maritime}')")

            connection.commit()


        '''
        cursor.execute(f"SELECT border_of_city FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        border_of_city_temp = str(cursor.fetchone()[0])

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

        if border_of_city != "-":
            if border_of_city_temp != "None":
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_city = CONCAT(border_of_city, '{name} ') WHERE iduser = {iduser_second_player}")
            else:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_city = '{name} ' WHERE iduser = {iduser_second_player}")

        connection.commit()

        cursor.execute(f"SELECT border_of_maritime FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        border_of_maritime_temp = str(cursor.fetchone()[0])

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

        if border_of_maritime != "-":
            if border_of_maritime_temp != "None":
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_maritime = CONCAT(border_of_maritime, '{name} ') WHERE iduser = {iduser_second_player}")
            else:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET border_of_maritime = '{name} ' WHERE iduser = {iduser_second_player}")

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

        while str(countries[counter_countries]) != namecolony:
            counter_countries += 1

        counter_countries += 1

        print(f"meta0")

        while str(towns_state[counter_towns]) != "Государство":
            counter_towns += 1

        while str(towns_state[counter_towns]) != namecolony:
            counter_towns += 1

        try:
            while str(towns_state[counter_towns]) == namecolony:
                counter_towns += 1
        except:
            pass

        counter_towns += 1

        while str(dompol[counter_internal_policy]) != "Государство":
            counter_internal_policy += 1

        while str(dompol[counter_internal_policy]) != namecolony:
            counter_internal_policy += 1

        counter_internal_policy += 1

        while str(resources[counter_resources]) != "Государство":
            counter_resources += 1

        while str(resources[counter_resources]) != namecolony:
            counter_resources += 1
        try:
            while str(resources[counter_resources]) == namecolony:
                counter_resources += 1
        except:
            pass

        counter_resources += 1

        while str(buildings[counter_buildings]) != "Государство":
            counter_buildings += 1

        while str(buildings[counter_buildings]) != namecolony:
            counter_buildings += 1
        try:
            while str(buildings[counter_buildings]) == namecolony:
                counter_buildings += 1
        except:
            pass

        counter_buildings += 1

        while str(laws[counter_laws]) != "Государство":
            counter_laws += 1

        while str(laws[counter_laws]) != namecolony:
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

        body_resources = [
            namecolony,
            name,
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
        ]

        sh.worksheet("Ресурсы").insert_row(body_resources, counter_resources, value_input_option = 'USER_ENTERED')

        sh.worksheet("Города").batch_update([
            {
                "range" : f"{town_unoccupied_population}{counter_towns_temp}:{town_unoccupied_population}{counter_towns_temp}",
                "values" : [[
                    f"{population_town-300}"
                ]]
            }
        ], raw = False)

        body_towns = [
            namecolony,
            name,
            f"=ЕСЛИ('Постройки'!{building_sawmill}{counter_buildings}>0,\"Лесопилка x\"&'Постройки'!{building_sawmill}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_quarry}{counter_buildings}>0,\"Каменоломня x\"&'Постройки'!{building_quarry}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_farm}{counter_buildings}>0,\"Ферма x\"&'Постройки'!{building_farm}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_scientific_center}{counter_buildings}>0,\"Научный центр x\"&'Постройки'!{building_scientific_center}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_paper_workshop}{counter_resources}>0,\"Бумажная мастерская x\"&'Постройки'!{building_paper_workshop}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_foundry_workshop}{counter_buildings}>0,\"Литейная мастерская x\"&'Постройки'!{building_foundry_workshop}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_textile_workshop}{counter_buildings}>0,\"Текстильная мастерская x\"&'Постройки'!{building_textile_workshop}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_rope_yard}{counter_buildings}>0,\"Канатный ярд x\"&'Постройки'!{building_rope_yard}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_plantation}{counter_buildings}>0,\"Плантация x\"&'Постройки'!{building_plantation}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_home}{counter_buildings}>0,\"Жилой дом x\"&'Постройки'!{building_home}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_church}{counter_buildings}>0,\"Церковь x\"&'Постройки'!{building_church}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_palace}{counter_buildings}>0,\"Дворец x\"&'Постройки'!{building_palace}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_barracks}{counter_buildings}>0,\"Казармы x\"&'Постройки'!{building_barracks}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_fortress}{counter_buildings}>0,\"Крепость x\"&'Постройки'!{building_fortress}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_capital_fortress}{counter_buildings}>0,\"Столичная крепость x\"&'Постройки'!{building_capital_fortress}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_port}{counter_buildings}>0,\"Порт x\"&'Постройки'!{building_port}{counter_buildings},)&\" \"&ЕСЛИ('Постройки'!{building_shipyard}{counter_buildings}>0,\"Верфь x\"&'Постройки'!{building_shipyard}{counter_buildings},)",
            f"Дерево x{wood}, Камень x{stone}, Провизия x{prodo}",
            f"=(((({town_estates_citizens}{counter_towns}/100*'Внутренняя политика'!{domestic_policy_taxes_citizens}{counter_internal_policy})))+((({town_estates_clergy}{counter_towns}/100*'Внутренняя политика'!{domestic_policy_taxes_clergy}{counter_internal_policy})))+((({town_estates_nobility}{counter_towns}/100*'Внутренняя политика'!{domestic_policy_taxes_nobility}{counter_internal_policy}))))*ЕСЛИ('Законы'!{laws_equality}{counter_laws}=\"Принято\",1.1,1)*ЕСЛИ('Законы'!{laws_significant_privileges}{counter_laws}=\"Принято\",0.8,1)*ЕСЛИ('Законы'!{laws_religion_doesnt_matter}{counter_laws}=\"Принято\",0.95,1)*ЕСЛИ('Законы'!{laws_fanaticism}{counter_laws}=\"Принято\",1.05,1)*ЕСЛИ('Законы'!{laws_natives_oppression}{counter_laws}=\"Принято\",1.1,1)*ЕСЛИ('Законы'!{laws_conditional_slavery}{counter_laws}=\"Принято\",1.1,1)*ЕСЛИ('Внутренняя политика'!{domestic_policy_loyality_clergy}{counter_internal_policy}>=60,1.1,1)",
            f"=ЕСЛИ('Постройки'!{building_sawmill}{counter_buildings}>0,\"Дерево x\"&'Ресурсы'!{resources_income_wood}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_quarry}{counter_buildings}>0,\"Камень x\"&'Ресурсы'!{resources_income_stone}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_farm}{counter_buildings}>0,\"Провизия x\"&'Ресурсы'!{resources_income_prodo}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_scientific_center}{counter_buildings}>0,\"Механизмы x\"&'Ресурсы'!{resources_income_mechanisms}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_paper_workshop}{counter_buildings}>0,\"Бумага x\"&'Ресурсы'!{resources_income_paper}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_foundry_workshop}{counter_buildings}>0,\"Металл x\"&'Ресурсы'!{resources_income_metall}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_textile_workshop}{counter_buildings}>0,\"Ткань x\"&'Ресурсы'!{resources_income_cloth}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_rope_yard}{counter_buildings}>0,\"Снасти x\"&'Ресурсы'!{resources_income_gear}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_plantation}{counter_buildings}>0,\"Бакалея x\"&'Ресурсы'!{resources_income_grocery}{counter_resources},\"\")&\" \"&ЕСЛИ('Постройки'!{building_gold_deposit}{counter_buildings}>0,\"Золото x\"&'Ресурсы'!{resources_income_gold}{counter_resources},\"\")",
            f"=ЕСЛИ('Постройки'!{building_fortress}{counter_buildings}>0,'Постройки'!{building_fortress}{counter_buildings}*50,0)",
            f"=ЕСЛИ('Ресурсы'!{resources_expenses_wood}{counter_resources}>0,\"Дерево x\"&'Ресурсы'!{resources_expenses_wood}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_stone}{counter_resources}>0,\"Камень x\"&'Ресурсы'!{resources_expenses_stone}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_prodo}{counter_resources}>0,\"Провизия x\"&'Ресурсы'!{resources_expenses_prodo}{counter_resources},\"\")&\" \"&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_mechanisms}{counter_resources}>0,\"Механизмы x\"&'Ресурсы'!{resources_expenses_mechanisms}{counter_resources},\"\")&\" \"&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_paper}{counter_resources}>0,\"Бумага x\"&'Ресурсы'!{resources_expenses_paper}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_metall}{counter_resources}>0,\"Металл x\"&'Ресурсы'!{resources_expenses_metall}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_cloth}{counter_resources}>0,\"Ткань x\"&'Ресурсы'!{resources_expenses_cloth}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_gear}{counter_resources}>0,\"Снасти x\"&'Ресурсы'!{resources_expenses_gear}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_grocery}{counter_resources}>0,\"Бакалея x\"&'Ресурсы'!{resources_expenses_grocery}{counter_resources},\"\")&\" \"&ЕСЛИ('Ресурсы'!{resources_expenses_gold}{counter_resources}>0,\"Золото x\"&'Ресурсы'!{resources_expenses_gold}{counter_resources},\"\")&\" \"",
            f"=300",
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
        ]

        sh.worksheet("Города").insert_row(body_towns, counter_towns, value_input_option = 'USER_ENTERED')

        body_buildings = [
            namecolony,
            name,
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
        ]

        sh.worksheet("Постройки").insert_row(body_buildings, counter_buildings, value_input_option = 'USER_ENTERED')

        worksheettown = sh.worksheet('Города')
        worksheetbuilding = sh.worksheet('Постройки')
        worksheetresources = sh.worksheet('Ресурсы')

        await asyncio.sleep(5)

        set_row_height(worksheettown, f"{counter_towns}", 50)
        set_row_height(worksheettown, f"{counter_towns+1}", 11)

        set_row_height(worksheetbuilding, f"{counter_buildings}", 50)
        set_row_height(worksheetbuilding, f"{counter_buildings+1}", 11)

        set_row_height(worksheetresources, f"{counter_resources}", 50)
        set_row_height(worksheetresources, f"{counter_resources+1}", 11)

        connection.commit()
        await ctx.send(f"**{member.mention}**, ваш город \"{name}\" внесен в таблицу!")




async def setup(bot):
    await bot.add_cog(town(bot))