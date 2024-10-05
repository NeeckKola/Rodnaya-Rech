from aiogram.types import (
KeyboardButton,
ReplyKeyboardMarkup
)


async def menu_kbrd(message):
    kb_btn = [
        [KeyboardButton(text="Жми!")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_btn,
        resize_keyboard=True,
        input_field_placeholder="Меню"
    )
    await message.answer("Нажми блядскую кнопку", reply_markup=keyboard)

