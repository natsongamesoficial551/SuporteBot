import discord
from discord.ext import commands, tasks

class AutoSend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1385778592150982788  # <<< Troque para o ID do canal do seu servidor
        self.send_messages.start()

    def cog_unload(self):
        self.send_messages.cancel()

    @tasks.loop(hours=3)
    async def send_messages(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            print(f"❌ Canal com ID {self.channel_id} não encontrado!")
            return

        try:
            # 1ª mensagem: divulgar seu serviço
            await channel.send(
                "📢 **Quer um bot personalizado?** Entre em contato comigo no WhatsApp: +55 21 99282-6074"
            )
            # 2ª mensagem: divulgar seu site
            await channel.send(
                "🌐 Visite meu site para saber mais: https://starlit-stardust-fe4cfb.netlify.app"
            )
            # 3ª mensagem: futura (ainda não implementada)
            # await channel.send("Mensagem futura aqui...")

            print(f"✅ Mensagens automáticas enviadas no canal {channel.name}")
        except Exception as e:
            print(f"❌ Erro ao enviar mensagens automáticas: {e}")

    @send_messages.before_loop
    async def before_send(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(AutoSend(bot))
