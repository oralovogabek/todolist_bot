from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import (
    add_task,
    get_tasks,
    get_completed_tasks,
    delete_task,
    complete_task,
)


router = Router()


class TaskState(StatesGroup):
    waiting_for_task = State()


# =========================
# ➕ VAZIFA QO‘SHISH
# =========================

@router.message(F.text == "➕ Vazifa qo‘shish")
async def add_task_start(message: Message, state: FSMContext):

    await state.set_state(TaskState.waiting_for_task)

    await message.answer(
        "📝 Bugun nima qilishingiz kerak?\n\n"
        "Vazifangizni yozing:"
    )


@router.message(TaskState.waiting_for_task)
async def save_task(message: Message, state: FSMContext):

    task = message.text.strip()

    if not task:
        await message.answer(
            "❌ Vazifa bo‘sh bo‘lishi mumkin emas."
        )
        return

    add_task(
        user_id=message.from_user.id,
        task=task
    )

    await state.clear()

    await message.answer(
        f"✅ Vazifa qo‘shildi!\n\n"
        f"📝 {task}\n"
        f"📌 Status: F"
    )


# =========================
# 📋 VAZIFALARIM
# =========================

@router.message(F.text == "📋 Vazifalarim")
async def my_tasks(message: Message):

    tasks = get_tasks(message.from_user.id)

    if not tasks:
        await message.answer(
            "📋 Sizda hozircha vazifalar yo‘q."
        )
        return

    text = "📋 Sizning vazifalaringiz:\n\n"

    buttons = []

    for task_id, task, status in tasks:

        text += f"{task_id}. {task} — {status}\n"

        # F bo‘lsa bajarish tugmasi chiqadi
        if status == "F":

            buttons.append([
                InlineKeyboardButton(
                    text=f"✅ Bajarish: {task}",
                    callback_data=f"complete:{task_id}"
                )
            ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await message.answer(
        text,
        reply_markup=keyboard
    )


# =========================
# ✅ VAZIFANI BAJARISH
# =========================

@router.callback_query(F.data.startswith("complete:"))
async def complete_task_callback(
    callback: CallbackQuery
):

    task_id = int(
        callback.data.split(":")[1]
    )

    complete_task(
        task_id=task_id,
        user_id=callback.from_user.id
    )

    await callback.answer(
        "✅ Vazifa bajarildi!"
    )

    # Vazifalarni qayta chiqaramiz
    tasks = get_tasks(
        callback.from_user.id
    )

    text = "📋 Sizning vazifalaringiz:\n\n"

    buttons = []

    for task_id, task, status in tasks:

        text += f"{task_id}. {task} — {status}\n"

        if status == "F":

            buttons.append([
                InlineKeyboardButton(
                    text=f"✅ Bajarish: {task}",
                    callback_data=f"complete:{task_id}"
                )
            ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboard
    )


# =========================
# 🗑 VAZIFA O‘CHIRISH
# =========================

@router.message(F.text == "🗑 Vazifa o‘chirish")
async def delete_task_menu(message: Message):

    tasks = get_tasks(message.from_user.id)

    # Faqat bajarilmagan vazifalar
    pending_tasks = [
        task for task in tasks
        if task[2] == "F"
    ]

    if not pending_tasks:

        await message.answer(
            "🗑 O‘chirish uchun vazifalar yo‘q."
        )

        return

    buttons = []

    for task_id, task, status in pending_tasks:

        buttons.append([
            InlineKeyboardButton(
                text=f"🗑 {task}",
                callback_data=f"delete:{task_id}"
            )
        ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await message.answer(
        "🗑 Qaysi vazifani o‘chirmoqchisiz?",
        reply_markup=keyboard
    )


# =========================
# 🗑 O‘CHIRISH
# =========================

@router.callback_query(F.data.startswith("delete:"))
async def delete_task_callback(
    callback: CallbackQuery
):

    task_id = int(
        callback.data.split(":")[1]
    )

    delete_task(
        task_id=task_id,
        user_id=callback.from_user.id
    )

    await callback.message.edit_text(
        "🗑 Vazifa o‘chirildi!"
    )

    await callback.answer()


# =========================
# ✅ BAJARILGANLAR
# =========================

@router.message(F.text == "✅ Bajarilganlar")
async def completed_tasks(message: Message):

    tasks = get_completed_tasks(
        message.from_user.id
    )

    if not tasks:

        await message.answer(
            "✅ Hali bajarilgan vazifalar yo‘q."
        )

        return

    text = "✅ Bajarilgan vazifalar:\n\n"

    for task_id, task, status in tasks:

        text += (
            f"{task_id}. {task} — {status}\n"
        )

    await message.answer(text)