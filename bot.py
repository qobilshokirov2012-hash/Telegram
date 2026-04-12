import asyncio
import os
from aiogram import Bot, Dispatcher

BOT_TOKEN = os.getenv("BOT_MAFIA")  # 👈 Railway variable

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def hello(msg):
    await msg.answer("Bot ishlayapti 🚀")

async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
