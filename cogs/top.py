import sqlite3
import random
import discord
import disnake
import calendar
import time
from disnake.ext import commands
from array import *
from discord.ui import Select, View
from operator import itemgetter


class TopButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(label='Сыгранные игры', style=disnake.ButtonStyle.green)
    async def top_games(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали Китти мафию')
        self.value = 'top_games'
        self.stop()

    @disnake.ui.button(label='Проведённые игры\n', style=disnake.ButtonStyle.green)
    async def top_games_finished(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали Китти мафию')
        self.value = 'top_games_finished'
        self.stop()

    @disnake.ui.button(label='Победы', style=disnake.ButtonStyle.green, emoji="🎉")
    async def top_wins(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали Китти мафию')
        self.value = 'top_wins'
        self.stop()

    @disnake.ui.button(label='Поражения', style=disnake.ButtonStyle.green, emoji="🧨")
    async def top_defeat(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали Китти мафию')
        self.value = 'top_defeat'
        self.stop()

    @disnake.ui.button(label='Процент побед', style=disnake.ButtonStyle.green)
    async def top_wins_percent(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали Китти мафию')
        self.value = 'top_wins_percent'
        self.stop()

    @disnake.ui.button(label='Процент поражений', style=disnake.ButtonStyle.green)
    async def top_defeat_percent(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали Китти мафию')
        self.value = 'top_defeat_percent'
        self.stop()


class GetTopCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="топ")
    async def top(self, ctx, user_discord_id=''):
        await ctx.response.defer()

        view = TopButtons()

        await ctx.send(view=view)
        await view.wait()

        # удаляем команду после выбора игры
        await ctx.channel.purge(limit=1)

        if user_discord_id == '':
            user_discord_id = ctx.author.id

        if view.value == 'top_games':
            embed = getTopGames(user_discord_id)
        elif view.value == 'top_games_finished':
            embed = getTopGamesFinished(user_discord_id)
        elif view.value == 'top_wins':
            embed = getTopWins(user_discord_id)
        elif view.value == 'top_defeat':
            embed = getTopDefeat(user_discord_id)
        elif view.value == 'top_wins_percent':
            embed = getTopWinsPercent(user_discord_id)
        elif view.value == 'top_defeat_percent':
            embed = getTopDefeatPercent(user_discord_id)
        else:
            embed = disnake.Embed(
                title='Не судьба',
                description='Я же сказал, кнопка в разработке, значит не работает',
                color=0xffffff
            )

        await ctx.send(embed=embed)


def getTopGames(user_discord_id):
    top_games = getTopGamesInDb()

    title = '**Топ по сыгранным играм**'
    result = ''
    i = 1
    for top_games_row in top_games:
        if i < 11:
            result += f"{i}. <@{top_games_row[1]}>, сыгранных игр: **{top_games_row[5]}**;\n"
        if str(top_games_row[1]) == str(user_discord_id) and i > 10:
            result += f"...\n{i}. <@{top_games_row[1]}>, сыгранных игр: **{top_games_row[5]}**;\n"

        i += 1

    top_embed = disnake.Embed(
        title=title,
        description=result,
        color=0xffffff
    )

    return top_embed


def getTopGamesInDb():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    top_games = cursor.execute(
        f"select members.id, members.discord_id, game_id, games.win_status, game_members.member_role, COUNT(*) as games_count from members  LEFT JOIN game_members ON members.id = game_members.member_id  LEFT JOIN games ON game_members.game_id = games.id where 1=1 and games.status = 'finished'GROUP by members.discord_id ORDER by games_count DESC").fetchall()
    return top_games


def getTopGamesFinished(user_discord_id):
    games = getTopGamesFinishedInDb()

    title = '**Топ по проведённым играм**'
    result = ''
    i = 1
    for game_row in games:
        if i < 11:
            result += f"{i}. <@{game_row[0]}>, проведённых игр: **{game_row[1]}**;\n"
        if str(game_row[0]) == str(user_discord_id) and i > 10:
            result += f"...\n{i}. <@{game_row[0]}>, проведённых игр: **{game_row[1]}**;\n"

        i += 1

    top_embed = disnake.Embed(
        title=title,
        description=result,
        color=0xffffff
    )

    return top_embed


def getTopGamesFinishedInDb():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    top_games_finished = cursor.execute(
        f"SELECT creator_id, COUNT(*) as games_count FROM games where status = 'finished' GROUP by creator_id ORDER by games_count DESC").fetchall()
    return top_games_finished


def getTopWins(user_discord_id):
    title = '**Топ по победам**'
    result = ''

    game_members = getGameMembers()
    members = getMembers()

    top_wins = {}
    for member in members:
        top_wins[member[1]] = 0
        for game_member in game_members:
            if member[0] == game_member[0]:
                if game_member[3] == 'maf':
                    if game_member[1] == 'maf' or game_member[1] == 'don':
                        top_wins[member[1]] += 1
                elif game_member[3] == 'mir':
                    if game_member[1] == 'mir' or game_member[1] == 'com' or game_member[1] == 'doc':
                        top_wins[member[1]] += 1
                elif game_member[3] == 'man' and game_member[1] == 'man':
                    top_wins[member[1]] += 1

    sorted_top_wins = {}
    sorted_top_wins_keys = sorted(top_wins.items(), key=lambda item: item[1], reverse=True)
    sorted_top_wins = {k: v for k, v in sorted_top_wins_keys}

    i = 1
    for member_discord_id in sorted_top_wins:
        if i < 11:
            result += f"{i}. <@{member_discord_id}>, выигранных игр: **{top_wins[member_discord_id]}**\n"
        if str(member_discord_id) == str(user_discord_id) and i > 10:
            result += f"...\n{i}. <@{member_discord_id}>, выигранных игр: **{top_wins[member_discord_id]}**;\n"

        i += 1

    top_embed = disnake.Embed(
        title=title,
        description=result,
        color=0xffffff
    )

    return top_embed


def getGameMembers():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    game_members = cursor.execute(
        f"select game_members.member_id, game_members.member_role, games.id as game_id, games.win_status, members.discord_id from game_members LEFT JOIN games ON game_members.game_id = games.id LEFT JOIN members ON game_members.member_id = members.id WHERE games.status = 'finished'").fetchall()
    return game_members


def getMembers():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    members = cursor.execute(f"select * from members").fetchall()
    return members


def getTopDefeat(user_discord_id):
    title = '**Топ по поражениям**'
    result = ''

    game_members = getGameMembers()
    members = getMembers()

    top_defeat = {}
    for member in members:
        top_defeat[member[1]] = 0
        for game_member in game_members:
            if member[0] == game_member[0]:
                if game_member[3] == 'maf':
                    if game_member[1] != 'maf' and game_member[1] != 'don':
                        top_defeat[member[1]] += 1
                elif game_member[3] == 'mir':
                    if game_member[1] != 'mir' and game_member[1] != 'com' and game_member[1] != 'doc':
                        top_defeat[member[1]] += 1
                elif game_member[3] == 'man' and game_member[1] != 'man':
                    top_defeat[member[1]] += 1

    sorted_top_defeat = {}
    sorted_top_wins_keys = sorted(top_defeat.items(), key=lambda item: item[1], reverse=True)
    sorted_top_defeat = {k: v for k, v in sorted_top_wins_keys}

    i = 1
    for member_discord_id in sorted_top_defeat:
        if i < 11:
            result += f"{i}. <@{member_discord_id}>, проигранных игр: **{top_defeat[member_discord_id]}**;\n"
        if str(member_discord_id) == str(user_discord_id) and i > 10:
            result += f"...\n{i}. <@{member_discord_id}>, проигранных игр: **{top_defeat[member_discord_id]}**;\n"

        i += 1

    top_embed = disnake.Embed(
        title=title,
        description=result,
        color=0xffffff
    )

    return top_embed


def getTopWinsPercent(user_discord_id):
    title = '**Топ по победам в процентах**\n*(для игроков, у которых 5 и более сыгранных игр)*'
    result = ''

    game_members = getGameMembers()
    members = getMembers()

    top_wins = {}
    top_defeat = {}
    member_games_count = {}
    for member in members:
        top_wins[member[1]] = 0
        top_defeat[member[1]] = 0
        member_games_count[member[1]] = 0
        for game_member in game_members:
            if member[0] == game_member[0]:
                member_games_count[member[1]] += 1
                if game_member[3] == 'maf':
                    if game_member[1] == 'maf' or game_member[1] == 'don':
                        top_wins[member[1]] += 1
                    else:
                        top_defeat[member[1]] += 1
                elif game_member[3] == 'mir':
                    if game_member[1] == 'mir' or game_member[1] == 'com' or game_member[1] == 'doc':
                        top_wins[member[1]] += 1
                    else:
                        top_defeat[member[1]] += 1
                elif game_member[3] == 'man':
                    if game_member[1] == 'man':
                        top_wins[member[1]] += 1
                    else:
                        top_defeat[member[1]] += 1

    top_wins_percent = {}
    for member_discord_id in top_wins:
        if member_games_count[member_discord_id] > 4:
            if top_wins[member_discord_id] < 1 or member_games_count[member_discord_id] < 1:
                top_wins_percent[member_discord_id] = 0
            else:
                top_wins_percent[member_discord_id] = round(
                    top_wins[member_discord_id] / member_games_count[member_discord_id] * 100, 2)

    sorted_top_wins_percent = {}
    sorted_top_wins_percent_keys = sorted(top_wins_percent.items(), key=lambda item: item[1], reverse=True)
    sorted_top_wins_percent = {k: v for k, v in sorted_top_wins_percent_keys}

    i = 1
    for member_discord_id in sorted_top_wins_percent:
        if i < 11:
            result += f"{i}. <@{member_discord_id}>, выигранных игр в процентах: **{sorted_top_wins_percent[member_discord_id]} %**;\n"
        if str(member_discord_id) == str(user_discord_id) and i > 10:
            result += f"...\n{i}. <@{member_discord_id}>, выигранных игр в процентах: **{sorted_top_wins_percent[member_discord_id]} %**;\n"

        i += 1

    top_embed = disnake.Embed(
        title=title,
        description=result,
        color=0xffffff
    )

    return top_embed

def getTopDefeatPercent(user_discord_id):
    title = '**Топ по поражениям в процентах**\n*(для игроков, у которых 5 и более сыгранных игр)*'
    result = ''

    game_members = getGameMembers()
    members = getMembers()

    top_wins = {}
    top_defeat = {}
    member_games_count = {}
    for member in members:
        top_wins[member[1]] = 0
        top_defeat[member[1]] = 0
        member_games_count[member[1]] = 0
        for game_member in game_members:
            if member[0] == game_member[0]:
                member_games_count[member[1]] += 1
                if game_member[3] == 'maf':
                    if game_member[1] == 'maf' or game_member[1] == 'don':
                        top_wins[member[1]] += 1
                    else:
                        top_defeat[member[1]] += 1
                elif game_member[3] == 'mir':
                    if game_member[1] == 'mir' or game_member[1] == 'com' or game_member[1] == 'doc':
                        top_wins[member[1]] += 1
                    else:
                        top_defeat[member[1]] += 1
                elif game_member[3] == 'man':
                    if game_member[1] == 'man':
                        top_wins[member[1]] += 1
                    else:
                        top_defeat[member[1]] += 1

    top_wins_percent = {}
    for member_discord_id in top_wins:
        if member_games_count[member_discord_id] > 4:
            if top_wins[member_discord_id] < 1 or member_games_count[member_discord_id] < 1:
                top_wins_percent[member_discord_id] = 0
            else:
                top_wins_percent[member_discord_id] = round(
                    top_defeat[member_discord_id] / member_games_count[member_discord_id] * 100, 2)

    sorted_top_wins_percent = {}
    sorted_top_wins_percent_keys = sorted(top_wins_percent.items(), key=lambda item: item[1], reverse=True)
    sorted_top_wins_percent = {k: v for k, v in sorted_top_wins_percent_keys}

    i = 1
    for member_discord_id in sorted_top_wins_percent:
        if i < 11:
            result += f"{i}. <@{member_discord_id}>, проигранных игр в процентах: **{sorted_top_wins_percent[member_discord_id]} %**;\n"
        if str(member_discord_id) == str(user_discord_id) and i > 10:
            result += f"...\n{i}. <@{member_discord_id}>, проигранных игр в процентах: **{sorted_top_wins_percent[member_discord_id]} %**;\n"

        i += 1

    top_embed = disnake.Embed(
        title=title,
        description=result,
        color=0xffffff
    )

    return top_embed


# class Dropdown(disnake.ui.StringSelect):
#     def __init__(self):
#         # Define the options that will be presented inside the dropdown
#         options = [
#             disnake.SelectOption(
#                 label="Мирный", value="mir"
#             ),
#             disnake.SelectOption(
#                 label="Мафия", value="maf"
#             ),
#             disnake.SelectOption(
#                 label="Дон", value="don"
#             ),
#             disnake.SelectOption(
#                 label="Комиссар", value="com"
#             ),
#         ]
#
#         # The placeholder is what will be shown when no option is chosen.
#         # The min and max values indicate we can only pick one of the three options.
#         # The options parameter defines the dropdown options, see above.
#         super().__init__(
#             min_values=1,
#             max_values=1,
#             options=options,
#         )


# class DropdownView(disnake.ui.View):
#     def __init__(self):
#         super().__init__()
#
#         # Add the dropdown to our view object.
#         self.add_item(Dropdown())


def setup(client):
    client.add_cog(GetTopCog(client))
