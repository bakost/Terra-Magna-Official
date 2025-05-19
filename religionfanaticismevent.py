import asyncio
import discord
import datetime
import random
import time

from discord.ext import commands
from connectmysql import connection, cursor
from config import sh, logschannel, eventchannel, smile, laws_fanaticism, laws_state, domestic_policy_state, domestic_policy_loyality_citizens, domestic_policy_loyality_clergy, domestic_policy_loyality_nobility, town_state, town_slaves, income_expenses_state, income_expenses_prestige

async def religionfanaticismevent(bot):
    while True:
        await asyncio.sleep(1)

        for guild in bot.guilds:

            now = datetime.datetime.now()

            if (now.hour == 18) and (now.minute == 55) and (now.second > 0) and (now.second < 5):
                await asyncio.sleep(30)

                laws = sh.worksheet("Законы").get(f"{laws_fanaticism}:{laws_fanaticism}")

                for i in range(4, len(laws)):
                    if str(laws[i][0]) == "Принято":

                        sh.worksheet("Законы").batch_update([
                            {
                                "range" : f"{laws_fanaticism}{i+1}:{laws_fanaticism}{i+1}",
                                "values" : [[f"Принято✓"]]
                            }
                        ], raw = False)

                        state = str(sh.worksheet("Законы").get(f"{laws_state}{i+1}"))[3:-3]

                        connection.connect()

                        cursor.execute(f"SELECT iduser FROM `{guild.id}` WHERE colony = '{state}'")
                        iduser = int(cursor.fetchone()[0])

                        cursor.execute(f"SELECT cash FROM `{guild.id}` WHERE iduser = {iduser}")
                        money = float(cursor.fetchone()[0])

                        channel = bot.get_channel(eventchannel)

                        dt = int(time.time())
                        timer = dt + 21600

                        await channel.send(f"""**<@{iduser}>** <t:{timer}:R>""")

                        message = await channel.send(f"""       
    **__ОХОТА НА ВЕДЬМ__**
    
    Милорд, недавно в одном из наших городов обнаружили культ ведьм. Наше религиозное общество сразу начало охоту на них, что повлекло за собой некоторые неприятные события.
    
    **__I__ Смерть ведьмам!**
    
    > *-100 {smile}*
    > *Население случайного города уменьшится на 7%*
    > *-2 престижа*
    
    **__II__ Остановите это немедленно!**
    
    > *-150 {smile}*
    > *Лояльность духовенства -10*
    > *Лояльность горожан -5*
                        """)

                        await message.add_reaction('1️⃣')
                        await message.add_reaction('2️⃣')

                        def check(reaction, user):
                            return (user.id == iduser) and ((str(reaction.emoji) == '1️⃣') or (str(reaction.emoji) == '2️⃣'))

                        try:
                            reaction, user = await bot.wait_for('reaction_add', timeout=21600.0, check=check)

                            if str(reaction.emoji) == '1️⃣':


                                #монеты

                                if money-100<0:
                                    dompolicy = sh.worksheet("Внутренняя политика").get(f"{domestic_policy_state}:{domestic_policy_state}")

                                    for j in range(3, len(dompolicy)):
                                        if str(dompolicy[j][0]) == state:

                                            loyalcitiz = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_citizens}{j+1}"))[3:-3])
                                            loyalclergy = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_clergy}{j+1}"))[3:-3])
                                            loyalnobil = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_nobility}{j+1}"))[3:-3])

                                            sh.worksheet("Внутренняя политика").batch_update([
                                                {
                                                    "range" : f"{domestic_policy_loyality_citizens}{j+1}:{domestic_policy_loyality_nobility}{j+1}",
                                                    "values" : [[
                                                        f"={loyalcitiz-10}",
                                                        f"={loyalclergy-10}",
                                                        f"={loyalnobil-10}"
                                                    ]]
                                                }
                                            ], raw = False)
                                else:
                                    cursor.execute(f"UPDATE `{guild.id}` SET cash = cash - 100 WHERE iduser = {iduser}")

                                #монеты


                                #население  случайного города уменьшится на 7%

                                towngos = sh.worksheet("Города").get(f"{town_state}:{town_state}")

                                count = 0

                                for j in range(3, len(towngos)):
                                    if str(towngos[j]) != '[]':
                                        if str(towngos[j][0]) == state:
                                            count += 1

                                randomtown = random.randint(1, count)

                                count = 0

                                for j in range(3, len(towngos)):
                                    if str(towngos[j]) != '[]':
                                        if str(towngos[j][0]) == state:
                                            count += 1

                                            if randomtown == count:
                                                population = str(sh.worksheet("Города").get(f"{town_slaves}{j+1}"))[3:-3]
                                                population = float(population)
                                                population = population - population*0.07

                                                sh.worksheet("Города").batch_update([
                                                    {
                                                        "range" : f"{town_slaves}{j+1}:{town_slaves}{j+1}",
                                                        "values" : [[f"={population}"]]
                                                    }
                                                ], raw = False)

                                #население  случайного города уменьшится на 7%


                                #престиж

                                income = sh.worksheet("Доходы/Расходы").get(f"{income_expenses_state}:{income_expenses_state}")

                                for j in range(3, len(income)):
                                    if str(income[j][0]) == state:
                                        prestige = str(sh.worksheet("Доходы/Расходы").get(f"{income_expenses_prestige}{j+1}"))[3:-3]
                                        prestige = float(prestige)
                                        prestige = prestige - 2

                                        sh.worksheet("Доходы/Расходы").batch_update([
                                            {
                                                "range" : f"{income_expenses_prestige}{j+1}:{income_expenses_prestige}{j+1}",
                                                "values" : [[f"={prestige}"]]
                                            }
                                        ], raw = False)

                                #престиж


                                connection.commit()
                                await channel.send(f"Вы выбрали 1 вариант.")

                            if str(reaction.emoji) == '2️⃣':

                                #монеты

                                if money-150<0:
                                    dompolicy = sh.worksheet("Внутренняя политика").get(f"{domestic_policy_state}:{domestic_policy_state}")

                                    for j in range(3, len(dompolicy)):
                                        if str(dompolicy[j][0]) == state:

                                            loyalcitiz = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_citizens}{j+1}"))[3:-3])
                                            loyalclergy = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_clergy}{j+1}"))[3:-3])
                                            loyalnobil = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_nobility}{j+1}"))[3:-3])

                                            sh.worksheet("Внутренняя политика").batch_update([
                                                {
                                                    "range" : f"{domestic_policy_loyality_citizens}{j+1}:{domestic_policy_loyality_nobility}{j+1}",
                                                    "values" : [[
                                                        f"={loyalcitiz-10}",
                                                        f"={loyalclergy-10}",
                                                        f"={loyalnobil-10}"
                                                    ]]
                                                }
                                            ], raw = False)
                                else:
                                    cursor.execute(f"UPDATE `{guild.id}` SET cash = cash - 150 WHERE iduser = {iduser}")

                                #монеты


                                #лояльность

                                dompolicy = sh.worksheet("Внутренняя политика").get(f"{domestic_policy_state}:{domestic_policy_state}")

                                for j in range(3, len(dompolicy)):
                                    if str(dompolicy[j][0]) == state:

                                        loyalcitiz = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_citizens}{j+1}"))[3:-3])
                                        loyalclergy = float(str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_loyality_clergy}{j+1}"))[3:-3])

                                        sh.worksheet("Внутренняя политика").batch_update([
                                            {
                                                "range" : f"{domestic_policy_loyality_citizens}{j+1}:{domestic_policy_loyality_clergy}{j+1}",
                                                "values" : [[
                                                    f"={loyalcitiz-5}",
                                                    f"={loyalclergy-10}"
                                                ]]
                                            }
                                        ], raw = False)

                                #лояльность


                                connection.commit()
                                await channel.send(f"Вы выбрали 2 вариант.")

                            await message.delete()

                        except asyncio.TimeoutError:
                            await channel.send(f"**<@{iduser}>**, время ожидания превышено, обратитесь к администрации!")

                            await message.delete()
