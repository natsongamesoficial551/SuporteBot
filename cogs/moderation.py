import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import json
import datetime

WARNS_FILE = 'warns.json'

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = {}
        self.load_warns()

    def load_warns(self):
        try:
            with open(WARNS_FILE, 'r') as f:
                self.warns = json.load(f)
        except:
            self.warns = {}

    def save_warns(self):
        with open(WARNS_FILE, 'w') as f:
            json.dump(self.warns, f, indent=4)

    def add_warn(self, guild_id, user_id, reason):
        guild_id = str(guild_id)
        user_id = str(user_id)
        if guild_id not in self.warns:
            self.warns[guild_id] = {}
        if user_id not in self.warns[guild_id]:
            self.warns[guild_id][user_id] = []
        warn_id = len(self.warns[guild_id][user_id]) + 1
        warn_data = {
            'id': warn_id,
            'reason': reason,
            'date': datetime.datetime.utcnow().isoformat()
        }
        self.warns[guild_id][user_id].append(warn_data)
        self.save_warns()
        return warn_id

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'✅ {member.mention} foi banido. Motivo: {reason}')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'✅ {member.mention} foi expulso. Motivo: {reason}')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time: int = 5):
        role = get(ctx.guild.roles, name="Mutado")
        if not role:
            role = await ctx.guild.create_role(name="Mutado")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False, speak=False, add_reactions=False)
        await member.add_roles(role)
        await ctx.send(f'🔇 {member.mention} foi mutado por {time} minutos.')
        await asyncio.sleep(time * 60)
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f'🔊 {member.mention} foi desmutado após {time} minutos.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        role = get(ctx.guild.roles, name="Mutado")
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f'🔊 {member.mention} foi desmutado.')
        else:
            await ctx.send(f'❌ {member.mention} não está mutado.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def limpar(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'🧹 {amount} mensagens foram limpas.', delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        warn_id = self.add_warn(ctx.guild.id, member.id, reason or "Sem motivo")
        await ctx.send(f'⚠️ {member.mention} recebeu um warn (ID: {warn_id}). Motivo: {reason}')

    @commands.command()
    async def warns(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        if guild_id in self.warns and user_id in self.warns[guild_id]:
            warns_list = self.warns[guild_id][user_id]
            embed = discord.Embed(title=f"⚠️ Warns de {member}", color=discord.Color.orange())
            for warn in warns_list:
                embed.add_field(name=f"Warn ID: {warn['id']}", value=f"Motivo: {warn['reason']}\nData: {warn['date']}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'✅ {member} não possui warns.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def removewarn(self, ctx, warn_id: int, member: discord.Member = None):
        member = member or ctx.author
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        if guild_id in self.warns and user_id in self.warns[guild_id]:
            warns_list = self.warns[guild_id][user_id]
            for warn in warns_list:
                if warn['id'] == warn_id:
                    warns_list.remove(warn)
                    self.save_warns()
                    await ctx.send(f'✅ Warn ID {warn_id} removido de {member}.')
                    return
            await ctx.send(f'❌ Warn ID {warn_id} não encontrado para {member}.')
        else:
            await ctx.send(f'❌ {member} não possui warns.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearwarns(self, ctx, member: discord.Member):
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        if guild_id in self.warns and user_id in self.warns[guild_id]:
            self.warns[guild_id][user_id] = []
            self.save_warns()
            await ctx.send(f'✅ Todos os warns de {member} foram removidos.')
        else:
            await ctx.send(f'❌ {member} não possui warns.')

    @commands.command()
    async def warnconfig(self, ctx):
        embed = discord.Embed(title="⚠️ Configuração de Punições por Warns", color=discord.Color.gold())
        embed.add_field(name="3 Warns", value="Mute automático por 10 minutos", inline=False)
        embed.add_field(name="5 Warns", value="Kick automático", inline=False)
        embed.add_field(name="7 Warns", value="Ban automático", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f'🔒 Canal {ctx.channel.mention} trancado.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f'🔓 Canal {ctx.channel.mention} destrancado.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f'🐢 Slowmode ativado: {seconds} segundos.')

async def setup(bot):
    await bot.add_cog(Moderation(bot))
