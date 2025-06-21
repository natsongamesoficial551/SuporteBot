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
        embed.add_field(name="📊 Level", value=f"{level}", inline=True)
        embed.add_field(name="⭐ XP", value=f"{xp:,}", inline=True)
        embed.add_field(name="🎯 Próximo Level", value=f"{xp_needed:,} XP", inline=True)
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='daily', aliases=['diario'])
    async def daily(self, ctx):
        self.ensure_user(ctx.author.id)
        user_id = str(ctx.author.id)
        cooldown = self.get_cooldown_time(user_id, "daily")
        if cooldown > 0:
            await ctx.reply(f"⏰ Você já coletou hoje! Volte em {self.format_time(cooldown)}", mention_author=False)
            return

        base_reward = random.randint(100, 200)
        streak_bonus = min(self.data[user_id]["streak"] * 10, 500)
        total_reward = base_reward + streak_bonus

        self.data[user_id]["balance"] += total_reward
        self.data[user_id]["total_earned"] += total_reward
        self.data[user_id]["last_daily"] = datetime.now().isoformat()
        self.data[user_id]["streak"] += 1

        level_up = self.add_xp(ctx.author.id, 25)

        embed = discord.Embed(title="🎉 Daily Coletado!", color=discord.Color.green())
        embed.add_field(name="💰 Recompensa", value=f"{total_reward:,} coins", inline=True)
        embed.add_field(name="🔥 Streak", value=f"{self.data[user_id]['streak']} dias", inline=True)
        if level_up:
            embed.add_field(name="🎊 LEVEL UP!", value=f"Agora você é level {self.data[user_id]['level']}!", inline=False)

        self.save_data()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='work', aliases=['trabalhar'])
    async def work(self, ctx):
        self.ensure_user(ctx.author.id)
        user_id = str(ctx.author.id)
        cooldown = self.get_cooldown_time(user_id, "work")
        if cooldown > 0:
            await ctx.reply(f"😴 Descanse mais {self.format_time(cooldown)} antes de trabalhar novamente.", mention_author=False)
            return

        level = self.data[user_id]["level"]
        jobs = [
            {"name": "Entregador de Pizza", "min": 20, "max": 80},
            {"name": "Garçom", "min": 30, "max": 100},
            {"name": "Programador Júnior", "min": 80, "max": 150},
            {"name": "Designer", "min": 100, "max": 200},
            {"name": "Programador Sênior", "min": 150, "max": 300},
            {"name": "Gerente", "min": 200, "max": 400},
            {"name": "CEO", "min": 300, "max": 500}
        ]

        job_index = min(level // 2, len(jobs) - 1)
        job = jobs[job_index]
        earnings = random.randint(job["min"], job["max"]) + level * 5

        self.data[user_id]["balance"] += earnings
        self.data[user_id]["total_earned"] += earnings
        self.data[user_id]["last_work"] = datetime.now().isoformat()

        level_up = self.add_xp(ctx.author.id, 15)

        embed = discord.Embed(title="💼 Trabalho Concluído!", color=discord.Color.blue())
        embed.add_field(name="👨‍💼 Cargo", value=job["name"], inline=True)
        embed.add_field(name="💰 Ganhos", value=f"{earnings:,} coins", inline=True)
        if level_up:
            embed.add_field(name="🎊 LEVEL UP!", value=f"Level {self.data[user_id]['level']}!", inline=False)

        self.save_data()
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='shop')
    async def shop(self, ctx):
        embed = discord.Embed(title="🛒 Loja", color=discord.Color.purple())
        for emoji, item in self.shop_items.items():
            embed.add_field(name=f"{emoji} {item['name']} - {item['price']:,} coins", value=item["description"], inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='buy')
    async def buy(self, ctx, emoji):
        self.ensure_user(ctx.author.id)
        user_id = str(ctx.author.id)
        if emoji not in self.shop_items:
            await ctx.reply("❌ Item não encontrado na loja.", mention_author=False)
            return
        price = self.shop_items[emoji]["price"]
        if self.data[user_id]["balance"] < price:
            await ctx.reply("❌ Saldo insuficiente.", mention_author=False)
            return
        self.data[user_id]["balance"] -= price
        self.data[user_id]["inventory"].append(emoji)
        self.save_data()
        await ctx.reply(f"✅ Você comprou {self.shop_items[emoji]['name']} por {price:,} coins.", mention_author=False)

    @commands.command(name='inventory', aliases=['inv'])
    async def inventory(self, ctx):
        self.ensure_user(ctx.author.id)
        user_id = str(ctx.author.id)
        inventory = self.data[user_id]["inventory"]
        if not inventory:
            await ctx.reply("🛒 Seu inventário está vazio.", mention_author=False)
            return
        embed = discord.Embed(title=f"🎒 Inventário de {ctx.author.display_name}", color=discord.Color.blurple())
        counts = {}
        for emoji in inventory:
            counts[emoji] = counts.get(emoji, 0) + 1
        for emoji, count in counts.items():
            name = self.shop_items.get(emoji, {}).get("name", "Item Desconhecido")
            embed.add_field(name=f"{emoji} {name}", value=f"Quantidade: {count}", inline=True)
        await ctx.reply(embed=embed, mention_author=False)

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
