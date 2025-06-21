import discord
from discord.ext import commands
import random

class Roleplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.missoes = {}  # missao atual por usuário
        self.respeito = {}  # respeito por usuário

        self.missoes_disponiveis = [
            "Configurar ambiente de desenvolvimento Python",
            "Criar um bot simples que responda a comandos",
            "Adicionar comando de saudação ao bot",
            "Implementar comando de ajuda",
            "Fazer o bot responder mensagens específicas",
            "Adicionar sistema de XP para usuários",
            "Criar comando para mostrar ranking de XP",
            "Implementar armazenamento dos dados dos usuários",
            "Adicionar comando de perfil para usuários",
            "Criar comando para mostrar saldo virtual",
            "Implementar sistema de economia simples",
            "Criar comando de trabalhar para ganhar moedas",
            "Adicionar comando de roubar moedas (com riscos)",
            "Criar sistema de loja virtual no bot",
            "Adicionar comando para comprar itens na loja",
            "Implementar inventário para usuários",
            "Adicionar comando para vender itens do inventário",
            "Criar sistema de apostas simples (cara ou coroa)",
            "Implementar comando de dados aleatórios",
            "Adicionar comando de piadas aleatórias",
            "Criar comando para enviar memes",
            "Implementar sistema de níveis e experiência",
            "Adicionar comando para ver o nível atual",
            "Criar comando para missão diária (daily)",
            "Implementar comando para leaderboard geral",
            "Adicionar suporte para múltiplos idiomas",
            "Criar sistema de tickets de suporte",
            "Implementar comando para abrir ticket",
            "Criar comando para fechar ticket",
            "Adicionar comando de avisos para moderação",
            "Implementar comando para banir usuários",
            "Adicionar comando para expulsar usuários",
            "Criar sistema de logs para ações de moderação",
            "Implementar comando de mute e unmute",
            "Adicionar comando para limpar mensagens",
            "Criar comandos divertidos (rps, adivinhação)",
            "Implementar comandos para mini-jogos",
            "Adicionar comando para contar histórias aleatórias",
            "Criar sistema de eventos semanais",
            "Implementar sistema de conquistas para usuários",
            "Adicionar comando para ver conquistas",
            "Criar sistema de níveis de programador (respeito)",
            "Implementar comando !respeito para ver status",
            "Adicionar comando !rankprogramador para ranking",
            "Criar comando para mostrar informações do bot",
            "Implementar deploy do bot para um servidor online",
            "Adicionar comando para reiniciar o bot",
            "Criar sistema de backup automático dos dados",
            "Implementar documentação automática dos comandos",
            "Adicionar comando para feedback dos usuários",
            "Criar comando para sugestões de melhorias"
        ]

    @commands.command(name='missao')
    async def missao(self, ctx):
        user_id = ctx.author.id
        if user_id in self.missoes:
            await ctx.reply(f"🗺️ Sua missão atual é: **{self.missoes[user_id]}**", mention_author=False)
        else:
            await ctx.reply("❌ Você não tem nenhuma missão ativa. Use !aceitar para receber uma missão.", mention_author=False)

    @commands.command(name='aceitar')
    async def aceitar_missao(self, ctx):
        user_id = ctx.author.id
        if user_id in self.missoes:
            await ctx.reply("❌ Você já tem uma missão ativa.", mention_author=False)
            return

        # Pega uma missão aleatória que o usuário ainda não fez (pode ser expandido pra banco)
        missao = random.choice(self.missoes_disponiveis)
        self.missoes[user_id] = missao
        # Dá um respeito inicial se não tiver
        if user_id not in self.respeito:
            self.respeito[user_id] = 0
        await ctx.reply(f"✅ Missão aceita: **{missao}**", mention_author=False)

    @commands.command(name='desistir_missao')
    async def desistir_missao(self, ctx):
        user_id = ctx.author.id
        if user_id not in self.missoes:
            await ctx.reply("❌ Você não tem missão para desistir.", mention_author=False)
            return
        del self.missoes[user_id]
        await ctx.reply("⚠️ Você desistiu da sua missão atual.", mention_author=False)

    @commands.command(name='completar')
    async def completar_missao(self, ctx):
        """Comando para o usuário completar a missão atual."""
        user_id = ctx.author.id
        if user_id not in self.missoes:
            await ctx.reply("❌ Você não tem nenhuma missão ativa para completar.", mention_author=False)
            return

        missao = self.missoes.pop(user_id)
        # Incrementa respeito do usuário ao completar a missão
        self.respeito[user_id] = self.respeito.get(user_id, 0) + 10  # +10 respeito por missão

        await ctx.reply(f"🎉 Parabéns! Você completou a missão: **{missao}**\nVocê ganhou 10 pontos de Respeito de Programador!", mention_author=False)

    @commands.command(name='respeito')
    async def respeito(self, ctx):
        user_id = ctx.author.id
        pontos = self.respeito.get(user_id, 0)
        await ctx.reply(f"🏆 Você tem **{pontos}** pontos de Respeito de Programador.", mention_author=False)

    @commands.command(name='rankprogramador')
    async def rankprogramador(self, ctx):
        # Ordena os usuários pelo respeito (decrescente)
        ranking = sorted(self.respeito.items(), key=lambda x: x[1], reverse=True)[:5]
        if not ranking:
            await ctx.reply("❌ Nenhum programador no ranking ainda.", mention_author=False)
            return

        texto = "🥇 **Ranking dos 5 Programadores com mais Respeito:**\n\n"
        for i, (user_id, pontos) in enumerate(ranking, start=1):
            member = ctx.guild.get_member(user_id)
            nome = member.display_name if member else f"Usuário ID {user_id}"
            texto += f"**{i}º** - {nome} — {pontos} pontos\n"

        await ctx.reply(texto, mention_author=False)

async def setup(bot):
    await bot.add_cog(Roleplay(bot))
