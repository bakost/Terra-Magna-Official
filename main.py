import asyncio
import discord
import datetime

from discord.ext import commands
from connectmysql import connection, cursor
from config import token, cogs, adminrole, texrole, logschannel, techwork, status, admins, table, playerrole

from playingame import playingame
from updatetimers import updatetimers
from replenishmentofresources import replenishmentofresources
from religionfanaticismevent import religionfanaticismevent
from hungerevent import hungerevent
from updategoogleworksheet import updategoogleworksheet
from loopcheckgraborprotect import loopcheckgraborprotect

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), strip_after_prefix=True, application_id='1088515461827805184')
bot.remove_command('help')

@bot.event
async def on_connect():
    print("Connection to the discord servers is successful!")
    f = open("loadedcogs.txt", "w")
    if status == "normal":
        print("Uploading cogs...")
        print()
        for extension in cogs:
            print("Uploading:", extension)
            f.write(f"{extension}\n")
            await bot.load_extension(extension)
            print(extension, "successfully uploaded!")
        print()
        print("Normal works on!")

    elif status == "techwork":
        print("Uploading cogs...")
        print()
        for extension in techwork:
            print("Uploading:", extension)
            f.write(f"{extension}\n")
            await bot.load_extension(extension)
            print(extension, "successfully uploading!")
        print()
        print("Technical works on!")
    f.close()

