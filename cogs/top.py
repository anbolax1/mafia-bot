import sqlite3
import random
import discord
import disnake
import calendar
import time
from disnake.ext import commands
from array import *
from discord.ui import Select, View


class CMDTop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="топ")
    async def top(self, ctx):
        select = Select(
            min_values=1,
            max_values=1,
            options=[
                disnake.SelectOption(
                    label="Мирный", value="mir"
                ),
                disnake.SelectOption(
                    label="Мафия", value="maf"
                ),
                disnake.SelectOption(
                    label="Дон", value="don"
                ),
                disnake.SelectOption(
                    label="Комиссар", value="com"
                ),
            ]
        )
        view = View()
        view.add_item(select)

        await ctx.send("Выберите роль, по которой хотите запросить топ", view=view)

        async def my_callback(interaction):
            await interaction.response.send_message(f"Ты выбрал: {view.values[0]}")


class Dropdown(disnake.ui.StringSelect):
    def __init__(self):
        # Define the options that will be presented inside the dropdown
        options = [
            disnake.SelectOption(
                label="Мирный", value="mir"
            ),
            disnake.SelectOption(
                label="Мафия", value="maf"
            ),
            disnake.SelectOption(
                label="Дон", value="don"
            ),
            disnake.SelectOption(
                label="Комиссар", value="com"
            ),
        ]

        # The placeholder is what will be shown when no option is chosen.
        # The min and max values indicate we can only pick one of the three options.
        # The options parameter defines the dropdown options, see above.
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
        )


class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        # Add the dropdown to our view object.
        self.add_item(Dropdown())


def setup(client):
    client.add_cog(CMDTop(client))
