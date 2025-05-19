import discord

from discord.ext import commands
from connectmysql import connection, cursor

class onguildjoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        connection.connect()

        for guild in self.bot.guilds:
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

        for guild in self.bot.guilds:
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

        for guild in self.bot.guilds:
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

        for guild in self.bot.guilds:
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


        for guild in self.bot.guilds:
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_time (
                id INT AUTO_INCREMENT,
                globaltime BIGINT DEFAULT 0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

        for guild in self.bot.guilds:
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

        for guild in self.bot.guilds:
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_squadron (
                id INT AUTO_INCREMENT,
                name VARCHAR(255),
                iduser BIGINT,
                squadron BIGINT DEFAULT 0,
                type VARCHAR(255),
                hp BIGINT DEFAULT 0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

        for guild in self.bot.guilds:
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_message (
                id INT AUTO_INCREMENT,
                name VARCHAR(255),
                iduser BIGINT,
                text VARCHAR(255),
                flag BIGINT DEFAULT 0,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

        for guild in self.bot.guilds:
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_towns (
                id INT AUTO_INCREMENT,
                first_town VARCHAR(255),
                first_type_of_locality VARCHAR(255),
                second_town VARCHAR(255),
                second_type_of_locality VARCHAR(255),
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

        for guild in self.bot.guilds:
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_maritimes (
                id INT AUTO_INCREMENT,
                town VARCHAR(255),
                maritime VARCHAR(255),
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")

        for guild in self.bot.guilds:
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

        for guild in self.bot.guilds:
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {guild.id}_events (
                id INT AUTO_INCREMENT,
                message LONGTEXT,
                countbuttons BIGINT,
                PRIMARY KEY (id)
            ) CHARACTER SET 'utf8'""")


        for guild in self.bot.guilds:
            for member in guild.members:
                if not member.bot:
                    cursor.execute(f"SELECT iduser FROM `{guild.id}` WHERE iduser = {member.id}")
                    row = cursor.fetchone()
                    if row == None:
                        cursor.execute(f"INSERT INTO `{guild.id}`(name, iduser, res3) VALUES ('{member}', {member.id}, 10)")
                    else:
                        pass


        connection.commit()

async def setup(bot):
    await bot.add_cog(onguildjoin(bot))