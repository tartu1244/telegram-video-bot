import os
import yt_dlp
from telegram.ext import Application, MessageHandler, filters, CommandHandler

TOKEN = os.getenv("7950096945:AAF8fZPhqNcyKaJ8rq_cQ3xiMZ6OhFl66xA")

app = Application.builder().token(TOKEN).build()

def download_video(url):
    ydl_opts = {'outtmpl': 'video.%(ext)s'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def start(update, context):
    await update.message.reply_text("👋 Send me any video link or forward a message containing one!")

async def handle_message(update, context):
    text = update.message.text
    if not text:
        return

    await update.message.reply_text("📥 Downloading your video...")

    try:
        file_path = download_video(text)
        size = os.path.getsize(file_path) / (1024 * 1024)

        if size > 1900:  # 2GB limit
            await update.message.reply_text("⚠️ File too large (over 2GB). Can't send via Telegram.")
        else:
            await update.message.reply_video(video=open(file_path, "rb"))

        os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
