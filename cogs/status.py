import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.reply(f'🏓 Pong! Latência: `{latency}ms`', mention_author=False)

    @commands.command(name='status')
    async def status_bot(self, ctx):
        total_guilds = len(self.bot.guilds)
        total_users = len(set(self.bot.get_all_members()))
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="📊 Status do Bot",
            color=discord.Color.blurple()
        )
        embed.add_field(name="🔗 Latência", value=f"`{latency}ms`", inline=True)
        embed.add_field(name="🌐 Servidores", value=f"`{total_guilds}`", inline=True)
        embed.add_field(name="👥 Usuários únicos", value=f"`{total_users}`", inline=True)
        embed.set_footer(text=f"Requisição feita por {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
    await bot.add_cog(Status(bot))
