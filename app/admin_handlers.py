<<<<<<< HEAD
from aiogram import Bot, Router, types
from aiogram.types import Message, FSInputFile
from sqlalchemy import select
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.database.models import async_session
=======
from aiogram import Bot, Dispatcher, F , Router, types
from aiogram.types import Message, CallbackQuery, FSInputFile, InputFile, Document
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.database.models import Content, async_session
from dotenv import load_dotenv
import tempfile
from io import BytesIO
import aiofiles
>>>>>>> 1587da78b16037c3502743504a3705f87a115717
import os

import app.keyboards as kb
import app.database.requests as rq

router_admin = Router()

<<<<<<< HEAD
=======
load_dotenv(dotenv_path="C:/Users/Taras/Desktop/SamKepskiiBOT/.venv/.env")

>>>>>>> 1587da78b16037c3502743504a3705f87a115717
# Додавання завдання до бази даних

ADD_TASK_PATH = r"FKEP"
CHECK_ADD_TASK_PATH = ADD_TASK_PATH

class AddTaskStates(StatesGroup):
    waiting_for_input = State()

@router_admin.message(Command('set_path_to_save_document'))
async def add_task(message: Message, state: FSMContext):
    if not os.path.exists(CHECK_ADD_TASK_PATH):
        await message.answer(f"Шлях {CHECK_ADD_TASK_PATH} не існує.")
        return
    
    await message.answer(
        "Введіть наступну папку в яку ви би хотіли зберегти документ\n\n"
        f"Початкова папка: {CHECK_ADD_TASK_PATH}"
    )
    await state.set_state(AddTaskStates.waiting_for_input)

@router_admin.message(AddTaskStates.waiting_for_input)
async def check_file(message: Message, state: FSMContext):
    global CHECK_ADD_TASK_PATH

    await state.update_data(waiting_for_input=message.text)
    data = await state.get_data()
    
    if not os.path.exists(CHECK_ADD_TASK_PATH):
        await message.answer(f"Шлях {CHECK_ADD_TASK_PATH} не існує.")
        return
    
    file_names = os.listdir(CHECK_ADD_TASK_PATH)
    directories = [folder for folder in file_names if os.path.isdir(os.path.join(CHECK_ADD_TASK_PATH, folder))]

    if not directories:
        await message.answer("У цій папці немає підкаталогів.")
        await state.clear()
        return

    next_name = data.get('waiting_for_input')
    if next_name in directories:
        CHECK_ADD_TASK_PATH = os.path.join(CHECK_ADD_TASK_PATH, next_name)
        await message.answer(f"Шлях оновлено до: {CHECK_ADD_TASK_PATH}")
    else:
        await message.answer(f"Цієї папки не існує. Можливість встановлювати шлях прирвалась. Встановлений шлях {CHECK_ADD_TASK_PATH}")
        await state.clear()

@router_admin.message(Command('add_file'))
async def save_document(message: Message, bot: Bot):
    global CHECK_ADD_TASK_PATH

    # Перевіряємо, чи повідомлення містить документ
    if not message.document:
        await message.answer("Це повідомлення не містить документ.")
        return

    # Нормалізуємо шлях
    normalized_path = os.path.normpath(CHECK_ADD_TASK_PATH)

    # Перевіряємо, чи існує папка
    if not os.path.exists(normalized_path):
        await message.answer(f"Шлях {normalized_path} не існує. Документ не збережено.")
        return

    # Отримуємо файл за допомогою file_id
    document = message.document
    file_info = await bot.get_file(document.file_id)
    file_content = await bot.download_file(file_info.file_path)

    # Створюємо повний шлях до файлу
    file_path = os.path.join(normalized_path, document.file_name)

    # Записуємо файл
    with open(file_path, 'wb') as file:
        file.write(file_content.read())  # Використовуємо .read() для отримання байтів із BytesIO

    await message.answer(f"Документ збережено у {normalized_path}.")

# Створити папку в базі даних

@router_admin.message(Command('add_folder'))
async def add_folder(message: Message):
    global CHECK_ADD_TASK_PATH

    # Отримуємо ім'я нової папки з повідомлення
    folder_name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not folder_name:
        await message.answer("Вкажіть ім'я папки після команди.")
        return

    # Створюємо повний шлях до нової папки
    new_folder_path = os.path.join(CHECK_ADD_TASK_PATH, folder_name)

    # Створюємо папку, якщо її не існує
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        await message.answer(f"Папка '{folder_name}' створена за шляхом: {new_folder_path}.")
    else:
        await message.answer(f"Папка '{folder_name}' вже існує за шляхом: {new_folder_path}.")

    CHECK_ADD_TASK_PATH = new_folder_path

<<<<<<< HEAD
=======
# Видалити файл або папку в базі даних

