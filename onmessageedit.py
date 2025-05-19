import discord

from discord.ext import commands
from config import logschannel

class onmessageedit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if not message_before.author.bot:
            embed = discord.Embed(title=f"""{message_before.author.name} отредактировал сообщение в канале {message_before.channel.name}!""", description="", color=0xf4e75d)
            if (message_before.content != None) and (message_after.content != None):
                if message_before.content != message_after.content:
                    embed.add_field(name="Сообщение до редактирования:", value=message_before.content, inline=False)
                    for attach in message_before.attachments:
                        embed.set_image(url=attach.url)
                    embed.add_field(name="Сообщение после редактирования:", value=message_after.content, inline=False)
                    for attach in message_after.attachments:
                        embed.set_image(url=attach.url)
                    channel = self.bot.get_channel(logschannel)
                    await channel.send(embed=embed)
                    

async def setup(bot):
    await bot.add_cog(onmessageedit(bot))