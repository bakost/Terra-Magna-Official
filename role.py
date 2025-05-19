import discord

from discord.ext import commands
from config import adminrole, texrole, admins, texadmins, texroleplayer, playerrole

class role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['role','роль'], pass_context=True)
    async def __role(self, ctx):
        member = ctx.message.author
        roles1 = discord.utils.get(member.guild.roles, id=adminrole)
        roles2 = discord.utils.get(member.guild.roles, id=texrole)
        if (member.id in texadmins):
            if (roles1 in ctx.author.roles) or (roles2 in ctx.author.roles):
                await ctx.send(f"**{member.mention}** снял")
                await ctx.author.remove_roles(roles1)
                await ctx.author.remove_roles(roles2)
            else:
                await ctx.send(f"**{member.mention}** выдано")
                await ctx.author.add_roles(roles1)
                await ctx.author.add_roles(roles2)
        elif (member.id in admins):
            if roles1 in ctx.author.roles:
                await ctx.send(f"**{member.mention}** снял")
                await ctx.author.remove_roles(roles1)
            else:
                await ctx.send(f"**{member.mention}** выдано")
                await ctx.author.add_roles(roles1)
        else:
            await ctx.send(f"**{member.mention}**, отказано в доступе!")



    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['tex-mode-on'], pass_context=True)
    async def __texmode(self, ctx):
        member = ctx.message.author
        roles1 = discord.utils.get(member.guild.roles, id=adminrole)
        roles2 = discord.utils.get(member.guild.roles, id=texrole)
        roles3 = discord.utils.get(member.guild.roles, id=texroleplayer)
        if (member.id in texadmins):
            for guild in self.bot.guilds: 
                for member in guild.members:
                    await member.add_roles(roles3)
        else:
            await ctx.send(f"**{member.mention}**, отказано в доступе!")
    

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['tex-mode-off'], pass_context=True)
    async def __texmode(self, ctx):
        member = ctx.message.author
        roles1 = discord.utils.get(member.guild.roles, id=adminrole)
        roles2 = discord.utils.get(member.guild.roles, id=texrole)
        roles3 = discord.utils.get(member.guild.roles, id=playerrole)
        if (member.id in texadmins):
            for guild in self.bot.guilds: 
                for member in guild.members:
                    await member.add_roles(roles3)
        else:
            await ctx.send(f"**{member.mention}**, отказано в доступе!")

async def setup(bot):
    await bot.add_cog(role(bot))