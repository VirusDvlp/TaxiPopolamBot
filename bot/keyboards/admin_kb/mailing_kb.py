from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_add_bt_kb() -> InlineKeyboardMarkup:
    add_bt = InlineKeyboardButton('ДОБАВИТЬ КНОПКУ', callback_data='add_bt')
    send_bt = InlineKeyboardButton('ОТПРАВИТЬ РАССЫЛКУ', callback_data='send')
    return InlineKeyboardMarkup(1).add(add_bt, send_bt)