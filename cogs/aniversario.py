import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime

ANIVERSARIOS_FILE = 'aniversarios.json'

class Aniversario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aniversarios = {}
        self.aniversarios_avisados_hoje = set()
        self.load_aniversarios()
        self.check_aniversario.start()

    def load_aniversarios(self):
        if os.path.exists(ANIVERSARIOS_FILE):
            with open(ANIVERSARIOS_FILE, 'r') as f:
                self.aniversarios = json.load(f)
        else:
            self.aniversarios = {}

    def save_aniversarios(self):
        with open(ANIVERSARIOS_FILE, 'w') as f:
            json.dump(self.aniversarios, f, indent=4)

    @commands.command(name='setaniversario')
    async def set_aniversario(self, ctx, data: str):
        """Salva seu aniversário no formato DD-MM (ex: 21-06)."""
        try:
            datetime.strptime(data, '%d-%m')
        except ValueError:
            await ctx.reply("❌ Formato inválido. Use DD-MM, ex: 21-06", mention_author=False)
            return
        self.aniversarios[str(ctx.author.id)] = data
        self.save_aniversarios()
        await ctx.reply(f"🎂 Seu aniversário foi salvo como {data}.", mention_author=False)

    @commands.command(name='veraniversario')
    async def ver_aniversario(self, ctx, member: discord.Member = None):
        """Mostra a data de aniversário do usuário mencionado ou do autor."""
        member = member or ctx.author
        data = self.aniversarios.get(str(member.id))
        if data:
            await ctx.reply(f"🎉 O aniversário de {member.display_name} é em {data}.", mention_author=False)
        else:
            await ctx.reply(f"🤔 Não encontrei o aniversário de {member.display_name}.", mention_author=False)

    @tasks.loop(minutes=60)
    async def check_aniversario(self):
        today = datetime.utcnow().strftime('%d-%m')

        # Resetar lista de avisados ao mudar o dia UTC
        if not hasattr(self, 'ultimo_dia'):
            self.ultimo_dia = today
        elif today != self.ultimo_dia:
            self.aniversarios_avisados_hoje.clear()
            self.ultimo_dia = today

        for user_id, data in self.aniversarios.items():
            if data == today and user_id not in self.aniversarios_avisados_hoje:
                user = self.bot.get_user(int(user_id))
                if not user:
                    continue
                self.aniversarios_avisados_hoje.add(user_id)

                for guild in self.bot.guilds:
                    member = guild.get_member(int(user_id))
                    if member:
                        # Tenta achar um canal chamado 'geral', 'general' ou o sistema padrão
                        channel = discord.utils.find(
                            lambda c: c.name.lower() in ['geral', 'general', 'chat', 'bate-papo', '💬-bate-papo-geral'] and isinstance(c, discord.TextChannel),
                            guild.channels
                        )
                        if channel is None:
                            channel = guild.system_channel  # fallback canal do sistema
                        if channel:
                            try:
                                await channel.send(f"🎉 Hoje é aniversário do(a) {member.mention}! Parabéns! 🎂🥳")
                            except discord.Forbidden:
                                print(f"❌ Sem permissão para enviar mensagem no canal {channel.name} do servidor {guild.name}")

    @check_aniversario.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Aniversario(bot))
