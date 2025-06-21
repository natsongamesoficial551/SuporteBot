import os
import discord
from discord.ext import commands
from flask import Flask
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# ==== Flask Server (Keep Alive no Render) ====
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot de Suporte Online!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))  # Render usa PORT nas ENV
    app.run(host='0.0.0.0', port=port)

# ==== Função para carregar todos os COGS automaticamente ====
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ Cog carregado: {filename}')
            except Exception as e:
                print(f'❌ Erro ao carregar {filename}: {e}')

# ==== Função principal ====
async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("DISCORD_TOKEN"))

# ==== Iniciar Flask em thread separada ====
import threading
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# ==== Rodar Bot ====
asyncio.run(main())
