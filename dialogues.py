import discord

from discord.ext import commands

from connectmysql import connection, cursor
from config import treatiseschannel, dialogueschannel, sh, income_expenses_state, income_expenses_prestige

class dialogues(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        dialogueschannelget = self.bot.get_channel(dialogueschannel)
        treatiseschannelget = self.bot.get_channel(treatiseschannel)
        if not message.author.bot:
            if (message.channel == dialogueschannelget) or (message.channel == treatiseschannelget):
                connection.connect()

                if '((' in message.content:
                    return

                cursor.execute(f"SELECT iduser FROM {message.author.guild.id}_message")
                reco = cursor.fetchall()

                flagstaff = 0

                for i in range(0, len(reco)):
                    if reco[i][0] != message.author.id:
                        flagstaff += 1

                #await message.channel.send(f"{flagstaff}, {len(reco)}")

                if flagstaff == len(reco):
                    cursor.execute(f"INSERT INTO {message.author.guild.id}_message(name, iduser, text) VALUES ('{member}',{member.id},'{message.content}')")
                    connection.commit()

                    cursor.execute(f"SELECT flag FROM {message.author.guild.id}_message WHERE iduser = {message.author.id}")
                    flag = str(cursor.fetchone()[0])

                    if (flag == "0") and (len(message.content) > 10):

                        cursor.execute(f"SELECT colony FROM `{message.author.guild.id}` WHERE iduser = {message.author.id}")
                        namecolony = str(cursor.fetchone()[0])

                        if namecolony == "None":
                            await message.channel.send(f"**{member.mention}** у вас нет государства!")
                            return

                        countries = sh.worksheet("Доходы/Расходы").get(f"{income_expenses_state}:{income_expenses_state}")
                        countries = str(countries)[1:-1]
                        countries = countries.replace("[", "")
                        countries = countries.replace("]", "")
                        countries = countries.replace(" \'", "")
                        countries = countries.replace("\'", "")
                        countries = countries.split(",")

                        k1 = 1

                        while str(countries[k1]) != "Государство":
                            k1 += 1

                        while str(countries[k1]) != namecolony:
                            k1 += 1

                        prestige = str(sh.worksheet("Доходы/Расходы").get(f"{income_expenses_prestige}{k1+1}"))[3:-3]
                        prestige = float(prestige)
                        prestige = prestige + 0.5


                        sh.worksheet("Доходы/Расходы").batch_update([
                            {
                                "range" : f"{income_expenses_prestige}{k1+1}:{income_expenses_prestige}{k1+1}",
                                "values" : [[f"={prestige}"]]
                            }
                        ], raw = False)

                        cursor.execute(f"UPDATE {message.author.guild.id}_message SET flag = '1' WHERE iduser = {message.author.id}")
                        connection.commit()
                        await message.channel.send(f"**{member.mention}**, Вы получили 0.5 престижа!")

                    return

                cursor.execute(f"SELECT text FROM {message.author.guild.id}_message WHERE iduser = {message.author.id}")
                text = str(cursor.fetchone()[0])

                cursor.execute(f"SELECT flag FROM {message.author.guild.id}_message WHERE iduser = {message.author.id}")
                flag = str(cursor.fetchone()[0])

                if text == "None":
                    cursor.execute(f"INSERT INTO {message.author.guild.id}_message(name, iduser, text) VALUES ('{member}',{member.id},'{message.content}')")
                else:
                    text = text + ' ' + message.content
                    cursor.execute(f"UPDATE {message.author.guild.id}_message SET text = '{text}' WHERE iduser = {message.author.id}")

                connection.commit()

                if (flag == "0") and (len(text) > 10):

                    cursor.execute(f"SELECT colony FROM `{message.author.guild.id}` WHERE iduser = {message.author.id}")
                    namecolony = str(cursor.fetchone()[0])

                    if namecolony == "None":
                        await message.channel.send(f"**{member.mention}** у вас нет государства!")
                        return

                    countries = sh.worksheet("Доходы/Расходы").get(f"{income_expenses_state}:{income_expenses_state}")
                    countries = str(countries)[1:-1]
                    countries = countries.replace("[", "")
                    countries = countries.replace("]", "")
                    countries = countries.replace(" \'", "")
                    countries = countries.replace("\'", "")
                    countries = countries.split(",")

                    k1 = 1

                    while str(countries[k1]) != "Государство":
                        k1 += 1

                    while str(countries[k1]) != namecolony:
                        k1 += 1

                    prestige = str(sh.worksheet("Доходы/Расходы").get(f"{income_expenses_prestige}{k1+1}"))[3:-3]
                    prestige = float(prestige)
                    prestige = prestige + 0.5


                    sh.worksheet("Доходы/Расходы").batch_update([
                        {
                            "range" : f"{income_expenses_prestige}{k1+1}:{income_expenses_prestige}{k1+1}",
                            "values" : [[f"={prestige}"]]
                        }
                    ], raw = False)

                    cursor.execute(f"UPDATE {message.author.guild.id}_message SET flag = '1' WHERE iduser = {message.author.id}")
                    connection.commit()
                    await message.channel.send(f"**{member.mention}**, Вы получили 0.5 престижа!")








async def setup(bot):
    await bot.add_cog(dialogues(bot))