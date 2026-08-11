from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Vazifa qo‘shish"),
            KeyboardButton(text="🗑 Vazifa o‘chirish"),
        ],
        [
            KeyboardButton(text="📋 Vazifalarim"),
            KeyboardButton(text="✅ Bajarilganlar"),
        ],
    ],
    resize_keyboard=True
)