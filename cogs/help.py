import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ajuda', aliases=['ajuda'])
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="📜 Lista de Comandos do Bot",
            description="Aqui estão todos os comandos organizados por categoria:",
            color=discord.Color.blurple()
        )

        # 🛡️ Moderação
        embed.add_field(
            name="🛡️ Moderação",
            value=(
                "`!ban <@membro> <motivo>` - Banir membro\n"
                "`!kick <@membro> <motivo>` - Expulsar membro\n"
                "`!mute <@membro> <tempo>` - Mutar membro\n"
                "`!unmute <@membro>` - Desmutar membro\n"
                "`!limpar <quantidade>` - Limpar mensagens\n"
                "`!warn <@membro> <motivo>` - Adicionar warn\n"
                "`!warns [@membro]` - Ver warns\n"
                "`!removewarn <id_warn>` - Remover warn\n"
                "`!clearwarns <@membro>` - Limpar todos os warns\n"
                "`!warnconfig` - Configurar warns\n"
                "`!lock` - Trancar canal\n"
                "`!unlock` - Destrancar canal"
            ),
            inline=False
        )

        # 🎉 Diversão
        embed.add_field(
            name="🎉 Diversão",
            value=(
                "`!piada` - Contar uma piada\n"
                "`!fato` - Fato curioso\n"
                "`!charada` - Receber uma charada\n"
                "`!resposta <resposta>` - Responder charada\n"
                "`!desistir` - Desistir da charada\n"
                "`!dados [quantidade] [lados]` - Rolar dados\n"
                "`!moeda` - Cara ou coroa\n"
                "`!roleta <opções>` - Escolher aleatoriamente\n"
                "`!pergunta <pergunta>` - Pergunta sim ou não\n"
                "`!meme` - Meme em texto\n"
                "`!countdown <segundos>` - Contagem regressiva\n"
                "`!quiz` - Começar quiz\n"
                "`!ranking` - Ranking do quiz\n"
                "`!stats` - Suas estatísticas no quiz"
            ),
            inline=False
        )

        # 💰 Economia / XP / Coins
        embed.add_field(
            name="💰 Economia / XP / Coins",
            value=(
                "`!balance` - Ver seu saldo\n"
                "`!daily` - Coletar recompensa diária\n"
                "`!work` - Trabalhar e ganhar coins\n"
                "`!crime` - Tentar cometer um crime\n"
                "`!rob <@membro>` - Roubar alguém\n"
                "`!deposit <quantia|all>` - Depositar no banco\n"
                "`!withdraw <quantia|all>` - Sacar do banco\n"
                "`!shop` - Ver a loja de itens\n"
                "`!buy <emoji>` - Comprar item da loja\n"
                "`!inventory` - Ver seu inventário\n"
                "`!xpboard` - Ranking de XP"
            ),
            inline=False
        )

        # 🎭 Roleplay / Modo Herói
        embed.add_field(
            name="🎭 Roleplay / Modo Herói",
            value=(
                "`!missao` - Ver missão atual\n"
                "`!aceitar` - Aceitar missão\n"
                "`!completar` - Completar missão\n"
                "`!desistir_missao` - Desistir da missão\n"
                "`!respeito` - Ver respeito de herói\n"
                "`!rankprogramador` - Ranking de programadores"
            ),
            inline=False
        )

        # 📝 Tickets
        embed.add_field(
            name="📝 Tickets",
            value=(
                "`!ticket <motivo>` - Abrir ticket\n"
                "`!fecharticket` - Fechar ticket"
            ),
            inline=False
        )

        # ✅ Status
        embed.add_field(
            name="✅ Status",
            value=(
                "`!ping` - Ver latência\n"
                "`!status` - Ver status do bot"
            ),
            inline=False
        )

        # 🎂 Aniversários
        embed.add_field(
            name="🎂 Aniversários",
            value=(
                "`!setaniversario <DD-MM>` - Salvar seu aniversário\n"
                "`!veraniversarios [@user]` - Ver aniversários salvos\n"
                "`(Auto)` O bot dá parabéns automaticamente"
            ),
            inline=False
        )

        embed.set_footer(text="Use os comandos com o prefixo '!'\nExemplo: !daily")
        await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
    await bot.add_cog(Help(bot))
    print("✅ Cog Help carregado com sucesso!")
