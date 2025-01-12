import asyncio
from aiogram import Bot

async def test_message():
    bot = Bot(token="7605591332:AAHMNis7iWIfxkpYf5SwC6xcJ1t-9cYBtL8")
    await bot.send_message(chat_id="1259689667", text="Привіт! Бот працює. 🎉")
    await bot.close()

asyncio.run(test_message())