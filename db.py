from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.mafia

users = db.users
games = db.games
async def get_user(uid):
    u = await users.find_one({"_id": uid})
    if not u:
        u = {"_id": uid, "coins": 0}
        await users.insert_one(u)
    return u

async def add_coins(uid, amount):
    await users.update_one({"_id": uid}, {"$inc": {"coins": amount}})
# game ichiga qo‘shiladi
# votes: {user_id: target_id}
async def reward(uid, action):
    if action == "kill":
        await add_coins(uid, 10)
    if action == "win":
        await add_coins(uid, 50)
    if action == "vote_win":
        await add_coins(uid, 5)
