import discord
from discord.ext import commands
import asyncio
import threading
import os

# Yerelde test ederken .env okusun, Railway'de doğrudan sistem değişkenlerini kullansın
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Railway Variables panelinden çekilen bilgiler
TOKEN_1 = os.getenv("TOKEN_1")
TOKEN_2 = os.getenv("TOKEN_2")
OWNER_ID = os.getenv("OWNER_ID")

# Güvenlik kontrolü
if not TOKEN_1 or not TOKEN_2 or not OWNER_ID:
    print("⚠️ UYARI: TOKEN_1, TOKEN_2 veya OWNER_ID eksik! Lütfen Railway Variables kısmını kontrol et.")
else:
    # Güvenlik için OWNER_ID'yi tam sayıya (integer) çeviriyoruz
    OWNER_ID = int(OWNER_ID)

# İki ayrı bot (client) nesnesi oluşturuyoruz
bot1 = commands.Bot(command_prefix="!", self_bot=True, help_command=None)
bot2 = commands.Bot(command_prefix="!", self_bot=True, help_command=None)

# Her hesap için ayrı hedef kanal ID değişkenleri
TARGET_CHANNEL_ID_1 = None
TARGET_CHANNEL_ID_2 = None

# ================= 1. HESAP İŞLEMLERİ =================

async def join_channel_1():
    global TARGET_CHANNEL_ID_1
    if not TARGET_CHANNEL_ID_1:
        return
    await bot1.wait_until_ready()
    channel = bot1.get_channel(TARGET_CHANNEL_ID_1)
    if channel:
        try:
            if bot1.voice_clients and bot1.voice_clients[0].channel and bot1.voice_clients[0].channel.id == TARGET_CHANNEL_ID_1:
                return
            for vc in bot1.voice_clients:
                await vc.disconnect()
            await channel.connect(self_deaf=True, self_mute=True)
            print(f"[Hesap 1] Başarıyla {channel.name} kanalına girildi.")
        except Exception as e:
            print(f"[Hesap 1] Bağlantı hatası: {e}")

@bot1.event
async def on_ready():
    print(f"1. Hesap Giriş Yaptı: {bot1.user} (ID: {bot1.user.id})")

@bot1.event
async def on_voice_state_update(member, before, after):
    global TARGET_CHANNEL_ID_1
    if not TARGET_CHANNEL_ID_1:
        return
    if member.id == bot1.user.id:
        if after.channel and after.channel.id == TARGET_CHANNEL_ID_1:
            return
        print("[Hesap 1] Sesten düşüldü, tekrar bağlanılıyor...")
        await asyncio.sleep(2)
        await join_channel_1()

@bot1.command(name="yardim1")
async def cmd_yardim1(ctx):
    # Sadece OWNER_ID komut verebilir
    if ctx.author.id != OWNER_ID:
        return
    global TARGET_CHANNEL_ID_1
    kanal_durumu = f"<#{TARGET_CHANNEL_ID_1}> (ID: `{TARGET_CHANNEL_ID_1}`)" if TARGET_CHANNEL_ID_1 else "❌ *Ayarlanmadı!*"
    
    panel = (
        "**🎛️ 1. Hesap Kontrol Paneli**\n"
        "──────────────────────────────\n"
        f"📍 **Kanal:** {kanal_durumu}\n\n"
        "🛠️ **Komutlar:**\n"
        "`!ayarla1 <id>` - 1. hesap kanalını seçer.\n"
        "`!gir1` - 1. hesabı sese sokar.\n"
        "`!cik1` - 1. hesabı sesten çıkarır.\n"
        "──────────────────────────────"
    )
    await ctx.message.edit(content=panel)

@bot1.command(name="ayarla1")
async def cmd_ayarla1(ctx, channel_id: int = None):
    if ctx.author.id != OWNER_ID:
        return
    global TARGET_CHANNEL_ID_1
    if not channel_id:
        await ctx.message.edit(content="❌ Lütfen geçerli bir Kanal ID'si yaz! Örnek: `!ayarla1 12345`")
        return
    TARGET_CHANNEL_ID_1 = channel_id
    channel = bot1.get_channel(TARGET_CHANNEL_ID_1)
    if channel:
        await ctx.message.edit(content=f"✅ 1. Hesap için kanal ayarlandı ve bağlanıldı: **{channel.name}**")
        await join_channel_1()
    else:
        await ctx.message.edit(content="❌ Hata: Bu ID ile kanal bulunamadı!")

@bot1.command(name="gir1")
async def cmd_gir1(ctx):
    if ctx.author.id != OWNER_ID:
        return
    if not TARGET_CHANNEL_ID_1:
        await ctx.message.edit(content="❌ Önce kanal ayarlamalısın: `!ayarla1 <id>`")
        return
    await join_channel_1()
    await ctx.message.edit(content="✅ 1. Hesap sese giriş yaptı.")

