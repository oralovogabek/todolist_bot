import asyncio
import os
from threading import Thread

from flask import Flask
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import create_database

from handlers.start import router as start_router
from handlers.tasks import router as tasks_router


app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is running!"


async def main():
    create_database()

    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(tasks_router)

    print("Bot ishga tushdi...")

    await dp.start_polling(bot)


def run_bot():
    asyncio.run(main())


if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)