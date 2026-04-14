from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "/vote")
async def vote(msg: Message):
    await msg.answer("🗳 Ovoz berish boshlandi")
