from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import logging
import aiomysql

from states import GeneralState
from db_functionality import DataBase
from menu import Menu


module_creation_router = Router()
db = DataBase()

user_module_names = {}


class SelectModule(StatesGroup):
    waiting_module_id_or_name = State()


@module_creation_router.message(F.text == "Создать модуль\U0001F6E0")
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


@module_creation_router.message(StateFilter(GeneralState.module_creation.module_name))
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


@module_creation_router.message(StateFilter(GeneralState.module_creation.module_description))
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
Теперь выбери как будут добавлены слова в модуль на кнопках ниже:"""
            await state.set_state(SelectModule.waiting_module_id_or_name)
            await msg.answer(response, reply_markup=Menu.add_words())
        except aiomysql.OperationalError as e:
            await msg.answer("Не вышло добавить описание для модуля\U0001F61E")
            logging.log(logging.ERROR, f"Error adding new description: {e}")
        except aiomysql.IntegrityError as e:
            await msg.answer("Не вышло добавить описание для модуля\U0001F61E")
            logging.log(logging.ERROR, f"Error adding new description: {e}")
        finally:
            await db.close_connection()
