from aiogram import Bot, Dispatcher, F , Router, types
from aiogram.types import Message, CallbackQuery, FSInputFile, InputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.callbackData import parse_callback
from sqlalchemy import select
import os

import app.keyboards as kb
import app.database.requests as rq
from app.database.models import async_session

router_user = Router()
bot = bot = os.getenv("BOT_TOKEN")

# Глобальна змінна для зберігання поточного шляху
BASE_DIR = "FKEP"
current_dir = BASE_DIR

async def browse_folders(message: types.Message):
    """
    Починає перегляд папок і файлів з базової директорії.
    """
    global current_dir
    current_dir = BASE_DIR
    items = kb.get_files_and_folders(current_dir)

    if not items:
        await message.answer("У цій директорії немає файлів чи папок.")
        return

    keyboard = kb.create_file_folder_buttons(current_dir)
    print("Call browse_folders")
    # await message.answer(f"Поточна директорія: {current_dir}", reply_markup=keyboard)

    return keyboard


async def handle_folder_callback(query: CallbackQuery):
    """
    Обробляє вибір файлу або папки через callback.
    """
    global current_dir

    # Розпарсити callback_data
    callback_data = query.data.split(":")
    item_type, item_name = callback_data[0], callback_data[1].replace("_", " ")

    if item_type == "folder":
        # Якщо це папка
        new_dir = os.path.join(current_dir, item_name)

        if not os.path.exists(new_dir):
            await query.message.answer(f"Директорія {item_name} не знайдена.")
            return

        current_dir = new_dir
        items = kb.get_files_and_folders(current_dir)

        if not items:
            await query.message.edit_text(f"У директорії {item_name} немає файлів чи папок.")
            return

        keyboard = kb.create_file_folder_buttons(current_dir)
        print("Call handle_folder_callback")
        await query.message.edit_text(f"Поточна директорія: {current_dir}", reply_markup=keyboard)
    elif item_type == "file":
        # Якщо це файл
        print(f"До: {item_name}")
        file_name = item_name.replace(" ", "_")
        print(f"Після: {file_name}")
        file_path = os.path.join(current_dir, file_name)

        if os.path.exists(file_path):
            try:
                file = FSInputFile(file_path)
                await query.message.answer_document(file)
            except Exception as e:
                await query.message.answer(f"Помилка під час надсилання файлу: {str(e)}")
        else:
            await query.message.answer(f"Файл '{file_name}' не знайдено.")

    # Відповісти на callback
    await query.answer()


@router_user.callback_query(F.data == "back_to_FKEP")
async def back_to_FKEP(callback: CallbackQuery):
    """
    Обробляє повернення до базової директорії.
    """
    global current_dir
    current_dir = BASE_DIR
    print(f"Current_dir: {current_dir}")
    keyboard = kb.create_file_folder_buttons(current_dir)
    await callback.message.edit_text(
        
        "У вас є можливість надіслати 5 завданнь, яких ще немає в боті і получити - допомогу адміністратора з презинтацією, практичною з графічного дизайну, вебсайтом, грою на python, лабораторна з Технологій\n\n"
        "Будь ласка не скидуйте завдання від Балабаника, у неї так всі завдання в мудлі\n\n"
        f"Повернуто до базової директорії: {current_dir}", reply_markup=keyboard)

# Надіслати документ адміністрації

DOWNLOADS_PATH = "downloads" 

if not os.path.exists(DOWNLOADS_PATH):
    os.makedirs(DOWNLOADS_PATH)

class SendDocument(StatesGroup):
    document = State()
    description = State()

@router_user.callback_query(lambda c: c.data == "to_send_content")
async def start_register(callback: CallbackQuery, state: FSMContext):
    await state.update_data(tg_id=callback.from_user.id)
    await state.set_state(SendDocument.document)
    await callback.message.answer("Надішліть ваш документ в форматі архіву")
    await callback.answer()  # Закриваємо сповіщення
    await bot.answer_callback_query(callback.id)

@router_user.message(SendDocument.document)
async def register_document(message: Message, state: FSMContext):
    if not message.document:
        await message.answer("Будь ласка, надішліть файл.")
        return

    # Завантаження документа з Telegram
    file_info = await bot.get_file(message.document.file_id)
    file_bytes_io = await bot.download_file(file_info.file_path)

    # Збереження документа в стані
    await state.update_data(file_bytes=file_bytes_io.read())
    await state.set_state(SendDocument.description)
    await message.answer("Файл отримано. Введіть опис")

@router_user.message(SendDocument.description)
async def register_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    
    tg_id = data.get('tg_id', message.from_user.id)  # Отримуємо tg_id з користувача
    file_bytes = data.get("file_bytes")  # Шлях до файлу
    description = message.text  # Опис

    # Формуємо ім'я файлу з tg_id і описом
    safe_description = description.replace(" ", "_").replace("/", "_")
    file_name = f'{tg_id}_{safe_description}.zip'
    file_path = os.path.join(DOWNLOADS_PATH, file_name)

    with open(file_path, "wb") as file:
        file.write(file_bytes)

    # Логіка для подальшої обробки файлу (за необхідності)
    await message.answer(
        f"Ваше завдання збережено.\n"
        f"Шлях до файлу: {file_name}\n"
    )
    
    await state.clear()


# Профіль користувача
class GetUserInfo(StatesGroup):
    user_id = State()

@router_user.callback_query(lambda c: c.data == "to_check_progress")
async def check_user_progress(callback: CallbackQuery):
    tg_id = callback.from_user.id  # Автоматично отримуємо Telegram ID користувача

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(rq.User).where(rq.User.tg_id == tg_id))
            user = result.scalars().first()

    if user:
        user_info = (
            f"👤 Інформація про ваш профіль:\n"
            f"ID: {user.id}\n"
            f"Telegram ID: {user.tg_id}\n"
            f"Прогрес: {user.progress}\n"
            f"Бонуси: {user.bonus}"
        )
        await callback.message.answer(user_info)
    else:
        await callback.message.answer("❌ Ваш профіль не знайдено в базі даних. Можливо, ви ще не зареєстровані.")

    await callback.answer()  # Закриваємо сповіщення

# Heandler на головну
@router_user.callback_query(lambda c: c.data == "to_main")
async def to_main(callback: CallbackQuery):
    await callback.message.answer("Ви повернулись на головну сторінку.")
    await callback.answer()
    await callback.message.answer('Виберіть нижче курс який вас цікавить:', reply_markup=kb.course)
    await bot.answer_callback_query(callback.id)
