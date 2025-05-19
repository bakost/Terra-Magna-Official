import discord

from discord.ext import commands
from connectmysql import connection, cursor
from config import adminrole

class inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['inventory','inv'], pass_context=True)
    async def __inventory(self, ctx, member: discord.Member = None):
        connection.connect()
        if member is None:
            cursor.execute(f"SELECT inventory FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco1 = cursor.fetchone()[0]

            cursor.execute(f"SELECT inventory_amount FROM `{ctx.author.guild.id}` WHERE iduser = {ctx.author.id}")
            reco2 = cursor.fetchone()[0]

            embed1 = discord.Embed(
                title="Terra Magna | ВПИ (Инвентарь)",
                description=f"Это ваш инвентарь. Чтобы использовать предмет, введите !use название количество",
                color = 0x00BFFF,
            )
            if reco1 == None:
                embed1.add_field(name=f"Здесь пусто, пора приобретать предметы!", value='~~=======================~~', inline=False)
                #embed1.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed1)
                return

            i = 1
            j = 1

            for keniga in reco1.split():
                i = i + 1
                for valuestin in reco2.split():
                    j = j + 1
                    if i == j:
                        embed1.add_field(name=f"{valuestin} - {keniga}", value='~~=======================~~', inline=False)
                j = 1

            #embed1.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed1)


        if member is not None:
            role = discord.utils.get(ctx.guild.roles, id=adminrole)
            if role in ctx.author.roles:
                cursor.execute(f"SELECT inventory FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
                reco1 = cursor.fetchone()[0]

                cursor.execute(f"SELECT inventory_amount FROM `{ctx.author.guild.id}` WHERE iduser = {member.id}")
                reco2 = cursor.fetchone()[0]

                embed2 = discord.Embed(
                    title="Terra Magna | ВПИ (Инвентарь)",
                    description=f"Это инвентарь игрока {member.mention}.",
                    color = 0x00BFFF,
                )
                if reco1 == None:
                    embed2.add_field(name=f"Здесь пусто, пора приобретать предметы!", value='~~=======================~~', inline=False)
                    #embed2.set_author(name=member.display_name, icon_url=member.avatar_url)
                    await ctx.send(embed=embed2)
                    return

                i = 1
                j = 1

                for keniga in reco1.split():
                    i = i + 1
                    for valuestin in reco2.split():
                        j = j + 1
                        if i == j:
                            embed2.add_field(name=f"{valuestin} - {keniga}", value='~~=======================~~', inline=False)
                    j = 1

                #embed2.set_author(name=member.display_name, icon_url=member.avatar_url)
                await ctx.send(embed=embed2)

            else:
                await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор.")


async def setup(bot):
    await bot.add_cog(inventory(bot))