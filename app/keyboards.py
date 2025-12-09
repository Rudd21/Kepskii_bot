from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_files_and_folders(path: str) -> list:
    """
    Повертає список файлів і папок у заданій директорії.
    """
    try:
        # Перевіряємо, чи існує папка
        if not os.path.exists(path):
            raise FileNotFoundError(f"Шлях {path} не знайдено.")
        
        # Отримуємо список файлів і папок
        return os.listdir(path)
    except Exception as e:
        print(f"Помилка при отриманні списку файлів і папок: {e}")
        return []

def create_file_folder_buttons(path: str) -> InlineKeyboardMarkup:
    """
    Генерує кнопки для файлів і папок у вказаній директорії.
    """
    # Отримуємо список файлів і папок
    items = get_files_and_folders(path)
    
    # Якщо елементів немає, повертаємо пусту клавіатуру
    if not items:
        return InlineKeyboardMarkup()
    
    # Створюємо список кнопок
    buttons = []
    for item in items:
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            # Якщо це папка
            callback_data = f"folder:{item.replace(' ', '_')}"
            buttons.append([InlineKeyboardButton(text=f"📁 {item}", callback_data=callback_data)])
        else:
            # Якщо це файл
            callback_data = f"file:{item.replace(' ', '_')}"
            buttons.append([InlineKeyboardButton(text=f"📄 {item}", callback_data=callback_data)])
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
    buttons.append([InlineKeyboardButton(text="Надіслати файл адміністрації", callback_data="file_to_admin"), InlineKeyboardButton(text="На Головну", callback_data="back_to_FKEP")])


    # Створюємо клавіатуру з кнопками
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ADMIN клавіатура
# admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Відправити повідомлення користувачу', callback_data='to_send_message')],
#     [InlineKeyboardButton(text='Скринька завдань', callback_data='download_all_files')],
#     [InlineKeyboardButton(text='Провірити бали користувача', callback_data='to_check_bonus')],
#     [InlineKeyboardButton(text='Добавити бали користувачу', callback_data='to_check_bonus')],
# ])
# from app.database.requests import get_category, get_category_item

# main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
#                                      [KeyboardButton(text='Корзина')],
#                                      [KeyboardButton(text='Контакти'),
#                                      KeyboardButton(text='Про нас')]],
#                             resize_keyboard=True,
#                             input_field_placeholder='Виберіть пункт меню...')

# async def get_category():
#     all_categories = await get_category()
#     keyboard = InlineKeyboardBuilder
#     for category in all_categories:
#         keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data='to_main'))
#     return keyboard.adjust(2).as_markup()

# async def items(category_id):
#     all_items = await get_category_item(category_id)
#     keyboard = InlineKeyboardBuilder
#     for item in all_items:
#         keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'category_{item.id}'))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data='to_main'))
#     return keyboard.adjust(2).as_markup()

# # USER клавіатура
# user_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Дивитись доступні завдання', callback_data='to_see_content')],
#     [InlineKeyboardButton(text='Відправити контент адміністрації', callback_data='to_send_content')],
#     [InlineKeyboardButton(text='Мій прогрес', callback_data='to_check_progress')],
# ])

# # Офісне програмне забезпечення
# FILES_PATH = {MAIN_PATH}
# files_FILES = os.listdir(FILES_PATH)

# async def find_files_FILES():
#     keyboard = InlineKeyboardBuilder()
#     for FILES_PATH in files_FILES:
#         keyboard.add(InlineKeyboardButton(text=FILES_PATH, callback_data=f"file_FILES_{FILES_PATH}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# course = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='1 Курс', callback_data='to_first')],
#     [InlineKeyboardButton(text='2 Курс', callback_data='to_second')]
# ])
# # Предмети за 2 курс
# subject2 = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Василь Ревтюх', callback_data='to_revtuh2')],
#     [InlineKeyboardButton(text='Марія Шнайдер', callback_data='to_schnaider2')],
#     [InlineKeyboardButton(text='Надія Нагірна', callback_data='to_NAHI2')],
#     [InlineKeyboardButton(text='Оксана Балабаник', callback_data='to_balaban2')],
#     [InlineKeyboardButton(text='Олександра Воронцова', callback_data='to_voron2')],
# ])
# # Графічний дизайн
# REVT2_PATH = "FKEP/2 курс/Графічний дизайн/Ревтюх/"
# files_REVT2 = [f for f in os.listdir(REVT2_PATH) if os.path.isfile(os.path.join(REVT2_PATH, f))]

