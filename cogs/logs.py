import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1385790682635173939  # Troque pelo ID do canal de logs

    async def send_log(self, embed):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        embed = discord.Embed(
            title="🗑️ Mensagem deletada",
            description=f"Autor: {message.author} ({message.author.id})\nCanal: {message.channel.mention}\nMensagem: {message.content}",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        embed = discord.Embed(
            title="✏️ Mensagem editada",
            description=(
                f"Autor: {before.author} ({before.author.id})\nCanal: {before.channel.mention}\n\n"
                f"Antes: {before.content}\nDepois: {after.content}"
            ),
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="➡️ Membro entrou",
            description=f"{member} ({member.id}) entrou no servidor.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            title="⬅️ Membro saiu",
            description=f"{member} ({member.id}) saiu do servidor.",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(
            title="⛔ Membro banido",
            description=f"{user} ({user.id}) foi banido do servidor.",
            color=discord.Color.dark_red(),
            timestamp=discord.utils.utcnow()
        )
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = discord.Embed(
            title="✅ Membro desbanido",
            description=f"{user} ({user.id}) foi desbanido do servidor.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(
            title="🗑️ Canal deletado",
            description=f"Canal {channel.name} ({channel.id}) foi deletado.",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(
            title="📢 Canal criado",
            description=f"Canal {channel.name} ({channel.id}) foi criado.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        embed = discord.Embed(
            title="✏️ Canal editado",
            description=(
                f"Antes: {before.name}\nDepois: {after.name}\nCanal ID: {before.id}"
            ),
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )
        await self.send_log(embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
