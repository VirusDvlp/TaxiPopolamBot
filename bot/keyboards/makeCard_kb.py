from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import json


def get_list_of_directions_kb() -> InlineKeyboardMarkup:
    with open('bot/pointsInfo.json', 'r', encoding='utf-8') as file:
        info = json.load(file)
    list_of_directions_kb = InlineKeyboardMarkup(1)
    for direct in info.keys():
        direct_bt = InlineKeyboardButton(info[direct]['name'], callback_data=f'direct_{direct}')
        list_of_directions_kb.add(direct_bt)
    return list_of_directions_kb


def get_list_of_points_kb(dir) -> InlineKeyboardMarkup:
    with open('bot/pointsInfo.json', 'r', encoding='utf-8') as file:
        info = json.load(file)
    list_of_points_kb = InlineKeyboardMarkup(1) 
    direct = info[str(dir)]
    for place in list(direct.keys())[1:]:
        i = 0
        for point in direct[place]:
            point_bt = InlineKeyboardButton(point, callback_data=f'point_{place}*{i}')
            i += 1
            list_of_points_kb.add(point_bt)
    return list_of_points_kb


def get_cancel_search_kb(trip_id: int) -> InlineKeyboardMarkup:
    cancel_search_kb = InlineKeyboardMarkup(1)
    cancel_bt = InlineKeyboardButton('ОСТАНОВИТЬ ПОИСК ПОПУТЧИКОВ❌', callback_data=f'cancel_{trip_id}')
    return cancel_search_kb.add(cancel_bt)

def get_step_back_kb() -> ReplyKeyboardMarkup:
    step_back_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_bt = KeyboardButton('ВЕРНУТЬСЯ В МЕНЮ')
    step_back_bt = KeyboardButton('ВЕРНУТЬСЯ НА ШАГ НАЗАД🔙')
    return step_back_kb.add(step_back_bt).add(cancel_bt)
