from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from texts import Texts
from createBot import ADMIN_ID


def get_main_kb(user_id: int) -> ReplyKeyboardMarkup:
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True)    
    if user_id == int(ADMIN_ID):
        admin_bt = KeyboardButton('АДМИН-ПАНЕЛЬ')
        main_kb.add(admin_bt)
    search_bt = KeyboardButton(Texts.searchButthonText)
    return main_kb.add(search_bt)