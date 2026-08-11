from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboard.main import main_keyboard


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "🤖 Men sizning To-Do List botingizman.\n\n"
        "Vazifalaringizni saqlash va nazorat qilishga yordam beraman.",
        reply_markup=main_keyboard
    )