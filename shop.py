import discord
import math

from discord.ext import commands
from connectmysql import connection, cursor
from config import smile, smile1, smile2, smile3, smile4, smile5, smile6, smile7, smile8, smile9, smile10, smile11

class shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['shop', 'store'], pass_context=True)
    async def __shop(self, ctx, *, args=None):
        if args is None:
            global i

            connection.connect()

            cursor.execute(f"SELECT name, description, cash, res1, res2, res3, res4, res5, res6, res7, res8, res9, res10, res11 FROM {ctx.author.guild.id}_shop ORDER BY id")
            reco = cursor.fetchall()

            cursor.execute(f"SELECT id FROM {ctx.author.guild.id}_shop ORDER BY id DESC")
            itemp = cursor.fetchone()[0]

            i = 1

            view1 = discord.ui.View()
            view2 = discord.ui.View()
            view3 = discord.ui.View()
            style = discord.ButtonStyle.blurple
            item1 = discord.ui.Button(style=style, label="Следующая страница")
            item2 = discord.ui.Button(style=style, label="Предыдущая страница")
            view1.add_item(item=item1)
            view2.add_item(item=item2)
            view3.add_item(item=item1)
            view3.add_item(item=item2)

            embed = discord.Embed(
                title="Terra Magna | ВПИ (Магазин)",
                description=f"Это магазин Terra Magna(лист {i})",
                color = 0x00BFFF,
            )



            for row1 in range(0,9):
                embed.add_field(name=f"{reco[row1][0]}:", value=f"""
                {smile} {reco[row1][2]} - {smile1} {reco[row1][3]} - {smile2} {reco[row1][4]} - {smile3} {reco[row1][5]} - {smile4} {reco[row1][6]} - {smile5} {reco[row1][7]} - {smile6} {reco[row1][8]} - {smile7} {reco[row1][9]} - {smile8} {reco[row1][10]} - {smile9} {reco[row1][11]} - {smile10} {reco[row1][12]} - {smile11} {reco[row1][13]}  
                Описание: {reco[row1][1]}""", inline=True)
            await ctx.send(embed=embed, view=view1)


            async def button_callback1(interaction):
                global i
                i = i + 1
                embed = discord.Embed(
                    title="Terra Magna | ВПИ (Магазин)",
                    description=f"Это магазин Terra Magna(лист {i})",
                    color = 0x00BFFF,
                )

                if itemp-i*9 >= 0:
                    for x in range(1, 9):
                        embed.remove_field(index=0)

                    for row1 in range(i*9-9, i*9):
                        embed.add_field(name=f"{reco[row1][0]}:", value=f"""
                    {smile} {reco[row1][2]} - {smile1} {reco[row1][3]} - {smile2} {reco[row1][4]} - {smile3} {reco[row1][5]} - {smile4} {reco[row1][6]} - {smile5} {reco[row1][7]} - {smile6} {reco[row1][8]} - {smile7} {reco[row1][9]} - {smile8} {reco[row1][10]} - {smile9} {reco[row1][11]} - {smile10} {reco[row1][12]} - {smile11} {reco[row1][13]}  
                    Описание: {reco[row1][1]}""", inline=True)
                else:
                    for x in range(1, 9):
                        embed.remove_field(index=0)

                    for row1 in range(i*9-9, itemp):
                        embed.add_field(name=f"{reco[row1][0]}:", value=f"""
                    {smile} {reco[row1][2]} - {smile1} {reco[row1][3]} - {smile2} {reco[row1][4]} - {smile3} {reco[row1][5]} - {smile4} {reco[row1][6]} - {smile5} {reco[row1][7]} - {smile6} {reco[row1][8]} - {smile7} {reco[row1][9]} - {smile8} {reco[row1][10]} - {smile9} {reco[row1][11]} - {smile10} {reco[row1][12]} - {smile11} {reco[row1][13]} 
                    Описание: {reco[row1][1]}""", inline=True)




                if i+1 > math.ceil(itemp/9):
                    await interaction.response.edit_message(embed=embed, view=view2)
                else:
                    await interaction.response.edit_message(embed=embed, view=view3)



            async def button_callback2(interaction):
                global i
                i = i - 1
                embed = discord.Embed(
                    title="Terra Magna | ВПИ (Магазин)",
                    description=f"Это магазин Terra Magna(лист {i})",
                    color = 0x00BFFF,
                )

                if itemp-i*9 >= 9:
                    for x in range(1, 9):
                        embed.remove_field(index=0)

                    for row1 in range(i*9-9, i*9):
                        embed.add_field(name=f"{reco[row1][0]}:", value=f"""
                    {smile} {reco[row1][2]} - {smile1} {reco[row1][3]} - {smile2} {reco[row1][4]} - {smile3} {reco[row1][5]} - {smile4} {reco[row1][6]} - {smile5} {reco[row1][7]} - {smile6} {reco[row1][8]} - {smile7} {reco[row1][9]} - {smile8} {reco[row1][10]} - {smile9} {reco[row1][11]} - {smile10} {reco[row1][12]} - {smile11} {reco[row1][13]}
                    Описание: {reco[row1][1]}""", inline=True)

                else:
                    for x in range(1, itemp-i*9):
                        embed.remove_field(index=0)

                    for row1 in range(i*9-9, i*9):
                        embed.add_field(name=f"{reco[row1][0]}:", value=f"""
                    {smile} {reco[row1][2]} - {smile1} {reco[row1][3]} - {smile2} {reco[row1][4]} - {smile3} {reco[row1][5]} - {smile4} {reco[row1][6]} - {smile5} {reco[row1][7]} - {smile6} {reco[row1][8]} - {smile7} {reco[row1][9]} - {smile8} {reco[row1][10]} - {smile9} {reco[row1][11]} - {smile10} {reco[row1][12]} - {smile11} {reco[row1][13]} 
                    Описание: {reco[row1][1]}""", inline=True)


                if i == 1:
                    await interaction.response.edit_message(embed=embed, view=view1)
                else:
                    await interaction.response.edit_message(embed=embed, view=view3)

            item1.callback = button_callback1
            item2.callback = button_callback2




async def setup(bot):
    await bot.add_cog(shop(bot))