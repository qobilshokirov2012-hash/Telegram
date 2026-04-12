users.update_one(
    {"user_id": update.effective_user.id},
    {"$set": {"name": update.effective_user.first_name}},
    upsert=True
)
