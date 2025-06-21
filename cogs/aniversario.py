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
        """Formato da data: DD-MM (ex: 21-06)"""
        try:
            datetime.strptime(data, '%d-%m')
        except ValueError:
            await ctx.reply("❌ Formato inválido. Use DD-MM, ex: 21-06", mention_author=False)
            return
        self.aniversarios[str(ctx.author.id)] = data
        self.save_aniversarios()
        await ctx.reply(f"🎂 Seu aniversário foi salvo como {data}.", mention_author=False)

    @tasks.loop(minutes=60)
    async def check_aniversario(self):
        today = datetime.utcnow().strftime('%d-%m')
        for user_id, data in self.aniversarios.items():
            if data == today:
                guilds = self.bot.guilds
                user = self.bot.get_user(int(user_id))
                if not user:
                    continue
                for guild in guilds:
                    member = guild.get_member(int(user_id))
                    if member:
                        channel = discord.utils.get(guild.text_channels, name='💬-bate-papo-geral')
                        if channel:
                            await channel.send(f"🎉 Hoje é aniversário do(a) {member.mention}! Parabéns! 🎂🥳")

    @check_aniversario.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Aniversario(bot))
