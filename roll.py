import discord
import random

from discord.ext import commands

class roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=['roll'], pass_context=True)
    async def __roll(self, ctx, *, args=None):
        if args is None:
            await ctx.send(f"Введите сначало минимальное, затем максимальное число, либо слова в строчку и я выберу случайное и них!")
            return
        if args is not None:
            if args.split()[0].isdigit() == False:
                if args.split()[1].isdigit() == False:
                    stroka = args.split()
                    obstroka = ' '.join(stroka)
                    cifra = obstroka.count(' ')
                    randoc = random.randint(0, cifra)
                    await ctx.send(args.split()[randoc])
                    return
            perv = args.split()[0]
            posle = args.split()[1]
            if int(perv) > int(posle):
                await ctx.send(f"Максимальное число меньше минимального числа!")
                return
            tera = random.randint(int(perv), int(posle))
            await ctx.send(f"Случайное число от [{perv}] до [{posle}] : [{tera}]")

async def setup(bot):
    await bot.add_cog(roll(bot))