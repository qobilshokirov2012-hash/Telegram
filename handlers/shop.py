SHOP = {
    "shield": 40,
    "anti_kill": 50,
    "gun": 60,
    "fake_doc": 70
}
from db import users, add_coins

async def buy_item(uid, item, price):
    user = await users.find_one({"_id": uid})

    if user["coins"] < price:
        return False

    await users.update_one(
        {"_id": uid},
        {
            "$inc": {"coins": -price},
            "$inc": {f"inventory.{item}": 1}
        }
    )
    return True
