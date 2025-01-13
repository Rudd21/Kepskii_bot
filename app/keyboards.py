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

    buttons.append([InlineKeyboardButton(text="На Головну", callback_data="back_to_FKEP")])


    # Створюємо клавіатуру з кнопками
    return InlineKeyboardMarkup(inline_keyboard=buttons)