# async def find_files_REVT2():
#     keyboard = InlineKeyboardBuilder()
#     for file_REVT2 in files_REVT2:
#         keyboard.add(InlineKeyboardButton(text=file_REVT2, callback_data=f"file_REVT2_{file_REVT2}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Офісне програмне забезпечення
# SNAI2_PATH = "FKEP/2 курс/ОПЗ/Шнайдер/"
# files_SNAI2 = [f for f in os.listdir(SNAI2_PATH) if os.path.isfile(os.path.join(SNAI2_PATH, f))]

# async def find_files_SNAI2():
#     keyboard = InlineKeyboardBuilder()
#     for file_SNAI2 in files_SNAI2:
#         keyboard.add(InlineKeyboardButton(text=file_SNAI2, callback_data=f"file_SNAI2_{file_SNAI2}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Фізика
# NAHI2_PATH = "FKEP/2 курс/Фізика/Нагірна/"
# files_NAHI2 = [f for f in os.listdir(NAHI2_PATH) if os.path.isfile(os.path.join(NAHI2_PATH, f))]

# async def find_files_NAHI2():
#     keyboard = InlineKeyboardBuilder()
#     for file_NAHI2 in files_NAHI2:
#         keyboard.add(InlineKeyboardButton(text=file_NAHI2, callback_data=f"file_NAHI2_{file_NAHI2}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Технології
# BALABAN2_PATH = "FKEP/2 курс/Технології/Балабаник/"
# files_BALABAN2 = [f for f in os.listdir(BALABAN2_PATH) if os.path.isfile(os.path.join(BALABAN2_PATH, f))]

# async def find_files_BALABAN2():
#     keyboard = InlineKeyboardBuilder()
#     for file_BALABAN2 in files_BALABAN2:
#         keyboard.add(InlineKeyboardButton(text=file_BALABAN2, callback_data=f"file_BALABAN2_{file_BALABAN2}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Математика
# VORON2_PATH = "FKEP/2 курс/Математика/Воронцова/"
# files_VORON2 = [f for f in os.listdir(VORON2_PATH) if os.path.isfile(os.path.join(VORON2_PATH, f))]

# async def find_files_VORON2():
#     keyboard = InlineKeyboardBuilder()
#     for file_VORON2 in files_VORON2:
#         keyboard.add(InlineKeyboardButton(text=file_VORON2, callback_data=f"file_VORON2_{file_VORON2}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# Предмети за 1 курс
# subject1 = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Надія Нагірна', callback_data='to_nahirna')],
#     [InlineKeyboardButton(text='Олександра Воронцова', callback_data='to_voronzova')],
#     [InlineKeyboardButton(text='Людмила Людкевич', callback_data='to_ludkevich')],
#     [InlineKeyboardButton(text='Роксана Скочинська', callback_data='to_sko4unska')],
#     [InlineKeyboardButton(text='Микола Василів', callback_data='to_vasuliv')],
#     [InlineKeyboardButton(text='Хз( Медицина )', callback_data='to_med')],
#     [InlineKeyboardButton(text='Олександра Прокіпчин', callback_data='to_prokipchun')],
#     [InlineKeyboardButton(text='Ірина Барчук', callback_data='to_barchuk')],
# ])

# # Фізика
# NAHI1_PATH = "FKEP/1 курс/Фізика/Нагірна/"
# files_NAHI1 = [f for f in os.listdir(NAHI1_PATH) if os.path.isfile(os.path.join(NAHI1_PATH, f))]

# async def find_files_NAHI1():
#     keyboard = InlineKeyboardBuilder()
#     for file_NAHI1 in files_NAHI1:
#         keyboard.add(InlineKeyboardButton(text=file_NAHI1, callback_data=f"file_NAHI1_{file_NAHI1}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Математика
# VORON1_PATH = "FKEP/1 курс/Математика/Воронцова/"
# files_VORON1 = [f for f in os.listdir(VORON1_PATH) if os.path.isfile(os.path.join(VORON1_PATH, f))]

