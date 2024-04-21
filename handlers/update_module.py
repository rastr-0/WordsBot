from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from menu import Menu
from document import XlsxFile, TxtFile
from states import GetFile


update_module_router = Router()


@update_module_router.message(F.text == "Добавить слова позже\U000023F3")
async def handle_add_words_later_case(msg: types.Message):
    response = """Ты можешь в любой момент вернуться к модулю и добавить в него слова\U0001F642"""
    await msg.answer(response, reply_markup=Menu.main_actions())


@update_module_router.message(F.text == "Слова из google документа\U0001F310")
async def handle_add_words_google_doc(msg: types.Message):
    pass


@update_module_router.message(F.text == "Слова из .txt или .xlsx документа\U0001F4C4")
async def handle_add_words_doc(msg: types.Message, state: FSMContext):
    response = """Выбери на кнопах какой документ ты хочешь отправить"""
    await msg.answer(response, Menu.get_file())
    await state.set_state(GetFile.waiting_file)

    await msg.answer_photo(chat_id=msg.from_user.id, photo="media/xlsx_table_example.jpg",
                           caption="Пример .xlsx файла, который бот сможет обработать")
    await msg.answer_photo(chat_id=msg.from_user.id, photo="media/txt_file_example.txt",
                           caption="Пример .txt файла, который бот сможет обработать")


@update_module_router.message(F.text == ".xlsx файл", StateFilter(GetFile.waiting_file))
async def write_xlsx_data_to_db(msg: types.Message):
    if not msg.document:
        await msg.reply("Пришли .xlsx файл \U0001F4C4 для добавления переведенных слов в базу бота!")
        return

    try:
        XlsxFile.parse(msg.document)
    except:
        pass


@update_module_router.message(F.text == ".txt файл", StateFilter(GetFile.waiting_file))
async def write_txt_data_to_db(msg: types.Message):
    pass


@update_module_router.message(F.text == "Вручную\U0000270D")
async def handle_add_words_manually(msg: types.Message):
    pass
