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
