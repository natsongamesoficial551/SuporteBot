import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime, timedelta

DATA_FILE = 'economy.json'
SHOP_FILE = 'shop.json'

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        self.shop_items = {}
        self.load_data()
        self.load_shop()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def load_shop(self):
        if os.path.exists(SHOP_FILE):
            with open(SHOP_FILE, 'r') as f:
                self.shop_items = json.load(f)
        else:
            self.shop_items = {
                "🎮": {"name": "Videogame", "price": 500, "description": "Um videogame para se divertir"},
                "📱": {"name": "Smartphone", "price": 800, "description": "Um smartphone de última geração"},
                "🚗": {"name": "Carro", "price": 5000, "description": "Um carro novinho em folha"},
                "🏠": {"name": "Casa", "price": 50000, "description": "Uma casa dos sonhos"},
                "✈️": {"name": "Avião", "price": 100000, "description": "Seu próprio jato particular"},
                "🎩": {"name": "Cartola", "price": 100, "description": "Uma cartola elegante"},
                "👑": {"name": "Coroa", "price": 1000, "description": "Uma coroa real"},
                "💎": {"name": "Diamante", "price": 2000, "description": "Um diamante precioso"},
                "🎭": {"name": "Máscara", "price": 50, "description": "Uma máscara misteriosa"},
                "🎪": {"name": "Circo", "price": 10000, "description": "Seu próprio circo"}
            }
            self.save_shop()

    def save_shop(self):
        with open(SHOP_FILE, 'w') as f:
            json.dump(self.shop_items, f, indent=4)

    def ensure_user(self, user_id):
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {
                "balance": 100,
                "bank": 0,
                "inventory": [],
                "last_daily": None,
                "last_work": None,
                "last_crime": None,
                "last_rob": None,
                "streak": 0,
                "total_earned": 0,
                "times_robbed": 0,
                "successful_crimes": 0,
                "level": 1,
                "xp": 0
            }

    def add_xp(self, user_id, amount):
        user_id = str(user_id)
        self.data[user_id]["xp"] += amount
        xp = self.data[user_id]["xp"]
        new_level = int((xp / 100) ** 0.5) + 1
        if new_level > self.data[user_id]["level"]:
            self.data[user_id]["level"] = new_level
            return True
        return False

    def get_cooldown_time(self, user_id, action):
        user_id = str(user_id)
        last_time_str = self.data.get(user_id, {}).get(f"last_{action}")
        if not last_time_str:
            return 0
        last_time = datetime.fromisoformat(last_time_str)
        cooldowns = {
            "daily": timedelta(hours=24),
            "work": timedelta(hours=1),
            "crime": timedelta(hours=2),
            "rob": timedelta(hours=6)
        }
        cooldown = cooldowns.get(action, timedelta(0))
        time_passed = datetime.now() - last_time
        return max(0, int((cooldown - time_passed).total_seconds()))

    def format_time(self, seconds):
        if seconds <= 0:
            return "Disponível"
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s" if minutes else f"{seconds}s"

    @commands.command(name='balance', aliases=['bal', 'saldo'])
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        self.ensure_user(member.id)
        user_data = self.data[str(member.id)]
        bal, bank, total = user_data["balance"], user_data["bank"], user_data["balance"] + user_data["bank"]
        level, xp = user_data["level"], user_data["xp"]
        xp_needed = ((level ** 2) * 100) - xp

        embed = discord.Embed(title=f"💰 Carteira de {member.display_name}", color=discord.Color.gold())
        embed.add_field(name="💵 Carteira", value=f"{bal:,} coins", inline=True)
        embed.add_field(name="🏦 Banco", value=f"{bank:,} coins", inline=True)
        embed.add_field(name="💎 Total", value=f"{total:,} coins", inline=True)
        embed.add_field(name="📊 Level", value=f"{level}", inline=True)
        embed.add_field(name="⭐ XP", value=f"{xp:,}", inline=True)
        embed.add_field(name="🎯 Próximo Level", value=f"{xp_needed:,} XP", inline=True)
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        await ctx.reply(embed=embed, mention_author=False)

    # Os outros comandos (daily, work, crime, rob, deposit, withdraw, shop, buy, inventory, xpboard)
    # continuam IGUAIS como já estavam no seu código, apenas certifique que estejam dentro da classe Economy.

async def setup(bot):
    await bot.add_cog(Economy(bot))
    print("✅ Cog Economy carregado com sucesso!")
