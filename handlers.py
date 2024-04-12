import logging

import aiomysql

from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from db_functionality import DataBase
from menu import Menu


router = Router()
db = DataBase()
user_module_names = {}


class ModuleCreation(StatesGroup):
    module_name = State()
    module_description = State()
    # determines how to add new words: manually, from txt/xlsx or from Google document


class GeneralState(StatesGroup):
    module_creation = ModuleCreation()
    modules_overview = State()
    note_creation = State()


@router.message(Command('start'))
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


@router.message(F.text == "Создать модуль\U0001F6E0")
async def create_module(msg: types.Message, state: FSMContext):
    await state.set_state(GeneralState.module_creation.module_name)

    user_id = msg.from_user.id

    # add user to the table Users
    await db.connect_to_db()
    try:
        await db.execute_sql(sql="INSERT IGNORE INTO Users (user_id) VALUES (%s)", args=(user_id,))
    except aiomysql.IntegrityError as e:
        logging.log(logging.ERROR, f"Users table was not updated: {e}")
    finally:
        await db.close_connection()

    response = """Теперь выбери название своего нового модуля"""
    await msg.answer(response)


@router.message(StateFilter(GeneralState.module_creation.module_name))
async def set_module_name(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id

    # add module name to users new module
    await db.connect_to_db()
    try:
        await db.execute_sql(sql="INSERT INTO Modules (user_id, module_name) VALUES (%s, %s)", args=(user_id, msg.text))

        response = """Хорошо\n
    Теперь добавь описание модуля, для пропуска этого пункта отправь \"ничего\""""
        await msg.answer(response)
        # temporary saving modules name for being able
        # to "recognize" for which module user wants to set description
        user_module_names[user_id] = msg.text

        await state.set_state(GeneralState.module_creation.module_description)
    except aiomysql.IntegrityError as e:
        # duplicate entry
        if e.args[0] == 1062:
            await msg.answer("Модуль с таким именем уже существует!\U000026A0"
                             "Выберите другое имя либо удалите существующий модуль")
        else:
            logging.log(logging.ERROR, f"Name for module was not set: {e}")
    finally:
        await db.close_connection()


@router.message(StateFilter(GeneralState.module_creation.module_description))
async def set_module_description(msg: types.Message, state: FSMContext):
    await db.connect_to_db()
    if msg.text.lower() != "ничего":
        user_id = msg.from_user.id
        await db.connect_to_db()
        try:
            await db.execute_sql(sql=f"UPDATE Modules SET description = %s "
                                     f"WHERE user_id = {user_id} AND module_name = %s",
                                 args=(msg.text, user_module_names[user_id]))
            # delete values associated with specific user_id
            del user_module_names[user_id]

            response = """
Модуль успешно создан\U0001F3C6
Теперь выбери как будут добавлены слова в модуль на кнопках ниже:
\t\t\U000025AB Вручную
\t\t\U000025AB Переведенные слова в Google документе
\t\t\U000025AB Переведенные слова в .txt и .xlsx документах
\t\t\U000025AB Добавить слова в модуль позже
"""
            await state.clear()
            await msg.answer(response, reply_markup=Menu.add_words())
        except aiomysql.OperationalError as e:
            await msg.answer("Не вышло добавить описание для модуля\U0001F61E")
            logging.log(logging.ERROR, f"Error adding new description: {e}")
        except aiomysql.IntegrityError as e:
            await msg.answer("Не вышло добавить описание для модуля\U0001F61E")
            logging.log(logging.ERROR, f"Error adding new description: {e}")
        finally:
            await db.close_connection()


@router.message(F.text == "Добавить слова позже\U000023F3")
async def handle_add_words_later_case(msg: types.Message):
    response = """Модуль успешно создан и ты можешь в любой момент добавить в него слова\U0001F642"""
    await msg.answer(response, reply_markup=Menu.main_actions())


@router.message(F.text == "Слова из google документа\U0001F310")
async def handle_add_words_google_doc(msg: types.Message):
    pass


@router.message(F.text == "Слова из .txt или .xlsx документа\U0001F4C4")
async def handle_add_words_doc(msg: types.Message):
    pass


@router.message(F.text == "Вручную\U0000270D")
async def handle_add_words_manually(msg: types.Message):
    pass


@router.message(F.text == "Мои модули\U0001F5C3")
async def my_modules(msg: types.Message):
    user_id = msg.from_user.id
    modules = db.show_modules_by_id(user_id)

