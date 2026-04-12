import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! 🤖 Anime botga xush kelibsiz!\n/anime bosing 🎴")

async def anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.waifu.pics/sfw/waifu"
    res = requests.get(url).json()
    await update.message.reply_photo(photo=res["url"])

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anime", anime))

    app.run_polling()

if __name__ == "__main__":
    main()
