import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "BU_YERGA_TOKENING"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom! 🤖 Anime botga xush kelibsiz!\n/anime bosing 🎴")

def anime(update: Update, context: CallbackContext):
    url = "https://api.waifu.pics/sfw/waifu"
    res = requests.get(url).json()
    img = res["url"]
    update.message.reply_photo(photo=img)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("anime", anime))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
