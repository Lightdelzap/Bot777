import os
import tempfile
import shutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from yt_dlp import YoutubeDL

# Paste your bot token here
BOT_TOKEN = "8210076404:AAGLKLh02zvo-kmTJYwAbESCis-4DIkiurA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Send /song <song name> to download music as MP3!")

async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /song <song name>")
        return

    query = " ".join(context.args)
    msg = await update.message.reply_text(f"🔍 Searching for '{query}'... please wait ⏳")

    tmpdir = tempfile.mkdtemp()
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "default_search": "ytsearch1",
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if "entries" in info:
                info = info["entries"][0]
            title = info.get("title", "Unknown Song")
            filename = ydl.prepare_filename(info)
            mp3_file = os.path.splitext(filename)[0] + ".mp3"

        await msg.edit_text(f"🎧 Sending '{title}'...")
        await update.message.reply_audio(audio=open(mp3_file, "rb"), title=title)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("song", song))
    print("✅ Music Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
