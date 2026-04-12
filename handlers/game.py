from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import games

router = Router()

# 🎮 GAME START
@router.message(F.text == "/game")
async def start_game(msg: types.Message):
    game = {
        "chat_id": msg.chat.id,
        "players": [],
        "started": False
    }

    await games.delete_many({"chat_id": msg.chat.id})
    await games.insert_one(game)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Join Game", callback_data="join")]
    ])

    await msg.answer(
        "🎲 Yangi Mafia o‘yini boshlandi!\n\n🎯 O‘yinchilar:\n(yo‘q)",
        reply_markup=kb
    )


# ➕ JOIN
@router.callback_query(F.data == "join")
async def join_game(call: types.CallbackQuery):
    game = await games.find_one({
        "chat_id": call.message.chat.id,
        "started": False
    })

    if not game:
        return await call.answer("O‘yin topilmadi", show_alert=True)

    if call.from_user.id not in game["players"]:
        game["players"].append(call.from_user.id)

        await games.update_one(
            {"_id": game["_id"]},
            {"$set": {"players": game["players"]}}
        )

    text = "🎯 O‘yinchilar:\n"
    for i, user_id in enumerate(game["players"], 1):
        text += f"{i}. <a href='tg://user?id={user_id}'>Player</a>\n"

    await call.message.edit_text(text, parse_mode="HTML")


# ▶️ START (kamida 3 ta player)
@router.message(F.text == "/startgame")
async def real_start(msg: types.Message):
    game = await games.find_one({
        "chat_id": msg.chat.id,
        "started": False
    })

    if not game:
        return

    if len(game["players"]) < 3:
        return await msg.answer("❌ Kamida 3 ta o‘yinchi kerak")

    await games.update_one(
        {"_id": game["_id"]},
        {"$set": {"started": True}}
    )

    await msg.answer("🌙 O‘yin boshlandi!\nRollar tarqatilmoqda...")

    # RANDOM ROLE
    import random

    roles = ["mafia", "doctor", "sheriff"]
    players = game["players"]

    assigned = {}

    for p in players:
        role = random.choice(roles)
        assigned[p] = role

    # PRIVATE MESSAGE
    for user_id, role in assigned.items():
        try:
            await msg.bot.send_message(
                user_id,
                f"🎭 Sizning rolingiz: <b>{role}</b>"
            )
        except:
            pass

    await msg.answer("🌃 Tun boshlandi...")
