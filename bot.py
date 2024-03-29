import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import env_data
import handlers


async def main():
    bot = Bot(token=env_data.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
