import asyncio
import logging
import os
import time
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp

# --- AYARLAR ---
API_TOKEN = '8576929907:AAF8Ncpj04JYRuzxh-jk5iwEthSENLBKtUg' # Öz tokenini daxil et

WAITING_STICKERS = [
    "https://t.me/addstickers/xaliqmustafayev4", # Bura stiker ID-lərini qoy
]
# ---------------

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salam mən Umud Hasanov tiktok və ya instaqram video linkini göndərin videonuzu yükləyim. ✨")

@dp.message()
async def handle_message(message: types.Message):
    url = message.text
    if url and ("tiktok.com" in url or "instagram.com" in url):
        start_time = time.time() # Vaxtı başlat
        
        # Stiker göndərmək
        sticker_msg = None
        if WAITING_STICKERS:
            random_sticker = random.choice(WAITING_STICKERS)
            try:
                sticker_msg = await message.answer_sticker(random_sticker)
            except:
                pass # ID səhvdirsə bot dayanmasın
            
        temp_msg = await message.answer("Video işlənir, zəhmət olmasa gözləyin... 🚀")
        
        try:
            # Yükləmə prosesi
            await asyncio.to_thread(download_video, url)
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            video_file = types.FSInputFile("video.mp4")
            await message.answer_video(
                video_file, 
                caption=f"✅ Hazırdır!\n\n⏱ Yükləmə vaxtı: {duration} saniye"
            )
            
            # Təmizlik
            if os.path.exists("video.mp4"):
                os.remove("video.mp4")
            await temp_msg.delete()
            if sticker_msg:
                await sticker_msg.delete()
                
        except Exception as e:
            await message.answer(f"Hata oluştu: {e}")
    else:
        await message.answer("@umudhasanovtm sizdən xahiş edir keçərli bir TikTok veya Instagram linki göndərin. 🤐")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot durduruldu")