import os
import random
import requests
from pymongo import MongoClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")
OWNER_ID = int(os.getenv("OWNER_ID"))

client = MongoClient(MONGO_URL)
db = client["animebot"]
users = db["users"]

def save_user(user_id):
    if not users.find_one({"user_id": user_id}):
        users.insert_one({"user_id": user_id})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    await update.message.reply_text(
        "🎌 Anime Botga xush kelibsiz!\n\n"
        "/anime Naruto\n"
        "/random\n"
        "/top"
    )

async def anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Anime nomini yozing.\nMisol: /anime Naruto")
        return

    query = " ".join(context.args)

    url = f"https://api.jikan.moe/v4/anime?q={query}&limit=1"
    r = requests.get(url).json()

    if not r["data"]:
        await update.message.reply_text("Anime topilmadi.")
        return

    a = r["data"][0]

    text = f"""
🎬 {a['title']}
⭐ Reyting: {a.get('score')}
📺 Qism: {a.get('episodes')}
📅 Status: {a.get('status')}
🎭 Janr: {a['genres'][0]['name'] if a['genres'] else 'Nomaʼlum'}
"""

    await update.message.reply_photo(photo=a["images"]["jpg"]["image_url"], caption=text)

async def random_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    page = random.randint(1, 20)
    url = f"https://api.jikan.moe/v4/top/anime?page={page}"
    r = requests.get(url).json()
    a = random.choice(r["data"])

    text = f"""
🎲 Random Anime

🎬 {a['title']}
⭐ {a.get('score')}
📺 {a.get('episodes')}
"""

    await update.message.reply_photo(photo=a["images"]["jpg"]["image_url"], caption=text)

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.jikan.moe/v4/top/anime?limit=10"
    r = requests.get(url).json()

    msg = "🏆 Top 10 Anime:\n\n"

    for i, a in enumerate(r["data"], start=1):
        msg += f"{i}. {a['title']} ⭐ {a.get('score')}\n"

    await update.message.reply_text(msg)

async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    count = users.count_documents({})
    await update.message.reply_text(f"👥 Foydalanuvchilar: {count}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("anime", anime))
app.add_handler(CommandHandler("random", random_anime))
app.add_handler(CommandHandler("top", top))
app.add_handler(CommandHandler("users", users_count))

print("Bot ishga tushdi...")
app.run_polling()
