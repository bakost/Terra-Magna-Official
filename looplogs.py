import discord
import datetime

from discord.ext import commands
from connectmysql import connection, cursor
from config import texrole
from colorama import Fore

class looplogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            connection.connect()

            now = datetime.datetime.now()
            try:
                if message.content != "":
                    cursor.execute(f"INSERT INTO {message.author.guild.id}_logs(author, iduser, day, time, message, channelid, type) VALUES ('{message.author}',{message.author.id},'{now.day}.{now.month}.{now.year}','{now.hour+3}:{now.minute}:{now.second}','{message.content}',{message.channel.id}, 'message')")
            except:
                print(f"{Fore.RED}[{now.day}.{now.month}.{now.year} {now.hour+5}:{now.minute}:{now.second}] Attention! An error occurred while saving logs in the database! ID:{message.id}")
                return

            for attach in message.attachments:
                cursor.execute(f"INSERT INTO {message.author.guild.id}_logs(author, iduser, day, time, message, channelid, type) VALUES ('{message.author}',{message.author.id},'{now.day}.{now.month}.{now.year}','{now.hour+3}:{now.minute}:{now.second}','{attach.url}',{message.channel.id}, 'attachments')")

            connection.commit()


async def setup(bot):
    await bot.add_cog(looplogs(bot))