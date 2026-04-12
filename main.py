import os
from pymongo import MongoClient

MONGO = os.getenv("MONGO_URL")
client = MongoClient(MONGO)

db = client["anime_bot"]
users = db["users"]
