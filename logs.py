import discord
import datetime

from discord.ext import commands
from connectmysql import connection, cursor
from config import texrole, admins
from numpy.core.defchararray import title

class logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['logs'], pass_context=True)
    async def __logs(self, ctx, *, args=None):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            member = ctx.message.author

            if args is None:
                await ctx.send(f"**{member.mention}**, введите дату, время выгрузки логов (МСК-2) и тип (attachments - фотографии, видео, вложения или message - сообщение). Пример: !logs 30.5.2000 22:0-23:0 (часы и минуты) message")
                return

            connection.connect()

            date = str(args.split()[0])

            date_d = int(date.split('.')[0])
            date_m = int(date.split('.')[1])
            date_y = int(date.split('.')[2])

            time = str(args.split()[1])

            time_1 = str(time.split('-')[0])
            time_2 = str(time.split('-')[1])

            time_h_1 = int(time_1.split(':')[0])
            time_m_1 = int(time_1.split(':')[1])
            #time_s_1 = int(time_1.split(':')[2])
            #time_ms_1 = int(time_1.split(':')[3])

            time_h_2 = int(time_2.split(':')[0])
            time_m_2 = int(time_2.split(':')[1])
            #time_s_2 = int(time_2.split(':')[2])
            #time_ms_2 = int(time_2.split(':')[3])

            typelogs = title(str(args.split()[2]))

            if typelogs == "Attachments":
                type = "attachments"
            elif typelogs == "Message":
                type = "message"
            else:
                await ctx.send(f"**{member.mention}**, не верный тип!")
                return

            if (time_h_2 - time_h_1) != 0:
                await ctx.send(f"**{member.mention}**, разница должна быть 0 часов!")
                return

            await ctx.send(f"**{member.mention}**, идет обработка запроса, пожалуйста, подождите (от 1 до 2 минут)!")

            embed = discord.Embed(
                title="Terra Magna | ВПИ (Логи)",
                description=f"Это выгрузка логов Terra Magna за {date_d}.{date_m}.{date_y} с {time_h_1}:{time_m_1} до {time_h_2}:{time_m_2}",
                color = 0x00BFFF,
            )

            for i in range(time_h_1,time_h_2+1):
                for j in range(time_m_1,time_m_2+1):
                    for x in range(0,60+1):
                        cursor.execute(f"SELECT message FROM {ctx.author.guild.id}_logs WHERE day = '{date_d}.{date_m}.{date_y}' and time = '{i}:{j}:{x}' and type = '{type}'")
                        row = cursor.fetchall()
                        if str(row) != '[]':
                            temp = row
                            cursor.execute(f"SELECT author FROM {ctx.author.guild.id}_logs WHERE day = '{date_d}.{date_m}.{date_y}' and time = '{i}:{j}:{x}' and type = '{type}'")
                            temp1 = cursor.fetchall()
                            cursor.execute(f"SELECT channelid FROM {ctx.author.guild.id}_logs WHERE day = '{date_d}.{date_m}.{date_y}' and time = '{i}:{j}:{x}' and type = '{type}'")
                            temp2 = cursor.fetchall()
                            for y in range(len(temp)):
                                embed.add_field(name=f"Время: {i}:{j}:{x} Ник: {temp1[y][0]} ID канала: {temp2[y][0]}", value=f"Сообщение: {temp[y][0]}", inline=False)

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(logs(bot))