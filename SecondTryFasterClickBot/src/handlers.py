import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from src import keyboards, conf
from aiogram import BaseMiddleware
from aiogram.types import Message

from src.conf import sleeptime

router = Router()

def set_blocked(blocked_flag, value):
    blocked_flag.value = value

@router.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id != conf.ADMIN_ID:
        await keyboards.menu_kbrd(message)

@router.message(F.text == "Жми!")
async def sendname(message: types.Message, blocked_flag):
    if not blocked_flag.value:
        await message.answer("Блядская кнопка нажата")
    else:
        await message.answer("Да пажжи блея")

    if not blocked_flag.value:
        user_name = message.from_user.username or message.from_user.full_name

        try:
            await message.bot.send_message(conf.ADMIN_ID, f"Ник пользователя: {user_name}")
        except Exception as e:
            await message.reply("Не удалось отправить сообщение админу.")
            print(f"Error: {e}")

        # Устанавливаем блокировку
        set_blocked(blocked_flag, True)

        # Ждем sleeptime секунд
        await asyncio.sleep(sleeptime)

        # Снимаем блокировку
        set_blocked(blocked_flag, False)

class BlockedFlagMiddleware(BaseMiddleware):
    def __init__(self, blocked_flag):
        super().__init__()
        self.blocked_flag = blocked_flag

    async def __call__(self, handler, event: Message, data: dict):
        data['blocked_flag'] = self.blocked_flag
        return await handler(event, data)
