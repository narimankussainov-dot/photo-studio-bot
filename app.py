import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db
from handlers import router

logging.basicConfig(level=logging.INFO)


async def main():
    # 1. Инициализируем базу данных
    init_db()

    # 2. Создаем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 3. Подключаем наши хэндлеры к диспетчеру
    dp.include_router(router)

    print("Бот успешно запущен...")
    # 4. Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())