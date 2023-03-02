import asyncio
import random
import sys

import disnake
from disnake.ext import commands
from array import *
# from mafia_modal import MafiaModal


class CMDMafia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="создать", aliases=["создание"], usage="создать https://discord.gg/fQc2nS2p", brief="<ссылка на сервер>")
    async def create(self, ctx, mafia_server_url, amount=1):
        await ctx.channel.purge(limit=amount)
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
            await ctx.reply(f"Создатель должен быть в голосовом чате!")
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

            # делаем срез списка ролей с 0 по кол-во участников и перемешиваем их
            sliced_roles = roles_list[0:voice_member_count]
            random.shuffle(sliced_roles)
            print(sliced_roles)

            roll_maf = ''
            roll_don = ''
            roll_com = ''
            roll_doc = ''
            roll_man = ''
            creator_embed_description = ''
            members_embed_description = ''
            for i, member_id in enumerate(members):
                member = ctx.guild.get_member(member_id)

                member_roles = member.roles
                if ctx.guild.owner_id == member.id:
                    is_can_change_name = False
                else:
                    is_can_change_name = True

                for member_role in member_roles:
                    if member_role.id in admin_roles_list:
                        is_can_change_name = False

                if not is_can_change_name:
                    await ctx.channel.send(f"{member.mention}, поставьте себе слот **{members_numbers_dict[i]}.** перед ником")
                else:
                    await member.edit(nick=f"{members_numbers_dict[i]}. {member.name}")

                if sliced_roles[i] == 'maf':
                    roll_maf += f"{members_numbers_dict[i] }"
                    role = 'Мафия'
                    task = roles_tasks_dict['maf']
                elif sliced_roles[i] == 'don':
                    roll_don = f"{members_numbers_dict[i] }"
                    role = 'Дон мафии'
                    task = roles_tasks_dict['don']
                elif sliced_roles[i] == 'com':
                    roll_com = f"{members_numbers_dict[i] }"
                    role = 'Комиссар'
                    task = roles_tasks_dict['com']
                elif sliced_roles[i] == 'doc':
                    roll_doc = f"{members_numbers_dict[i] }"
                    role = 'Доктор'
                    task = roles_tasks_dict['doc']
                elif sliced_roles[i] == 'man':
                    roll_man = f"{members_numbers_dict[i] }"
                    role = 'Маньяк'
                    task = roles_tasks_dict['man']
                else:
                    role = 'Мирный житель'
                    task = roles_tasks_dict['mir']

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

                members_embed_description += f"{members_numbers_dict[i]}. {member.mention};\n"

            members_embed_description += f"\n**Ведущий:** {creator.mention}"

            creator_embed = disnake.Embed(
                title="Ролл",
                description=creator_embed_description,
                color=0xffffff
            )
            await creator.send(embed=creator_embed)

            members_embed = disnake.Embed(
                title="Участники игры",
                description=members_embed_description,
                color=0xffffff
            )
            await ctx.reply(embed=members_embed)

    @commands.slash_command(name='cоздать-игру')
    async def slash_create(self, ctx, mafia_server_url: str):
        await ctx.response.defer()
        # await asyncio.sleep(10)
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

            # делаем срез списка ролей с 0 по кол-во участников и перемешиваем их
            sliced_roles = roles_list[0:voice_member_count]
            random.shuffle(sliced_roles)
            print(sliced_roles)

            roll_maf = ''
            roll_don = ''
            roll_com = ''
            roll_doc = ''
            roll_man = ''
            creator_embed_description = ''
            members_embed_description = ''
            for i, member_id in enumerate(members):
                member = ctx.guild.get_member(member_id)

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

                members_embed_description += f"{members_numbers_dict[i]}. {member.mention};\n"

            members_embed_description += f"\n**Ведущий:** {creator.mention}"

            creator_embed = disnake.Embed(
                title="Ролл",
                description=creator_embed_description,
                color=0xffffff
            )
            await creator.send(embed=creator_embed)

            members_embed = disnake.Embed(
                title="Участники игры",
                description=members_embed_description,
                color=0xffffff
            )

            # await ctx.send_modal()
            await ctx.edit_original_message(embed=members_embed)

    @commands.slash_command()
    async def ping(self, inter: disnake.CommandInteraction, url):
        await inter.response.send_message('Pong!')

    @commands.slash_command()
    async def defer(self, inter: disnake.CommandInteraction):
        await inter.response.defer()
        await asyncio.sleep(10)
        await inter.edit_original_message(content="Ожидание закончилось!")

    @commands.slash_command(name='test')
    async def slash_test(self, ctx):
        await ctx.response.defer()
        await asyncio.sleep(10)
        await ctx.edit_original_message(content="Ожидание закончилось!")

    # @commands.slash_command(name='modal')
    # async def tags(self, ctx: disnake.AppCmdInter):
    #     """Sends a Modal to create a tag."""
    #     await ctx.response.send_modal(modal=MafiaModal())

def setup(bot):
    bot.add_cog(CMDMafia(bot))
