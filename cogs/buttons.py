import sqlite3
import random
import disnake
import calendar
import time
from disnake.ext import commands
from array import *


class CreateGameButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(label='Китти', style=disnake.ButtonStyle.green, emoji="😁")
    async def kitty(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали Китти мафию')
        self.value = 'kitty'
        self.stop()

    @disnake.ui.button(label='Город', style=disnake.ButtonStyle.green, emoji="🙌")
    async def city(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали городскую мафию')
        self.value = 'city'
        self.stop()

    @disnake.ui.button(label='Классика', style=disnake.ButtonStyle.green, emoji="😎")
    async def classic(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали городскую мафию')
        self.value = 'classic'
        self.stop()

    @disnake.ui.button(label='Кастом', style=disnake.ButtonStyle.green, emoji="🤔")
    async def custom(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали городскую мафию')
        self.value = 'custom'
        self.stop()


def addGameToDb(creator_id, game_type, time_stamp, status='created'):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    # если существуеют незавершенные игры от ведущего (status=created), удаляем эти игры и всех участников этих игр из базы
    current_game_ids = cursor.execute(
        f"SELECT id FROM games WHERE creator_id = '{creator_id}' and status = 'created'").fetchall()

    if current_game_ids is not None:
        for current_game_id in current_game_ids:
            cursor.execute(f"DELETE FROM games WHERE id = {current_game_id[0]}")
            cursor.execute(f"DELETE FROM game_members WHERE game_id = {current_game_id[0]}")

    # Заносим в таблицу данные по игре
    cursor.execute(
        f"INSERT INTO games (creator_id, type, status, win_status, started_at, finished_at) VALUES ('{creator_id}', '{game_type}', '{status}', '', '{time_stamp}', '')")
    conn.commit()

    game_id = cursor.execute(f"SELECT id FROM games WHERE creator_id = {creator_id} and status = 'created'").fetchone()[0]
    return game_id


class CreateGameCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="создать-тест")
    async def createNewGame(self, ctx, mafia_server_url):
        await ctx.response.defer()

        current_gmt = time.gmtime()
        time_stamp = calendar.timegm(current_gmt)

        view = CreateGameButtons()

        await ctx.send(view=view)
        await view.wait()

        # удаляем команду после выбора игры
        await ctx.channel.purge(limit=1)

        creator_id = ctx.author.id

        # если чел не бродкастер (id = 1003680754959650856), игра будет с типом non-rating,
        creator = ctx.guild.get_member(creator_id)
        creator_roles = creator.roles
        is_broadcaster = False
        for creator_role in creator_roles:
            if creator_role.id == 1003680754959650856:
                is_broadcaster = True

        game_id = 0
        members_limit = 0
        roles_list = None
        if is_broadcaster is not True:
            game_id = addGameToDb(creator_id, 'non-rating', time_stamp, 'created')
            members_limit = 20
        elif view.value == 'kitty':
            game_id = addGameToDb(creator_id, view.value, time_stamp, 'created')
            members_limit = 20
            # await ctx.send("Создаём Китти-мафию!")
        elif view.value == 'city':
            game_id = addGameToDb(creator_id, view.value, time_stamp, 'created')
            members_limit = 10
            # await ctx.send("Создаём городскую мафию!")
        elif view.value == 'classic':
            game_id = addGameToDb(creator_id, view.value, time_stamp, 'created')
            members_limit = 10
            # await ctx.send("Создаём классическую мафию!")
        else:
            game_id = addGameToDb(creator_id, view.value, time_stamp, 'created')
            members_limit = 20
            # await ctx.send("Создаём кастомную мафию!")

        await set_game_roll(ctx, game_id, members_limit, mafia_server_url, roles_list)


class FinishGameButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(label='Победа мирных', style=disnake.ButtonStyle.green, emoji="❤")
    async def kitty(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали Китти мафию')
        self.value = 'mir'
        self.stop()

    @disnake.ui.button(label='Победа мафии', style=disnake.ButtonStyle.green, emoji="🖤")
    async def city(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        # await inter.response.send_message('Вы создали городскую мафию')
        self.value = 'maf'
        self.stop()


class FinishGameCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="завершить")
    async def finishGame(self, ctx):
        await ctx.response.defer()

        roles_descriptions = {
            'don': 'Дон',
            'maf': 'Мафия',
            'mir': 'Мирный',
            'com': 'Комиссар',
            'doc': 'Доктор',
            'man': 'Маньяк',
        }

        game_type_descriptions = {
            'kitty': 'Китти-мафия',
            'city': 'Городская мафия',
            'classic': 'Классическая мафия',
            'custom': 'Кастомная мафия',
        }

        current_gmt = time.gmtime()
        finished_at = calendar.timegm(current_gmt)

        view = FinishGameButtons()

        await ctx.send(view=view)
        await view.wait()

        # удаляем команду после нажатия кнопки
        await ctx.channel.purge(limit=1)

        creator_id = ctx.author.id

        # обновляем статус игры
        game = updateGameFinishStatus(creator_id, view.value, finished_at)

        if game == 'game_not_exists':
            await ctx.send("Не найдено запущенной игры!")
        else:
            avg_rating = getAvgRating(game[2])
            game_members = getGameMembers(game[0])

            start_points = 5
            delta_points = 1.5

            result_members = ''
            # если рейтинг участника выше среднего, то за победу ему начислится 5 поинтов, если меньше среднего, то 5*1.5
            # если рейтинг участника выше среднего, то за поражение у него отнимется 5*1.5 поинтов; если ниже среднего, то 5
            for game_member in game_members:
                lose_delta = 0
                win_delta = 0

                game_member_role = game_member[3]
                game_member_slot = game_member[4]
                member_rating = getMemberRatingById(game_member[2], game[2])

                member_discord_id = getMemberDiscordId(game_member[2])
                member = ctx.guild.get_member(member_discord_id)

                if float(member_rating) >= float(avg_rating):
                    if game_member[3] == view.value:
                        win_delta = start_points
                    elif game_member[3] == 'maf' and view.value == 'maf':
                        win_delta = start_points
                    elif game_member[3] == 'don' and view.value == 'maf':
                        win_delta = start_points
                    elif game_member[3] == 'com' and view.value == 'mir':
                        win_delta = start_points
                    # elif game_member[3] == 'man' and view.value == 'man':
                    #     win_delta = start_points
                    elif game_member[3] == 'doc' and view.value == 'mir':
                        win_delta = start_points
                    else:
                        lose_delta = start_points * delta_points
                else:
                    if game_member[3] == view.value:
                        win_delta = start_points * delta_points
                    elif game_member[3] == 'maf' and view.value == 'maf':
                        win_delta = start_points * delta_points
                    elif game_member[3] == 'don' and view.value == 'maf':
                        win_delta = start_points * delta_points
                    elif game_member[3] == 'com' and view.value == 'mir':
                        win_delta = start_points * delta_points
                    # elif game_member[3] == 'man' and view.value == 'man':
                    #     win_delta = start_points * delta_points
                    elif game_member[3] == 'doc' and view.value == 'mir':
                        win_delta = start_points * delta_points
                    else:
                        lose_delta = start_points

                if win_delta > 0:
                    new_member_rating = float(member_rating) + win_delta

                    updateMemberRating(game_member[2], new_member_rating, game[2])
                    result_members += f"{game_member_slot}. <@{member_discord_id}>, роль: **{roles_descriptions[game_member[3]]}**, рейтинг: **{new_member_rating} (+{win_delta})**\n"
                else:
                    new_member_rating = float(member_rating) - lose_delta

                    updateMemberRating(game_member[2], new_member_rating, game[2])
                    result_members += f"{game_member_slot}. <@{member_discord_id}>, роль: **{roles_descriptions[game_member[3]]}**, рейтинг: **{new_member_rating} (-{lose_delta})**\n"

            win_description = ''
            if view.value == 'mir':
                win_description = '**Победа мирных!**'
            elif view.value == 'maf':
                win_description = '**Победа мафии!**'
            elif view.value == 'man':
                win_description = '**Победа маньяка!**'

            game_duration_in_sec = finished_at - int(game[5])

            sec = game_duration_in_sec % (24 * 3600)
            hour = sec // 3600
            sec %= 3600
            min = sec // 60
            sec %= 60

            game_duration = f"%02d ч. %02d м. %02d с." % (hour, min, sec)

            embed_description = f"{win_description}\n\n{result_members}\n\nПродолжительность игры: *{game_duration}*"
            embed = disnake.Embed(
                title=f"Результат игры, {game_type_descriptions[game[2]]}",
                description=embed_description,
                color=0xffffff
            )

            await ctx.send(embed=embed)


def updateGameFinishStatus(creator_id, win_status, finished_at):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    game = cursor.execute(f"SELECT * FROM games WHERE creator_id = '{creator_id}' and status = 'created'").fetchone()
    print(game)
    print(type(game))
    if game is not None:
        game_id = game[0]
        cursor.execute(
            f"UPDATE games SET status = 'finished', win_status = '{win_status}', finished_at = '{finished_at}' WHERE id = {game_id}")
        conn.commit()
        return game
    else:
        print("НОНТАЙП!!!!!!!!!!!!!!!!!!!")
        return 'game_not_exists'


async def set_game_roll(ctx, game_id, members_limit, mafia_server_url, roles_list=None):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    if roles_list is None:
        roles_list = [
            'mir',
            'don',
            'mir',
            'mir',
            'mir',
            'mir',
            'maf',
            'com',
            'mir',
            'maf',
            'doc',
            'maf',
            'mir',
            'man',
            'mir',
            'mir',
            'mir',
            'mir',
            'mir',
            'mir',
            'mir',
        ]

    roles_tasks_dict = {
        'don': 'Убивать мирных жителей вместе со своей мафией и искать ночью комиссара, написав в лс ведущему *Я дон чек <номер игрока>*',
        'maf': 'Убивать мирных жителей и не выдать себя',
        'com': 'Искать ночью мафию, написав в лс ведущему `Я ком чек <номер игрока>`',
        'doc': 'Лечить мирных жителей, чтобы их не убила мафия ночью',
        'man': 'Убивать, кого угодно. Маньяк побеждает, когда остаётся с любой ролью 1 на 1',
        'mir': 'Попытаться найти мафию и вывести её на дневном голосовании',
    }
    members_numbers_dict = {
        0: '01',
        1: '02',
        2: '03',
        3: '04',
        4: '05',
        5: '06',
        6: '07',
        7: '08',
        8: '09',
        9: '10',
        10: '11',
        11: '12',
        12: '13',
        13: '14',
        14: '15',
        15: '16',
        16: '17',
        17: '18',
        18: '19',
        19: '20',
    }

    admin_roles_list = [1003712928354152538, 1041438559577579550, 1079165971190775878]

    creator_id = ctx.author.id
    creator = ctx.guild.get_member(creator_id)

    creator_voice = creator.voice
    if creator_voice is None:
        await ctx.send(f"Создатель должен быть в голосовом чате!")
    else:
        creator_channel_id = creator_voice.channel.id
        channel = ctx.guild.get_channel(creator_channel_id)
        channel_members = channel.members

        voice_member_count = 0
        members = array('Q')
        for channel_member in channel_members:
            if channel_member.id != creator_id and channel_member.voice.self_video:
                voice_member_count += 1
                members.append(channel_member.id)

            if ctx.guild.owner_id == channel_member.id:
                is_can_change_name = False
            else:
                is_can_change_name = True

            for member_role in channel_member.roles:
                if member_role.id in admin_roles_list:
                    is_can_change_name = False

            if not is_can_change_name:
                if channel_member.id != creator_id and not channel_member.voice.self_video:
                    # new_name = "Зр. " + channel_member.name
                    # await channel_member.edit(nick=f"{new_name}")
                    await ctx.channel.send(f"{channel_member.mention}, поставьте себе слот **Зр.** перед ником")
                if channel_member.id == creator_id:
                    # new_name = "!Вед. " + channel_member.name
                    # await channel_member.edit(nick=f"{new_name}")
                    await ctx.channel.send(f"{channel_member.mention}, поставьте себе слот **!Вед.** перед ником")
            else:
                if channel_member.id != creator_id and not channel_member.voice.self_video:
                    new_name = "Зр. " + channel_member.name
                    await channel_member.edit(nick=f"{new_name}")
                    # await ctx.channel.send(f"{channel_member.mention}, поставьте себе слот *Зр.* перед ником")
                if channel_member.id == creator_id:
                    new_name = "!Вед. " + channel_member.name
                    await channel_member.edit(nick=f"{new_name}")
                    # await ctx.channel.send(f"{channel_member.mention}, поставьте себе слот *!Вед.* перед ником")

        random.shuffle(members)

        members = members[0:members_limit]

        # делаем срез списка ролей с 0 по кол-во участников и перемешиваем их
        sliced_roles = roles_list[0:len(members)]
        random.shuffle(sliced_roles)
        print(sliced_roles)

        roll_maf = ''
        roll_don = ''
        roll_com = ''
        roll_doc = ''
        roll_man = ''
        creator_embed_description = ''
        members_embed_description = '**Участники игры:**\n'

        # Получаем тип игры (Китти, город и т.д., чтобы добавить в эмбед)
        game_type = cursor.execute(f"SELECT type FROM games WHERE id = {game_id}").fetchone()[0]

        for i, member_discord_id in enumerate(members):
            # добавляем участника в общую таблицу участников
            member_id = insertMemberIntoMembersTable(member_discord_id)

            member = ctx.guild.get_member(member_discord_id)

            member_roles = member.roles
            if ctx.guild.owner_id == member.id:
                is_can_change_name = False
            else:
                is_can_change_name = True

            for member_role in member_roles:
                if member_role.id in admin_roles_list:
                    is_can_change_name = False

            if not is_can_change_name:
                await ctx.channel.send(
                    f"{member.mention}, поставьте себе слот **{members_numbers_dict[i]}.** перед ником")
            else:
                await member.edit(nick=f"{members_numbers_dict[i]}. {member.name}")

            if sliced_roles[i] == 'maf':
                roll_maf += f"{members_numbers_dict[i]} "
                role = 'Мафия'
                task = roles_tasks_dict['maf']
            elif sliced_roles[i] == 'don':
                roll_don = f"{members_numbers_dict[i]}"
                role = 'Дон мафии'
                task = roles_tasks_dict['don']
            elif sliced_roles[i] == 'com':
                roll_com = f"{members_numbers_dict[i]}"
                role = 'Комиссар'
                task = roles_tasks_dict['com']
            elif sliced_roles[i] == 'doc':
                roll_doc = f"{members_numbers_dict[i]}"
                role = 'Доктор'
                task = roles_tasks_dict['doc']
            elif sliced_roles[i] == 'man':
                roll_man = f"{members_numbers_dict[i]}"
                role = 'Маньяк'
                task = roles_tasks_dict['man']
            else:
                role = 'Мирный житель'
                task = roles_tasks_dict['mir']

            # добавляем участника в таблицу участников текущей игры
            insertMemberIntoGameMembersTable(game_id, member_id, sliced_roles[i])

            if sliced_roles[i] == 'maf':
                embed_description = f"Ваша роль: **{role}**, Ваша задача: {task}. Удачи!\nСсылка на сервер мафии: {mafia_server_url}"
            elif sliced_roles[i] == 'don':
                embed_description = f"Ваша роль: **{role}**, Ваша задача: {task}. Удачи!\nСсылка на сервер мафии: {mafia_server_url}"
            else:
                embed_description = f"Ваша роль: **{role}**, Ваша задача: {task}. Удачи!"
            embed = disnake.Embed(
                title="Ваша роль",
                description=embed_description,
                color=0xffffff
            )
            await member.send(embed=embed)

            creator_embed_description = f"Дон: {roll_don}"
            if roll_maf != '':
                creator_embed_description += f"\nМафия: {roll_maf}"
            if roll_com != '':
                creator_embed_description += f"\nКомиссар: {roll_com}"
            if roll_doc != '':
                creator_embed_description += f"\nДоктор: {roll_doc}"
            if roll_man != '':
                creator_embed_description += f"\nМаньяк: {roll_man}"

            member_rating = getMemberRating(game_type, member_discord_id)

            members_embed_description += f"{members_numbers_dict[i]}. {member.mention} (рейтинг: {member_rating});\n"

        members_embed_description += f"\n**Ведущий:** {creator.mention}"

        creator_embed = disnake.Embed(
            title="Ролл",
            description=creator_embed_description,
            color=0xffffff
        )
        await creator.send(embed=creator_embed)


        title = ''
        if game_type == 'kitty':
            title = 'Китти мафия'
        elif game_type == 'city':
            title = 'Городская мафия'
        elif game_type == 'classic':
            title = 'Классическая мафия'
        elif game_type == 'custom':
            title = 'Кастомная мафия'
        elif game_type == 'non-rating':
            title = 'Безрейтинговая мафия'

        members_embed = disnake.Embed(
            title=title,
            description=members_embed_description,
            color=0xffffff
        )

        # await ctx.send_modal()
        await ctx.send(embed=members_embed)


def insertMemberIntoMembersTable(member_discord_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    member_row = cursor.execute(f"SELECT * FROM members WHERE discord_id = '{member_discord_id}'").fetchone()

    if member_row is None:
        cursor.execute(f"INSERT INTO members (discord_id) VALUES ('{member_discord_id}')")

    member_id = cursor.execute(f"SELECT * FROM members WHERE discord_id = '{member_discord_id}'").fetchone()[0]

    conn.commit()

    return member_id


def insertMemberIntoGameMembersTable(game_id, member_id, member_role):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute(
        f"INSERT INTO game_members (game_id, member_id, member_role) VALUES ({game_id}, {member_id}, '{member_role}')")
    conn.commit()


def getMemberRating(game_type, member_discord_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    member_rating = cursor.execute(f"SELECT {game_type}_rating FROM members WHERE discord_id = '{member_discord_id}'").fetchone()[0]
    return member_rating

def getMemberRatingById(member_id, game_type):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    member_rating = cursor.execute(f"SELECT {game_type}_rating FROM members WHERE id = '{member_id}'").fetchone()[0]
    return member_rating



def getAvgRating(game_type):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    ratings = cursor.execute(f"SELECT {game_type}_rating FROM members").fetchall()

    avg_rating = 0
    ratings_sum = 0
    ratings_count = 0

    if ratings is not None:
        for rating in ratings:
            ratings_sum += float(rating[0])
            ratings_count += 1

    avg_rating = ratings_sum / ratings_count
    return avg_rating


def getGameMembers(game_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    members = cursor.execute(f"SELECT * FROM game_members WHERE game_id = {game_id}").fetchall()

    return members


def getMemberDiscordId(game_member_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    member_discord_id = cursor.execute(f"SELECT discord_id FROM members WHERE id = {game_member_id}").fetchone()[0]

    return member_discord_id


def updateMemberRating(game_member_id, new_rating, game_type):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute(f"UPDATE members SET {game_type}_rating = '{new_rating}' WHERE id = {game_member_id}")
    conn.commit()


class CMDStats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="Статистика", aliases=["стата", "стат", "статистика"])
    async def stats(self, ctx):
        await ctx.response.defer()

        conn = sqlite3.connect("bot.db")
        cursor = conn.cursor()

        user_id = ctx.author.id

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



def setup(client):
    client.add_cog(CreateGameCog(client))
    client.add_cog(FinishGameCog(client))
    client.add_cog(CMDStats(client))
