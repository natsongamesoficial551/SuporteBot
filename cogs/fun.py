import discord
from discord.ext import commands
import random
import asyncio
import json
import os
from datetime import datetime, timedelta

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia_sessions = {}
        self.quiz_data = self.load_quiz_data()
        self.user_stats = self.load_user_stats()
        
    def load_quiz_data(self):
        return [
            {"pergunta": "Qual linguagem foi criada por Guido van Rossum?", "opcoes": ["Python", "Java", "C++", "JavaScript"], "resposta": 0},
            {"pergunta": "O que significa 'HTML'?", "opcoes": ["Hyper Text Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyper Transfer Markup Language"], "resposta": 0},
            {"pergunta": "Qual empresa criou o sistema operacional Android?", "opcoes": ["Apple", "Microsoft", "Google", "Samsung"], "resposta": 2},
            {"pergunta": "Em que ano foi criado o Python?", "opcoes": ["1989", "1991", "1995", "2000"], "resposta": 1},
            {"pergunta": "Qual é a linguagem mais usada para desenvolvimento web frontend?", "opcoes": ["Python", "Java", "JavaScript", "C#"], "resposta": 2}
        ]
    
    def load_user_stats(self):
        if os.path.exists('fun_stats.json'):
            with open('fun_stats.json', 'r') as f:
                return json.load(f)
        return {}
    
    def save_user_stats(self):
        with open('fun_stats.json', 'w') as f:
            json.dump(self.user_stats, f, indent=4)
    
    def update_user_stats(self, user_id, stat_type):
        user_id = str(user_id)
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {"quiz_wins": 0, "games_played": 0, "trivia_points": 0}
        self.user_stats[user_id][stat_type] += 1
        self.save_user_stats()

    @commands.command(name='piada')
    async def piada(self, ctx):
        piadas = [
            "Por que o programador confunde Halloween com Natal? Porque OCT 31 == DEC 25!",
            "Qual o animal que programa? O C# (C sharp)!",
            "Por que o Java é tão preguiçoso? Porque ele só executa métodos quando chamado.",
            "Por que os programadores preferem o modo escuro? Porque a luz atrai bugs!",
            "Como você chama um programador que não documenta o código? Um terrorista!",
            "Por que o CSS estava triste? Porque não tinha classe!",
            "O que um programador faz quando está com fome? Ele come um byte!",
            "Por que o JavaScript foi ao psicólogo? Porque tinha problemas de closure!",
            "Como se chama um programador que trabalha no jardim? Um dev-ops!",
            "Por que o Python é tão educado? Porque sempre usa indentação!"
        ]
        await ctx.reply(random.choice(piadas), mention_author=False)
        self.update_user_stats(ctx.author.id, "games_played")

    @commands.command(name='fato')
    async def fato(self, ctx):
        fatos = [
            "O primeiro computador eletrônico foi criado em 1943.",
            "O Python foi criado por Guido van Rossum e lançado em 1991.",
            "O símbolo '#' em programação é chamado de 'hash' ou 'sharp'.",
            "O primeiro vírus de computador foi criado em 1971 e se chamava 'Creeper'.",
            "A linguagem C foi desenvolvida por Dennis Ritchie na Bell Labs em 1972.",
            "O termo 'bug' em programação vem de um inseto real encontrado em um computador em 1947.",
            "O primeiro domínio da internet foi registrado em 1985: symbolics.com",
            "JavaScript foi criado em apenas 10 dias por Brendan Eich em 1995.",
            "O protocolo HTTP foi criado por Tim Berners-Lee em 1989.",
            "A linguagem Java foi originalmente chamada de 'Oak'."
        ]
        await ctx.reply(random.choice(fatos), mention_author=False)

    @commands.command(name='moeda')
    async def moeda(self, ctx):
        resultado = random.choice(['cara', 'coroa'])
        emoji = "🪙" if resultado == "cara" else "🔄"
        await ctx.reply(f"{emoji} Você jogou uma moeda e caiu: **{resultado.upper()}**!", mention_author=False)
        self.update_user_stats(ctx.author.id, "games_played")

    @commands.command(name='dados')
    async def dados(self, ctx, quantidade: int = 1, lados: int = 6):
        if quantidade > 20:
            await ctx.reply("❌ Você pode rolar no máximo 20 dados.", mention_author=False)
            return
        if lados < 2 or lados > 100:
            await ctx.reply("❌ O dado deve ter entre 2 e 100 lados.", mention_author=False)
            return
            
        resultados = [random.randint(1, lados) for _ in range(quantidade)]
        total = sum(resultados)
        
        embed = discord.Embed(title="🎲 Resultado dos Dados", color=discord.Color.blue())
        embed.add_field(name="Resultados", value=f"{', '.join(str(r) for r in resultados)}", inline=False)
        embed.add_field(name="Total", value=str(total), inline=True)
        embed.add_field(name="Dados", value=f"{quantidade}d{lados}", inline=True)
        
        await ctx.reply(embed=embed, mention_author=False)
        self.update_user_stats(ctx.author.id, "games_played")

    @commands.command(name='roleta')
    async def roleta(self, ctx, *, opcoes: str):
        opcoes_lista = [o.strip() for o in opcoes.split(',')]
        if len(opcoes_lista) < 2:
            await ctx.reply("❌ Forneça pelo menos duas opções separadas por vírgula.", mention_author=False)
            return
        
        # Animação da roleta
        msg = await ctx.reply("🎯 Girando a roleta...", mention_author=False)
        await asyncio.sleep(1)
        
        for i in range(3):
            temp_escolha = random.choice(opcoes_lista)
            await msg.edit(content=f"🎯 Girando... **{temp_escolha}**")
            await asyncio.sleep(0.7)
        
        escolha_final = random.choice(opcoes_lista)
        await msg.edit(content=f"🎯 **RESULTADO:** {escolha_final}")
        
        self.update_user_stats(ctx.author.id, "games_played")

    @commands.command(name='charada')
    async def charada(self, ctx):
        charadas = [
            {"pergunta": "O que é, o que é? Tem pernas mas não anda.", "resposta": "cadeira"},
            {"pergunta": "O que é, o que é? Tem dentes mas não morde.", "resposta": "pente"},
            {"pergunta": "O que é, o que é? Passa na frente do sol e não faz sombra.", "resposta": "vento"},
            {"pergunta": "O que é, o que é? Quanto mais se tira, maior fica.", "resposta": "buraco"},
            {"pergunta": "O que é, o que é? Tem coroa mas não é rei.", "resposta": "abacaxi"},
            {"pergunta": "O que é, o que é? Nasce grande e morre pequena.", "resposta": "vela"},
            {"pergunta": "O que é, o que é? Tem pescoço mas não tem cabeça.", "resposta": "garrafa"},
            {"pergunta": "O que é, o que é? Quanto mais rugas tem, mais nova ela é.", "resposta": "pneu"}
        ]
        charada = random.choice(charadas)
        
        embed = discord.Embed(title="🤔 Charada do Dia", description=charada['pergunta'], color=discord.Color.orange())
        embed.set_footer(text="Responda com !resposta <sua resposta>")
        
        await ctx.reply(embed=embed, mention_author=False)
        self.current_charada = charada

    @commands.command(name='resposta')
    async def resposta(self, ctx, *, resposta_usuario):
        if not hasattr(self, 'current_charada'):
            await ctx.reply("❌ Nenhuma charada ativa no momento. Use `!charada` primeiro.", mention_author=False)
            return
            
        correta = self.current_charada['resposta'].lower()
        if resposta_usuario.lower().strip() == correta:
            embed = discord.Embed(title="✅ Parabéns!", description="Resposta correta!", color=discord.Color.green())
            embed.add_field(name="Resposta", value=self.current_charada['resposta'].title())
            await ctx.reply(embed=embed, mention_author=False)
            self.update_user_stats(ctx.author.id, "quiz_wins")
            del self.current_charada
        else:
            await ctx.reply("❌ Resposta incorreta. Tente novamente!", mention_author=False)

    @commands.command(name='quiz')
    async def quiz(self, ctx):
        if ctx.channel.id in self.trivia_sessions:
            await ctx.reply("❌ Já existe um quiz ativo neste canal.", mention_author=False)
            return
            
        pergunta = random.choice(self.quiz_data)
        self.trivia_sessions[ctx.channel.id] = {
            "pergunta": pergunta,
            "participants": {},
            "start_time": datetime.now()
        }
        
        embed = discord.Embed(title="🧠 Quiz Time!", description=pergunta["pergunta"], color=discord.Color.purple())
        
        opcoes_text = ""
        for i, opcao in enumerate(pergunta["opcoes"]):
            opcoes_text += f"{chr(65+i)}) {opcao}\n"
        
        embed.add_field(name="Opções:", value=opcoes_text, inline=False)
        embed.set_footer(text="Responda com A, B, C ou D. Você tem 30 segundos!")
        
        await ctx.reply(embed=embed, mention_author=False)
        
        # Timer para o quiz
        await asyncio.sleep(30)
        await self.end_quiz(ctx.channel)

    async def end_quiz(self, channel):
        if channel.id not in self.trivia_sessions:
            return
            
        session = self.trivia_sessions[channel.id]
        pergunta = session["pergunta"]
        resposta_correta = chr(65 + pergunta["resposta"])
        
        winners = [user_id for user_id, answer in session["participants"].items() 
                  if answer.upper() == resposta_correta]
        
        embed = discord.Embed(title="⏰ Quiz Finalizado!", color=discord.Color.gold())
        embed.add_field(name="Resposta Correta", value=f"{resposta_correta}) {pergunta['opcoes'][pergunta['resposta']]}", inline=False)
        
        if winners:
            winner_mentions = [f"<@{user_id}>" for user_id in winners]
            embed.add_field(name="🏆 Vencedores", value=", ".join(winner_mentions), inline=False)
            for winner_id in winners:
                self.update_user_stats(winner_id, "quiz_wins")
                self.update_user_stats(winner_id, "trivia_points")
        else:
            embed.add_field(name="😢 Resultado", value="Ninguém acertou desta vez!", inline=False)
        
        await channel.send(embed=embed)
        del self.trivia_sessions[channel.id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        # Verificar respostas do quiz
        if message.channel.id in self.trivia_sessions:
            if message.content.upper() in ['A', 'B', 'C', 'D']:
                self.trivia_sessions[message.channel.id]["participants"][message.author.id] = message.content.upper()
                await message.add_reaction("✅")

    @commands.command(name='countdown')
    async def countdown(self, ctx, segundos: int):
        if segundos < 1 or segundos > 60:
            await ctx.reply("❌ O número deve estar entre 1 e 60 segundos.", mention_author=False)
            return
            
        embed = discord.Embed(title="⏳ Countdown", description=f"Iniciando contagem de {segundos} segundos", color=discord.Color.blue())
        message = await ctx.reply(embed=embed, mention_author=False)
        
        for i in range(segundos, 0, -1):
            embed.description = f"⏳ **{i}** segundos restantes"
            if i <= 5:
                embed.color = discord.Color.red()
            elif i <= 10:
                embed.color = discord.Color.orange()
                
            await message.edit(embed=embed)
            await asyncio.sleep(1)
            
        embed.title = "⏰ Tempo Esgotado!"
        embed.description = "🚨 **ACABOU O TEMPO!** 🚨"
        embed.color = discord.Color.red()
        await message.edit(embed=embed)

    @commands.command(name='pergunta')
    async def pergunta(self, ctx, *, pergunta_usuario):
        respostas = [
            "Sim, definitivamente!",
            "Não, de jeito nenhum.",
            "Talvez, quem sabe?",
            "Com certeza absoluta!",
            "Não conte com isso.",
            "É bem possível.",
            "Definitivamente não.",
            "As chances são boas.",
            "Melhor não te dizer agora...",
            "Concentre-se e pergunte novamente.",
            "Sem dúvidas!",
            "Minha resposta é não.",
            "Sim, mas com ressalvas.",
            "É incerto."
        ]
        
        resposta = random.choice(respostas)
        
        embed = discord.Embed(title="🎱 Bola 8 Mágica", color=discord.Color.dark_blue())
        embed.add_field(name="❓ Sua Pergunta:", value=pergunta_usuario, inline=False)
        embed.add_field(name="💬 Minha Resposta:", value=f"**{resposta}**", inline=False)
        
        await ctx.reply(embed=embed, mention_author=False)
        self.update_user_stats(ctx.author.id, "games_played")

    @commands.command(name='meme')
    async def meme(self, ctx):
        memes = [
            "Quando o código funciona na primeira tentativa... É bug ou milagre?",
            "Programador: aquela pessoa que resolve problemas que você não sabia que tinha.",
            "Debugging: a arte de remover bugs... e adicionar outros.",
            "Se funcionou uma vez, funcionará sempre... ou não.",
            "Comentários no código: 'Isso aqui eu entendo depois'... 2 anos depois...",
            "Stack Overflow: salvando vidas desde 2008.",
            "Ctrl+C, Ctrl+V: as teclas mais usadas por programadores.",
            "Quando o PM pede 'só uma mudancinha rápida'... RIP weekend.",
            "Git commit -m 'fix bug'... cria 3 bugs novos.",
            "Café: o combustível oficial dos programadores."
        ]
        
        meme_text = random.choice(memes)
        embed = discord.Embed(title="😂 Meme do Dia", description=meme_text, color=discord.Color.green())
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='stats')
    async def stats(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_id = str(member.id)
        
        if user_id not in self.user_stats:
            await ctx.reply(f"❌ {member.display_name} ainda não jogou nenhum jogo.", mention_author=False)
            return
            
        stats = self.user_stats[user_id]
        
        embed = discord.Embed(title=f"📊 Estatísticas de {member.display_name}", color=discord.Color.blue())
        embed.add_field(name="🎮 Jogos Jogados", value=stats.get("games_played", 0), inline=True)
        embed.add_field(name="🏆 Quiz Vencidos", value=stats.get("quiz_wins", 0), inline=True)
        embed.add_field(name="⭐ Pontos Trivia", value=stats.get("trivia_points", 0), inline=True)
        
        win_rate = 0
        if stats.get("games_played", 0) > 0:
            win_rate = (stats.get("quiz_wins", 0) / stats.get("games_played", 0)) * 100
            
        embed.add_field(name="📈 Taxa de Vitória", value=f"{win_rate:.1f}%", inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='ranking')
    async def ranking(self, ctx, categoria: str = "pontos"):
        if categoria.lower() not in ["pontos", "vitorias", "jogos"]:
            await ctx.reply("❌ Categoria inválida. Use: `pontos`, `vitorias` ou `jogos`", mention_author=False)
            return
            
        if categoria.lower() == "pontos":
            sorted_users = sorted(self.user_stats.items(), key=lambda x: x[1].get("trivia_points", 0), reverse=True)
            title = "🏆 Ranking - Pontos Trivia"
            stat_key = "trivia_points"
        elif categoria.lower() == "vitorias":
            sorted_users = sorted(self.user_stats.items(), key=lambda x: x[1].get("quiz_wins", 0), reverse=True)
            title = "🥇 Ranking - Vitórias em Quiz"
            stat_key = "quiz_wins"
        else:
            sorted_users = sorted(self.user_stats.items(), key=lambda x: x[1].get("games_played", 0), reverse=True)
            title = "🎮 Ranking - Jogos Jogados"
            stat_key = "games_played"
        
        embed = discord.Embed(title=title, color=discord.Color.gold())
        
        for i, (user_id, stats) in enumerate(sorted_users[:10]):
            try:
                user = self.bot.get_user(int(user_id))
                if user:
                    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}º"
                    embed.add_field(
                        name=f"{medal} {user.display_name}",
                        value=f"{stats.get(stat_key, 0)} {categoria}",
                        inline=False
                    )
            except:
                continue
                
        if not embed.fields:
            embed.description = "Nenhum dado encontrado ainda."
            
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='rps')
    async def rock_paper_scissors(self, ctx, escolha: str):
        escolha = escolha.lower()
        opcoes = {'pedra': '🗿', 'papel': '📄', 'tesoura': '✂️'}
        
        if escolha not in opcoes:
            await ctx.reply("❌ Escolha: `pedra`, `papel` ou `tesoura`", mention_author=False)
            return
            
        bot_escolha = random.choice(list(opcoes.keys()))
        user_emoji = opcoes[escolha]
        bot_emoji = opcoes[bot_escolha]
        
        # Determinar vencedor
        if escolha == bot_escolha:
            resultado = "🤝 Empate!"
            cor = discord.Color.orange()
        elif (escolha == 'pedra' and bot_escolha == 'tesoura') or \
             (escolha == 'papel' and bot_escolha == 'pedra') or \
             (escolha == 'tesoura' and bot_escolha == 'papel'):
            resultado = "🎉 Você ganhou!"
            cor = discord.Color.green()
            self.update_user_stats(ctx.author.id, "quiz_wins")
        else:
            resultado = "😢 Você perdeu!"
            cor = discord.Color.red()
            
        embed = discord.Embed(title="🎮 Pedra, Papel, Tesoura", color=cor)
        embed.add_field(name="Sua escolha", value=f"{user_emoji} {escolha.title()}", inline=True)
        embed.add_field(name="Minha escolha", value=f"{bot_emoji} {bot_escolha.title()}", inline=True)
        embed.add_field(name="Resultado", value=resultado, inline=False)
        
        await ctx.reply(embed=embed, mention_author=False)
        self.update_user_stats(ctx.author.id, "games_played")

async def setup(bot):
    await bot.add_cog(Fun(bot))