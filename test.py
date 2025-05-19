import discord
import datetime
import asyncio
import openai

from discord.ext import commands
from discord.ui import View, Button

from connectmysql import connection, cursor
from config import admins, adminrole, token_openai, sh, texrole
from PIL import Image, ImageDraw, ImageFont

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    openai.api_key = token_openai

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases=['test'], pass_context=True)
    async def __test(self, ctx):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            member = ctx.message.author
            await ctx.send(f"**{member.mention}** эта команда для проверки работоспособности бота!")

    @commands.command(aliases=['test2'], pass_context=True)
    async def __test2(self, ctx):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            view = View()
            style = discord.ButtonStyle.blurple
            item = Button(style=style, label="Test")
            view.add_item(item=item)
            async def button_callback(interaction):
                 await interaction.response.send_message("Hi!")

            item.callback = button_callback
            await ctx.send("Hello World!", view=view)

    @commands.command(aliases=['test3'], pass_context=True)
    async def __test3(self, ctx):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            mass = [1,2,3,4,5,6,7,8,9,10,11,12,51,52,53,54,55,56,57]
            await ctx.send(mass)
            await ctx.send(mass[0])

    @commands.command(aliases=['test4'], pass_context=True)
    async def __test4(self, ctx):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            now = datetime.datetime.now()
            await ctx.send(f"{now.hour},{now.minute},{now.second}")

    @commands.command(aliases=['test5'], pass_context=True)
    async def __test5(self, ctx):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            await ctx.send(f"<@&{adminrole}>")

    @commands.command(aliases=['test6'], pass_context=True)
    async def __test6(self, ctx, *,  args=None):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            member = ctx.message.author
            if args is None:
                await ctx.send(f"**{member.mention}**, отсутствуют аргументы! Пример команды: !test6 [Текст]")
                return

            texttm = str(args.split()[0])

            image = Image.open("fon.png")

            font = ImageFont.truetype("tnr.ttf", size=25)

            draw_text = ImageDraw.Draw(image)
            draw_text.text(
                (100,100),
                texttm,
                font=font,
                fill=('#1C0606')
            )
            image.save("tempfon.png")

            await asyncio.sleep(2)
            await ctx.send(file=discord.File("tempfon.png"))


    @commands.command(aliases=['test7'], pass_context=True)
    async def __test7(self, ctx, *, args=None):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            result = str(args)
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=result,
                temperature=0.9,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=["You:"]
            )
            await ctx.send(embed=discord.Embed(title=f'{result}',description=response['choices'][0]['text']))

    @commands.command(aliases=['test8'], pass_context=True)
    async def __test8(self, ctx):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):
            towns = sh.worksheet("Города").get(f"B:M")
            state = sh.worksheet("Доходы/Расходы").get(f"B:C")
            await ctx.send(f"{towns}")
            await ctx.send(f"{towns[1][6]}")
            await ctx.send(f"{state}")

    @commands.command(aliases=['test9'], pass_context=True)
    async def __test9(self, ctx):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):


            '''sh.worksheet("тесты").batch_update([body])
            body = {
                "range" : f"F1:F1",
                "values" : [[
                    f"голубочик"
                ]]
            }'''

            insertRow = ["hello", 5, "red", "blue"]


            sh.worksheet("тесты").insert_row(insertRow, 3)

            await ctx.send(f"+")

    @commands.command(aliases=['bdmessclear'], pass_context=True)
    async def __bdmessclear(self, ctx):
        roles = discord.utils.get(ctx.guild.roles, id=texrole)
        if (roles in ctx.author.roles) or (ctx.message.author.id in admins):

            connection.cursor()
            cursor.execute(f"TRUNCATE TABLE {ctx.author.guild.id}_message")
            connection.commit()

            await ctx.send(f"+")





async def setup(bot):
    await bot.add_cog(test(bot))