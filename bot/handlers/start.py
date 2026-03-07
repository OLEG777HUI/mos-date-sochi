import os
import json
from aiogram import Router, types, F
from aiogram.filters import CommandStart
# Заменили импорты на Inline-кнопки
from aiogram.types import WebAppInfo, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    # Твоя правильная ссылка
    web_app_url = "https://oleg777hui.github.io/Prive-Club-Sochi/"
    
    # Делаем Inline-кнопку, чтобы она висела красиво прямо под текстом (как на твоем скрине)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✨ Открыть Privé Club", web_app=WebAppInfo(url=web_app_url))]
        ]
    )

    welcome_text = (
        "✨ <b>Bienvenue à Privé Club Sochi</b> ✨\n\n"
        "Добро пожаловать в закрытое сообщество самых успешных и "
        "привлекательных людей столицы курортов.\n\n"
        "Здесь вы найдете не просто знакомства, а эксклюзивный круг "
        "общения и единомышленников. Это закрытое сообщество для тех, "
        "кто ищет «своих»: людей, которые не стоят на месте.\n\n"
        "<i>Вы достойны большего. Нажмите ниже, чтобы начать.</i>"
    )

    # Путь к файлу анимации в корне проекта
    animation_path = "logo.gif.mp4"

    if os.path.exists(animation_path):
        await message.answer_animation(
            animation=FSInputFile(animation_path),
            caption=welcome_text,
            reply_markup=kb,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text=welcome_text,
            reply_markup=kb,
            parse_mode="HTML"
        )

# =======================================================
# ЭТОТ БЛОК ЛОВИТ АНКЕТУ, КОГДА ЖМУТ "ЗАВЕРШИТЬ РЕГИСТРАЦИЮ"
# =======================================================
@router.message(F.web_app_data)
async def web_app_handler(message: types.Message):
    # Расшифровываем данные, которые мы собрали в index.html
    data = json.loads(message.web_app_data.data)
    
    name = data.get('name', 'Не указано')
    age = data.get('age', 'Не указано')
    gender = data.get('gender', 'Не указано')
    location = data.get('location', 'Не указано')
    
    # Отправляем сообщение-подтверждение в бот
    await message.answer(
        f"👑 <b>Ваша анкета резидента Privé успешно создана:</b>\n\n"
        f"👤 Имя: {name}\n"
        f"🎂 Возраст: {age}\n"
        f"🚻 Пол: {gender}\n"
        f"📍 Локация: {location}\n\n"
        f"<i>Теперь вы можете использовать все функции клуба.</i>",
        parse_mode="HTML"
    )