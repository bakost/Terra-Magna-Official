import discord

from discord.ext import commands
from connectmysql import connection, cursor
from config import adminrole

class fleet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['fleet'], pass_context=True)
    async def __fleet(self, ctx, member: discord.Member = None):
        connection.connect()
        if member is None:
            cursor.execute(f"SELECT fleet FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco1 = cursor.fetchone()[0]

            cursor.execute(f"SELECT fleet_amount FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco2 = cursor.fetchone()[0]

            cursor.execute(f"SELECT fleet_amount_usable FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco3 = cursor.fetchone()[0]

            embed1 = discord.Embed(
                title="Terra Magna | ВПИ (Флот)",
                description=f"Это ваш свободный флот.",
                color = 0x00BFFF,
            )

            embed2 = discord.Embed(
                title="Terra Magna | ВПИ (Флот)",
                description=f"Это ваш флот на заданиях.",
                color = 0x00BFFF,
            )

            if reco1 == None:
                embed1.add_field(name=f"Здесь пусто.", value='~~=======================~~', inline=False)
                embed2.add_field(name=f"Здесь пусто.", value='~~=======================~~', inline=False)
                #embed1.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed1)
                await ctx.send(embed=embed2)
                return

            i = 1
            j = 1

            for keniga in reco1.split():
                i += 1
                for valuestin in reco2.split():
                    j += 1
                    if i == j:
                        embed1.add_field(name=f"{valuestin} - {keniga}", value='~~=======================~~', inline=False)
                j = 1

            i = 1
            j = 1

            for keniga in reco1.split():
                i += 1
                for valuestin in reco3.split():
                    j += 1
                    if i == j:
                        embed2.add_field(name=f"{valuestin} - {keniga}", value='~~=======================~~', inline=False)
                j = 1

            #embed1.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed1)
            await ctx.send(embed=embed2)


        if member is not None:
            role = discord.utils.get(ctx.guild.roles, id=adminrole)
            if role in ctx.author.roles:
                cursor.execute(f"SELECT fleet FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
                reco1 = cursor.fetchone()[0]

                cursor.execute(f"SELECT fleet_amount FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
                reco2 = cursor.fetchone()[0]

                cursor.execute(f"SELECT fleet_amount_usable FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
                reco3 = cursor.fetchone()[0]

                embed1 = discord.Embed(
                    title="Terra Magna | ВПИ (Флот)",
                    description=f"Это свободный флот игрока {member.mention}",
                    color = 0x00BFFF,
                )

                embed2 = discord.Embed(
                    title="Terra Magna | ВПИ (Флот)",
                    description=f"Это флот на заданиях игрока {member.mention}",
                    color = 0x00BFFF,
                )

                if reco1 == None:
                    embed1.add_field(name=f"Здесь пусто.", value='~~=======================~~', inline=False)
                    embed2.add_field(name=f"Здесь пусто.", value='~~=======================~~', inline=False)
                    #embed2.set_author(name=member.display_name, icon_url=member.avatar_url)
                    await ctx.send(embed=embed1)
                    await ctx.send(embed=embed2)
                    return

                i = 1
                j = 1

                for keniga in reco1.split():
                    i += 1
                    for valuestin in reco2.split():
                        j += 1
                        if i == j:
                            embed1.add_field(name=f"{valuestin} - {keniga}", value='~~=======================~~', inline=False)
                    j = 1

                i = 1
                j = 1

                for keniga in reco1.split():
                    i += 1
                    for valuestin in reco3.split():
                        j += 1
                        if i == j:
                            embed2.add_field(name=f"{valuestin} - {keniga}", value='~~=======================~~', inline=False)
                    j = 1

                #embed2.set_author(name=member.display_name, icon_url=member.avatar_url)
                await ctx.send(embed=embed1)
                await ctx.send(embed=embed2)

            else:
                await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор.")


async def setup(bot):
    await bot.add_cog(fleet(bot))