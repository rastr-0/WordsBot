from aiogram.fsm.state import State, StatesGroup


class ModuleCreation(StatesGroup):
    module_name = State()
    module_description = State()
    # determines how to add new words: manually, from txt/xlsx or from Google document


class GeneralState(StatesGroup):
    module_creation = ModuleCreation()
    modules_overview = State()
    note_creation = State()


class GetFile(StatesGroup):
    waiting_file = State()


class SelectModule(StatesGroup):
    waiting_module_id_or_name = State()
