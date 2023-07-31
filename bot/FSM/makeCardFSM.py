'''FSM for companion searching'''
from aiogram.dispatcher.filters.state import State, StatesGroup


class MakeCardFSM(StatesGroup):
    whereFromDirectionState = State()
    whereFromPointState = State()
    whereDirectionState = State()
    wherePointState = State()
    dateTimeState = State()
    techSupprotState = State()
    