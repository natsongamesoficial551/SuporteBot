import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = 1385778592150982788  # ✅ Troque pelo ID do canal 💬-bate-papo-geral

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.welcome_channel_id)
        if channel:
            embed = discord.Embed(
                title="👋 Bem-vindo(a)!",
                description=(
                    f"Olá {member.mention}, seja muito bem-vindo(a) ao servidor de suporte oficial da nossa criação de bots para Discord!\n\n"
                    "📌 **Leia as regras em:** <#1385777821133312091>\n"
                    "❓ **FAQ:** <#1385777897213526077>\n"
                    "🚀 **Dica:** Pergunte sempre que tiver dúvidas!"
                ),
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(self.welcome_channel_id)
        if channel:
            embed = discord.Embed(
                title="😢 Membro saiu!",
                description=(
                    f"O membro **{member}** acabou de sair do servidor.\n\n"
                    "👥 Desejamos boa sorte e esperamos que volte um dia!"
                ),
                color=discord.Color.red()
            )
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
