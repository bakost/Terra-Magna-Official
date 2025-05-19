import discord

from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor
from config import texrole

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['economy-edit'], pass_context=True)
    async def __economyedit(self, ctx, *, args=None):
        role = discord.utils.get(ctx.guild.roles, id=texrole)
        if role in ctx.author.roles:
            member = ctx.message.author

            if args is None:
                await ctx.send(f"**{member.mention}**, введите название государства, которому хотите сбросить экономику!")
                return

            connection.connect()

            namer = title(args.split()[0])

            cursor.execute(f"SELECT name FROM {ctx.author.guild.id}_economy WHERE name = '{namer}'")
            town = cursor.fetchone()

            if town is None:
                await ctx.send(f"**{member.mention}**, государство не найдено!")
                return

            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res1 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res2 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res3 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res4 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res5 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res6 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res7 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res8 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res9 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res10 = 0.2 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res11 = 50 WHERE name = '{namer}'")


            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res1 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res2 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res3 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res4 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res5 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res6 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res7 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res8 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res9 = 50 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res10 = 0.2 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res11 = 50 WHERE name = '{namer}'")


            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res1 = 20 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res2 = 20 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res3 = 20 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res4 = 20 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res5 = 20 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res6 = 20 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res7 = 20 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res8 = 20 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res9 = 20 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res10 = 3000 WHERE name = '{namer}'")
            cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res11 = 20 WHERE name = '{namer}'")


            connection.commit()
            await ctx.send(f"Экономика государства {namer} сброшена!")

        else:
            await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор.")


async def setup(bot):
    await bot.add_cog(economy(bot))