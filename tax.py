import discord
import gspread

from discord.ext import commands
from connectmysql import connection, cursor
from numpy.core.defchararray import title
from config import sh, income_expenses_state, income_expenses_prestige, domestic_policy_taxes_citizens, domestic_policy_taxes_clergy, domestic_policy_taxes_nobility, domestic_policy_state

class tax(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['tax'], pass_context=True)
    async def __tax(self, ctx, *,  args=None):
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}** отсутствуют аргументы! Пример команды: **!tax [Горожане/Духовенство/Дворянство] [%]** _(Не более 50%)_")
            return

        connection.connect()

        cursor.execute(f"SELECT colony FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        namecolony = str(cursor.fetchone()[0])

        if namecolony == "None":
            await ctx.send(f"**{member.mention}** у вас нет государства!")
            return

        typetax = title(str(args.split()[0]))
        amount = str(args.split()[1])

        amount = int(amount)

        if (typetax != "Горожане") and (typetax != "Духовенство") and (typetax != "Дворянство"):
            await ctx.send(f"**{member.mention}** не по форме!")
            return

        if amount > 50:
            await ctx.send(f"**{member.mention}** налог не должен превышать 50%!")
            return

        if amount < 5:
            await ctx.send(f"**{member.mention}** налог не должен быть меньше 5%!")
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





        countries = sh.worksheet("Доходы/Расходы").get(f"{income_expenses_state}:{income_expenses_state}")
        countries = str(countries)[1:-1]
        countries = countries.replace("[", "")
        countries = countries.replace("]", "")
        countries = countries.replace(" \'", "")
        countries = countries.replace("\'", "")
        countries = countries.split(",")

        k2 = 1

        while str(countries[k2]) != "Государство":
            k2 += 1

        while str(countries[k2]) != namecolony:
            k2 += 1

        cursor.execute(f"SELECT didtheprestigechangeduringtheturn FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        didtheprestigechangeduringtheturn = int(cursor.fetchone()[0])

        procentprestige = 1

        if amount > didtheprestigechangeduringtheturn:
            if typetax == "Горожане":
                procentprestige = str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_taxes_citizens}{k2+1}"))[3:-3]
                procentprestige = int(procentprestige)

                if (amount<procentprestige) or (amount==procentprestige):
                    procentprestige = 1
                else:
                    procentprestige = amount - procentprestige

                sh.worksheet("Внутренняя политика").batch_update([
                    {
                        "range" : f"{domestic_policy_taxes_citizens}{k1+1}",
                        "values" : [[f"={amount}"]]
                    }
                ], raw = False)
                await ctx.send(f"**{member.mention}**, вы сменили налоговую ставку горожан в своем государстве на {amount}%")

            if typetax == "Духовенство":
                procentprestige = str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_taxes_clergy}{k2+1}"))[3:-3]
                procentprestige = int(procentprestige)

                if (amount<procentprestige) or (amount==procentprestige):
                    procentprestige = 1
                else:
                    procentprestige = amount - procentprestige

                sh.worksheet("Внутренняя политика").batch_update([
                    {
                        "range" : f"{domestic_policy_taxes_clergy}{k1+1}",
                        "values" : [[f"={amount}"]]
                    }
                ], raw = False)
                await ctx.send(f"**{member.mention}**, вы сменили налоговую ставку духовенства в своем государстве на {amount}%")

            if typetax == "Дворянство":
                procentprestige = str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_taxes_nobility}{k2+1}"))[3:-3]
                procentprestige = int(procentprestige)

                if (amount<procentprestige) or (amount==procentprestige):
                    procentprestige = 1
                else:
                    procentprestige = amount - procentprestige

                sh.worksheet("Внутренняя политика").batch_update([
                    {
                        "range" : f"{domestic_policy_taxes_nobility}{k1+1}",
                        "values" : [[f"={amount}"]]
                    }
                ], raw = False)
                await ctx.send(f"**{member.mention}**, вы сменили налоговую ставку дворян в своем государстве на {amount}%")


            prestige = str(sh.worksheet("Доходы/Расходы").get(f"{income_expenses_prestige}{k2+1}"))[3:-3]
            prestige = float(prestige)
            prestigestatic = prestige
            prestige = prestige - 1*procentprestige

            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET didtheprestigechangeduringtheturn = {prestigestatic} WHERE iduser = {ctx.author.id}")
            connection.commit()

            sh.worksheet("Доходы/Расходы").batch_update([
                {
                    "range" : f"{income_expenses_prestige}{k2+1}:{income_expenses_prestige}{k2+1}",
                    "values" : [[f"={prestige}"]]
                }
            ], raw = False)

        else:
            if typetax == "Горожане":
                procentprestige = str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_taxes_citizens}{k2+1}"))[3:-3]
                procentprestige = int(procentprestige)

                procentprestige = procentprestige - amount

                sh.worksheet("Внутренняя политика").batch_update([
                    {
                        "range" : f"{domestic_policy_taxes_citizens}{k1+1}",
                        "values" : [[f"={amount}"]]
                    }
                ], raw = False)
                await ctx.send(f"**{member.mention}**, вы сменили налоговую ставку горожан в своем государстве на {amount}%")

            if typetax == "Духовенство":
                procentprestige = str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_taxes_clergy}{k2+1}"))[3:-3]
                procentprestige = int(procentprestige)

                procentprestige = procentprestige - amount

                sh.worksheet("Внутренняя политика").batch_update([
                    {
                        "range" : f"{domestic_policy_taxes_clergy}{k1+1}",
                        "values" : [[f"={amount}"]]
                    }
                ], raw = False)
                await ctx.send(f"**{member.mention}**, вы сменили налоговую ставку духовенства в своем государстве на {amount}%")

            if typetax == "Дворянство":
                procentprestige = str(sh.worksheet("Внутренняя политика").get(f"{domestic_policy_taxes_nobility}{k2+1}"))[3:-3]
                procentprestige = int(procentprestige)

                procentprestige = procentprestige - amount

                sh.worksheet("Внутренняя политика").batch_update([
                    {
                        "range" : f"{domestic_policy_taxes_nobility}{k1+1}",
                        "values" : [[f"={amount}"]]
                    }
                ], raw = False)
                await ctx.send(f"**{member.mention}**, вы сменили налоговую ставку дворян в своем государстве на {amount}%")


            prestige = str(sh.worksheet("Доходы/Расходы").get(f"{income_expenses_prestige}{k2+1}"))[3:-3]
            prestige = float(prestige)
            prestige = prestige + procentprestige

            cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET didtheprestigechangeduringtheturn = 0 WHERE iduser = {ctx.author.id}")
            connection.commit()

            sh.worksheet("Доходы/Расходы").batch_update([
                {
                    "range" : f"{income_expenses_prestige}{k2+1}:{income_expenses_prestige}{k2+1}",
                    "values" : [[f"={prestige}"]]
                }
            ], raw = False)




async def setup(bot):
    await bot.add_cog(tax(bot))