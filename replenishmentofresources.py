import asyncio
import discord
import datetime

from discord.ext import commands
from connectmysql import connection, cursor
from config import logschannel

async def replenishmentofresources(bot):
    while True:
        await asyncio.sleep(1)
        connection.connect()

        for guild in bot.guilds:

            now = datetime.datetime.now()

            if (now.hour == 19) and (now.minute == 0) and (now.second > 0) and (now.second < 5):
                await asyncio.sleep(30)
                channel = bot.get_channel(logschannel)
                await channel.send(f"Пополняю ресурсы...")

                for i in range(1,12):
                    cursor.execute(f"SELECT res{i} FROM {guild.id}_economy WHERE type = 'Количество'")
                    reco = float(cursor.fetchone()[0])

                    if (reco<20):
                        cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} + 10 WHERE type = 'Количество'")

                    if (i == 10) and (reco<3000):
                        cursor.execute(f"UPDATE {guild.id}_economy SET res{i} = res{i} + 90 WHERE type = 'Количество'")


                connection.commit()
                await channel.send(f"Ресурсы успешно пополнены!")