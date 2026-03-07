from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import BigInteger, String, Boolean, Text, Integer

# 1. Создаем движок базы данных. Файл будет называться prive.db
engine = create_async_engine('sqlite+aiosqlite:///prive.db', echo=False)

# 2. Создаем фабрику сессий (через нее бот будет общаться с базой)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# 3. Базовый класс
Base = declarative_base()

# ==========================================
# ТАБЛИЦА 1: ПОЛЬЗОВАТЕЛИ (АНКЕТЫ)
# ==========================================
class User(Base):
    __tablename__ = 'users'

    # Основная информация
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True) # ID в Телеграме
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(10))
    location: Mapped[str] = mapped_column(String(50))
    
    # Дополнительно
    description: Mapped[str] = mapped_column(Text, nullable=True)
    job: Mapped[str] = mapped_column(String(100), nullable=True)
    social_links: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Фото и видео (добавил 3-е фото под твой дизайн)
    photo_1: Mapped[str] = mapped_column(String(100), nullable=True)
    photo_2: Mapped[str] = mapped_column(String(100), nullable=True)
    photo_3: Mapped[str] = mapped_column(String(100), nullable=True)
    video_1: Mapped[str] = mapped_column(String(100), nullable=True)

    # Статусы подписки и модерации
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    is_elite: Mapped[bool] = mapped_column(Boolean, default=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False) # Прошел ли проверку

# ==========================================
# ТАБЛИЦА 2: СВАЙПЫ И ЛАЙКИ
# ==========================================
class Swipe(Base):
    __tablename__ = 'swipes'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_from: Mapped[int] = mapped_column(BigInteger) # Кто лайкнул
    user_to: Mapped[int] = mapped_column(BigInteger)   # Кого лайкнули
    action: Mapped[str] = mapped_column(String(20))    # 'like', 'dislike' или 'superlike'

# ==========================================
# ТАБЛИЦА 3: МЭТЧИ (ВЗАИМНЫЕ СИМПАТИИ)
# ==========================================
class Match(Base):
    __tablename__ = 'matches'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_1: Mapped[int] = mapped_column(BigInteger) # ID первого пользователя
    user_2: Mapped[int] = mapped_column(BigInteger) # ID второго пользователя

# ==========================================
# ФУНКЦИЯ ДЛЯ СОЗДАНИЯ БАЗЫ
# ==========================================
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)