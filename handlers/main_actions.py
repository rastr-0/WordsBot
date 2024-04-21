from aiogram import types, Router, F
from aiogram.filters import Command

import aiomysql
import logging

from menu import Menu
from db_functionality import DataBase


main_actions_router = Router()
db = DataBase()


@main_actions_router.message(Command('start'))
async def start_handler(msg: types.Message):
    response = """Привет\U0001F44B\n
Я - твой персональный языковой бот\U0001F916, который поможет тебе быстро и легко изучать новые иностранные слова\n
Я предоставляю следующий функционал:\n
\U0001F537 Создание новых карточек со словами:
\t\t\U000025AB Вручную
\t\t\U000025AB Переведенные слова в Google документе
\t\t\U000025AB Переведенные слова в .txt и .xlsx документах
\U0001F537 Группировка карточек в отдельные модули
\U0001F537 Эффективное запоминание слов
\U0001F537 Автоматическое создание картинок для карточек с помощью нейросетей
\U0001F537 Удобные заметки, позволяющие распределить новые слова в модули позже"""

    await msg.answer(response, reply_markup=Menu.main_actions())


@main_actions_router.message(F.text == "Мои модули\U0001F5C3")
async def my_modules(msg: types.Message):
    user_id = msg.from_user.id
    await db.connect_to_db()
    try:
        response_msg = "\U0001F4CB <b>Список ваших модулей</b>:\n\n"
        # already cleaned information and ready to be sent in text message
        modules = await db.show_modules_by_id(user_id)
        if modules is not None:
            for module in modules:
                response_msg += f"\U0001F194: {module['id']}\n"
                response_msg += f" \U0001F4D1 Название: {module['name']}\n"
                if len(module) == 3:
                    response_msg += f" \U0001F4DD Описание: {module['description']}\n"
                response_msg += "----------\n"

        await msg.answer(response_msg)
        await msg.answer("Вы можете выбрать модуль для дальнейших действий введя "
                         "<b>Название</b> либо \U0001F194")
    except aiomysql.OperationalError as e:
        await msg.answer("Не вышло показать модули\U0001F61E")
        logging.log(logging.ERROR, f"Error adding new description: {e}")
    finally:
        await db.close_connection()
