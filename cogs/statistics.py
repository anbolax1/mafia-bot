import sqlite3
import random
import disnake
import calendar
import time
from disnake.ext import commands
from array import *


class CMDStatistics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="статистика", aliases=["стата", "стат"])
    async def stats(self, ctx, user_id=''):
        await ctx.response.defer()

        conn = sqlite3.connect("bot.db")
        cursor = conn.cursor()

        if user_id == '':
            user_id = ctx.author.id

        games_created_by_user = getCreatedGameByUser(user_id)

        # общее кол-во созданных и проведённых игр
        games_created_by_user_count = len(games_created_by_user)

        kitty_games_count = 0
        city_games_count = 0
        classic_games_count = 0
        custom_games_count = 0
        nonrating_games_count = 0

        for game_created_by_user in games_created_by_user:
            if game_created_by_user[2] == 'kitty':
                kitty_games_count += 1
            elif game_created_by_user[2] == 'city':
                city_games_count += 1
            elif game_created_by_user[2] == 'classic':
                classic_games_count += 1
            elif game_created_by_user[2] == 'custom':
                custom_games_count += 1
            elif game_created_by_user[2] == 'nonrating':
                nonrating_games_count += 1

        member_statistics = f"Пользователь: <@{user_id}>" \
                            f"\n**__Ведущий__**" \
                            f"\nОбщее количество проведённых игр: {games_created_by_user_count}" \
                            f"\nКитти-мафия: {kitty_games_count}" \
                            f"\nГородская мафия: {city_games_count}" \
                            f"\nКлассическая мафия: {classic_games_count}" \
                            f"\nКастомная мафия: {custom_games_count}" \
                            f"\nБезрейтинговая мафия: {nonrating_games_count}"
        # получаем участника
        member = getMemberByDiscordId(user_id)

        if member is not None:
            # получаем все игры участника
            member_games = getMemberGames(member[0])
            member_games_count = len(member_games)  # общее кол-во сыгранных игр
            member_games_win_count = 0  # общее кол-во выигранных игр

            member_games_kitty_count = 0  # кол-во сыгранных Китти-мафий
            member_games_city_count = 0  # кол-во сыгранных городских мафий
            member_games_classic_count = 0  # кол-во сыгранных классических мафий
            member_games_custom_count = 0  # кол-во сыгранных кастомных мафий
            member_games_nonrating_count = 0 # кол-во сыгранных безрейтинговых мафий

            member_games_kitty_win_count = 0  # кол-во выигранных Китти-мафий
            member_games_city_win_count = 0  # кол-во выигранных городских мафий
            member_games_classic_win_count = 0  # кол-во выигранных классических мафий
            member_games_custom_win_count = 0  # кол-во выигранных кастомных мафий
            member_games_nonrating_win_count = 0  # кол-во выигранных безрейтинговых мафий

            member_win_mir_count = 0  # кол-во побед за мирного
            member_win_maf_count = 0  # кол-во побед за мафию
            member_win_don_count = 0  # кол-во побед за дона
            member_win_com_count = 0  # кол-во побед за комиссара
            member_win_doc_count = 0  # кол-во побед за доктора
            member_win_man_count = 0  # кол-во побед за маньяка

            member_win_percent = 0  # общее кол-во побед в процентах
            member_win_kitty_percent = 0  # кол-во побед в Китти-мафии в процентах
            member_win_city_percent = 0  # кол-во побед в городской мафии в процентах
            member_win_classic_percent = 0  # кол-во побед в классической мафии в процентах
            member_win_custom_percent = 0  # кол-во побед в кастомной мафии в процентах
            member_win_nonrating_percent = 0  # кол-во побед в безрейтинговой мафии в процентах

            member_win_mir_percent = 0  # кол-во побед за мирного в процентах
            member_win_maf_percent = 0  # кол-во побед за мафию в процентах
            member_win_don_percent = 0  # кол-во побед за дона в процентах
            member_win_com_percent = 0  # кол-во побед за комиссара в процентах
            member_win_doc_percent = 0  # кол-во побед за доктора в процентах
            member_win_man_percent = 0  # кол-во побед за маньяка в процентах

            member_was_mir = 0
            member_was_maf = 0
            member_was_don = 0
            member_was_com = 0
            member_was_doc = 0
            member_was_man = 0

            rating_kitty = member[2]
            rating_city = member[3]
            rating_classic = member[4]
            rating_custom = member[5]
            for member_game in member_games:
                game = getGameByGameId(member_game[1])

                if member_game[3] == 'mir':
                    member_was_mir += 1
                    if game[4] == 'mir':
                        member_win_mir_count += 1
                        member_games_win_count += 1
                elif member_game[3] == 'maf':
                    member_was_maf += 1
                    if game[4] == 'maf':
                        member_win_maf_count += 1
                        member_games_win_count += 1
                elif member_game[3] == 'don':
                    member_was_don += 1
                    if game[4] == 'maf':
                        member_win_don_count += 1
                        member_games_win_count += 1
                elif member_game[3] == 'com':
                    member_was_com += 1
                    if game[4] == 'mir':
                        member_win_com_count += 1
                        member_games_win_count += 1
                elif member_game[3] == 'man':
                    member_was_man += 1
                    if game[4] == 'man':
                        member_win_man_count += 1
                        member_games_win_count += 1
                elif member_game[3] == 'doc':
                    member_was_doc += 1
                    if game[4] == 'mir':
                        member_win_doc_count += 1
                        member_games_win_count += 1

                if game[2] == 'kitty':
                    member_games_kitty_count += 1
                    if game[4] == 'maf':
                        if member_game[3] == 'maf' or member_game[3] == 'don':
                            member_games_kitty_win_count += 1
                    elif game[4] == 'mir':
                        if member_game[3] == 'mir' or member_game[3] == 'doc' or member_game[3] == 'com':
                            member_games_kitty_win_count += 1
                    elif game[4] == 'man':
                        if member_game[3] == 'man':
                            member_games_kitty_win_count += 1
                elif game[2] == 'city':
                    member_games_city_count += 1
                    if game[4] == 'maf':
                        if member_game[3] == 'maf' or member_game[3] == 'don':
                            member_games_city_win_count += 1
                    elif game[4] == 'mir':
                        if member_game[3] == 'mir' or member_game[3] == 'doc' or member_game[3] == 'com':
                            member_games_city_win_count += 1
                    elif game[4] == 'man':
                        if member_game[3] == 'man':
                            member_games_city_win_count += 1
                elif game[2] == 'classic':
                    member_games_classic_count += 1
                    if game[4] == 'maf':
                        if member_game[3] == 'maf' or member_game[3] == 'don':
                            member_games_classic_win_count += 1
                    elif game[4] == 'mir':
                        if member_game[3] == 'mir' or member_game[3] == 'doc' or member_game[3] == 'com':
                            member_games_classic_win_count += 1
                    elif game[4] == 'man':
                        if member_game[3] == 'man':
                            member_games_classic_win_count += 1
                elif game[2] == 'custom':
                    member_games_custom_count += 1
                    if game[4] == 'maf':
                        if member_game[3] == 'maf' or member_game[3] == 'don':
                            member_games_custom_win_count += 1
                    elif game[4] == 'mir':
                        if member_game[3] == 'mir' or member_game[3] == 'doc' or member_game[3] == 'com':
                            member_games_custom_win_count += 1
                    elif game[4] == 'man':
                        if member_game[3] == 'man':
                            member_games_custom_win_count += 1
                elif game[2] == 'nonrating':
                    member_games_nonrating_count += 1
                    if game[4] == 'maf':
                        if member_game[3] == 'maf' or member_game[3] == 'don':
                            member_games_nonrating_win_count += 1
                    elif game[4] == 'mir':
                        if member_game[3] == 'mir' or member_game[3] == 'doc' or member_game[3] == 'com':
                            member_games_nonrating_win_count += 1
                    elif game[4] == 'man':
                        if member_game[3] == 'man':
                            member_games_nonrating_win_count += 1

            # считаем проценты побед в различных играх
            if member_games_count == 0:
                member_win_percent = 0
            else:
                member_win_percent = member_games_win_count / member_games_count * 100

            if member_games_kitty_count == 0:
                member_win_kitty_percent = 0
            else:
                member_win_kitty_percent = member_games_kitty_win_count / member_games_kitty_count * 100

            if member_games_city_count == 0:
                member_win_city_percent = 0
            else:
                member_win_city_percent = member_games_city_win_count / member_games_city_count * 100

            if member_games_classic_count == 0:
                member_win_classic_percent = 0
            else:
                member_win_classic_percent = member_games_classic_win_count / member_games_classic_count * 100

            if member_games_custom_count == 0:
                member_win_custom_percent = 0
            else:
                member_win_custom_percent = member_games_custom_win_count / member_games_custom_count * 100

            if member_games_nonrating_count == 0:
                member_win_nonrating_percent = 0
            else:
                member_win_nonrating_percent = member_games_nonrating_win_count / member_games_nonrating_count * 100

            # считаем процент побед на различных ролях
            if member_was_mir == 0:
                member_win_mir_percent = 0
            else:
                member_win_mir_percent = member_win_mir_count / member_was_mir * 100

            if member_was_maf == 0:
                member_win_maf_percent = 0
            else:
                member_win_maf_percent = member_win_maf_count / member_was_maf * 100

            if member_was_don == 0:
                member_win_don_percent = 0
            else:
                member_win_don_percent = member_win_don_count / member_was_don * 100

            if member_was_com == 0:
                member_win_com_percent = 0
            else:
                member_win_com_percent = member_win_com_count / member_was_com * 100

            if member_was_doc == 0:
                member_win_doc_percent = 0
            else:
                member_win_doc_percent = member_win_doc_count / member_was_doc * 100

            if member_was_man == 0:
                member_win_man_percent = 0
            else:
                member_win_man_percent = member_win_man_count / member_was_man * 100


            member_statistics += f"\n\n**__Участник__**" \
                                 f"\n**Рейтинг**" \
                                 f"\nКитти-мафия: {rating_kitty}" \
                                 f"\nГородская мафия: {rating_city}" \
                                 f"\nКлассическая мафия: {rating_classic}" \
                                 f"\nКастомная: {rating_custom}" \
                                 f"\n" \
                                 f"\nОбщее количество сыгранных игр: {member_games_count}, побед: {member_games_win_count} ({member_win_percent}%)" \
                                 f"\nКитти: {member_games_kitty_count}, побед: {member_games_kitty_win_count} ({member_win_kitty_percent}%)" \
                                 f"\nГородская: {member_games_city_count}, побед: {member_games_city_win_count} ({member_win_city_percent}%)" \
                                 f"\nКлассическая: {member_games_classic_count}, побед: {member_games_classic_win_count} ({member_win_classic_percent}%)" \
                                 f"\nКастомная: {member_games_custom_count}, побед: {member_games_custom_win_count} ({member_win_custom_percent}%)" \
                                 f"\nБезрейтинговая: {member_games_nonrating_count}, побед: {member_games_nonrating_win_count} ({member_win_nonrating_percent}%)" \
                                 f"\n" \
                                 f"\nБыл мирным {member_was_mir} раз(а), побед: {member_win_mir_count} ({member_win_mir_percent}%)" \
                                 f"\nБыл комиссаром {member_was_com} раз(а), побед: {member_win_com_count} ({member_win_com_percent}%)" \
                                 f"\nБыл доктор ом {member_was_doc} раз(а), побед: {member_win_doc_count} ({member_win_doc_percent}%)" \
                                 f"\nБыл доном {member_was_don} раз(а), побед: {member_win_don_count} ({member_win_don_percent}%)" \
                                 f"\nБыл мафией {member_was_maf} раз(а), побед: {member_win_maf_count} ({member_win_maf_percent}%)" \
                                 f"\nБыл маньяком {member_was_man} раз(а), побед: {member_win_man_count} ({member_win_man_percent}%)" \

        member_statistics_embed = disnake.Embed(
            title=f"Статистика",
            description=member_statistics,
            color=0xffffff
        )

        await ctx.edit_original_message(embed=member_statistics_embed)


