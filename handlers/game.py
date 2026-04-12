import random
from db import games

roles_pool = [
    "mafia",
    "doctor",
    "sheriff",
    "citizen",
    "citizen",
    "citizen"
]

async def create_game(chat_id):
    await games.delete_many({"chat_id": chat_id})
    await games.insert_one({
        "chat_id": chat_id,
        "players": [],
        "started": False,
        "roles": {}
    })

async def join_game(chat_id, user_id):
    game = await games.find_one({"chat_id": chat_id})
    if user_id not in game["players"]:
        game["players"].append(user_id)
    await games.update_one({"chat_id": chat_id}, {"$set": {"players": game["players"]}})

async def start_game(chat_id):
    game = await games.find_one({"chat_id": chat_id})
    players = game["players"]

    random.shuffle(players)
    random.shuffle(roles_pool)

    roles = {}
    for i, p in enumerate(players):
        roles[p] = roles_pool[i % len(roles_pool)]

    await games.update_one(
        {"chat_id": chat_id},
        {"$set": {"roles": roles, "started": True}}
    )

    return roles
import asyncio
from db import games

async def night_phase(chat_id, bot):
    game = await games.find_one({"chat_id": chat_id})

    await bot.send_message(chat_id, "🌙 Tun boshlandi...")

    # mafia action placeholder
    await asyncio.sleep(10)

    await bot.send_message(chat_id, "🌅 Tong otdi...")
    async def day_phase(chat_id, bot):
    await bot.send_message(chat_id, "🏙 Kun boshlandi, muhokama!")

    await asyncio.sleep(20)

    await bot.send_message(chat_id, "🗳 Ovoz berish boshlandi!")
    async def game_loop(chat_id, bot):
    while True:
        await night_phase(chat_id, bot)
        await day_phase(chat_id, bot)
        ROLES = {
    "mafia": "🔪 Mafia",
    "doctor": "💉 Doctor",
    "sheriff": "🕵️ Sheriff",

    "daydi": "🧙🏼‍♂️ Daydi",
    "koldun": "⚡ Koldun",
    "spy": "🦇 Ayg‘oqchi",
    "labarant": "👨‍🔬 Labarant",
    "minior": "☠️ Minior"
        }
async def reward(uid, action):
    if action == "kill":
        await add_coins(uid, 10)
    if action == "win":
        await add_coins(uid, 50)
    if action == "vote_win":
        await add_coins(uid, 5)
