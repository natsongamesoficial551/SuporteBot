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

    # (... todos os comandos anteriores balance, daily, work, shop, buy, etc ...)

    @commands.command(name="crime")
    async def crime(self, ctx):
        self.ensure_user(ctx.author.id)
        user_id = str(ctx.author.id)
        cooldown = self.get_cooldown_time(user_id, "crime")
        if cooldown > 0:
            await ctx.reply(f"⏱️ Espere {self.format_time(cooldown)} antes de cometer outro crime.", mention_author=False)
            return

        success = random.random() < 0.5  # 50% de chance
        amount = random.randint(100, 500)
        if success:
            self.data[user_id]["balance"] += amount
            self.data[user_id]["successful_crimes"] += 1
            result = f"🕵️ Você cometeu um crime com sucesso e ganhou {amount} coins!"
        else:
            penalty = min(self.data[user_id]["balance"], amount)
            self.data[user_id]["balance"] -= penalty
            result = f"🚓 Você foi pego cometendo um crime e perdeu {penalty} coins!"

        self.data[user_id]["last_crime"] = datetime.now().isoformat()
        self.save_data()
        await ctx.reply(result, mention_author=False)

    @commands.command(name="deposit", aliases=["dep"])
    async def deposit(self, ctx, amount: str):
        self.ensure_user(ctx.author.id)
        user_id = str(ctx.author.id)
        bal = self.data[user_id]["balance"]

        if amount.lower() == "all":
            if bal == 0:
                await ctx.reply("❌ Você não tem nada para depositar.", mention_author=False)
                return
            self.data[user_id]["bank"] += bal
            self.data[user_id]["balance"] = 0
            msg = f"✅ Você depositou {bal:,} coins no banco."
        else:
            try:
                amount = int(amount)
                if amount <= 0 or amount > bal:
                    raise ValueError
                self.data[user_id]["balance"] -= amount
                self.data[user_id]["bank"] += amount
                msg = f"✅ Você depositou {amount:,} coins no banco."
            except:
                msg = "❌ Valor inválido para depósito."

        self.save_data()
        await ctx.reply(msg, mention_author=False)

    @commands.command(name="withdraw", aliases=["sacar"])
    async def withdraw(self, ctx, amount: str):
        self.ensure_user(ctx.author.id)
        user_id = str(ctx.author.id)
        bank = self.data[user_id]["bank"]

        if amount.lower() == "all":
            if bank == 0:
                await ctx.reply("❌ Você não tem nada no banco para sacar.", mention_author=False)
                return
            self.data[user_id]["balance"] += bank
            self.data[user_id]["bank"] = 0
            msg = f"✅ Você sacou {bank:,} coins da sua conta bancária."
        else:
            try:
                amount = int(amount)
                if amount <= 0 or amount > bank:
                    raise ValueError
                self.data[user_id]["bank"] -= amount
                self.data[user_id]["balance"] += amount
                msg = f"✅ Você sacou {amount:,} coins do banco."
            except:
                msg = "❌ Valor inválido para saque."

        self.save_data()
        await ctx.reply(msg, mention_author=False)

    @commands.command(name='xpboard', aliases=['rank', 'xprank'])
    async def xpboard(self, ctx):
        if not self.data:
            await ctx.reply("Nenhum dado de XP encontrado.", mention_author=False)
            return
        sorted_users = sorted(self.data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)
        top_10 = sorted_users[:10]
        embed = discord.Embed(title="🏆 Ranking de XP", color=discord.Color.gold())
        for i, (user_id, user_data) in enumerate(top_10, start=1):
            member = ctx.guild.get_member(int(user_id))
            name = member.display_name if member else f"Usuário {user_id}"
            embed.add_field(name=f"{i}. {name}", value=f"Level: {user_data.get('level', 1)} - XP: {user_data.get('xp', 0):,}", inline=False)
        await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
    await bot.add_cog(Economy(bot))
    print("✅ Cog Economy carregado com sucesso!")
