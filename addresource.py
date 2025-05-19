import discord

from discord.ext import commands
from connectmysql import connection, cursor
from config import smile, adminrole

class addresource(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['add-cash'], pass_context=True)
    async def __addcash(self, ctx, member: discord.Member = None, amount: float = None):
        role = discord.utils.get(ctx.guild.roles, id=adminrole)
        if role in ctx.author.roles:
            connection.connect()
            if member is None:
                await ctx.send(f"**{ctx.message.author.mention}**, укажите пользователя, которому нужно выдать монеты.")
            else:
                if amount is None:
                    await ctx.send(f"**{ctx.message.author.mention}**, укажите сумму монет, которую нужно выдать.")
                elif amount < 0:
                    await ctx.send(f"**{ctx.message.author.mention}**, указанное количество меньше 0.")
                else:
                    cursor.execute(f"UPDATE `{member.guild.id}` SET cash = cash + {amount} WHERE iduser = {member.id}")
                    connection.commit()
                    await ctx.send(f"Выдана сумма {amount}{smile} игроку {member.mention}")
        else:
            await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор.")

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['add-resource', 'add-res'], pass_context=True)
    async def __addresource(self, ctx, *, args=None):
        role = discord.utils.get(ctx.guild.roles, id=adminrole)
        if role in ctx.author.roles:
            connection.connect()
            if args is None:
                await ctx.send(f"Введите пинг игрока, id и количество ресурса, которые вы хотите выдать!")
                return
            playerping = args.split()[0]
            res = int(args.split()[1])
            kolvor = int(args.split()[2])

            tag = playerping.replace("<","")
            tag = tag.replace(">","")
            tag = tag.replace("@","")

            tag = int(tag)

            if kolvor < 0:
                await ctx.send(f"**{ctx.message.author.mention}**, указанное количество меньше 0.")
            else:
                cursor.execute(f"UPDATE `{ctx.author.guild.id}` SET res{res} = res{res} + {kolvor} WHERE iduser = {tag}")
                connection.commit()
                await ctx.send(f"Выдана сумма {kolvor} ресурса {res} id игроку {playerping}")
        else:
            await ctx.send(f"**{ctx.message.author.mention}**, вы не администратор.")



async def setup(bot):
    await bot.add_cog(addresource(bot))