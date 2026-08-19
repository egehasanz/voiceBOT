import os
import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", self_bot=True)
TOKEN = os.getenv("TOKEN")

@bot.event
async def on_ready():
    print(f"Giriş yapıldı: {bot.user} (ID: {bot.user.id})")
    
    # Gateway ve önbelleğin tamamen oturması için 3 saniye bekliyoruz
    await asyncio.sleep(3)
    
    CHANNEL_ID = 1486461566554472579  
    
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.connect(self_deaf=True, self_mute=True)
            print(f"Başarıyla {channel.name} ses kanalına girildi!")
        else:
            print("Kanal bulunamadı!")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    if not TOKEN:
        print("HATA: TOKEN çevresel değişkeni bulunamadı!")
    else:
        bot.run(TOKEN)
