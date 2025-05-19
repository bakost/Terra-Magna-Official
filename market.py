import discord

from discord.ext import commands
from numpy.core.defchararray import title
from connectmysql import connection, cursor
from config import res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11, smilepriceup, smilepricedown, smilepricedefault, smile, smile1, smile2, smile3, smile4, smile5, smile6, smile7, smile8, smile9, smile10, smile11

class market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['market'], pass_context=True)
    async def __market(self, ctx, *, args=None):
        member = ctx.message.author
        connection.connect()

        if args is None:

            cursor.execute(f"SELECT res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11 FROM {ctx.author.guild.id}_economy WHERE type = 'Покупка'")
            reco = cursor.fetchall()[0]
            cursor.execute(f"SELECT res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11 FROM {ctx.author.guild.id}_economy WHERE type = 'Продажа'")
            reco1 = cursor.fetchall()[0]
            cursor.execute(f"SELECT res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11 FROM {ctx.author.guild.id}_economy WHERE type = 'Количество'")
            reco2 = list(cursor.fetchall()[0])
            embed = discord.Embed(
                title=f"""Terra Magna | ВПИ (Ресурсы)""",
                description = f"""Мировой рынок""",
                color = 0x00BFFF
            )

            cursor.execute(f"SELECT res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11 FROM {ctx.author.guild.id}_economy WHERE type = 'Тренд'")
            reco3 = list(cursor.fetchall()[0])


            for i in range(0,11):
                if float(reco2[i]) > 20.1:
                    reco3[i] = smilepricedown
                elif float(reco2[i] == 20.0):
                    reco3[i] = smilepricedefault
                else:
                    reco3[i] = smilepriceup


            embed.add_field(name=f"""Ресурс:""", value=f"""
            {res1} {smile1}:  
            {res2} {smile2}: 
            {res3} {smile3}: 
            {res4} {smile4}: 
            {res5} {smile5}: 
            {res6} {smile6}: 
            {res7} {smile7}: 
            {res8} {smile8}: 
            {res9} {smile9}: 
            {res10} {smile10}: 
            {res11} {smile11}: 
            """, inline=True)
            embed.add_field(name=f"""Цена:""", value=f"""
            {reco[0]} {reco3[0]} 
            {reco[1]} {reco3[1]} 
            {reco[2]} {reco3[2]} 
            {reco[3]} {reco3[3]} 
            {reco[4]} {reco3[4]} 
            {reco[5]} {reco3[5]} 
            {reco[6]} {reco3[6]} 
            {reco[7]} {reco3[7]} 
            {reco[8]} {reco3[8]} 
            {reco[9]} {reco3[9]} 
            {reco[10]} {reco3[10]} 
            """, inline=True)
            embed.add_field(name=f"""Количество:""", value=f"""
            {reco2[0]} 
            {reco2[1]} 
            {reco2[2]}
            {reco2[3]}
            {reco2[4]}
            {reco2[5]} 
            {reco2[6]} 
            {reco2[7]} 
            {reco2[8]} 
            {reco2[9]} 
            {reco2[10]} 
            """, inline=True)
            await ctx.send(embed=embed)

        else:

            if (len(args.split()) == 1) or (len(args.split()) == 2):
                await ctx.send(f"**{member.mention}**, если вы хотите купить/продать ресурс, введите: !market [Buy/Sell] [id ресурса] [Количество]")
                return

            type = title(args.split()[0])

            if type == 'Buy':

                nameres = str(args.split()[1])
                kolvor = float(args.split()[2])

                nameres = int(nameres)

                if kolvor < 1:
                    await ctx.send(f"**{ctx.message.author.mention}**, указанное количество меньше 0.")
                    return

                if (nameres != '10') and (kolvor > 100):
                    await ctx.send(f"**{ctx.message.author.mention}**, указанное количество больше 100.")
                    return


                #рабы

                if (nameres == '10') and (kolvor % 100 != 0):
                    await ctx.send(f"**{ctx.message.author.mention}**, указанное количество рабов не кратно 100.")
                    return

                #рабы


                cursor.execute(f"SELECT res{nameres} FROM {ctx.author.guild.id}_economy WHERE type = 'Количество'")
                reco1 = float(cursor.fetchone()[0])

                if kolvor > reco1:
                    await ctx.send(f"**{ctx.message.author.mention}**, у бота недостаточно данного ресурса.")
                    return

                cursor.execute(f"SELECT cash FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
                reco1 = float(cursor.fetchone()[0])

                cursor.execute(f"SELECT res{nameres} FROM {ctx.author.guild.id}_economy WHERE type = 'Покупка'")
                reco = float(cursor.fetchone()[0])

                sumtrat = kolvor*reco
                procent = kolvor*0.25

                if sumtrat > reco1:
                    await ctx.send(f"У вас не достаточно монет!")
                    return

                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash - {sumtrat} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res{nameres} = res{nameres} + {kolvor} WHERE iduser = {ctx.author.id}")

                cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{nameres} = res{nameres} + {procent} WHERE type = 'Продажа'")
                cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{nameres} = res{nameres} + {procent} WHERE type = 'Покупка'")

                #cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{nameres} = 0.0 WHERE type = 'Тренд'")

                cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{nameres} = res{nameres} - {kolvor} WHERE type = 'Количество'")

                connection.commit()
                await ctx.send(f"Вы купили предмет с id {nameres} {kolvor} раз за {sumtrat}{smile}!")



            elif type == 'Sell':

                nameres = str(args.split()[1])
                kolvor = float(args.split()[2])

                nameres = int(nameres)

                if kolvor < 1:
                    await ctx.send(f"**{ctx.message.author.mention}**, указанное количество меньше 0.")
                    return

                if kolvor > 100:
                    await ctx.send(f"**{ctx.message.author.mention}**, указанное количество больше 100.")
                    return

                cursor.execute(f"SELECT res{nameres} FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
                reco1 = float(cursor.fetchone()[0])

                cursor.execute(f"SELECT res{nameres} FROM {ctx.author.guild.id}_economy WHERE type = 'Продажа'")
                reco = float(cursor.fetchone()[0])

                sumtrat = kolvor*reco
                procent = kolvor*0.25

                if kolvor > reco1:
                    await ctx.send(f"У вас не достаточно ресурсов!")
                    return

                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET cash = cash + {sumtrat} WHERE iduser = {ctx.author.id}")
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res{nameres} = res{nameres} - {kolvor} WHERE iduser = {ctx.author.id}")

                cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{nameres} = res{nameres} - {procent} WHERE type = 'Продажа'")
                cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{nameres} = res{nameres} - {procent} WHERE type = 'Покупка'")

                #cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{nameres} = 1.0 WHERE type = 'Тренд'")

                cursor.execute(f"UPDATE {ctx.author.guild.id}_economy SET res{nameres} = res{nameres} + {kolvor} WHERE type = 'Количество'")

                connection.commit()
                await ctx.send(f"Вы продали предмет с id {nameres} {kolvor} раз за {sumtrat}{smile}!")






async def setup(bot):
    await bot.add_cog(market(bot))