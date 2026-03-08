import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.models import AsyncSessionLocal, User

app = FastAPI()

# Разрешаем твоему сайту отправлять сюда данные (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем папку для загрузки файлов, если её еще нет
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# "Раздаем" статику, чтобы фотки можно было посмотреть по ссылке
app.mount("/static", StaticFiles(directory="static"), name="static")

# Вспомогательная функция для подключения к БД
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ==========================================
# РОУТ: РЕГИСТРАЦИЯ И ЗАГРУЗКА ФОТО
# ==========================================
@app.post("/api/register")
async def register_user(
    tg_id: int = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    location: str = Form(...),
    description: str = Form(""),
    job: str = Form(""),
    social_links: str = Form(""),
    photo_1: UploadFile = File(None),
    photo_2: UploadFile = File(None),
    photo_3: UploadFile = File(None),
    video_1: UploadFile = File(None),
    db = Depends(get_db)
):
    # Проверяем, есть ли уже такой человек в базе
    existing_user = await db.get(User, tg_id)
    if existing_user:
        return {"status": "ok", "message": "Пользователь уже зарегистрирован"}

    # 1. Сохраняем файлы на диск сервера
    paths = {"photo_1": None, "photo_2": None, "photo_3": None, "video_1": None}
    files = {"photo_1": photo_1, "photo_2": photo_2, "photo_3": photo_3, "video_1": video_1}
    
    for key, file in files.items():
        if file and file.filename:
            # Уникальное имя файла: ID_пользователя_photo_1.jpg
            safe_filename = f"{tg_id}_{key}_{file.filename}"
            file_path = os.path.join(UPLOAD_DIR, safe_filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            paths[key] = f"/{file_path}"

    # 2. Создаем новую запись в базе!
    new_user = User(
        tg_id=tg_id,
        name=name,
        age=age,
        gender=gender,
        location=location,
        description=description,
        job=job,
        social_links=social_links,
        photo_1=paths["photo_1"],
        photo_2=paths["photo_2"],
        photo_3=paths["photo_3"],
        video_1=paths["video_1"],
        is_approved=True # Ставим True, чтобы сразу видеть анкету в барабане
    )
    
    db.add(new_user)
    await db.commit()
    
    return {"status": "success", "message": "Анкета с фото успешно сохранена в базу Privé!"}