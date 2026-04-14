import random
from db import games

ROLES = ["mafia", "doctor", "sheriff", "citizen", "citizen", "citizen"]

async def create_game(chat_id):
    await games.delete_many({"chat_id": chat_id})
    await games.insert_one({
        "chat_id": chat_id,
        "players": [],
        "started": False,
        "roles": {}
    })

async def join_game(chat_id, uid):
    game = await games.find_one({"chat_id": chat_id})
    if uid not in game["players"]:
        game["players"].append(uid)

    await games.update_one(
        {"chat_id": chat_id},
        {"$set": {"players": game["players"]}}
    )

async def start_game(chat_id):
    game = await games.find_one({"chat_id": chat_id})
    players = game["players"]

    if len(players) < 3:
        return None

    random.shuffle(players)

    roles = {}
    for i, p in enumerate(players):
        roles[p] = ROLES[i % len(ROLES)]

    await games.update_one(
        {"chat_id": chat_id},
        {"$set": {"roles": roles, "started": True}}
    )

    return roles
