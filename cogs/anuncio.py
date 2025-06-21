import discord
from discord.ext import commands

class Anuncio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.announce_channel_id = 1385777709334003733  # Substitua pelo ID do canal de anúncios

    @commands.command(name='anunciar')
    @commands.has_permissions(administrator=True)
    async def anunciar(self, ctx, *, mensagem: str):
        channel = self.bot.get_channel(self.announce_channel_id)
        if not channel:
            await ctx.reply('❌ Canal de anúncios não encontrado. Verifique a configuração.', mention_author=False)
            return

        embed = discord.Embed(
            title="📢 Anúncio Importante",
            description=mensagem,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f'Anúncio feito por {ctx.author}', icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)

        await channel.send(embed=embed)
        await ctx.reply('✅ Anúncio enviado com sucesso!', mention_author=False)

async def setup(bot):
    await bot.add_cog(Announce(bot))
