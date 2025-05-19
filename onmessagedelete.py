import discord

from discord.ext import commands
from config import logschannel

class onmessagedelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    #@commands.Cog.listener()
    #async def on_message_delete(self, message):
    #    if not message.author.bot:
    #        embed = discord.Embed(title=f"""{message.author.name} удалил сообщение из канала {message.channel.name}!""", description="", color=0xFF0000)
    #        if message.content != None:
    #            embed.add_field(name="Это сообщение было удалено:", value=message.content, inline=False)
    #            for attach in message.attachments:
    #                embed.set_image(url=attach.url)
    #            channel = self.bot.get_channel(logschannel)
    #            await channel.send(embed=embed)

    
    @commands.Cog.listener() 
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = discord.Embed(
                title=f"{message.author.name} удалил сообщение из канала {message.channel.name}!",
                description="",
                color=0xFF0000
            )
            
            if message.content:
                embed.add_field(name="Это сообщение было удалено:", value=message.content, inline=False)
            
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)
                
                if len(message.attachments) > 1:
                    for i, attachment in enumerate(message.attachments[1:], start=2): 
                        embed.add_field(name=f"Вложение {i}", value=attachment.url, inline=False)
            
            channel = self.bot.get_channel(logschannel)
            
            if channel:
                await channel.send(embed=embed)

            else:
                print(f"Ошибка: Канал с ID {logschannel} не найден!")


async def setup(bot):
    await bot.add_cog(onmessagedelete(bot))