@router_admin.message(Command('delete_item'))
async def delete_item(message: Message):
    global CHECK_ADD_TASK_PATH

    # Отримуємо ім'я файлу або папки з повідомлення
    item_name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not item_name:
        await message.answer("Вкажіть ім'я файлу або папки після команди.")
        return

    # Створюємо повний шлях до файлу або папки
    item_path = os.path.join(CHECK_ADD_TASK_PATH, item_name)

    # Перевіряємо, чи існує файл або папка
    if os.path.exists(item_path):
        try:
            # Якщо це файл, видаляємо його
            if os.path.isfile(item_path):
                os.remove(item_path)
                await message.answer(f"Файл '{item_name}' видалено.")
            # Якщо це папка, видаляємо її рекурсивно
            elif os.path.isdir(item_path):
                import shutil
                shutil.rmtree(item_path)
                await message.answer(f"Папка '{item_name}' видалена.")
        except Exception as e:
            await message.answer(f"Сталася помилка під час видалення: {e}")
    else:
        await message.answer(f"Файл або папка '{item_name}' не існує за шляхом: {item_path}.")


>>>>>>> 1587da78b16037c3502743504a3705f87a115717
# Функція вертає корінь бази даних

@router_admin.message(Command('original_path'))
async def return_original_path(message: Message):
    global CHECK_ADD_TASK_PATH
    CHECK_ADD_TASK_PATH = ADD_TASK_PATH 
    await message.answer(f'Корінь папки вернувся до {CHECK_ADD_TASK_PATH}')

# Надсилання завдання адміністратору

DOWNLOADS_PATH = "downloads"

# @router_admin.message(Command('download_all_files'))
# async def handle_download_all_files(callback: types.CallbackQuery):
#     async with async_session() as session:
#         await rq.download_all_files_from_db(callback, session)

@router_admin.message(Command('download_all_files'))
async def send_all_files(message: Message):
    if not os.path.exists(DOWNLOADS_PATH):
        await message.answer('Папки downloads не існує')
        return
    
    files = os.listdir(DOWNLOADS_PATH)
    if not files:
        await message.answer('Папка downloads пуста!')
        return
    
    for file_name in files:
        file_path = os.path.join(DOWNLOADS_PATH, file_name)
        if os.path.isfile(file_path):
            file = FSInputFile(file_path)
            await message.answer_document(file)

    for file_name in files:
        file_path = os.path.join(DOWNLOADS_PATH, file_name)
        try:
            os.remove(file_path)
        except Exception as e:
            await message.answer(f"Невдалось видалити файл '{file_path}': {e}")

    await message.answer('Усі файли було відправлено та папку очищено!')

# Надсилання відповіді користувачу
class SendDocument(StatesGroup):
    user_id = State()
    message = State()

@router_admin.message(Command('send_message'))
async def message_id(message: Message, state: FSMContext):
    await message.answer('Надішліть id користувача:')
    await state.set_state(SendDocument.user_id)