# async def find_files_VORON1():
#     keyboard = InlineKeyboardBuilder()
#     for file_VORON1 in files_VORON1:
#         keyboard.add(InlineKeyboardButton(text=file_VORON1, callback_data=f"file_VORON1_{file_VORON1}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Економіка
# LUDKE_ECON1_PATH = "FKEP/1 курс/Економіка/Людкевич"
# files_LUDKE_ECON1 = [f for f in os.listdir(LUDKE_ECON1_PATH) if os.path.isfile(os.path.join(LUDKE_ECON1_PATH, f))]

# async def find_files_LUDKE_ECON1():
#     keyboard = InlineKeyboardBuilder()
#     for file_LUDKE_ECON1 in files_LUDKE_ECON1:
#         keyboard.add(InlineKeyboardButton(text=file_LUDKE_ECON1, callback_data=f"file_LUDKE_ECON1_{file_LUDKE_ECON1}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)  # Встановіть кількість стовпців
#     return keyboard.as_markup()


# # Біологія
# PROK1_PATH = "FKEP/1 курс/Біологія/Прокіпчин/"
# files_PROK1 = [f for f in os.listdir(PROK1_PATH) if os.path.isfile(os.path.join(PROK1_PATH, f))]

# async def find_files_PROK1():
#     keyboard = InlineKeyboardBuilder()
#     for file_PROK1 in files_PROK1:
#         keyboard.add(InlineKeyboardButton(text=file_PROK1, callback_data=f"file_PROK1_{file_PROK1}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Інформатика
# VASU1_PATH = "FKEP/1 курс/Інформатика/Микола Василів/"
# files_VASU1 = [f for f in os.listdir(VASU1_PATH) if os.path.isfile(os.path.join(VASU1_PATH, f))]

# async def find_files_VASU1():
#     keyboard = InlineKeyboardBuilder()
#     for file_VASU1 in files_VASU1:
#         keyboard.add(InlineKeyboardButton(text=file_VASU1, callback_data=f"file_VASU1_{file_VASU1}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Медицина
# MEDI_PATH = "FKEP/1 курс/Медицина/"
# files_MEDI = [f for f in os.listdir(MEDI_PATH) if os.path.isfile(os.path.join(MEDI_PATH, f))]

# async def find_files_MEDI():
#     keyboard = InlineKeyboardBuilder()
#     for file_MEDI in files_MEDI:
#         keyboard.add(InlineKeyboardButton(text=file_MEDI, callback_data=f"file_medi_{file_MEDI}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Правознавство
# BARC1_PATH = "FKEP/1 курс/Правознавство/Барчук/"
# files_BARC1 = [f for f in os.listdir(BARC1_PATH) if os.path.isfile(os.path.join(BARC1_PATH, f))]

# async def find_files_BARC1():
#     keyboard = InlineKeyboardBuilder()
#     for file_BARC1 in files_BARC1:
#         keyboard.add(InlineKeyboardButton(text=file_BARC1, callback_data=f"file_BARC1_{file_BARC1}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# # Хімія
# SCHOCH1_PATH = "FKEP/1 курс/Хімія/Скочинська/"
# files_SCHOCH1 = [f for f in os.listdir(SCHOCH1_PATH) if os.path.isfile(os.path.join(SCHOCH1_PATH, f))]

# async def find_files_SCHOCH1():
#     keyboard = InlineKeyboardBuilder()
#     for file_SCHOCH1 in files_SCHOCH1:
#         keyboard.add(InlineKeyboardButton(text=file_SCHOCH1, callback_data=f"file_SCHOCH1_{file_SCHOCH1}"))
#     keyboard.add(InlineKeyboardButton(text='На головну', callback_data="to_main"))
#     keyboard.adjust(2)
#     return keyboard.as_markup()

# Кнопка на головну
# to_main = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='На головну', callback_data='to_main')],
# ])

# catalog = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Футболки', callback_data='t-shirt')],
#     [InlineKeyboardButton(text='Кросовки', callback_data='sneakers')],
#     [InlineKeyboardButton(text='Кепки', callback_data='cap')]
# ])

# get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Відправити номер',
#                                                            request_contact=True)]],
#                                                            resize_keyboard=True)