import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
admin_id = 5815674712

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
