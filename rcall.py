import discord
import gspread

from discord.ext import commands
from connectmysql import connection, cursor
from numpy.core.defchararray import title
from config import sh, domestic_policy_state, domestic_policy_recruitment_call

class rcall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['recruit'], pass_context=True)
    async def __recruit(self, ctx, *,  args=None):
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}** отсутствуют аргументы! Пример команды: **!recruit [%]** _(Не более 5%)_ ")
            return

        connection.connect()

        cursor.execute(f"SELECT colony FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        namecolony = str(cursor.fetchone()[0])

        if namecolony == "None":
            await ctx.send(f"**{member.mention}** у вас нет государства!")
            return

        amount = str(args.split()[0])

        amount = int(amount)

        if amount > 10:
            await ctx.send(f"**{member.mention}** рекрутский призыв не должен превышать 10%!")
            return

        if amount < 1:
            await ctx.send(f"**{member.mention}** рекрутский призыв не должен быть меньше 1%!")
            return

        dompol = sh.worksheet("Внутренняя политика").get(f"{domestic_policy_state}:{domestic_policy_state}")
        dompol = str(dompol)[1:-1]
        dompol = dompol.replace("[", "")
        dompol = dompol.replace("]", "")
        dompol = dompol.replace(" \'", "")
        dompol = dompol.replace("\'", "")
        dompol = dompol.split(",")

        k1 = 1

        while str(dompol[k1]) != namecolony:
            k1 += 1
            if k1 > len(dompol):
                await ctx.send(f"**{member.mention}** вашего государства нет в таблице, свяжитесь с администрацией!")
                return

        while k1 != len(dompol):
            k1 += 1

        sh.worksheet("Внутренняя политика").batch_update([
            {
                "range" : f"{domestic_policy_recruitment_call}{k1}",
                "values" : [[f"={amount}"]]
            }
        ], raw = False)

        await ctx.send(f"**{member.mention}**, вы сменили процент рекрутского призыва в своем государстве на {amount}%")







async def setup(bot):
    await bot.add_cog(rcall(bot))