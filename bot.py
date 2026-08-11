import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import create_database

from handlers.start import router as start_router
from handlers.tasks import router as tasks_router


async def main():

    create_database()

    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(tasks_router)

    print("Bot ishga tushdi...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())