import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from config import BOT_TOKEN
from game import create_game, join_game, start_game
from db import games

# 🤖 BOT + DISPATCHER
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🧩 ROUTERS (shop + voting)
from voting import router as voting_router
from shop import router as shop_router

dp.include_router(voting_router)
dp.include_router(shop_router)

# =========================
# 🚀 START COMMAND
# =========================
@dp.message(F.text == "/start")
async def start(msg: Message):
    await msg.answer(
        "👋 Mafia botga xush kelibsiz!\n\n"
        "🎮 O‘yin boshlash uchun /game yozing"
    )

# =========================
# 🎮 CREATE GAME
# =========================
@dp.message(F.text == "/game")
async def game(msg: Message):
    await create_game(msg.chat.id)
    await msg.answer("🎮 Mafia boshlandi!\n/join yozing")

# =========================
# ➕ JOIN GAME
# =========================
@dp.message(F.text == "/join")
async def join(msg: Message):
    await join_game(msg.chat.id, msg.from_user.id)
    await msg.answer("✅ Siz o‘yinga qo‘shildingiz")

# =========================
# 🌙 START GAME (ROLES)
# =========================
@dp.message(F.text == "/startgame")
async def startgame(msg: Message):
    roles = await start_game(msg.chat.id)

    if not roles:
        return await msg.answer("❌ Kamida 3 ta o‘yinchi kerak")

    # 📩 ROLE SENDING
    for uid, role in roles.items():
        try:
            await bot.send_message(
                uid,
                f"🎭 Sizning rolingiz: {role}"
            )
        except:
            pass

    await msg.answer("🌙 O‘yin boshlandi!")

# =========================
# 📊 STATUS
# =========================
@dp.message(F.text == "/status")
async def status(msg: Message):
    game = await games.find_one({"chat_id": msg.chat.id})

    if not game:
        return await msg.answer("❌ Hozircha game yo‘q")

    await msg.answer(f"👥 Players: {len(game['players'])}")

# =========================
# 🚀 START BOT
# =========================
async def main():
    print("🚀 PRO MAFIA BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
