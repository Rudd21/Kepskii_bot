import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message ,InlineKeyboardButton, CallbackQuery
from aiogram import Router
from dotenv import load_dotenv
from app.config import bot, dp, admin_id
import os

from app.handlers import router_user, browse_folders, handle_folder_callback
from app.admin_handlers import router_admin
from app.database.models import async_main
import app.keyboards as kb

import app.handlers as h

load_dotenv()


@dp.callback_query()
async def handle_callback(query: CallbackQuery, state: FSMContext):
    print("Callback_Query відпрацював")

    if query.data == "back_to_FKEP":
        await h.back_to_FKEP(query)
    else:
        await h.handle_folder_callback(query, state) 
        print(f"Отримано callback_data: {query.data}")

current_dir = h.BASE_DIR

async def main():
    await async_main()
    bot = Bot(token='7605591332:AAHMNis7iWIfxkpYf5SwC6xcJ1t-9cYBtL8')

    dp.include_router(router_user)
    dp.include_router(router_admin)

    @dp.message(CommandStart())
    async def check_user(message: types.Message):

        """Визначення ролі користувача"""
        if message.from_user.id == admin_id:
            await message.answer(
                "Oh, Hello moderator!😏\n"
                "Команди для керування:\n\n"
                "/set_path_to_save_document - встановити шлях до папки з якою хочете взаємодіяти\n"
                "/original_path - вернутись до головної папки\n"
                "/add_file - додати завдання в папку\n"
                "/add_folder <Ім'я папки> - додати папку\n"
                "/send_message - надіслати інформацію користувачу\n"
                "/to_send_document - надіслати документ користувачу\n"
                "/download_all_files - завантажити всі файли які були відправлені на перевірку\n"
                "/get_user_info - провірити дані користувача\n"
                "/update_user - видати користувачу бонуси")
        else:
            keyboard = await h.browse_folders(message)
            await message.answer(                
                "Привіт!🤩\n\n"
                "Це бот для студентів КЕПу\n"
                "Тут можна знайти конрольні, лабораторні, самостійні роботи раніше терміну:\n\n"
                "У вас є можливість надіслати 5 завданнь, яких ще немає в боті і получити - допомогу адміністратора з презинтацією, практичною з графічного дизайну, вебсайтом, грою на python, лабораторна з Технологій\n\n"
                "Будь ласка не скидуйте завдання від Балабаника, у неї так всі завдання в мудлі\n", reply_markup=keyboard)

        
    """
    Головна функція запуску бота.
    """
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот відключений!")

