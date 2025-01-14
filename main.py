import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, Message ,InlineKeyboardButton, CallbackQuery
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram import Router
from dotenv import load_dotenv
import os

from app.handlers import router_user, browse_folders, handle_folder_callback
from app.admin_handlers import router_admin
from app.database.models import async_main
import app.keyboards as kb

import app.handlers as h

load_dotenv(dotenv_path="C:/Users/Taras/Desktop/SamKepskiiBOT/.venv/.env")
# admin_id = 1259689667
PORT = int(os.getenv("PORT", 8080))
admin_id = 5815674712

RENDER_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}:{PORT}/webhook"

WEBAPP_HOST = "0.0.0.0"  # Хост для запуску
WEBAPP_PORT = PORT        # Порт для запуску

dp = Dispatcher()
bot = Bot(token=os.getenv("BOT_TOKEN"))

o = "OOOOOO"

@dp.callback_query()
async def handle_callback(query: CallbackQuery):
    """
    Обробляє callback від кнопок.
    """
    print("Callback_Query відпрацював")
    if query.data == "back_to_FKEP":
        await h.back_to_FKEP(query)
    else:
        await h.handle_folder_callback(query)
        print(f"Отримано callback_data: {query.data}")

current_dir = h.BASE_DIR


# Функції запуску і завершення роботи

SHUTDOWN_ENABLED = False  # Спочатку вимкнено
shutdown_delay = 15 * 60  # 15 хвилин в секундах

async def delayed_shutdown():
    global SHUTDOWN_ENABLED
    await asyncio.sleep(shutdown_delay)
    SHUTDOWN_ENABLED = True
    print("SHUTDOWN_ENABLED змінено на True через 15 хвилин")

async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Вебхук встановлено: {WEBHOOK_URL}")

async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    print("Вебхук видалено")

async def main():
    await async_main()  # Ініціалізація бази даних

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
                "/delete_item <Iм'я папки> - видалити папку або файл"
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
                "Команди:\n"
                "/to_send_content - надіслати контект адміністрації\n"
                "/to_check_progress - перевірка кількості своїх скинутих завданнь\n\n"
                "Будь ласка не скидуйте завдання від Балабаника, у неї і так всі завдання в мудлі\n", reply_markup=keyboard)

        
        # await h.browse_folders(message)
    """
    Головна функція запуску бота.
    """
    # await dp.start_polling(bot)

# Налаштування сервера aiohttp
async def create_app():
    app = web.Application()

    # Реєструємо маршрути Aiogram
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

    # Налаштовуємо старт
    app.on_startup.append(lambda _: asyncio.create_task(on_startup()))

    # Запускаємо асинхронну задачу для 15 хвилин
    asyncio.create_task(delayed_shutdown())

    # Додаємо on_shutdown тільки якщо SHUTDOWN_ENABLED True
    if SHUTDOWN_ENABLED:
        app.on_shutdown.append(lambda _: asyncio.create_task(on_shutdown()))

    # Інтегруємо Dispatcher
    setup_application(app, dp)
    return app

if __name__ == "__main__":
    try:
        web.run_app(create_app(), host="0.0.0.0", port=PORT)
    except KeyboardInterrupt:
        print("Бот відключений!")

