import discord

from discord.ext import commands
import random

class pony(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['pony'], pass_context=True)
    async def __pony(self, ctx):
        rand = random.randrange(0,112)
        member = ctx.message.author
        await ctx.send(f"**{member.mention}**, держи поняшку: ")
        if rand in range(0,10):
            await ctx.send(f"https://tenor.com/view/my-little-pony-sad-crying-tears-gif-7890864")
        if rand in range(10,20):
            await ctx.send(f"https://tenor.com/view/mlp-mlp-hug-moondancer-twilight-sparkle-twilight-sparkle-mlp-gif-26178208")
        if rand in range(20,30):
            await ctx.send(f"https://tenor.com/view/mlp-my-little-pony-friendship-is-magic-my-little-pony-smile-cute-gif-12071512")
        if rand in range(30,40):
            await ctx.send(f"https://tenor.com/view/%D0%BC%D0%BB%D0%BF-%D0%BC%D0%BB%D0%BF-%D0%BC%D1%83%D0%BB%D1%8C%D1%8F%D0%B8%D0%BB%D1%8C%D0%BC%D0%B4%D0%BB%D1%8F%D0%B4%D0%B5%D1%82%D0%B5%D0%B9-%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D0%B4%D0%BB%D1%8F%D0%B4%D0%B5%D1%82%D0%B5%D0%B9-%D1%84%D0%BB%D0%B0%D1%82%D1%82%D0%B5%D1%80%D1%88%D0%B0%D0%B9-gif-20903623")
        if rand in range(40,50):
            await ctx.send(f"https://tenor.com/view/twilight-sparkle-gif-9352714")
        if rand in range(50,60):
            await ctx.send(f"https://tenor.com/view/fluttershy-smile-happy-my-little-pony-mlp-gif-17239499")
        if rand in range(60,70):
            await ctx.send(f"https://tenor.com/view/glimglam-mlp-glim-glam-yawn-yawn-starlight-tired-glimmer-sleepy-glim-gif-18413098")
        if rand in range(70,80):
            await ctx.send(f"https://tenor.com/view/mlp-hug-trixie-starlight-glimmer-gif-14521586")
        if rand in range(80,90):
            await ctx.send(f"https://tenor.com/view/bon-bon-mlp-lyra-mlp-hug-mlp-pony-hug-gift-gif-17083954")
        if rand in range(90,100):
            await ctx.send(f"https://tenor.com/view/mlp-my-little-pony-smile-gif-12074329")
        if rand in range(100,110):
            await ctx.send(f"https://tenor.com/view/deal-with-it-sweetie-belle-my-little-pony-mlp-gif-25927378")
        if rand == 111:
            await ctx.send(f"https://tenor.com/view/%D0%B2%D0%B5%D0%BB%D0%B8%D0%BA%D0%BE-%D1%81%D0%B2%D0%B8%D0%BD-%D1%81%D0%B2%D0%B8%D0%BD%D1%8C%D1%8F-%D0%BE%D0%B3%D1%80%D0%BE%D0%BC%D0%BD%D0%B0%D1%8F-%D0%BF%D0%B8%D0%B7%D0%B4%D0%B5%D1%86-gif-24946258")
        if rand == 112:
            await ctx.send(f"https://cdn.discordapp.com/attachments/888927750025531453/888927873010892850/image0-65-1.gif")


async def setup(bot):
    await bot.add_cog(pony(bot))