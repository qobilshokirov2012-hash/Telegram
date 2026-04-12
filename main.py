async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    users.update_one(
        {"user_id": user.id},
        {"$set": {"name": user.first_name}},
        upsert=True
    )

    await update.message.reply_text("Bot ishlayapti 🚀")
