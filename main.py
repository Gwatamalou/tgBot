import asyncio
from aiogram import Bot, Dispatcher, F
from handlers import router
from config import TOKEN_BOT



async def main():
    bot = Bot(token=TOKEN_BOT)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
