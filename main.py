import asyncio
import logging
import sys
import uvicorn # Новый импорт для сервера

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from bot.handlers.start import router as start_router

from database.models import init_db
from api import app # Импортируем наш сервер из файла api.py

# Функция, которая запускает веб-сервер
async def start_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )

    # Initialize Bot and Dispatcher
    bot = Bot(
        token=settings.bot_token.get_secret_value(), 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Register routers
    dp.include_router(start_router)

    # Database initialization
    logging.info("Создание базы данных Privé Club...")
    await init_db()
    logging.info("База данных успешно загружена!")

    # Запускаем ОДНОВРЕМЕННО и бота, и веб-сервер!
    logging.info("✨ Запуск бота и API-сервера...")
    
    # Создаем две параллельные задачи
    bot_task = asyncio.create_task(dp.start_polling(bot))
    api_task = asyncio.create_task(start_api())
    
    try:
        # Ждем выполнения обеих (они будут работать бесконечно)
        await asyncio.gather(bot_task, api_task)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot and API stopped.")