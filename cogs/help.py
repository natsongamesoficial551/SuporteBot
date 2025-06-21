from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['ajuda'])
    async def ajuda(self, ctx, categoria: str = None):
        categorias = {
            "aniversario": (
                "`!setaniversario` - Salvar seu aniversário (formato DD-MM, ex: 21-06)\n"
                "`!veraniversarios [@usuário]` - Ver aniversários salvos"
            ),
            "fun": (
                "`!charada` - Receber uma charada\n"
                "`!countdown` - Contagem regressiva\n"
                "`!dados` - Rolar dados\n"
                "`!fato` - Fato interessante\n"
                "`!meme` - Enviar meme do dia\n"
                "`!moeda` - Cara ou coroa\n"
                "`!pergunta` - Pergunta para bola 8 mágica\n"
                "`!piada` - Contar piada\n"
                "`!quiz` - Começar quiz de perguntas\n"
                "`!ranking` - Ranking dos jogadores\n"
                "`!resposta` - Responder charada\n"
                "`!roleta` - Escolher aleatoriamente\n"
                "`!rps` - Pedra, papel, tesoura\n"
                "`!stats` - Ver estatísticas"
            ),
            "moderation": (
                "`!ban` - Banir membro\n"
                "`!clearwarns` - Limpar avisos de um usuário\n"
                "`!kick` - Expulsar membro\n"
                "`!limpar` - Limpar mensagens\n"
                "`!lock` - Trancar canal\n"
                "`!mute` - Mutar membro\n"
                "`!removewarn` - Remover um warn\n"
                "`!slowmode` - Configurar slowmode\n"
                "`!unlock` - Destrancar canal\n"
                "`!unmute` - Desmutar membro\n"
                "`!warn` - Avisar usuário\n"
                "`!warnconfig` - Configuração de warns\n"
                "`!warns` - Ver avisos"
            ),
            "roleplay": (
                "`!aceitar` - Aceitar missão\n"
                "`!completar` - Completar missão atual\n"
                "`!desistir_missao` - Desistir missão\n"
                "`!missao` - Ver missão atual\n"
                "`!rankprogramador` - Ver ranking de programadores\n"
                "`!respeito` - Ver respeito acumulado"
            ),
            "status": (
                "`!ping` - Testar bot\n"
                "`!status` - Ver status do bot"
            ),
            "tickets": (
                "`!fecharticket` - Fechar ticket\n"
                "`!ticket` - Abrir ticket"
            ),
            "nocategory": (
                "`!help` - Mostrar essa mensagem"
            )
        }

        if categoria:
            cat = categoria.lower()
            if cat in categorias:
                embed = discord.Embed(
                    title=f"📂 Comandos da categoria: {cat.capitalize()}",
                    description=categorias[cat],
                    color=discord.Color.blue()
                )
                embed.set_footer(text="Use !help para ver todas as categorias.")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Categoria '{categoria}' não encontrada. Use `!help` para ver as categorias disponíveis.")
        else:
            embed = discord.Embed(
                title="📚 Lista de Categorias de Comandos",
                description=(
                    "Use `!help <categoria>` para ver os comandos de uma categoria específica.\n\n"
                    "**Aniversário:**\n  setaniversario, veraniversarios\n"
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
    print("✅ Cog Help carregado com sucesso!")
