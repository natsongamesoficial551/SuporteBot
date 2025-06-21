import os
import discord
from discord.ext import commands
from flask import Flask
import threading
import requests
import time
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

# ==== Função auto-ping que roda numa thread e ping no Render a cada 10 minutos ====
def auto_ping():
    url = os.getenv('RENDER_EXTERNAL_URL')  # Defina essa variável de ambiente no Render
    if not url:
        print("⚠️ Variável RENDER_EXTERNAL_URL não definida. Auto-ping desativado.")
        return
    while True:
        try:
            requests.get(url)
            print(f"✅ Auto-ping enviado para: {url}")
        except Exception as e:
            print(f"❌ Erro no auto-ping: {e}")
        time.sleep(600)  # 600 segundos = 10 minutos

# ==== Função principal async para rodar o bot ====
async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("DISCORD_TOKEN"))

# ==== Iniciar Flask e Auto-ping em threads e rodar bot async ====
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    threading.Thread(target=auto_ping).start()
    asyncio.run(main())
