import discord
from discord.ext import commands
import asyncio
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TOKEN_1 = os.getenv("TOKEN_1")
OWNER_ID = os.getenv("OWNER_ID")

if not TOKEN_1 or not OWNER_ID:
    print("⚠️ UYARI: TOKEN_1 veya OWNER_ID eksik!")
else:
    OWNER_ID = int(OWNER_ID)

bot1 = commands.Bot(command_prefix="!", self_bot=True, help_command=None)
TARGET_CHANNEL_ID_1 = None

async def join_channel_1():
    global TARGET_CHANNEL_ID_1
    if not TARGET_CHANNEL_ID_1:
        return
    await bot1.wait_until_ready()
    try:
        channel = bot1.get_channel(TARGET_CHANNEL_ID_1) or await bot1.fetch_channel(TARGET_CHANNEL_ID_1)
        if channel:
            if bot1.voice_clients:
                vc = bot1.voice_clients[0]
                if vc.channel and vc.channel.id == TARGET_CHANNEL_ID_1 and vc.is_connected():
                    return
                await vc.disconnect()
            
            await channel.connect(self_deaf=True, self_mute=True)
            print(f"[Hesap 1] {channel.name} kanalına bağlanıldı.")
    except Exception as e:
        print(f"[Hesap 1] Bağlantı hatası: {e}")

@bot1.event
async def on_ready():
    print(f"Bot Giriş Yaptı: {bot1.user}")

@bot1.command(name="yardim")
async def cmd_yardim(ctx):
    if ctx.author.id != OWNER_ID:
        return
    global TARGET_CHANNEL_ID_1
    kd = f"<#{TARGET_CHANNEL_ID_1}>" if TARGET_CHANNEL_ID_1 else "❌ *Ayarlanmadı!*"
    panel = (
        "**🎛️ Ses Botu Kontrol Paneli**\n"
        "──────────────────────────────\n"
        f"📍 **Kanal:** {kd}\n\n"
        "🛠️ **Komutlar:**\n"
        "`!ayarla <id>` - Hedef kanalı seçer ve bağlanır.\n"
        "`!gir` - Sese giriş yapar.\n"
        "`!cik` - Sesten çıkar.\n"
        "──────────────────────────────"
    )
    await ctx.message.edit(content=panel)

@bot1.command(name="ayarla")
async def cmd_ayarla(ctx, channel_id: int = None):
    if ctx.author.id != OWNER_ID:
        return
    global TARGET_CHANNEL_ID_1
    if not channel_id:
        await ctx.message.edit(content="❌ Lütfen geçerli bir Kanal ID'si yaz!")
        return
    TARGET_CHANNEL_ID_1 = channel_id
    await join_channel_1()
    await ctx.message.edit(content=f"✅ Kanal ayarlandı ve bağlanıldı.")

@bot1.command(name="gir")
async def cmd_gir(ctx):
    if ctx.author.id != OWNER_ID:
        return
    if not TARGET_CHANNEL_ID_1:
        await ctx.message.edit(content="❌ Önce kanal ayarlamalısın: `!ayarla <id>`")
        return
    await join_channel_1()
    await ctx.message.edit(content=f"✅ Sese giriş yapıldı.")

@bot1.command(name="cik")
async def cmd_cik(ctx):
    if ctx.author.id != OWNER_ID:
        return
    global TARGET_CHANNEL_ID_1
    TARGET_CHANNEL_ID_1 = None
    for vc in bot1.voice_clients:
        await vc.disconnect()
    await ctx.message.edit(content="🚪 Sesten çıkıldı.")

async def keep_alive_task():
    while True:
        await asyncio.sleep(15)
        for vc in bot1.voice_clients:
            if vc and vc.is_connected():
                try:
                    await vc.ws.speak(True)
                except:
                    pass

async def main():
    asyncio.create_task(keep_alive_task())
    async with bot1:
        await bot1.start(TOKEN_1)

if __name__ == "__main__":
    asyncio.run(main())
