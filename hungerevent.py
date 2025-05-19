import asyncio
import discord
import datetime
import random
import time

from discord.ext import commands
from connectmysql import connection, cursor
from config import sh, logschannel, eventchannel, income_expenses_state, smile, town_slaves, town_state, town_towns, town_unoccupied_population, town_occupied_population, income_expenses_prestige, domestic_policy_state, domestic_policy_loyality_citizens, domestic_policy_loyality_clergy, domestic_policy_loyality_nobility, income_expenses_income_taxes

async def hungerevent(bot):
    while True:
        await asyncio.sleep(1)

        for guild in bot.guilds:

            now = datetime.datetime.now()

            if (now.hour == 18) and (now.minute == 55) and (now.second > 0) and (now.second < 5):
                await asyncio.sleep(30)

                connection.connect()

                states = sh.worksheet("Доходы/Расходы").get(f"{income_expenses_state}:{income_expenses_state}")

                for i in range(3, len(states)):
                    state = str(sh.worksheet("Доходы/Расходы").get(f"{income_expenses_state}{i+1}"))[3:-3]

                    cursor.execute(f"SELECT iduser FROM `{guild.id}` WHERE colony = '{state}'")
                    iduser = int(cursor.fetchone()[0])

                    cursor.execute(f"SELECT res3 FROM `{guild.id}` WHERE iduser = {iduser}")
                    prodo = float(cursor.fetchone()[0])

                    cursor.execute(f"SELECT cash FROM `{guild.id}` WHERE iduser = {iduser}")
                    money = float(cursor.fetchone()[0])

                    quarterly_income = 0

                    if prodo<0:
                        channel = bot.get_channel(eventchannel)

                        dt = int(time.time())
                        timer = dt + 21600

                        await channel.send(f"""**<@{iduser}>** <t:{timer}:R>""")

                        towngos = sh.worksheet("Города").get(f"{town_state}:{town_state}")

                        count = 0

                        for j in range(3, len(towngos)):
                            if str(towngos[j]) != '[]':
                                if str(towngos[j][0]) == state:
                                    count += 1

                        randomtown = random.randint(1, count)

                        count = 0

                        towns = sh.worksheet("Города").get(f"{town_towns}:{town_towns}")

                        town = ""
                        counttown = 0
                        countloyality = 0
                        countprestigeandtaxes = 0
                        loyalcitiz = 0
                        loyalnobil = 0
                        loyalclergy = 0
                        prestige = 0

                        for j in range(3, len(towngos)):
                            if str(towngos[j]) != '[]':
                                if str(towngos[j][0]) == state:
                                    count += 1
                                    if count == randomtown:
                                        town = str(towns[j][0])
                                        counttown = j + 1



                        #престиж

                        income = sh.worksheet("Доходы/Расходы").get(f"{income_expenses_state}:{income_expenses_state}")

                        for j in range(3, len(income)):
                            if str(income[j][0]) == state:
                                prestige = str(sh.worksheet("Доходы/Расходы").get(f"{income_expenses_prestige}{j+1}"))[3:-3]
                                prestige = float(prestige)
                                countprestigeandtaxes = j+1

                        #престиж


                        #-5 престижа

                        prestige5 = prestige - 5

                        #-5 престижа


                        #-10 престижа

                        prestige10 = prestige - 10

                        #-10 престижа


                        #-20% квартального дохода

                        quarterly_income = str(sh.worksheet("Доходы/Расходы").get(f"{income_expenses_income_taxes}{countprestigeandtaxes}"))[3:-3]

                        quarterly_income = float(quarterly_income)
                        quarterly_income = int(round(quarterly_income*0.2))

                        #-20% квартального дохода


                        #-20% населения рандомного города

                        population20unocc = str(sh.worksheet("Города").get(f"{town_unoccupied_population}{counttown}"))[3:-3]
                        #population20occ = str(sh.worksheet("Города").get(f"{town_occupied_population}{counttown}"))[3:-3]
                        #population20slav = str(sh.worksheet("Города").get(f"{town_slaves}{counttown}"))[3:-3]

                        population20unocc = int(population20unocc)
                        population20unoccstandard = int(population20unocc)
                        population20unocc = int(round(population20unocc*0.2))

                        #population20occ = float(population20occ)
                        #population20occ = population20occ - population20occ*0.2

                        #population20slav = float(population20slav)
                        #population20slav = population20slav - population20slav*0.2

                        #-20% населения рандомного города


                        #-15% населения рандомного города

                        population15unocc = str(sh.worksheet("Города").get(f"{town_unoccupied_population}{counttown}"))[3:-3]
                        #population15occ = str(sh.worksheet("Города").get(f"{town_occupied_population}{counttown}"))[3:-3]
                        #population15slav = str(sh.worksheet("Города").get(f"{town_slaves}{counttown}"))[3:-3]

                        population15unocc = int(population15unocc)
                        population15unoccstandard = int(population15unocc)
                        population15unocc = int(round(population15unocc*0.15))

                        #population15occ = float(population15occ)
                        #population15occ = population15occ - population15occ*0.15

                        #population15slav = float(population15slav)
                        #population15slav = population15slav - population15slav*0.15

                        #-15% населения рандомного города


                        #-10 всех сословий
                        dompolicy = sh.worksheet("Внутренняя политика").get(f"{domestic_policy_state}:{domestic_policy_state}")

                        for j in range(3, len(dompolicy)):
                            if str(dompolicy[j][0]) == state:

                                loyalcitiz = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_citizens}{j+1}"))[3:-3])
                                loyalclergy = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_clergy}{j+1}"))[3:-3])
                                loyalnobil = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_nobility}{j+1}"))[3:-3])

                                countloyality = j + 1

                        #-10 всех сословий



                        if money>quarterly_income:
                            message = await channel.send(f"""  
    __**ГОЛОД**__
    
    Милорд! Граждане города **{town}** устроили голодный бунт! Разъярённая толпа громит пустые прилавки. По словам недовольных, в городе кончился абсолютно весь хлеб.
    
    __**I**__ Компенсировать их убытки за счёт казны
    > *-{quarterly_income}{smile}*
    > *Население города {town} уменьшится на {population15unocc}*
    
    __**II**__ Если нет хлеба, пусть едят пирожные
    > *-5 Престижа*
    > *Население города {town} уменьшится на {population20unocc}*
                        """)
                        else:
                            message = await channel.send(f"""
    __**ГОЛОД**__
    
    Милорд! Граждане города **{town}** устроили голодный бунт! Разъярённая толпа громит пустые прилавки. По словам недовольных, в городе кончился абсолютно весь хлеб.
    
    __**I**__ Компенсировать их убытки за счёт казны
    > *-{quarterly_income}{smile}* ***Не хватает денег и приведёт к банкротству!*** *(-10 лояльности всех сословий, -10 престижа)*
    > *Население города {town} уменьшится на {population15unocc}*
    
    __**II**__ Если нет хлеба, пусть едят пирожные
    > *-5 Престижа*
    > *Население города {town} уменьшится на {population20unocc}*               
                            """)


                        await message.add_reaction('1️⃣')
                        await message.add_reaction('2️⃣')

                        def check(reaction, user):
                            return (user.id == iduser) and ((str(reaction.emoji) == '1️⃣') or (str(reaction.emoji) == '2️⃣'))

                        try:
                            reaction, user = await bot.wait_for('reaction_add', timeout=21600.0, check=check)

                            if money>quarterly_income:
                                if str(reaction.emoji) == '1️⃣':

                                    #-20% квартального дохода

                                    cursor.execute(f"UPDATE `{guild.id}` SET cash = cash - {quarterly_income} WHERE iduser = {iduser}")

                                    #-20% квартального дохода


                                    #-15% населения рандомного города
                                    sh.worksheet("Города").batch_update([
                                        {
                                            "range" : f"{town_unoccupied_population}{counttown}:{town_unoccupied_population}{counttown}",
                                            "values" : [[f"={population15unoccstandard-population15unocc}"]]
                                        }
                                    ], raw = False)
                                    #sh.worksheet("Города").batch_update([
                                    #    {
                                    #        "range" : f"{town_occupied_population}{counttown}:{town_occupied_population}{counttown}",
                                    #        "values" : [[f"={population15occ}"]]
                                    #    }
                                    #], raw = False)
                                    #sh.worksheet("Города").batch_update([
                                    #    {
                                    #        "range" : f"{town_slaves}{counttown}:{town_slaves}{counttown}",
                                    #        "values" : [[f"={population15slav}"]]
                                    #    }
                                    #], raw = False)
                                    #-15% населения рандомного города

                                    connection.commit()
                                    await channel.send(f"Вы выбрали 1 вариант.")


                                if str(reaction.emoji) == '2️⃣':

                                    #-20% населения рандомного города
                                    sh.worksheet("Города").batch_update([
                                        {
                                            "range" : f"{town_unoccupied_population}{counttown}:{town_unoccupied_population}{counttown}",
                                            "values" : [[f"={population20unoccstandard-population20unocc}"]]
                                        }
                                    ], raw = False)
                                    #sh.worksheet("Города").batch_update([
                                    #    {
                                    #        "range" : f"{town_occupied_population}{counttown}:{town_occupied_population}{counttown}",
                                    #        "values" : [[f"={population20occ}"]]
                                    #    }
                                    #], raw = False)
                                    #sh.worksheet("Города").batch_update([
                                    #    {
                                    #        "range" : f"{town_slaves}{counttown}:{town_slaves}{counttown}",
                                    #        "values" : [[f"={population20slav}"]]
                                    #    }
                                    #], raw = False)
                                    #-20% населения рандомного города


                                    #-5 престижа
                                    sh.worksheet("Доходы/Расходы").batch_update([
                                        {
                                            "range" : f"{income_expenses_prestige}{countprestigeandtaxes}:{income_expenses_prestige}{countprestigeandtaxes}",
                                            "values" : [[f"={prestige5}"]]
                                        }
                                    ], raw = False)
                                    #-5 престижа

                                    connection.commit()
                                    await channel.send(f"Вы выбрали 2 вариант.")


                            else:
                                if str(reaction.emoji) == '1️⃣':

                                    #-20% квартального дохода

                                    cursor.execute(f"UPDATE `{guild.id}` SET cash = cash - {quarterly_income} WHERE iduser = {iduser}")

                                    #-20% квартального дохода


                                    #-15% населения рандомного города
                                    sh.worksheet("Города").batch_update([
                                        {
                                            "range" : f"{town_unoccupied_population}{counttown}:{town_unoccupied_population}{counttown}",
                                            "values" : [[f"={population15unoccstandard-population15unocc}"]]
                                        }
                                    ], raw = False)
                                    #sh.worksheet("Города").batch_update([
                                    #    {
                                    #        "range" : f"{town_occupied_population}{counttown}:{town_occupied_population}{counttown}",
                                    #        "values" : [[f"={population15occ}"]]
                                    #    }
                                    #], raw = False)
                                    #sh.worksheet("Города").batch_update([
                                    #    {
                                    #        "range" : f"{town_slaves}{counttown}:{town_slaves}{counttown}",
                                    #        "values" : [[f"={population15slav}"]]
                                    #    }
                                    #], raw = False)
                                    #-15% населения рандомного города


                                    #-10% престижа
                                    sh.worksheet("Доходы/Расходы").batch_update([
                                        {
                                            "range" : f"{income_expenses_prestige}{countprestigeandtaxes}:{income_expenses_prestige}{countprestigeandtaxes}",
                                            "values" : [[f"={prestige10}"]]
                                        }
                                    ], raw = False)
                                    #-10% престижа


                                    #-10 всех сословий
                                    sh.worksheet("Внутренняя политика").batch_update([
                                        {
                                            "range" : f"{domestic_policy_loyality_citizens}{countloyality}:{domestic_policy_loyality_nobility}{countloyality}",
                                            "values" : [[
                                                f"={loyalcitiz-10}",
                                                f"={loyalclergy-10}",
                                                f"={loyalnobil-10}"
                                            ]]
                                        }
                                    ], raw = False)
                                    #-10 всех сословий

                                    connection.commit()
                                    await channel.send(f"Вы выбрали 1 вариант.")

                                if str(reaction.emoji) == '2️⃣':

                                    #-20% населения рандомного города
                                    sh.worksheet("Города").batch_update([
                                        {
                                            "range" : f"{town_unoccupied_population}{counttown}:{town_unoccupied_population}{counttown}",
                                            "values" : [[f"={population20unoccstandard-population20unocc}"]]
                                        }
                                    ], raw = False)
                                    #sh.worksheet("Города").batch_update([
                                    #    {
                                    #        "range" : f"{town_occupied_population}{counttown}:{town_occupied_population}{counttown}",
                                    #        "values" : [[f"={population20occ}"]]
                                    #    }
                                    #], raw = False)
                                    #sh.worksheet("Города").batch_update([
                                    #    {
                                    #        "range" : f"{town_slaves}{counttown}:{town_slaves}{counttown}",
                                    #        "values" : [[f"={population20slav}"]]
                                    #    }
                                    #], raw = False)
                                    #-20% населения рандомного города


                                    #-5 престижа
                                    sh.worksheet("Доходы/Расходы").batch_update([
                                        {
                                            "range" : f"{income_expenses_prestige}{countprestigeandtaxes}:{income_expenses_prestige}{countprestigeandtaxes}",
                                            "values" : [[f"={prestige5}"]]
                                        }
                                    ], raw = False)
                                    #-5 престижа

                                    connection.commit()
                                    await channel.send(f"Вы выбрали 2 вариант.")

                            await message.delete()


                        except:
                            if money>quarterly_income:
                                #-20% квартального дохода

                                cursor.execute(f"UPDATE `{guild.id}` SET cash = cash - {quarterly_income} WHERE iduser = {iduser}")

                                #-20% квартального дохода


                                #-15% населения рандомного города
                                sh.worksheet("Города").batch_update([
                                    {
                                        "range" : f"{town_unoccupied_population}{counttown}:{town_unoccupied_population}{counttown}",
                                        "values" : [[f"={population15unoccstandard-population15unocc}"]]
                                    }
                                ], raw = False)
                                #sh.worksheet("Города").batch_update([
                                #    {
                                #        "range" : f"{town_occupied_population}{counttown}:{town_occupied_population}{counttown}",
                                #        "values" : [[f"={population15occ}"]]
                                #    }
                                #], raw = False)
                                #sh.worksheet("Города").batch_update([
                                #    {
                                #        "range" : f"{town_slaves}{counttown}:{town_slaves}{counttown}",
                                #        "values" : [[f"={population15slav}"]]
                                #    }
                                #], raw = False)
                                #-15% населения рандомного города

                                connection.commit()

                            else:
                                #-20% квартального дохода

                                cursor.execute(f"UPDATE `{guild.id}` SET cash = cash - {quarterly_income} WHERE iduser = {iduser}")

                                #-20% квартального дохода


                                #-15% населения рандомного города
                                sh.worksheet("Города").batch_update([
                                    {
                                        "range" : f"{town_unoccupied_population}{counttown}:{town_unoccupied_population}{counttown}",
                                        "values" : [[f"={population15unoccstandard-population15unocc}"]]
                                    }
                                ], raw = False)
                                #sh.worksheet("Города").batch_update([
                                #    {
                                #        "range" : f"{town_occupied_population}{counttown}:{town_occupied_population}{counttown}",
                                #        "values" : [[f"={population15occ}"]]
                                #    }
                                #], raw = False)
                                #sh.worksheet("Города").batch_update([
                                #    {
                                #        "range" : f"{town_slaves}{counttown}:{town_slaves}{counttown}",
                                #        "values" : [[f"={population15slav}"]]
                                #    }
                                #], raw = False)
                                #-15% населения рандомного города


                                #-10% престижа
                                sh.worksheet("Доходы/Расходы").batch_update([
                                    {
                                        "range" : f"{income_expenses_prestige}{countprestigeandtaxes}:{income_expenses_prestige}{countprestigeandtaxes}",
                                        "values" : [[f"={prestige10}"]]
                                    }
                                ], raw = False)
                                #-10% престижа


                                #-10 всех сословий
                                sh.worksheet("Внутренняя политика").batch_update([
                                    {
                                        "range" : f"{domestic_policy_loyality_citizens}{countloyality}:{domestic_policy_loyality_nobility}{countloyality}",
                                        "values" : [[
                                            f"={loyalcitiz-10}",
                                            f"={loyalclergy-10}",
                                            f"={loyalnobil-10}"
                                        ]]
                                    }
                                ], raw = False)
                                #-10 всех сословий

                                connection.commit()

                            await channel.send(f"**<@{iduser}>**, время ожидания превышено, первый вариант был выбран автоматически!")

                            await message.delete()