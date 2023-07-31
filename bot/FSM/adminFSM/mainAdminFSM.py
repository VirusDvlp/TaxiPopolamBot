from aiogram.dispatcher.filters.state import State, StatesGroup


class MainAdminFSM(StatesGroup):
    adminState = State()