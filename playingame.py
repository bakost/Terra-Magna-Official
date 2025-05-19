import asyncio
import discord

async def playingame(bot):
    while True:
        await asyncio.sleep(1)
        game = discord.Game("Terra Magna | ВПИ")
        try:
            await bot.change_presence(status=discord.Status.online, activity=game)
        except:
            pass