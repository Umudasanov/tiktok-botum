import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp

# --- TOKENİNİ BURAYA YAZ ---
API_TOKEN = '8576929907:AAF8Ncpj04JYRuzxh-jk5iwEthSENLBKtUg' 

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
    await message.answer(f"Salam {message.from_user.first_name}! Linki göndər, yükləyim. ✨")

@dp.message()
async def handle_message(message: types.Message):
    url = message.text
    if url and ("tiktok.com" in url or "instagram.com" in url):
        temp_msg = await message.answer("Yüklənir, gözləyin...")
        try:
            await asyncio.to_thread(download_video, url)
            video_file = types.FSInputFile("video.mp4")
            await message.answer_video(video_file)
            if os.path.exists("video.mp4"): os.remove("video.mp4")
            await temp_msg.delete()
        except Exception as e:
            await message.answer("Xəta baş verdi. Linki yoxlayın.")
    else:
        await message.answer("Zəhmət olmasa düzgün link göndərin.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
