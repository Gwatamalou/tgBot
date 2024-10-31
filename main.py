import asyncio
from aiogram import Bot, Dispatcher, F
from handlers import router
from config import TOKEN_BOT
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start',
                   description='главное меню бота'),
        BotCommand(command='/random',
                   description='узнать рандомный факт'),
        BotCommand(command='/gpt',
                   description='Задать вопрос ChatGPT'),
        BotCommand(command='/talk',
                   description='поговорить с известной личностью'),
        BotCommand(command='/quiz',
                   description='проверить свои знания'),
        BotCommand(command='/translator',
                   description='переводчик'),
        BotCommand(command='/idea',
                   description='Генератор идей'),

    ]

    await bot.set_my_commands(main_menu_commands)


async def main():
    bot = Bot(token=TOKEN_BOT)
    dp = Dispatcher()
    dp.startup.register(set_main_menu)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
