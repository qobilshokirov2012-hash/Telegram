from db import games

async def vote(chat_id, voter, target):
    game = await games.find_one({"chat_id": chat_id})

    if "votes" not in game:
        game["votes"] = {}

    game["votes"][str(voter)] = target

    await games.update_one(
        {"chat_id": chat_id},
        {"$set": {"votes": game["votes"]}}
    )
from collections import Counter

async def calculate_votes(game):
    votes = game.get("votes", {})
    count = Counter(votes.values())

    if not count:
        return None

    target = count.most_common(1)[0][0]
    return int(target)
