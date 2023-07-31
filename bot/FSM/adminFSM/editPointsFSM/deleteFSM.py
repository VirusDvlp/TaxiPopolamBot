from aiogram.dispatcher.filters.state import StatesGroup, State


class DeleteFSM(StatesGroup):
    directState = State()
    pointState = State()
