import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import env_data
from handlers import main_actions, module_creation, module_actions, update_module


async def main():
    bot = Bot(token=env_data.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # connect all handlers
    dp.include_router(main_actions.main_actions_router)
    dp.include_router(module_creation.module_creation_router)
    dp.include_router(update_module.update_module_router)
    dp.include_router(module_actions.module_actions_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