@router_admin.message(SendDocument.user_id)
async def message_text(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Будь ласка, введіть коректний числовий ID користувача.')
        return
    await state.update_data(user_id=message.text)
    await message.answer('Надішліть текст повідомлення:')
    await state.set_state(SendDocument.message)

@router_admin.message(SendDocument.message)
async def send_message_to_user(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id = int(data['user_id'])
    message_text = "Відповідь адміністратора: " + message.text

    try:
        await bot.send_message(user_id, message_text, parse_mode="HTML")
        await message.answer('Повідомлення успішно надіслано!')
    except Exception as e:
        await message.answer(f"Помилка при відправці повідомлення: {e}")
    finally:
        await state.clear()
    
# Надіслати документ користувачу

DOCUMENT_USER = "document_user"

if not os.path.exists(DOCUMENT_USER):
    os.makedirs(DOCUMENT_USER)

class SendTask(StatesGroup):
    user_id = State()
    document = State()

@router_admin.message(Command('to_send_document'))
async def ask_user_id(message: Message, state: FSMContext):
    await message.answer('Введіть ID користувача, якому хочете надіслати документ:')
    await state.set_state(SendTask.user_id)

@router_admin.message(SendTask.user_id)
async def ask_document(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Будь ласка, введіть коректний числовий ID користувача.')
        return

    user_id = int(message.text)
    await state.update_data(user_id=user_id)
    await message.answer(f'Збережено ID користувача: {user_id}. Тепер надішліть документ:')
    await state.set_state(SendTask.document)

@router_admin.message(SendTask.document)
async def send_document_to_user(message: types.Message, state: FSMContext ,bot: Bot):
    if not message.document:
        await message.answer("Будь ласка, надішліть файл.")
        return
    

    document = message.document

    file_info = await bot.get_file(document.file_id)
    file_bytes_io = await bot.download_file(file_info.file_path)

    await state.update_data(file_bytes = file_bytes_io.read())
    await state.set_state(SendTask.document)

    data = await state.get_data()
    user_id = data.get("user_id")
    file_bytes = data.get("file_bytes")

    save_document= os.path.join(DOCUMENT_USER, document.file_name)

    with open(save_document, "wb") as file:
        file.write(file_bytes)

    files = os.listdir(DOCUMENT_USER)
    if not files:
        await message.answer('Папка document_user пуста!')
        return
    
    for file_name in files:
        file_path = os.path.join(DOCUMENT_USER, file_name)
        if os.path.isfile(file_path):
            file = FSInputFile(file_path)
            await bot.send_document(user_id, file)
        
    await message.answer("Файл був відправлений користувачу")

    for file_name in files:
        file_path = os.path.join(DOCUMENT_USER, file_name)
        try:
            os.remove(file_path)
        except Exception as e:
            await message.answer(f"Невдалось видалити файл '{file_path}': {e}")

<<<<<<< HEAD
=======
# @router_admin.message(SendTask.document)
# async def send_document_to_user(message: Message, state: FSMContext, bot: Bot):
    # if not message.document:
    #     await message.answer("Будь ласка, надішліть файл.")
    #     return

#     data = await state.get_data()
#     user_id = data['user_id']

#     try:
#         # Завантажуємо документ
#         file_info = await bot.get_file(message.document.file_id)
#         file_bytes_io = await bot.download_file(file_info.file_path)

#         # Перевірка, чи правильно ми отримали байти
#         file_bytes = file_bytes_io.getvalue()  # отримуємо байти з _io.BytesIO

#         # Відправляємо документ користувачу
#         await bot.send_document(
#             user_id,
#             document=FSInputFile(BytesIO(file_bytes), filename=message.document.file_name),
#             caption="Від адміністратора"
#         )
#         await message.answer('Документ успішно надіслано!')

#     except Exception as e:
#         await message.answer(f"Помилка при відправці документа: {e}")
#     finally:
#         await state.clear()


>>>>>>> 1587da78b16037c3502743504a3705f87a115717
# Провірка користувача
class GetUserInfo(StatesGroup):
    user_id = State()

@router_admin.message(Command('get_user_info'))
async def ask_user_id(message: Message, state: FSMContext):
    await message.answer('Введіть Telegram ID користувача:')
    await state.set_state(GetUserInfo.user_id)

@router_admin.message(GetUserInfo.user_id)
async def fetch_user_info(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Будь ласка, введіть коректний числовий Telegram ID.')
        return

    tg_id = int(message.text)

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(rq.User).where(rq.User.tg_id == tg_id))
            user = result.scalars().first()

    if user:
        user_info = (
            f"👤 Інформація про користувача:\n"
            f"ID: {user.id}\n"
            f"Telegram ID: {user.tg_id}\n"
            f"Прогрес: {user.progress}\n"
            f"Бонуси: {user.bonus}"
        )
        await message.answer(user_info)
    else:
        await message.answer(f"❌ Користувача з Telegram ID {tg_id} не знайдено.")

    await state.clear()

# Функція начислення бонусу
class UpdateUserFields(StatesGroup):
    user_id = State()
    bonus = State()
    progress = State()

@router_admin.message(Command('update_user'))
async def ask_user_id(message: Message, state: FSMContext):
    await message.answer("Введіть Telegram ID користувача:")
    await state.set_state(UpdateUserFields.user_id)

@router_admin.message(UpdateUserFields.user_id)
async def ask_bonus(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Будь ласка, введіть коректний числовий Telegram ID.")
        return
    await state.update_data(user_id=int(message.text))
    await message.answer("Введіть нове значення для бонусів:")
    await state.set_state(UpdateUserFields.bonus)

@router_admin.message(UpdateUserFields.bonus)
async def ask_progress(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Бонуси мають бути числом. Спробуйте ще раз.")
        return
    await state.update_data(bonus=int(message.text))
    await message.answer("Введіть нове значення для прогресу:")
    await state.set_state(UpdateUserFields.progress)

@router_admin.message(UpdateUserFields.progress)
async def update_user(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Прогрес має бути числом. Спробуйте ще раз.")
        return

    await state.update_data(progress=int(message.text))
    data = await state.get_data()
    tg_id = data['user_id']
    bonus = data['bonus']
    progress = data['progress']

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(rq.User).where(rq.User.tg_id == tg_id))
            user = result.scalars().first()

            if user:
                user.bonus = bonus
                user.progress = progress
                await session.commit()
                await message.answer(
                    f"✅ Дані оновлено:\n"
                    f"Telegram ID: {tg_id}\n"
                    f"Нові бонуси: {bonus}\n"
                    f"Новий прогрес: {progress}"
                )
            else:
                await message.answer(f"❌ Користувача з Telegram ID {tg_id} не знайдено.")
    
    await state.clear()