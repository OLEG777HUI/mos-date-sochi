from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database.models import AsyncSessionLocal, User  # Импортируем нашу базу

# Создаем приложение-сервер
app = FastAPI()

# Разрешаем твоему сайту на GitHub отправлять сюда данные (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Принимать запросы откуда угодно
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Описываем структуру: какие именно данные мы ждем от сайта
class RegisterRequest(BaseModel):
    tg_id: int
    name: str
    age: int
    gender: str
    location: str

# Эндпоинт (адрес), куда сайт будет отправлять анкету при нажатии "Завершить регистрацию"
@app.post("/api/register")
async def register_user(data: RegisterRequest):
    # Открываем подключение к базе данных
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже такой человек в базе (по его ID в Телеграме)
        existing_user = await session.get(User, data.tg_id)
        
        if existing_user:
            return {"status": "ok", "message": "Пользователь уже зарегистрирован"}

        # Если его нет — создаем новую запись в базе!
        new_user = User(
            tg_id=data.tg_id,
            name=data.name,
            age=data.age,
            gender=data.gender,
            location=data.location
        )
        session.add(new_user)
        await session.commit() # Сохраняем навсегда
        
        return {"status": "success", "message": "Анкета успешно сохранена в базу Privé!"}