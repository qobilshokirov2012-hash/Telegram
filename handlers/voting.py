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
