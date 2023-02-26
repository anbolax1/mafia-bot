import disnake
from disnake.ext import commands


class CMDExceptions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)

        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды")
        elif isinstance(error, commands.UserInputError):
            await ctx.reply(embed=disnake.Embed(
                description=f"Правильное использования команды: `{ctx.prefix}{ctx.command.name}` (<ссылка на сервер)\nExample: {ctx.prefix}{ctx.command.usage}"
                ))


def setup(bot):
    bot.add_cog(CMDExceptions(bot))