@bot.event
async def on_ready():
    print("Cogs successfully uploaded!")
    print("Loading the database...")

    connection.connect()

    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS `{guild.id}` (
                id INT AUTO_INCREMENT,
                name VARCHAR(255),
                iduser BIGINT,
                colony VARCHAR(255),
                capital VARCHAR(255),
                type_of_locality VARCHAR(255),
                didtheprestigechangeduringtheturn BIGINT DEFAULT 0,
                cash DOUBLE(16,2) DEFAULT 0.0,
                res1 DOUBLE(16,2) DEFAULT 0.0,
                res2 DOUBLE(16,2) DEFAULT 0.0,
                res3 DOUBLE(16,2) DEFAULT 0.0,
                res4 DOUBLE(16,2) DEFAULT 0.0,
                res5 DOUBLE(16,2) DEFAULT 0.0,
                res6 DOUBLE(16,2) DEFAULT 0.0,
                res7 DOUBLE(16,2) DEFAULT 0.0,
                res8 DOUBLE(16,2) DEFAULT 0.0,
                res9 DOUBLE(16,2) DEFAULT 0.0,
                res10 DOUBLE(16,2) DEFAULT 0.0,
                res11 DOUBLE(16,2) DEFAULT 0.0,
                inventory VARCHAR(1000),
                inventory_amount VARCHAR(1000),
                fleet VARCHAR(1000),
                fleet_amount VARCHAR(1000),
                fleet_amount_usable VARCHAR(1000),
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")


    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_shop (
                id INT AUTO_INCREMENT,
                name VARCHAR(255),
                description VARCHAR(8000),
                type BIGINT DEFAULT 0,
                cash DOUBLE(16,2) DEFAULT 0.0,
                res1 DOUBLE(16,2) DEFAULT 0.0,
                res2 DOUBLE(16,2) DEFAULT 0.0,
                res3 DOUBLE(16,2) DEFAULT 0.0,
                res4 DOUBLE(16,2) DEFAULT 0.0,
                res5 DOUBLE(16,2) DEFAULT 0.0,
                res6 DOUBLE(16,2) DEFAULT 0.0,
                res7 DOUBLE(16,2) DEFAULT 0.0,
                res8 DOUBLE(16,2) DEFAULT 0.0,
                res9 DOUBLE(16,2) DEFAULT 0.0,
                res10 DOUBLE(16,2) DEFAULT 0.0,
                res11 DOUBLE(16,2) DEFAULT 0.0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")


    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_economy (
                id INT AUTO_INCREMENT,
                type VARCHAR(255),
                res1 DOUBLE(16,2) DEFAULT 0.0,
                res2 DOUBLE(16,2) DEFAULT 0.0,
                res3 DOUBLE(16,2) DEFAULT 0.0,
                res4 DOUBLE(16,2) DEFAULT 0.0,
                res5 DOUBLE(16,2) DEFAULT 0.0,
                res6 DOUBLE(16,2) DEFAULT 0.0,
                res7 DOUBLE(16,2) DEFAULT 0.0,
                res8 DOUBLE(16,2) DEFAULT 0.0,
                res9 DOUBLE(16,2) DEFAULT 0.0,
                res10 DOUBLE(16,2) DEFAULT 0.0,
                res11 DOUBLE(16,2) DEFAULT 0.0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")


    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_buildings (
                id INT AUTO_INCREMENT,
                building VARCHAR(8000),
                arbeiter BIGINT DEFAULT 0,
                count_building VARCHAR(255),
                count_building_max BIGINT DEFAULT 0,
                cash DOUBLE(16,2) DEFAULT 0.0,
                res1 DOUBLE(16,2) DEFAULT 0.0,
                res2 DOUBLE(16,2) DEFAULT 0.0,
                res3 DOUBLE(16,2) DEFAULT 0.0,
                res4 DOUBLE(16,2) DEFAULT 0.0,
                res5 DOUBLE(16,2) DEFAULT 0.0,
                res6 DOUBLE(16,2) DEFAULT 0.0,
                res7 DOUBLE(16,2) DEFAULT 0.0,
                res8 DOUBLE(16,2) DEFAULT 0.0,
                res9 DOUBLE(16,2) DEFAULT 0.0,
                res10 DOUBLE(16,2) DEFAULT 0.0,
                res11 DOUBLE(16,2) DEFAULT 0.0,
                qcash DOUBLE(16,2) DEFAULT 0.0,
                qres1 DOUBLE(16,2) DEFAULT 0.0,
                qres2 DOUBLE(16,2) DEFAULT 0.0,
                qres3 DOUBLE(16,2) DEFAULT 0.0,
                qres4 DOUBLE(16,2) DEFAULT 0.0,
                qres5 DOUBLE(16,2) DEFAULT 0.0,
                qres6 DOUBLE(16,2) DEFAULT 0.0,
                qres7 DOUBLE(16,2) DEFAULT 0.0,
                qres8 DOUBLE(16,2) DEFAULT 0.0,
                qres9 DOUBLE(16,2) DEFAULT 0.0,
                qres10 DOUBLE(16,2) DEFAULT 0.0,
                qres11 DOUBLE(16,2) DEFAULT 0.0,
                acash DOUBLE(16,2) DEFAULT 0.0,
                ares1 DOUBLE(16,2) DEFAULT 0.0,
                ares2 DOUBLE(16,2) DEFAULT 0.0,
                ares3 DOUBLE(16,2) DEFAULT 0.0,
                ares4 DOUBLE(16,2) DEFAULT 0.0,
                ares5 DOUBLE(16,2) DEFAULT 0.0,
                ares6 DOUBLE(16,2) DEFAULT 0.0,
                ares7 DOUBLE(16,2) DEFAULT 0.0,
                ares8 DOUBLE(16,2) DEFAULT 0.0,
                ares9 DOUBLE(16,2) DEFAULT 0.0,
                ares10 DOUBLE(16,2) DEFAULT 0.0,
                ares11 DOUBLE(16,2) DEFAULT 0.0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_time (
                id INT AUTO_INCREMENT,
                globaltime BIGINT DEFAULT 0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")


    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_grab (
                id INT AUTO_INCREMENT,
                name VARCHAR(255),
                iduser BIGINT,
                maritime VARCHAR(255),
                galeons BIGINT DEFAULT 0,
                karavells BIGINT DEFAULT 0,
                type BIGINT DEFAULT 0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")


    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_squadron (
                id INT AUTO_INCREMENT,
                name VARCHAR(255),
                iduser BIGINT,
                squadron BIGINT DEFAULT 0,
                type VARCHAR(255),
                hp BIGINT DEFAULT 0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_message (
                id INT AUTO_INCREMENT,
                name VARCHAR(255),
                iduser BIGINT,
                text VARCHAR(255),
                flag BIGINT DEFAULT 0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_towns (
                id INT AUTO_INCREMENT,
                first_town VARCHAR(255),
                first_type_of_locality VARCHAR(255),
                second_town VARCHAR(255),
                second_type_of_locality VARCHAR(255),
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_maritimes (
                id INT AUTO_INCREMENT,
                town VARCHAR(255),
                maritime VARCHAR(255),
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_logs (
                id INT AUTO_INCREMENT,
                day VARCHAR(255),
                time VARCHAR(255),
                author VARCHAR(255),
                iduser BIGINT,
                message LONGTEXT,
                channelid BIGINT,
                type VARCHAR(255),
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

    for guild in bot.guilds:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_events (
                id INT AUTO_INCREMENT,
                message LONGTEXT,
                countbuttons BIGINT,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")


    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:
                cursor.execute(f"SELECT iduser FROM `{guild.id}` WHERE iduser = {member.id}")
                row = cursor.fetchone()
                if row == None:
                    cursor.execute(f"INSERT INTO `{guild.id}`(name, iduser, res3) VALUES ('{member}', {member.id}, 10)")
                else:
                    pass

    connection.commit()


    #================================================

    bot.loop.create_task(playingame(bot))
    #bot.loop.create_task(updatetimers(bot))
    #bot.loop.create_task(replenishmentofresources(bot))
    #bot.loop.create_task(religionfanaticismevent(bot))
    #bot.loop.create_task(hungerevent(bot))
    #bot.loop.create_task(updategoogleworksheet(bot))
    #bot.loop.create_task(loopcheckgraborprotect(bot))

    #================================================


    print("The database is loaded!")
    print()
    print("Bot started!")
    print()
    print("----------------------------------------------------")
    channel = bot.get_channel(logschannel)
    await channel.send(f"Bot started!")

@bot.command(aliases=['table'], pass_context=True)
async def __table(ctx):
    roles = discord.utils.get(ctx.guild.roles, id=playerrole)
    rolesadmin = discord.utils.get(ctx.guild.roles, id=adminrole)
    rolestexadmin = discord.utils.get(ctx.guild.roles, id=texrole)
    if (roles in ctx.author.roles) or (ctx.message.author.id in admins) or (rolesadmin in ctx.author.roles) or (rolestexadmin in ctx.author.roles):
        embed = discord.Embed(
            title="Terra Magna | ВПИ (Таблица)",
            description=f"Таблица для игроков Terra Magna | ВПИ",
            color = 0x00BFFF,
        )
        embed.add_field(name=f"", value=f"{table}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"**{ctx.message.author.mention}**, вы не игрок/администратор.")


@bot.command(aliases=['cogsloaded','CL'], pass_context=True)
async def __cogsloaded(ctx):
    roles = discord.utils.get(ctx.guild.roles, id=texrole)
    if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
        print()
        print(f"{ctx.message.author.name} unloaded the loaded cogs!")
        print()
        embed = discord.Embed(
            title="Terra Magna | ВПИ (Cogs)",
            description=f"Cogs, загруженные на Terra Magna | ВПИ",
            color = 0x00BFFF,
        )
        await ctx.send(f"Загруженные cogs:")
        f = open("loadedcogs.txt", "r")
        k = 0
        for i in f:
            k += 1
            embed.add_field(name=f"", value=f"{k}) {i}", inline=False)
        await ctx.send(embed=embed)

@bot.command(aliases=['techwork-on','TON'], pass_context=True)
async def __techworkon(ctx):
    roles = discord.utils.get(ctx.guild.roles, id=texrole)
    if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
        print()
        print("Unloading cogs...")
        print()
        for extension in cogs:
            print("Unloading:", extension)
            await bot.unload_extension(extension)
            print(extension, "successfully unloading!")
        print()
        print("Uploading cogs...")
        print()
        for extension in techwork:
            print("Uploading:", extension)
            await bot.load_extension(extension)
            print(extension, "successfully uploading!")
        print()
        print("Technical works on!")
        await ctx.send(f"<@&{texrole}>, включен режим технических работ!")

@bot.command(aliases=['techwork-off','TOF'], pass_context=True)
async def __techworkoff(ctx):
    roles = discord.utils.get(ctx.guild.roles, id=texrole)
    if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
        print()
        print("Unloading cogs...")
        print()
        for extension in techwork:
            print("Unloading:", extension)
            await bot.unload_extension(extension)
            print(extension, "successfully unloading!")
        print()
        print("Uploading cogs...")
        print()
        for extension in cogs:
            print("Uploading:", extension)
            await bot.load_extension(extension)
            print(extension, "successfully uploading!")
        print()
        print("Technical works on!")
        await ctx.send(f"<@&{texrole}>, выключен режим технических работ!")

@bot.command(aliases=['loadcogsname','LCN'], pass_context=True)
async def __loadcogsname(ctx, *, args=None):
    roles = discord.utils.get(ctx.guild.roles, id=texrole)
    if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
        print()
        print("Uploading:", args)
        await bot.load_extension(args)
        print(args, "successfully uploading!")
        print()
        print(f"Cog {args} successfully uploaded!")
        await ctx.send(f"Cog {args} успешно загружен!")

@bot.command(aliases=['unloadcogsname','UCN'], pass_context=True)
async def __unloadcogsname(ctx, *, args=None):
    roles = discord.utils.get(ctx.guild.roles, id=texrole)
    if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
        print()
        print("Unloading:", args)
        await bot.unload_extension(args)
        print(args, "successfully unloading!")
        print()
        print(f"Cog {args} successfully unloaded!")
        await ctx.send(f"Cog {args} успешно выгружен!")

@bot.command(aliases=['loadcogs','LC'], pass_context=True)
async def __loadcogs(ctx):
    roles = discord.utils.get(ctx.guild.roles, id=texrole)
    if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
        print()
        print("Uploading cogs...")
        print()
        for extension in cogs:
            print("Uploading:", extension)
            await bot.load_extension(extension)
            print(extension, "successfully uploading!")
        print()
        print("Cogs successfully uploaded!")
        await ctx.send(f"Cogs успешно загружены!")

@bot.command(aliases=['unloadcogs','UC'], pass_context=True)
async def __unloadcogs(ctx):
    roles = discord.utils.get(ctx.guild.roles, id=texrole)
    if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
        print()
        print("Unloading cogs...")
        print()
        for extension in cogs:
            print("Unloading:", extension)
            await bot.unload_extension(extension)
            print(extension, "successfully unloading!")
        print()
        print("Cogs successfully unloading!")
        await ctx.send(f"Cogs успешно выгружены!")

@bot.command(aliases=['reloadcogs','RC'], pass_context=True)
async def __reloadcogs(ctx):
    roles = discord.utils.get(ctx.guild.roles, id=texrole)
    if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
        print()
        print("Reloading cogs...")
        print()
        for extension in cogs:
            print("Reloading:", extension)
            await bot.unload_extension(extension)
            await bot.load_extension(extension)
            print(extension, "successfully reloading!")
        print()
        print("Cogs successfully reloading!")
        await ctx.send(f"Cogs успешно перезагружены!")


bot.run(token)