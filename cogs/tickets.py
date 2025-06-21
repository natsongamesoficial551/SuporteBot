import discord
from discord.ext import commands
import asyncio

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_category_id = 1385778561549602867  # ✅ Substitua pelo ID da categoria onde os tickets serão criados
        self.admin_role_id = 1385783190852997170      # ✅ Substitua pelo ID do cargo de Administrador

    @commands.command(name='ticket')
    async def abrir_ticket(self, ctx, *, motivo="Sem motivo especificado"):
        guild = ctx.guild
        author = ctx.author

        # Verificar se o usuário já tem um ticket aberto
        existing_channel = discord.utils.get(guild.channels, name=f'ticket-{author.name.lower()}')
        if existing_channel:
            await ctx.reply(f'❌ Você já tem um ticket aberto: {existing_channel.mention}')
            return

        category = guild.get_channel(self.ticket_category_id)
        if category is None:
            await ctx.reply('❌ Categoria de tickets não encontrada. Avise um administrador.')
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.get_role(self.admin_role_id): discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        }

        ticket_channel = await guild.create_text_channel(
            name=f'ticket-{author.name}',
            category=category,
            overwrites=overwrites,
            topic=f'Ticket aberto por {author} | Motivo: {motivo}'
        )

        await ticket_channel.send(
            f'🎫 | Olá {author.mention}, seu ticket foi criado com sucesso!\n'
            f'📌 **Motivo:** {motivo}\n\n'
            f'👤 Nossa equipe irá te atender em breve.\n'
            f'❗ Apenas um administrador pode fechar este ticket.'
        )

        await ctx.reply(f'✅ Seu ticket foi criado: {ticket_channel.mention}', mention_author=False)

    @commands.command(name='fecharticket')
    @commands.has_permissions(administrator=True)
    async def fechar_ticket(self, ctx):
        if ctx.channel.name.startswith('ticket-'):
            await ctx.send('✅ Este ticket será fechado em 5 segundos...')
            await asyncio.sleep(5)
            await ctx.channel.delete()
        else:
            await ctx.reply('❌ Este comando só pode ser usado dentro de um canal de ticket.')

async def setup(bot):
    await bot.add_cog(Tickets(bot))
