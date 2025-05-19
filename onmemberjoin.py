import discord

from discord.ext import commands
from connectmysql import connection, cursor
from config import registrationchannel, guidechannel, playerrole

class onmemberjoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        roles_player = discord.utils.get(member.guild.roles, id=playerrole)#player
        #roles0 = discord.utils.get(member.guild.roles, id=)#Сервер
        #roles1 = discord.utils.get(member.guild.roles, id=1088507936545984522)#Игрок
        #roles2 = discord.utils.get(member.guild.roles, id=1088507936545984523)#Технические работы
        #roles3 = discord.utils.get(member.guild.roles, id=)#Держава
        await member.add_roles(roles_player)
        #await member.add_roles(roles0)
        #await member.add_roles(roles1)
        #await member.add_roles(roles2)
        #await member.add_roles(roles3)

        #rchannel = self.bot.get_channel(registrationchannel)
        #gchannel = self.bot.get_channel(guidechannel)

        #rmessage = await rchannel.send(f"<@{member.id}>")
        #await rmessage.delete()

        #gmessage = await gchannel.send(f"<@{member.id}>")
        #await gmessage.delete()

        connection.connect()

        cursor.execute(f"SELECT iduser FROM `{member.guild.id}` WHERE iduser = {member.id}")
        iduser = cursor.fetchone()

        if iduser == None:
            cursor.execute(f"INSERT INTO `{member.guild.id}`(name, iduser) VALUES ('{member}',{member.id})")
        else:
            pass

        connection.commit()

async def setup(bot):
    await bot.add_cog(onmemberjoin(bot))