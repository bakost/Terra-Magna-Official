import discord

from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor
from config import sh, laws_state, laws_democracy, laws_dictatorship, laws_spirituality, laws_equality, laws_fanaticism, laws_neutrality, laws_isolation, laws_oligarchy, laws_emphasis_army, laws_emphasis_fleet, laws_limited_slavery, laws_conditional_slavery, laws_average_openness, laws_open_doors, laws_balance_armyflot, laws_minor_inequality, laws_natives_peaceful, laws_natives_oppression, laws_significant_privileges, laws_religion_doesnt_matter, laws_slave_owning_society,laws_state_system_frame_1,laws_state_system_frame_2, laws_civil_rights_frame_1, laws_civil_rights_frame_2, laws_openness_of_the_state_frame_1, laws_openness_of_the_state_frame_2,laws_religion_frame_1, laws_religion_frame_2, laws_attitude_towards_the_natives_frame_1, laws_attitude_towards_the_natives_frame_2,laws_army_and_fleet_frame_1, laws_army_and_fleet_frame_2, laws_slaves_frame_1, laws_slaves_frame_2

class law(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['law'], pass_context=True)
    async def __law(self, ctx, *,  args=None):
        member = ctx.message.author

        if args is None:
            await ctx.send(f"**{member.mention}** отсутствуют аргументы! Пример команды: !law [Раздел] [Закон]")
            return

        connection.connect()

        chapt = title(str(args.split()[0]))
        law = title(str(args.split()[1]))


        cursor.execute(f"SELECT colony FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        namecolony = str(cursor.fetchone()[0])

        cursor.execute(f"SELECT res5 FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
        paper = int(cursor.fetchone()[0])


        if namecolony == "None":
            await ctx.send(f"**{member.mention}** у вас нет государства!")
            return

        if paper < 5:
            await ctx.send(f"**{member.mention}** у вас не хватает бумаги!")
            return

        laws = sh.worksheet("Законы").get(f"{laws_state}:{laws_state}")
        laws = str(laws)[1:-1]
        laws = laws.replace("[", "")
        laws = laws.replace("]", "")
        laws = laws.replace(" \'", "")
        laws = laws.replace("\'", "")
        laws = laws.split(",")

        k1 = 1

        while str(laws[k1]) != namecolony:
            k1 += 1
            if k1 > len(laws):
                await ctx.send(f"**{member.mention}** вашего государства нет в таблице, свяжитесь с администрацией!")
                return

        k2 = 1

        while str(laws[k2]) != "Государство":
            k2 += 1

        while str(laws[k2]) != namecolony:
            k2 += 1

        k2 += 1

        control = ""
        control1 = ""
        control2 = ""



        if chapt == "Государственный-Строй":
            control1 = laws_state_system_frame_1
            control2 = laws_state_system_frame_2
        elif chapt == "Гражданские-Права":
            control1 = laws_civil_rights_frame_1
            control2 = laws_civil_rights_frame_2
        elif chapt == "Открытость-Государства":
            control1 = laws_openness_of_the_state_frame_1
            control2 = laws_openness_of_the_state_frame_2
        elif chapt == "Религия":
            control1 = laws_religion_frame_1
            control2 = laws_religion_frame_2
        elif chapt == "Отношение-К-Туземцам":
            control1 = laws_attitude_towards_the_natives_frame_1
            control2 = laws_attitude_towards_the_natives_frame_2
        elif chapt == "Армия-И-Флот":
            control1 = laws_army_and_fleet_frame_1
            control2 = laws_army_and_fleet_frame_2
        elif chapt == "Рабство":
            control1 = laws_slaves_frame_1
            control2 = laws_slaves_frame_2
        else:
            await ctx.send(f"**{member.mention}** ошибка в разделе законов!")
            return

        if law == "Демократия":
            control = laws_democracy
        elif law == "Олигархия":
            control = laws_oligarchy
        elif law == "Диктатура":
            control = laws_dictatorship
        elif law == "Равноправие":
            control = laws_equality
        elif law == "Незначительное-Неравенство":
            control = laws_minor_inequality
        elif law == "Значительные-Привилегии":
            control = laws_significant_privileges
        elif law == "Открытые-Двери":
            control = laws_open_doors
        elif law == "Средняя-Открытость":
            control = laws_average_openness
        elif law == "Изоляция":
            control = laws_isolation
        elif law == "Не-Имеет-Значения":
            control = laws_religion_doesnt_matter
        elif law == "Духовность":
            control = laws_spirituality
        elif law == "Фанатизм":
            control = laws_fanaticism
        elif law == "Миролюбие":
            control = laws_natives_peaceful
        elif law == "Нейтралитет":
            control = laws_neutrality
        elif law == "Угнетение":
            control = laws_natives_oppression
        elif law == "Упор-На-Флот":
            control = laws_emphasis_fleet
        elif law == "Равновесие":
            control = laws_balance_armyflot
        elif law == "Упор-На-Армию":
            control = laws_emphasis_army
        elif law == "Условное-Рабство":
            control = laws_conditional_slavery
        elif law == "Ограниченное-Рабство":
            control = laws_limited_slavery
        elif law == "Рабовладельческое-Общество":
            control = laws_slave_owning_society
        else:
            await ctx.send(f"**{member.mention}** ошибка в законе!")
            return

        sh.worksheet("Законы").update(f"{control1}{k2}:{control2}{k2}", [[f"",f"",f""]])
        sh.worksheet("Законы").update(f"{control}{k2}", "Принято")


        cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res5 = res5 - 5.0 WHERE iduser = {ctx.author.id}")


        connection.commit()
        await ctx.send(f"**{member.mention}** принял \"{law}\" в разделе \"{chapt}\" в своём государстве \"{namecolony}\"!")

async def setup(bot):
    await bot.add_cog(law(bot))