import asyncio

import os
from aiogram import Dispatcher, Bot
from app.handlers import router
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_API"))

dp = Dispatcher()

async def on_startup(_):
    print('Бот успішно запущений')

async def main():
    dp.include_router(router)
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
