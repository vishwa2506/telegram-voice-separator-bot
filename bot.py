import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from spleeter.separator import Separator
import subprocess

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Bot Token environment variable එකෙන් ගන්න

separator = Separator('spleeter:2stems')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me an MP3 file, I'll separate voice and music for you.")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.audio.get_file()
    file_path = f"{file.file_id}.mp3"
    await file.download_to_drive(file_path)
    await update.message.reply_text("Processing your file, please wait...")

    try:
        output_dir = f"./separated_{file.file_id}"
        separator.separate_to_file(file_path, output_dir)

        voice_path = os.path.join(output_dir, 'vocals.wav')
        music_path = os.path.join(output_dir, 'accompaniment.wav')

        voice_mp3 = f"voice_{file.file_id}.mp3"
        music_mp3 = f"music_{file.file_id}.mp3"

        subprocess.run(['ffmpeg', '-y', '-i', voice_path, voice_mp3], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['ffmpeg', '-y', '-i', music_path, music_mp3], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        await update.message.reply_audio(audio=open(voice_mp3, 'rb'), caption='Here is the voice track.')
        await update.message.reply_audio(audio=open(music_mp3, 'rb'), caption='Here is the background music.')

        os.remove(file_path)
        os.remove(voice_mp3)
        os.remove(music_mp3)
        subprocess.run(['rm', '-rf', output_dir])

    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))

    print("Bot is running...")
    app.run_polling()
