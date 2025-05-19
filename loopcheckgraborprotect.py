import asyncio
import discord

from discord.ext import commands
from connectmysql import connection, cursor

async def loopcheckgraborprotect(bot):
    while True:
        connection.connect()

        for guild in bot.guilds:
            channel = bot.get_channel(1038070621487235163)

            cursor.execute(f"SELECT maritime FROM {guild.id}_grab")
            maritimegrab = cursor.fetchall()

            cursor.execute(f"SELECT iduser FROM {guild.id}_grab")
            idusergrab = cursor.fetchall()

            cursor.execute(f"SELECT type FROM {guild.id}_grab")
            typegrab = cursor.fetchall()

            for i in range(0, len(idusergrab)):
                for j in range(0, len(idusergrab)):
                    if i != j:
                        if maritimegrab[i] == maritimegrab[j]:
                            temps1 = str(typegrab[i])[1:-2]
                            temps1 = int(temps1)

                            temps2 = str(typegrab[j])[1:-2]
                            temps2 = int(temps2)

                            iduser1 = str(idusergrab[i])[1:-2]
                            iduser1 = int(iduser1)

                            iduser2 = str(idusergrab[j])[1:-2]
                            iduser2 = int(iduser2)

                            maritimeob = str(maritimegrab[i])[2:-3]

                            if (temps1 == 1) and (temps2 == 2):
                                connection.connect()

                                cursor.execute(f"SELECT metropoly FROM `{guild.id}` WHERE iduser = {iduser1}")
                                metropoly1 = cursor.fetchone()[0]

                                metropoly1 = str(metropoly1)

                                cursor.execute(f"SELECT metropoly FROM `{guild.id}` WHERE iduser = {iduser2}")
                                metropoly2 = cursor.fetchone()[0]

                                metropoly2 = str(metropoly2)

                                if metropoly1 == metropoly2:
                                    break


                                cursor.execute(f"SELECT colony FROM `{guild.id}` WHERE iduser = {iduser1}")
                                colony1 = cursor.fetchone()[0]

                                colony1 = str(colony1)

                                if colony1 == "None":
                                    break

                                cursor.execute(f"SELECT colony FROM `{guild.id}` WHERE iduser = {iduser2}")
                                colony2 = cursor.fetchone()[0]

                                colony2 = str(colony2)

                                if colony2 == "None":
                                    break

                                cursor.execute(f"SELECT galeons FROM {guild.id}_grab WHERE iduser = {iduser1} and maritime = '{maritimeob}' and type = 1")
                                galeons1 = cursor.fetchone()[0]

                                galeons1 = int(galeons1)

                                cursor.execute(f"SELECT karavells FROM {guild.id}_grab WHERE iduser = {iduser1} and maritime = '{maritimeob}' and type = 1")
                                karavells1 = cursor.fetchone()[0]

                                karavells1 = int(karavells1)

                                cursor.execute(f"SELECT galeons FROM {guild.id}_grab WHERE iduser = {iduser2} and maritime = '{maritimeob}' and type = 2")
                                galeons2 = cursor.fetchone()[0]

                                galeons2 = int(galeons2)

                                cursor.execute(f"SELECT karavells FROM {guild.id}_grab WHERE iduser = {iduser2} and maritime = '{maritimeob}' and type = 2")
                                karavells2 = cursor.fetchone()[0]

                                karavells2 = int(karavells2)

                                sum1 = 15*galeons1+5*karavells1
                                sum2 = 15*galeons2+5*karavells2

                                await channel.send(f"Конвой из колонии __**{colony2}**__ наткнулся на враждебных каперов из колонии __**{colony1}**__ в морском регионе **{maritimeob}**!")
                                await channel.send(f"Мощь конвоя: **{sum2}** очков")
                                await channel.send(f"Мощь каперов: **{sum1}** очков")


                                if (sum1 > sum2) or (sum1 == sum2):
                                    await channel.send(f"**Каперы** смогли разбить охранный конвой в регионе **{maritimeob}**!")
                                    await channel.send(f"Потери каперов: ")
                                    await channel.send(f"Потери конвоя: ")

                                    cursor.execute(f"SELECT fleet FROM `{guild.id}` WHERE iduser = {iduser2}")
                                    fleet = cursor.fetchall()

                                    cursor.execute(f"SELECT fleet_amount FROM `{guild.id}` WHERE iduser = {iduser2}")
                                    fleet_amount = cursor.fetchall()

                                    cursor.execute(f"SELECT fleet_amount_usable FROM `{guild.id}` WHERE iduser = {iduser2}")
                                    fleet_amount_usable = cursor.fetchall()

                                    cursor.execute(f"SELECT galeons FROM {guild.id}_grab WHERE iduser = {iduser2} and maritime = '{maritimeob}' and type = 2")
                                    galeons = cursor.fetchone()[0]

                                    cursor.execute(f"SELECT karavells FROM {guild.id}_grab WHERE iduser = {iduser2} and maritime = '{maritimeob}' and type = 2")
                                    karavells = cursor.fetchone()[0]

                                    fleet = str(fleet)[3:-4]
                                    fleet = fleet.split()

                                    fleet_amount = str(fleet_amount)[3:-4]
                                    fleet_amount = fleet_amount.split()

                                    fleet_amount_usable = str(fleet_amount_usable)[3:-4]
                                    fleet_amount_usable = fleet_amount_usable.split()

                                    for i in range(0, len(fleet)):
                                        temp = str(fleet[i])

                                        temp2 = str(fleet_amount[i])
                                        temp2 = int(temp2)

                                        if temp == "Галеон":
                                            fleet_amount[i] = temp2 + galeons
                                            fleet_amount_usable[i] = int(fleet_amount_usable[i]) - galeons

                                        if temp == "Каравелла":
                                            fleet_amount[i] = temp2 + karavells
                                            fleet_amount_usable[i] = int(fleet_amount_usable[i]) - karavells

                                    fleet_amount = [str(x) for x in fleet_amount]
                                    fleet_amount_usable = [str(x) for x in fleet_amount_usable]

                                    str_fleet_amount = ' '.join(fleet_amount)
                                    str_fleet_amount_usable = ' '.join(fleet_amount_usable)

                                    cursor.execute(f"UPDATE `{guild.id}` SET fleet_amount = '{str_fleet_amount} ' WHERE iduser = {iduser2}")
                                    cursor.execute(f"UPDATE `{guild.id}` SET fleet_amount_usable = '{str_fleet_amount_usable} ' WHERE iduser = {iduser2}")

                                    cursor.execute(f"DELETE FROM {guild.id}_grab WHERE maritime = '{maritimeob}' and type = 2")

                                    connection.commit()

                                if sum1 < sum2:
                                    await channel.send(f"**Каперы** были изгнаны из региона **{maritimeob}**!")
                                    await channel.send(f"Потери каперов: ")
                                    await channel.send(f"Потери конвоя: ")


                                    cursor.execute(f"SELECT fleet FROM `{guild.id}` WHERE iduser = {iduser1}")
                                    fleet = cursor.fetchall()

                                    cursor.execute(f"SELECT fleet_amount FROM `{guild.id}` WHERE iduser = {iduser1}")
                                    fleet_amount = cursor.fetchall()

                                    cursor.execute(f"SELECT fleet_amount_usable FROM `{guild.id}` WHERE iduser = {iduser1}")
                                    fleet_amount_usable = cursor.fetchall()

                                    cursor.execute(f"SELECT galeons FROM {guild.id}_grab WHERE maritime = '{maritimeob}' and type = 1")
                                    galeons = cursor.fetchone()[0]

                                    cursor.execute(f"SELECT karavells FROM {guild.id}_grab WHERE maritime = '{maritimeob}' and type = 1")
                                    karavells = cursor.fetchone()[0]

                                    fleet = str(fleet)[3:-4]
                                    fleet = fleet.split()

                                    fleet_amount = str(fleet_amount)[3:-4]
                                    fleet_amount = fleet_amount.split()

                                    fleet_amount_usable = str(fleet_amount_usable)[3:-4]
                                    fleet_amount_usable = fleet_amount_usable.split()

                                    for i in range(0, len(fleet)):
                                        temp = str(fleet[i])

                                        temp2 = str(fleet_amount[i])
                                        temp2 = int(temp2)

                                        if temp == "Галеон":
                                            fleet_amount[i] = temp2 + galeons
                                            fleet_amount_usable[i] = int(fleet_amount_usable[i]) - galeons

                                        if temp == "Каравелла":
                                            fleet_amount[i] = temp2 + karavells
                                            fleet_amount_usable[i] = int(fleet_amount_usable[i]) - karavells

                                    fleet_amount = [str(x) for x in fleet_amount]
                                    fleet_amount_usable = [str(x) for x in fleet_amount_usable]

                                    str_fleet_amount = ' '.join(fleet_amount)
                                    str_fleet_amount_usable = ' '.join(fleet_amount_usable)

                                    cursor.execute(f"UPDATE `{guild.id}` SET fleet_amount = '{str_fleet_amount} ' WHERE iduser = {iduser1}")
                                    cursor.execute(f"UPDATE `{guild.id}` SET fleet_amount_usable = '{str_fleet_amount_usable} ' WHERE iduser = {iduser1}")

                                    cursor.execute(f"DELETE FROM {guild.id}_grab WHERE maritime = '{maritimeob}' and type = 1")

                                    connection.commit()

        await asyncio.sleep(30)