@bot1.command(name="cik1")
async def cmd_cik1(ctx):
    if ctx.author.id != OWNER_ID:
        return
    global TARGET_CHANNEL_ID_1
    TARGET_CHANNEL_ID_1 = None
    for vc in bot1.voice_clients:
        await vc.disconnect()
    await ctx.message.edit(content="🚪 1. Hesap sesten çıktı ve otomatik bağlama durduruldu.")


# ================= 2. HESAP İŞLEMLERİ =================

async def join_channel_2():
    global TARGET_CHANNEL_ID_2
    if not TARGET_CHANNEL_ID_2:
        return
    await bot2.wait_until_ready()
    channel = bot2.get_channel(TARGET_CHANNEL_ID_2)
    if channel:
        try:
            if bot2.voice_clients and bot2.voice_clients[0].channel and bot2.voice_clients[0].channel.id == TARGET_CHANNEL_ID_2:
                return
            for vc in bot2.voice_clients:
                await vc.disconnect()
            await channel.connect(self_deaf=True, self_mute=True)
            print(f"[Hesap 2] Başarıyla {channel.name} kanalına girildi.")
        except Exception as e:
            print(f"[Hesap 2] Bağlantı hatası: {e}")

@bot2.event
async def on_ready():
    print(f"2. Hesap Giriş Yaptı: {bot2.user} (ID: {bot2.user.id})")

@bot2.event
async def on_voice_state_update(member, before, after):
    global TARGET_CHANNEL_ID_2
    if not TARGET_CHANNEL_ID_2:
        return
    if member.id == bot2.user.id:
        if after.channel and after.channel.id == TARGET_CHANNEL_ID_2:
            return
        print("[Hesap 2] Sesten düşüldü, tekrar bağlanılıyor...")
        await asyncio.sleep(2)
        await join_channel_2()

@bot2.command(name="yardim2")
async def cmd_yardim2(ctx):
    # OWNER_ID kontrolü (2. botu da sadece ana hesabın kontrol edebilir)
    if ctx.author.id != OWNER_ID:
        return
    global TARGET_CHANNEL_ID_2
    kanal_durumu = f"<#{TARGET_CHANNEL_ID_2}> (ID: `{TARGET_CHANNEL_ID_2}`)" if TARGET_CHANNEL_ID_2 else "❌ *Ayarlanmadı!*"
    
    panel = (
        "**🎛️ 2. Hesap Kontrol Paneli**\n"
        "──────────────────────────────\n"
        f"📍 **Kanal:** {kanal_durumu}\n\n"
        "🛠️ **Komutlar:**\n"
        "`!ayarla2 <id>` - 2. hesap kanalını seçer.\n"
        "`!gir2` - 2. hesabı sese sokar.\n"
        "`!cik2` - 2. hesabı sesten çıkarır.\n"
        "──────────────────────────────"
    )
    await ctx.message.edit(content=panel)

@bot2.command(name="ayarla2")
async def cmd_ayarla2(ctx, channel_id: int = None):
    if ctx.author.id != OWNER_ID:
        return
    global TARGET_CHANNEL_ID_2
    if not channel_id:
        await ctx.message.edit(content="❌ Lütfen geçerli bir Kanal ID'si yaz! Örnek: `!ayarla2 12345`")
        return
    TARGET_CHANNEL_ID_2 = channel_id
    channel = bot2.get_channel(TARGET_CHANNEL_ID_2)
    if channel:
        await ctx.message.edit(content=f"✅ 2. Hesap için kanal ayarlandı ve bağlanıldı: **{channel.name}**")
        await join_channel_2()
    else:
        await ctx.message.edit(content="❌ Hata: Bu ID ile kanal bulunamadı!")

@bot2.command(name="gir2")
async def cmd_gir2(ctx):
    if ctx.author.id != OWNER_ID:
        return
    if not TARGET_CHANNEL_ID_2:
        await ctx.message.edit(content="❌ Önce kanal ayarlamalısın: `!ayarla2 <id>`")
        return
    await join_channel_2()
    await ctx.message.edit(content="✅ 2. Hesap sese giriş yaptı.")

@bot2.command(name="cik2")
async def cmd_cik2(ctx):
    if ctx.author.id != OWNER_ID:
        return
    global TARGET_CHANNEL_ID_2
    TARGET_CHANNEL_ID_2 = None
    for vc in bot2.voice_clients:
        await vc.disconnect()
    await ctx.message.edit(content="🚪 2. Hesap sesten çıktı ve otomatik bağlama durduruldu.")


# ================= ÇİFT HESAP BAŞLATICI =================

def run_bot1():
    if TOKEN_1:
        bot1.run(TOKEN_1)

def run_bot2():
    if TOKEN_2:
        bot2.run(TOKEN_2)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_bot1)
    t2 = threading.Thread(target=run_bot2)
    
    t1.start()
    t2.start()