# Статистика будет выглядеть так:
#
# Ведущий:
# Общее количество проведённых игр: n
# Китти: n
# Город: n
# Классика: n
# Кастом: n
# Безрейтинговая: n
#
#
# Участник:
# Рейтинг:
# Китти:
# Город:
# Классика:
# Кастом:

# Общее количество сыгранных игр: n
# Китти: n, побед: m (k %)
# Город: n, побед: m (k %)
# Классика: n, побед: m (k %)
# Кастом: n, побед: m (k %)
# Безрейтинговая: n, побед: m (k %)

# Был мирным n раз, побед m (k %)
# Был мафией n раз, побед m (k %)
# Был доном n раз, побед m (k %)
# Был комиссаром n раз, побед m (k %)
# Был доктором n раз, побед m (k %)
# Был маньяком n раз, побед m (k %)


def getCreatedGameByUser(user_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    return cursor.execute(f"SELECT * FROM games WHERE creator_id = '{user_id}' AND status = 'finished'").fetchall()


def getMemberByDiscordId(user_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    return cursor.execute(f"SELECT * FROM members WHERE discord_id = '{user_id}'").fetchone()


def getMemberGames(member_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    return cursor.execute(f"SELECT * FROM game_members LEFT JOIN games ON game_members.game_id = games.id WHERE member_id = {member_id} AND games.status ='finished'").fetchall()


def getGameByGameId(game_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    return cursor.execute(f"SELECT * FROM games WHERE id = {game_id}").fetchone()


def setup(client):
    client.add_cog(CMDStatistics(client))
