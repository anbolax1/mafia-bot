import disnake
from disnake.ext import commands


class CMDUsers(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready to work!")

    # Выводим эмбед, когда присоединяется новый участник
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = disnake.utils.get(member.guild.roles, id=1079165971190775878)
        channel = self.bot.get_channel(1046294793157885996)

        embed = disnake.Embed(
            title="Здорова!",
            description=f"{member.name}#{member.discriminator}",
            color=0xffffff
        )
        await member.add_roles(role)
        await channel.send(embed=embed)

    @commands.command()
    async def profile(self, ctx):
        await ctx.reply("Привет! ты используешь COGS!")

    @commands.command()
    async def clear(self, ctx, amount=20):
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(CMDUsers(bot))
