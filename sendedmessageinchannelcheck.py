import discord

from discord.ext import commands

from connectmysql import connection, cursor
from config import texworkchannel, testchannel, newchannel, adminrole

class sendedmessageinchannelcheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        texworkchannelget = self.bot.get_channel(texworkchannel)
        newchannelget = self.bot.get_channel(newchannel)
        testchannelget = self.bot.get_channel(testchannel)
        if not message.author.bot:
            if (message.channel == testchannelget):
                #await texworkchannelget.send(f"Администратор <@{message.author.id}> отправил сообщение:")
                #await texworkchannelget.send(message.content)
                await testchannelget.send(f"Администратор <@{message.author.id}> отправил сообщение в канал новостей: {message.content}")
                await newchannelget.send(message.content)
                


async def setup(bot):
    await bot.add_cog(sendedmessageinchannelcheck(bot))