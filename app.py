import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db
from handlers import router

logging.basicConfig(level=logging.INFO)

# Крошечный веб-сервер для обмана Render (заглушка)
async def health_check(request):
    return web.Response(text="Бот жив и работает!")

async def main():
    # 1. Инициализируем базу данных
    init_db()

    # 2. Создаем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # 3. --- ЗАПУСК ЗАГЛУШКИ ДЛЯ RENDER ---
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render сам выдаст нам порт, мы его ловим
    port = int(os.environ.get("PORT", 8000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    # -------------------------------------

    print("Бот успешно запущен...")
    # 4. Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())