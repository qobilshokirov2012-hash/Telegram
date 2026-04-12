import os

TOKEN = os.getenv("BOT_TOKEN")

print("TOKEN:", TOKEN)

from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
