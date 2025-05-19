import asyncio
import discord
import datetime

from discord.ext import commands
from connectmysql import connection, cursor
from config import sh, logschannel, income_expenses_prestige, income_expenses_sheet, town_sheet, town_unoccupied_population

async def updategoogleworksheet(bot):
    while True:
        await asyncio.sleep(1)
        connection.connect()

        for guild in bot.guilds:
            now = datetime.datetime.now()

            if (now.hour == 19) and (now.minute == 0) and (now.second > 0) and (now.second < 5):
                await asyncio.sleep(10)
                channel = bot.get_channel(logschannel)
                await channel.send(f"Начинаю обновлять таблицу...")
                towns = sh.worksheet("Города").get(f"{town_sheet}")
                state = sh.worksheet("Доходы/Расходы").get(f"{income_expenses_sheet}")

                cursor.execute(f"UPDATE `{guild.id}` SET didtheprestigechangeduringtheturn = 0")

                cursor.execute(f"TRUNCATE TABLE {guild.id}_message")

                for k1 in range(3, len(state)):
                    prestige = str(sh.worksheet("Доходы/Расходы").get(f"{income_expenses_prestige}{k1+1}"))[3:-3]

                    try:
                        prestige = float(prestige)

                        if prestige > 1.0:
                            prestige -= 0.5

                        elif prestige < -1.0:
                            prestige += 0.5

                        sh.worksheet("Доходы/Расходы").batch_update([
                            {
                                "range" : f"{income_expenses_prestige}{k1+1}:{income_expenses_prestige}{k1+1}",
                                "values" : [[f"={prestige}"]]
                            }
                        ], raw = False)

                        await asyncio.sleep(5)

                    except:
                        pass


                for k1 in range(3, len(towns)):
                    if str(towns[k1]) != "[]":
                        godprirost = towns[k1][12]#считать 0
                        nezanyannaselenie = towns[k1][9]#считать 0

                        godprirost = str(godprirost)

                        try:
                            godprirost = float(godprirost)

                            nezanyannaselenie = str(nezanyannaselenie)
                            nezanyannaselenie = float(nezanyannaselenie)

                            itog = godprirost+nezanyannaselenie

                            sh.worksheet("Города").batch_update([
                                {
                                    "range" : f"{town_unoccupied_population}{k1+1}",
                                    "values" : [[f"={itog}"]]
                                }
                            ], raw = False)

                            await asyncio.sleep(5)

                        except:
                            pass

                '''
                procent = 0.1

                mass = [1,2,3,4,5,6,7,8,9,10,11,12,51,52,53,54,55,56,57]
                
                for i in mass:
                    cursor.execute(f"SELECT res{i} FROM {guild.id}_economy WHERE id = 3")
                    reco = float(cursor.fetchone()[0])

                    cursor.execute(f"SELECT res{i} FROM {guild.id}_economy WHERE id = 1")
                    reco1 = float(cursor.fetchone()[0])

                    cursor.execute(f"SELECT res{i} FROM {guild.id}_economy WHERE id = 2")
                    reco2 = float(cursor.fetchone()[0])

                    if reco > 100:
                        if ((reco1 > 10) and (reco2 > 10)):
                            cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} - res{i} * {procent} WHERE id = 1")
                            cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} - res{i} * {procent} WHERE id = 2")
                        cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} - 3 WHERE id = 3")

                    if reco < 100:
                        cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} + res{i} * {procent} WHERE id = 1")
                        cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} + res{i} * {procent} WHERE id = 2")
                        cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} + 3 WHERE id = 3")

                    if reco == 100:
                        if ((reco1 > 10) and (reco2 > 10)):
                            cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} - res{i} * {procent} WHERE id = 1")
                            cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} - res{i} * {procent} WHERE id = 2")
                '''

                connection.commit()
                await channel.send(f"Таблица успешно обновлена!")