import os
import tabulate
import sqlite3
import discord
import json

from sqlite3 import Error
from tabulate import tabulate
# import keep_alive

import disnake
from disnake.ext import commands

client = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all(), test_guilds=[1046294792717475870,1001894169326915695])

CENSORED_WORDS = ["пидор","уебок","уёбок","уебок","уебан","гандон","пидр"]

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

# запуск бота
# @bot.event
# async def on_ready():
# 	print(f"Bot {bot.user} is ready to work!")


# # Выводим эмбед, когда присоединяется новый участник
# @bot.event
# async def on_member_join(member):
# 	role = disnake.utils.get(member.guild.roles, id=1079165971190775878)
# 	channel = bot.get_channel(1046294793157885996)
#
# 	embed = disnake.Embed(
# 		title="Здорова!",
# 		description=f"{member.name}#{member.discriminator}",
# 		color=0xffffff
# 		)
# 	await member.add_roles(role)
# 	await channel.send(embed=embed)
#
#
# # Обработка сообщений в текстовых каналах
# @bot.event
# async def on_message(message):
# 	await bot.process_commands(message)
#
# 	for content in message.content.split():
# 		for censcored_word in CENSORED_WORDS:
# 			if content.lower() == censcored_word or content.find(censcored_word.lower()) >= 0:
# 				await message.delete()
# 				await message.channel.send(f"{message.author.mention} такие слова запрещены!")
#
#
# # Обработка ошибок
# @bot.event
# async def on_command_error(ctx, error):
# 	print(error)
#
# 	if isinstance(error, commands.MissingPermissions):
# 		await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды")
# 	elif isinstance(error, commands.UserInputError):
# 		await ctx.send(embed=disnake.Embed(
# 			description=f"Правильное использования команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
# 			))
#
#
# # Команда !кик
# @bot.command(name="кик", aliases=["кикаю"], usage="кик <@user> <reason=None>")
# @commands.has_permissions(kick_members=True, administrator=True)
# async def kick(ctx, member: disnake.Member, *, reason="Пошёл вон!"):
# 	await ctx.send(f"Админ {ctx.author.mention} выгнал нахер пользователя {member.mention}", delete_after=3)
# 	await member.kick(reason=reason)
# 	await ctx.message.delete()
#
#
# # Калькулятор /calc
# @bot.slash_command()
# async def calc(inter, a: int, oper: str, b: int):
# 	if oper == "+":
# 		result = a + b
# 	elif oper == "*":
# 		result = a * b
#
# 	await inter.send(str(result))


@client.command()
@commands.is_owner()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
	client.reload_extension(f"cogs.{extension}")


for filename in os.listdir("cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

client.run("MTA0NjQwNzk1ODY4ODQ1MjYzOA.GiIr4w.QlwqRvGxStXw-2iXYkNaI7ysHHZVjwQNMuD-Lg")

# keep_alive.keep_alive()

# client.run(os.environ.get('TOKEN'), reconnect=True)