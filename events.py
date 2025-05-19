import discord
import asyncio

from discord.ext import commands
from connectmysql import connection, cursor
from config import eventchannel, adminrole

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['event'], pass_context=True)
    async def __event(self, ctx, *,  args=None):
        member = ctx.message.author
        if args is None:
            await ctx.send(f"**{member.mention}**, отсутствуют аргументы! Пример команды: !event [id ивента] [Упоминание игрока]")
            return

        role = discord.utils.get(ctx.guild.roles, id=adminrole)
        if role in ctx.author.roles:
            idevent = int(args.split()[0])

            iduser = args.split()[1]
            iduser = iduser.replace("<","")
            iduser = iduser.replace(">","")
            iduser = iduser.replace("@","")
            iduser = int(iduser)

            connection.connect()

            cursor.execute(f"SELECT message FROM {ctx.author.guild.id}_events WHERE id = {idevent}")
            mesevent = cursor.fetchone()[0]

            cursor.execute(f"SELECT countbuttons FROM {ctx.author.guild.id}_events WHERE id = {idevent}")
            countbuttons = int(cursor.fetchone()[0])

            channel = self.bot.get_channel(eventchannel)

            message = await channel.send(mesevent)

            listnumbers = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']


            for i in range(0,countbuttons):
                await message.add_reaction(f"{listnumbers[i]}")

            def check(reaction, user):
                return (user.id == iduser) and (
                        (str(reaction.emoji) == '1️⃣') or
                        (str(reaction.emoji) == '2️⃣') or
                        (str(reaction.emoji) == '3️⃣') or
                        (str(reaction.emoji) == '4️⃣') or
                        (str(reaction.emoji) == '5️⃣') or
                        (str(reaction.emoji) == '6️⃣') or
                        (str(reaction.emoji) == '7️⃣') or
                        (str(reaction.emoji) == '8️⃣') or
                        (str(reaction.emoji) == '9️⃣')
                )

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=600.0, check=check)

                for i in range(0,countbuttons):
                    if str(reaction.emoji) == f"{listnumbers[i]}":
                        await channel.send(f"Вы выбрали {i+1} вариант.")
                        await message.delete()

            except asyncio.TimeoutError:
                await channel.send(f"**<@{iduser}>**, время ожидания превышено, обратитесь к администрации!")
                await message.delete()

        else:
            await ctx.send(f"**{member.mention}**, вы не администратор.")



async def setup(bot):
    await bot.add_cog(events(bot))