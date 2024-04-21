from aiogram import types, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from states import SelectModule


module_actions_router = Router()


@module_actions_router.message(StateFilter(SelectModule.waiting_module_id_or_name))
async def handle_selecting_module(msg: types.Message, state: StatesGroup):
    pass
