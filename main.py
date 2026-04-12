from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from pymongo import MongoClient
import os

TOKEN = os.getenv("BOT_TOKEN")
MONGO = os.getenv("MONGO_URL")

# MongoDB
client = MongoClient(MONGO)
db = client["anime_bot"]
users = db["users"]

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user

        users.update_one(
            {"user_id": user.id},
            {"$set": {"name": user.first_name}},
            upsert=True
        )

        await update.message.reply_text("🎌 Bot ishlayapti!")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# MAIN BOT
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
