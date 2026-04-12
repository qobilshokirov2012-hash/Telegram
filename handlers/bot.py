import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from config import BOT_TOKEN
from game import create_game, join_game, start_game
from db import games

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.text == "/game")
async def game(msg: Message):
    await create_game(msg.chat.id)
    await msg.answer("🎮 Mafia boshlandi! Join qiling: /join")


@dp.message(F.text == "/join")
async def join(msg: Message):
    await join_game(msg.chat.id, msg.from_user.id)
    await msg.answer("✅ Qo‘shildingiz!")


@dp.message(F.text == "/startgame")
async def start(msg: Message):
    roles = await start_game(msg.chat.id)

    for uid, role in roles.items():
        try:
            await bot.send_message(uid, f"🎭 Role: {role}")
        except:
            pass

    await msg.answer("🌙 O‘yin boshlandi!")


@dp.message(F.text == "/status")
async def status(msg: Message):
    game = await games.find_one({"chat_id": msg.chat.id})
    await msg.answer(f"👥 Players: {len(game['players'])}")
    

async def main():
    print("BOT STARTED 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
