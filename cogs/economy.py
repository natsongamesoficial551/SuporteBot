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
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    @commands.command(name='balance', aliases=['bal', 'saldo'])
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        self.ensure_user(member.id)
        user_data = self.data[str(member.id)]
        embed = discord.Embed(title=f"💰 Carteira de {member.display_name}", color=discord.Color.gold())
        embed.add_field(name="💵 Carteira", value=f"{user_data['balance']} coins")
        embed.add_field(name="🏦 Banco", value=f"{user_data['bank']} coins")
        embed.add_field(name="📊 Level", value=f"{user_data['level']}")
        embed.add_field(name="⭐ XP", value=f"{user_data['xp']}")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='daily', aliases=['diario'])
    async def daily(self, ctx):
        self.ensure_user(ctx.author.id)
        cooldown = self.get_cooldown_time(ctx.author.id, "daily")
        if cooldown > 0:
            await ctx.reply(f"⏰ Você já pegou seu daily! Volte em {self.format_time(cooldown)}", mention_author=False)
            return

        reward = random.randint(150, 300)
        user_id = str(ctx.author.id)
        self.data[user_id]["balance"] += reward
        self.data[user_id]["last_daily"] = datetime.now().isoformat()
        self.add_xp(user_id, 20)
        self.save_data()
        await ctx.reply(f"🎉 Você ganhou {reward} coins no seu daily!", mention_author=False)

    @commands.command(name='work', aliases=['trabalhar'])
    async def work(self, ctx):
        self.ensure_user(ctx.author.id)
        cooldown = self.get_cooldown_time(ctx.author.id, "work")
        if cooldown > 0:
            await ctx.reply(f"😴 Você precisa esperar mais {self.format_time(cooldown)} antes de trabalhar de novo.", mention_author=False)
            return

        jobs = ["Entregador de Pizza", "Programador", "Mecânico", "Youtuber", "Streamer", "Designer"]
        job = random.choice(jobs)
        earnings = random.randint(200, 400)
        user_id = str(ctx.author.id)
        self.data[user_id]["balance"] += earnings
        self.data[user_id]["last_work"] = datetime.now().isoformat()
        self.add_xp(user_id, 15)
        self.save_data()
        await ctx.reply(f"💼 Você trabalhou como **{job}** e ganhou **{earnings} coins**!", mention_author=False)

    @commands.command(name='crime')
    async def crime(self, ctx):
        self.ensure_user(ctx.author.id)
        cooldown = self.get_cooldown_time(ctx.author.id, "crime")
        user_id = str(ctx.author.id)
        if cooldown > 0:
            await ctx.reply(f"🚔 Espere mais {self.format_time(cooldown)} antes de tentar outro crime!", mention_author=False)
            return

        success = random.random() < 0.6
        if success:
            reward = random.randint(300, 600)
            self.data[user_id]["balance"] += reward
            msg = f"😈 Você cometeu um crime e ganhou **{reward} coins**!"
        else:
            fine = random.randint(150, 300)
            self.data[user_id]["balance"] = max(0, self.data[user_id]["balance"] - fine)
            msg = f"🚓 Você foi pego e perdeu **{fine} coins** de multa!"

        self.data[user_id]["last_crime"] = datetime.now().isoformat()
        self.add_xp(user_id, 10)
        self.save_data()
        await ctx.reply(msg, mention_author=False)

    @commands.command(name='rob', aliases=['assaltar'])
    async def rob(self, ctx, target: discord.Member):
        if target == ctx.author or target.bot:
            await ctx.reply("❌ Você não pode roubar essa pessoa!", mention_author=False)
            return

        self.ensure_user(ctx.author.id)
        self.ensure_user(target.id)
        cooldown = self.get_cooldown_time(ctx.author.id, "rob")
        if cooldown > 0:
            await ctx.reply(f"⏳ Espere mais {self.format_time(cooldown)} antes de roubar novamente!", mention_author=False)
            return

        target_balance = self.data[str(target.id)]["balance"]
        if target_balance < 100:
            await ctx.reply(f"❌ {target.display_name} não tem dinheiro suficiente para ser roubado!", mention_author=False)
            return

        success = random.random() < 0.5
        if success:
            amount = random.randint(50, min(300, target_balance))
            self.data[str(ctx.author.id)]["balance"] += amount
            self.data[str(target.id)]["balance"] -= amount
            msg = f"💰 Você roubou **{amount} coins** de {target.display_name}!"
        else:
            fine = random.randint(100, 200)
            self.data[str(ctx.author.id)]["balance"] = max(0, self.data[str(ctx.author.id)]["balance"] - fine)
            msg = f"🚨 Você falhou e perdeu **{fine} coins**!"

        self.data[str(ctx.author.id)]["last_rob"] = datetime.now().isoformat()
        self.add_xp(ctx.author.id, 20)
        self.save_data()
        await ctx.reply(msg, mention_author=False)

    @commands.command(name='deposit', aliases=['dep'])
    async def deposit(self, ctx, amount: str):
        self.ensure_user(ctx.author.id)
        user_id = str(ctx.author.id)
        if amount.lower() == "all":
            amount = self.data[user_id]["balance"]
        else:
            try:
                amount = int(amount)
            except:
                await ctx.reply("❌ Valor inválido.", mention_author=False)
                return

        if amount <= 0 or self.data[user_id]["balance"] < amount:
            await ctx.reply("❌ Saldo insuficiente.", mention_author=False)
            return

        self.data[user_id]["balance"] -= amount
        self.data[user_id]["bank"] += amount
        self.save_data()
        await ctx.reply(f"🏦 Você depositou **{amount} coins** no banco.", mention_author=False)

    @commands.command(name='withdraw', aliases=['sacar'])
    async def withdraw(self, ctx, amount: str):
        self.ensure_user(ctx.author.id)
        user_id = str(ctx.author.id)
        if amount.lower() == "all":
            amount = self.data[user_id]["bank"]
        else:
            try:
                amount = int(amount)
            except:
                await ctx.reply("❌ Valor inválido.", mention_author=False)
                return

        if amount <= 0 or self.data[user_id]["bank"] < amount:
            await ctx.reply("❌ Saldo insuficiente no banco.", mention_author=False)
            return

        self.data[user_id]["bank"] -= amount
        self.data[user_id]["balance"] += amount
        self.save_data()
        await ctx.reply(f"💵 Você sacou **{amount} coins** do banco.", mention_author=False)

    @commands.command(name='shop')
    async def shop(self, ctx):
        embed = discord.Embed(title="🛒 Loja", color=discord.Color.purple())
        for emoji, item in self.shop_items.items():
            embed.add_field(name=f"{emoji} {item['name']}", value=f"{item['description']} - **{item['price']} coins**", inline=False)
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
            await ctx.reply("❌ Você não tem dinheiro suficiente.", mention_author=False)
            return

        self.data[user_id]["balance"] -= price
        self.data[user_id]["inventory"].append(emoji)
        self.save_data()
        await ctx.reply(f"✅ Você comprou **{self.shop_items[emoji]['name']}** por **{price} coins**.", mention_author=False)

    @commands.command(name='inventory', aliases=['inv'])
    async def inventory(self, ctx):
        self.ensure_user(ctx.author.id)
        inv = self.data[str(ctx.author.id)]["inventory"]
        if not inv:
            await ctx.reply("🎒 Seu inventário está vazio.", mention_author=False)
            return

        embed = discord.Embed(title=f"🎒 Inventário de {ctx.author.display_name}", color=discord.Color.blurple())
        items = {}
        for item in inv:
            items[item] = items.get(item, 0) + 1

        for emoji, count in items.items():
            name = self.shop_items.get(emoji, {}).get("name", "Item desconhecido")
            embed.add_field(name=f"{emoji} {name}", value=f"Quantidade: {count}", inline=True)

        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='xpboard', aliases=['rank', 'xprank'])
    async def xpboard(self, ctx):
        top_users = sorted(self.data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)[:10]
        embed = discord.Embed(title="🏆 Ranking de XP", color=discord.Color.gold())
        for idx, (user_id, info) in enumerate(top_users, start=1):
            user = ctx.guild.get_member(int(user_id))
            name = user.display_name if user else f"Usuário {user_id}"
            embed.add_field(name=f"{idx}. {name}", value=f"Level: {info['level']} | XP: {info['xp']}", inline=False)
        await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
    await bot.add_cog(Economy(bot))
    print("✅ Cog Economy carregado com sucesso!")
