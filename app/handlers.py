from aiogram import Bot, Dispatcher, F , Router, types
from aiogram.types import Message, CallbackQuery, FSInputFile, InputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from app.config import bot, admin_id
import os

import app.keyboards as kb
import app.database.requests as rq
from app.database.models import async_session

router_user = Router()

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

    return keyboard


async def process_callback(callback_data: str, query: CallbackQuery, current_dir: str, state: FSMContext = None):
    if ":" in callback_data:
        item_type, item_name = callback_data.split(":", 1)
        item_name = item_name.replace("_", " ")

        if item_type == "folder":
            new_dir = os.path.join(current_dir, item_name)
            if not os.path.exists(new_dir):
                await query.message.answer(f"Директорія {item_name} не знайдена.")
                return current_dir
            current_dir = new_dir
            items = kb.get_files_and_folders(current_dir)
            if not items:
                await query.message.edit_text(f"У директорії {item_name} немає файлів чи папок.")
                return current_dir
            keyboard = kb.create_file_folder_buttons(current_dir)
            await query.message.edit_text(f"Поточна директорія: {current_dir}", reply_markup=keyboard)
            return current_dir

        elif item_type == "file":
            file_path = os.path.join(current_dir, item_name.replace(" ", "_"))
            if os.path.exists(file_path):
                try:
                    await query.message.answer_document(FSInputFile(file_path))
                except Exception as e:
                    await query.message.answer(f"Помилка під час надсилання файлу: {str(e)}")
            else:
                await query.message.answer(f"Файл '{item_name}' не знайдено.")
            return current_dir

    else:
        if callback_data == "file_to_admin" and state is not None:
            await state.update_data(id_user=query.from_user.id)
            await state.set_state(SendTask.file_user)
            await query.message.answer("Надішліть файл та текст з поясненням")
        else:
            await query.message.answer(f"Невідома дія: {callback_data}")

    await query.answer()
    return current_dir

@router_user.callback_query()
async def handle_folder_callback(query: CallbackQuery, state: FSMContext):
    global current_dir
    current_dir = await process_callback(query.data, query, current_dir, state)


class SendTask(StatesGroup):
    file_user = State()
    text_user = State()

@router_user.callback_query(F.data == "file_to_admin")
async def back_to_FKEP(state: FSMContext, callback: CallbackQuery):
    """
    Надсилає адміністрації файл.
    """
    await state.update_data(id_user = callback.from_user.id)

    await state.set_state(SendTask.file_user)

    await callback.message.answer("Надішліть файл")

@router_user.message(SendTask.file_user)
async def get_file(message: Message, state: FSMContext):
    if not message.document:
        print("Надішліть саме ФАЙЛ!")
        return
    
    file = message.document.file_id

    await state.update_data(file_user = file)

    await message.answer("Надішліть текст пояснення")
    await state.set_state(SendTask.text_user)

@router_user.message(SendTask.text_user)
async def get_text(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    id_user = data['id_user']
    file_user = data['file_user']
    text = message.text 

    caption = (
        "Нове повідомлення!\n"
        f"Користувач: {id_user}\n"
        f"Пояснення: \n{text}"
    )

    await bot.send_document(chat_id=admin_id, document=file_user, caption=caption)

    await message.answer("Завдання надіслане адміністрації. Дякуєм!")

    await state.clear()


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
