import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from src import conf, handlers, logger, timer
import multiprocessing
import tkinter as tk


def start_timer(blocked_flag, timer_active):
    print("Starting timer process...")
    root = tk.Tk()
    timer.CountdownTimer(root, blocked_flag, timer_active)
    root.mainloop()

async def main(blocked_flag):
    print("Starting bot...")
    mybot = Bot(token=conf.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(handlers.BlockedFlagMiddleware(blocked_flag))
    dp.include_router(handlers.router)
    await mybot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(mybot, skip_updates=True, allowed_updates=dp.resolve_used_update_types())
    print("Bot started.")

def run_bot(blocked_flag):
    print("Running bot...")
    asyncio.run(main(blocked_flag))

if __name__ == "__main__":
    logger.setup_logging()

    manager = multiprocessing.Manager()
    blocked_flag = manager.Value('b', False)
    timer_active = manager.Value('b', True)  # Флаг для активации таймера

    # Процесс для бота
    p1 = multiprocessing.Process(target=run_bot, args=(blocked_flag,))

    # Процесс для таймера
    p2 = multiprocessing.Process(target=start_timer, args=(blocked_flag, timer_active))

    # Запуск процессов
    p1.start()
    p2.start()

    p1.join()
    p2.join()
