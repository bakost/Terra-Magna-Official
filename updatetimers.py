import asyncio
import discord

from discord.ext import commands
from connectmysql import connection, cursor

async def updatetimers(bot):
    while True:
        await asyncio.sleep(1)
        connection.connect()

        for guild in bot.guilds:
            #пустой
            cursor.execute(f"SELECT globaltime FROM {guild.id}_time WHERE id = 1")
            reco1 = int(cursor.fetchone()[0])

            #таймер для создания государства 60 секунд
            cursor.execute(f"SELECT globaltime FROM {guild.id}_time WHERE id = 2")
            reco2 = int(cursor.fetchone()[0])

            #таймер для создания города 30 секунд
            cursor.execute(f"SELECT globaltime FROM {guild.id}_time WHERE id = 3")
            reco3 = int(cursor.fetchone()[0])

            if reco1 >= 1:
                cursor.execute(f"UPDATE {guild.id}_time SET globaltime = globaltime - 1 WHERE id = 1")

            if reco2 >= 1:
                cursor.execute(f"UPDATE {guild.id}_time SET globaltime = globaltime - 1 WHERE id = 2")

            if reco3 >= 1:
                cursor.execute(f"UPDATE {guild.id}_time SET globaltime = globaltime - 1 WHERE id = 3")

            connection.commit()