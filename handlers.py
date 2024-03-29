from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup, InlineKeyboardButton

from db_functionality import DataBase


def actions_menu_buttons():
    kb = [
        [types.KeyboardButton(text="Мои модули\U0001F5C3")],
        [types.KeyboardButton(text="Создать модуль\U0001F6E0")],
        [types.KeyboardButton(text="Заметки\U0001F4DD")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


class Module:
    def __init__(self):
        self.data = {}

    def name(self, module_name):
        self.data['name'] = module_name

    def description(self, module_description):
        self.data['description'] = module_description

    def data(self):
        return self.data


router = Router()
db = DataBase()
module = Module()


class ModuleCreation(StatesGroup):
    module_name = State()
    module_description = State()
    # determines how to add new words: manually, from txt/xlsx or from Google document
    adding_words_type = State()


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

    await msg.answer(response, reply_markup=actions_menu_buttons())


@router.message(F.text == "Создать модуль\U0001F6E0")
async def create_module(msg: types.Message, state: FSMContext):
    await state.set_state(GeneralState.module_creation.module_name)

    user_id = msg.from_user.id

    # add user to the table Users
    await db.connect_to_db()
    await db.execute_sql("INSERT INTO Users (user_id) VALUES (%s)", user_id)
    await db.close_connection()

    response = """Теперь выбери название своего нового модуля"""
    await msg.answer(response)


@router.message(StateFilter(GeneralState.module_creation.module_name))
async def set_module_name(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id

    # add module name to users new module
    await db.connect_to_db()
    await db.execute_sql("INSERT INTO Modules (user_id, module_name) VALUES (%s, %s)", (user_id, msg.text))
    await db.close_connection()

    module.name(msg.text)

    response = """Хорошо\n
Теперь добавь описание модуля, для пропуска этого пункта отправь \"ничего\""""
    await msg.answer(response)
    await state.set_state(GeneralState.module_creation.module_description)


@router.message(StateFilter(GeneralState.module_creation.module_description))
async def set_module_description(msg: types.Message, state: FSMContext):
    await db.connect_to_db()
    if msg.text != "Ничего":
        module.description(msg.text)

    await state.set_state(GeneralState.module_creation.adding_words_type)


@router.message(StateFilter(GeneralState.module_creation.adding_words_type))
async def determine_type_for_adding_new_words(msg: types.Message, state: FSMContext):
    response = """Ты выбрал название и описание для модуля
Теперь выбери как будут добавлены слова в модуль на кнопках ниже:
\t\t\U000025AB Вручную
\t\t\U000025AB Переведенные слова в Google документе
\t\t\U000025AB Переведенные слова в .txt и .xlsx документах
\t\t\U000025AB Добавить слова в модуль позже
"""
    kb = [
        [InlineKeyboardButton(text="Вручную\U0000270D")],
        [InlineKeyboardButton(text='Слова из google документа\U0001F310')],
        [InlineKeyboardButton(text='Слова из .txt или .xlsx документа\U0001F4C4')],
        [InlineKeyboardButton(text='Добавить слова позже\U000023F3')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await state.clear()
    await msg.answer(response, reply_markup=keyboard)


@router.message(F.text == "Добавить слова позже")
async def handle_add_words_later_case(msg: types.Message):
    response = """Модуль успешно создан и ты можешь в любой момент добавить в него слова\U0001F642"""
    await msg.answer(response, reply_markup=actions_menu_buttons())


@router.message(F.text == "Слова из google документа")
async def handle_add_words_google_doc(msg: types.Message):
    pass