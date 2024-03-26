import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


async def main():
    bot = Bot(token=env_data.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
