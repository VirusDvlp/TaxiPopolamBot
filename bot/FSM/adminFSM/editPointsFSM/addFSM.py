from aiogram.dispatcher.filters.state import StatesGroup, State


class AddFSM(StatesGroup):
    directNameState = State()
    directState = State()
    addTypeState = State() # ask if admin wnat to add new key in the same directory or add new
    pointState = State()
    pointNameState = State()
