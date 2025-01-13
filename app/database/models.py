from sqlalchemy import BigInteger, String, ForeignKey, LargeBinary
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    progress: Mapped[int] = mapped_column(nullable=False, default=0)
    bonus: Mapped[int] = mapped_column(nullable=False, default=0) 
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)  # TG ID обов'язковий

class Content(Base):
    __tablename__ = 'content'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)  # TG ID обов'язковий
    document: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)  # Зберігаємо байти
    desciption: Mapped[str] = mapped_column(String(100))



# class Category(Base):
#     __tablename__ = 'categories'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(25))

# class Item(Base):
#     __tablename__ = 'items'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(25))
#     description: Mapped[str] = mapped_column(String(120))
#     price: Mapped[int] = mapped_column()
#     category: Mapped[str] = mapped_column(ForeignKey('categories.id'))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)