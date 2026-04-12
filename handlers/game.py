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
