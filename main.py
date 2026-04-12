import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# 🔘 Tugmalar
def get_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎴 Random Anime", callback_data="anime")],
        [InlineKeyboardButton("❤️ Waifu", callback_data="waifu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 🤖 Anime botga xush kelibsiz!\nTugmalardan birini tanlang 👇",
        reply_markup=get_keyboard()
    )

# 🎴 Anime rasmi
def get_anime():
    url = "https://api.waifu.pics/sfw/waifu"
    return requests.get(url).json()["url"]

# 🔁 Tugma bosilganda
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    img = get_anime()
    await query.message.reply_photo(photo=img)

# /anime komandasi
async def anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    img = get_anime()
    await update.message.reply_photo(photo=img)

# 🚀 Bot ishga tushishi
def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN topilmadi!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anime", anime))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot ishga tushdi 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
