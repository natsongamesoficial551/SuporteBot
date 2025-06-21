import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['ajuda'])
    async def ajuda(self, ctx, categoria_comando: str = None):
        categorias = {
            "aniversario": [
                "`!setaniversario` - Salvar seu aniversário (formato DD-MM, ex: 21-06)"
                "`!veraniversarios @user` - Ver o aniversários das pessoas"
            ],
            "fun": [
                "`!charada` - Receber uma charada",
                "`!countdown` - Contagem regressiva",
                "`!dados` - Rolar dados",
                "`!fato` - Fato interessante",
                "`!meme` - Enviar meme do dia",
                "`!moeda` - Cara ou coroa",
                "`!pergunta` - Pergunta para bola 8 mágica",
                "`!piada` - Contar piada",
                "`!quiz` - Começar quiz de perguntas",
                "`!ranking` - Ranking dos jogadores",
                "`!resposta` - Responder charada",
                "`!roleta` - Escolher aleatoriamente",
                "`!rps` - Pedra, papel, tesoura",
                "`!stats` - Ver estatísticas"
            ],
            "moderation": [
                "`!ban` - Banir membro",
                "`!clearwarns` - Limpar avisos de um usuário",
                "`!kick` - Expulsar membro",
                "`!limpar` - Limpar mensagens",
                "`!lock` - Trancar canal",
                "`!mute` - Mutar membro",
                "`!removewarn` - Remover um warn",
                "`!slowmode` - Configurar slowmode",
                "`!unlock` - Destrancar canal",
                "`!unmute` - Desmutar membro",
                "`!warn` - Avisar usuário",
                "`!warnconfig` - Configuração de warns",
                "`!warns` - Ver avisos"
            ],
            "roleplay": [
                "`!aceitar` - Aceitar missão",
                "`!completar` - Completar missão atual",
                "`!desistir_missao` - Desistir missão",
                "`!missao` - Ver missão atual",
                "`!rankprogramador` - Ver ranking de programadores",
                "`!respeito` - Ver respeito acumulado"
            ],
            "status": [
                "`!ping` - Testar bot",
                "`!status` - Ver status do bot"
            ],
            "tickets": [
                "`!fecharticket` - Fechar ticket",
                "`!ticket` - Abrir ticket"
            ],
            "nocategory": [
                "`!help` - Mostrar essa mensagem"
            ]
        }

        if categoria_comando:
            categoria = categoria_comando.lower()
            if categoria in categorias:
                embed = discord.Embed(
                    title=f"📂 Comandos da categoria: {categoria.capitalize()}",
                    description="\n".join(categorias[categoria]),
                    color=discord.Color.blue()
                )
                embed.set_footer(text="Use !help para ver todas as categorias.")
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(f"❌ Categoria '{categoria_comando}' não encontrada. Use `!help` para ver as categorias disponíveis.")
                return
        
        # Se não passou categoria, mostra todas as categorias com resumo
        embed = discord.Embed(
            title="📚 Lista de Categorias de Comandos",
            description=(
                "Use `!help <categoria>` para ver os comandos de uma categoria específica.\n\n"
                "**Aniversário:**\n  setaniversario\n"
                "**Fun:**\n  charada, countdown, dados, fato, meme, moeda, pergunta, piada, quiz, ranking, resposta, roleta, rps, stats\n"
                "**Moderação:**\n  ban, clearwarns, kick, limpar, lock, mute, removewarn, slowmode, unlock, unmute, warn, warnconfig, warns\n"
                "**Roleplay:**\n  aceitar, completar, desistir_missao, missao, rankprogramador, respeito\n"
                "**Status:**\n  ping, status\n"
                "**Tickets:**\n  fecharticket, ticket\n"
                "**No Category:**\n  help"
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text=(
            "Type !help <command> for more info on a command.\n"
            "You can also type !help <category> for more info on a category."
        ))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
