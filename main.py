import os
import discord
from discord.ext import commands

# Self-bot istemcisini oluşturuyoruz (self_bot=True burada kritik)
bot = commands.Bot(command_prefix="!", self_bot=True)

# Token'ı Railway Environment Variables (Variables) kısmından alıyoruz
TOKEN = os.getenv("TOKEN")

@bot.event
async def on_ready():
    print(f"Giriş yapıldı: {bot.user} (ID: {bot.user.id})")
    
    # Sese bağlanmak istediğin kanalın ID'si
    CHANNEL_ID = 1536785743014527076  
    
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.connect(self_deaf=True, self_mute=True)
            print(f"Başarıyla {channel.name} ses kanalına girildi!")
        else:
            print("Kanal bulunamadı!")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

# Token kontrolü ekleyerek güvenliği artırıyoruz
if __name__ == "__main__":
    if not TOKEN:
        print("HATA: TOKEN çevresel değişkeni (environment variable) bulunamadı!")
    else:
        bot.run(TOKEN)
