from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "/shop")
async def shop(msg: Message):
    await msg.answer("🛒 Shop ochildi")
