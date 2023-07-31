from aiogram.dispatcher.filters.state import StatesGroup, State


class WhatFSM(StatesGroup):
    typeState = State()
    whatState = State()
