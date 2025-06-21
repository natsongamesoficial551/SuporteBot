import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ajuda', aliases=['help'])
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="📚 Lista de Comandos do Bot",
            description="Aqui estão todos os comandos organizados por categoria:",
            color=discord.Color.blue()
        )
        
        # Moderação (exemplo)
        embed.add_field(
            name="🛡️ Moderação",
            value=(
                "`!limpar <quantidade>` - Limpa mensagens\n"
                "`!ban <@membro> <motivo>` - Banir membro\n"
                "`!kick <@membro> <motivo>` - Expulsar membro\n"
                "`!mute <@membro> <tempo>` - Mutar membro\n"
                "`!unmute <@membro>` - Desmutar membro\n"
                "`!warn <@usuário> <motivo>` - Avisar usuário\n"
                "`!warns [@usuário]` - Ver avisos\n"
                "`!clearwarns <@usuário>` - Limpar avisos"
            ),
            inline=False
        )
        
        # Economia
        embed.add_field(
            name="💰 Economia",
            value=(
                "`!balance [usuário]` - Ver saldo\n"
                "`!daily` - Coletar recompensa diária\n"
                "`!work` - Trabalhar\n"
                "`!crime` - Cometer crime\n"
                "`!rob <usuário>` - Roubar usuário\n"
                "`!deposit <quantia>` - Depositar dinheiro\n"
                "`!withdraw <quantia>` - Sacar dinheiro\n"
                "`!transfer <@usuário> <quantia>` - Transferir dinheiro\n"
                "`!shop` - Ver loja\n"
                "`!buy <emoji>` - Comprar item\n"
                "`!sell <emoji>` - Vender item\n"
                "`!inventory [usuário]` - Ver inventário\n"
                "`!coinflip <quantia> <cara/coroa>` - Apostar cara ou coroa\n"
                "`!leaderboard [categoria]` - Ranking (balance, bank, total, level, crimes)\n"
                "`!profile [usuário]` - Ver perfil"
            ),
            inline=False
        )
        
        # Diversão (Fun)
        embed.add_field(
            name="🎉 Diversão",
            value=(
                "`!piada` - Contar piada\n"
                "`!fato` - Fato interessante\n"
                "`!moeda` - Cara ou coroa\n"
                "`!dados [quantidade] [lados]` - Rolar dados\n"
                "`!roleta <opção1, opção2, ...>` - Escolher aleatoriamente\n"
                "`!charada` - Receber uma charada\n"
                "`!resposta <sua resposta>` - Responder charada\n"
                "`!quiz` - Começar quiz de perguntas\n"
                "`!countdown <segundos>` - Contagem regressiva\n"
                "`!pergunta <pergunta>` - Pergunta para bola 8 mágica\n"
                "`!meme` - Enviar meme do dia\n"
                "`!stats [usuário]` - Ver estatísticas de jogos\n"
                "`!ranking [pontos/vitorias/jogos]` - Ranking dos jogadores\n"
                "`!rps <pedra/papel/tesoura>` - Jogo Pedra, Papel, Tesoura"
            ),
            inline=False
        )
        
        # Roleplay / RPG (Criação de Bots + XP)
        embed.add_field(
            name="🎭 Roleplay / RPG (Criação de Bots)",
            value=(
                "`!missao` - Ver missão atual\n"
                "`!aceitar` - Aceitar missão\n"
                "`!desistir_missao` - Desistir missão\n"
                "`!completar` - Completar missão e ganhar respeito\n"
                "`!respeito` - Ver respeito acumulado\n"
                "`!rankprogramador` - Ver ranking dos programadores\n"
                "`!xp` - Ver sua experiência atual\n"
                "`!rankxp` - Ver ranking de XP"
            ),
            inline=False
        )
        
        # Tickets de suporte
        embed.add_field(
            name="🎫 Tickets",
            value=(
                "`!ticket <motivo>` - Abrir ticket\n"
                "`!fecharticket` - Fechar ticket"
            ),
            inline=False
        )
        
        # Logs e outros comandos
        embed.add_field(
            name="📜 Outros",
            value=(
                "`!ping` - Testar bot\n"
                "`!status` - Ver status do bot\n"
                "`!userinfo <usuário>` - Ver info do usuário"
            ),
            inline=False
        )
        
        embed.set_footer(text="Use o prefixo '!' antes de cada comando.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
