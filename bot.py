import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import create_database

from handlers.start import router as start_router
from handlers.tasks import router as tasks_router


async def home(request):
    return web.Response(text="Bot is running!")


async def start_http_server():
    app = web.Application()
    app.router.add_get("/", home)

    port = int(os.environ.get("PORT", 10000))

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"HTTP server ishga tushdi: {port}")


async def start_bot():
    create_database()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(tasks_router)

    print("🤖 Bot ishga tushdi...")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def main():
    await start_http_server()
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
