import random

import disnake
from disnake.ext import commands
from array import *


class CMDMafia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="создание", aliases=["создать"], usage="создать <ссылка на сервер>", )
    async def create(self, ctx, mafia_server_url=''):
        roles_dict = {
            1: 'mir',
            2: 'don',
            3: 'mir',
            4: 'mir',
            5: 'mir',
            6: 'mir',
            7: 'maf',
            8: 'com',
            9: 'mir',
            10: 'maf',
            11: 'doc',
            12: 'man',
        }

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
        }

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
                elif ctx.guild.owner_id != channel_member.id and channel_member.id != creator_id:
                    new_name = "Зр. " + channel_member.name
                    await channel_member.edit(nick=f"{new_name}")
                elif ctx.guild.owner_id != channel_member.id:
                    new_name = "!Вед. " + channel_member.name
                    await channel_member.edit(nick=f"{new_name}")

            roles = []
            for role_dict_key in roles_dict:
                if role_dict_key > voice_member_count:
                    break
                else:
                    roles.append(roles_dict[role_dict_key])

            random.shuffle(members)

            roll_maf = ''
            roll_don = ''
            roll_com = ''
            roll_doc = ''
            roll_man = ''
            creator_embed_description = ''
            members_embed_description = ''
            for i, member_id in enumerate(members):
                member = ctx.guild.get_member(member_id)
                if ctx.guild.owner_id == member_id:
                    await ctx.channel.send(f"{member.mention}, поставьте себе слот {members_numbers_dict[i]}")
                else:
                    await member.edit(nick=f"{members_numbers_dict[i]}. {member.name}")

                if roles_dict[i + 1] == 'maf':
                    roll_maf += f"{members_numbers_dict[i] }"
                    role = 'Мафия'
                    task = roles_tasks_dict['maf']
                elif roles_dict[i + 1] == 'don':
                    roll_don = f"{members_numbers_dict[i] }"
                    role = 'Дон мафии'
                    task = roles_tasks_dict['don']
                elif roles_dict[i + 1] == 'com':
                    roll_com = f"{members_numbers_dict[i] }"
                    role = 'Комиссар'
                    task = roles_tasks_dict['com']
                elif roles_dict[i + 1] == 'doc':
                    roll_doc = f"{members_numbers_dict[i] }"
                    role = 'Доктор'
                    task = roles_tasks_dict['doc']
                elif roles_dict[i + 1] == 'man':
                    roll_man = f"{members_numbers_dict[i] }"
                    role = 'Маньяк'
                    task = roles_tasks_dict['man']
                else:
                    role = 'Мирный житель'
                    task = roles_tasks_dict['mir']

                if roles_dict[i + 1] == 'maf':
                    embed_description = f"Ваша роль: **{role}**, Ваша задача: {task}. Удачи!\nСсылка на сервер мафии: {mafia_server_url}"
                elif roles_dict[i + 1] == 'don':
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


def setup(bot):
    bot.add_cog(CMDMafia(bot))
