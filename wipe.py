import discord

from discord.ext import commands
from connectmysql import connection, cursor
from config import admins, texrole

class wipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['wipe'], pass_context=True)
    async def __wipe(self, ctx, *, args=None):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            connection.connect()

            if args is None:
                await ctx.send(f"Введите пинг игрока, которому хотите очистить деньги, ресурсы и инвентарь!")
                return

            a = args.split()[0]

            vladiok1 = a.replace("<","")
            vladiok1 = vladiok1.replace(">","")
            vladiok1 = vladiok1.replace("@","")

            vladiok1 = int(vladiok1)

            cursor.execute(f"SELECT name FROM `{ctx.author.guild.id}` WHERE iduser = {vladiok1}")
            reco = cursor.fetchone()[0]

            if reco is None:
                await ctx.send(f"**{ctx.message.author.mention}**, указанный пользователь не найден в базе данных!")
                return

            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = 0 WHERE iduser = {ctx.author.id}")

            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET colony = Null WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET capital = Null WHERE iduser = {ctx.author.id}")

            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res1 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res2 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res3 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res4 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res5 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res6 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res7 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res8 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res9 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res10 = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res11 = 0 WHERE iduser = {ctx.author.id}")


            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET kdwork = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET kdtrade = 0 WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET kdproduct = 0 WHERE iduser = {ctx.author.id}")

            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory = Null WHERE iduser = {ctx.author.id}")
            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET inventory_amount = Null WHERE iduser = {ctx.author.id}")


            connection.commit()
            await ctx.send(f"**{ctx.message.author.mention}**, очистил деньги, ресурсы и инвентарь игрока <@{vladiok1}>")
        else:
            await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор.")

async def setup(bot):
    await bot.add_cog(wipe(bot))