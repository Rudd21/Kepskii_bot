from app.database.models import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import types
import os

# from app.database.models import User, Category, Item
from app.database.models import User
from app.database.models import Content

from sqlalchemy import select

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
    
async def safe_content(tg_id, document, description):
    async with async_session() as session:
        async with session.begin():
            new_content = Content(
                tg_id=tg_id,
                document=document,
                desciption=description
            )
            session.add(new_content)

async def download_all_files_from_db(callback: types.CallbackQuery, session: AsyncSession):
    async with async_session() as session:
        # Запит до бази даних
        result = await session.execute(select(Content))
        content_records = result.scalars().all()

        if not content_records:
            await callback.answer("Не знайдено жодного файлу.")
            return

        # Створюємо директорію для завантажених файлів, якщо її немає
        download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)

        # Перебираємо всі записи і зберігаємо файли
        for content in content_records:
            id = content.id
            tg_id = content.tg_id
            document_data = content.document
            description = content.desciption

            # Додаємо розширення .pdf до файлу
            file_path = os.path.join(download_dir, f"{id}_{tg_id}.pdf")
            with open(file_path, 'wb') as f:
                f.write(document_data)

            # Зберігаємо опис у окремому файлі
            description_file_path = os.path.join(download_dir, f"{id}_{tg_id}_description.txt")
            with open(description_file_path, 'w') as f_desc:
                f_desc.write(description)

        await callback.answer(f"Усі файли та описи були завантажені у папку {download_dir}.")

# async def set_user(tg_id):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))

#         if not user:
#             session.add(User(tg_id=tg_id))
#             await session.commit()

# async def get_category():
#     async with async_session() as session:
#         return await session.scalars(select(Category))
    
# async def get_category_item(category_id):
#     async with async_session() as session:
#         return await session.scalars(select(Item).where(Item.category))
    
# async def get_item(item_id):
#     async with async_session() as session:
#         return await session.scalars(select(Item).where(Item.id == item_id))