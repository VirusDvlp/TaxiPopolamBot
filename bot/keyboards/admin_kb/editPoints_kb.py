from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_change_type_kb() -> InlineKeyboardMarkup:
    change_type_kb = InlineKeyboardMarkup(1)
    add_bt = InlineKeyboardButton('ДОБАВИТЬ НОВОЕ', callback_data='add')
    del_bt = InlineKeyboardButton('УДАЛИТЬ УЖЕ ИМЯЮЩЕЕСЯ', callback_data='del')
    return change_type_kb.add(add_bt, del_bt)


def get_what_change_kb() -> InlineKeyboardMarkup:
    what_change_kb = InlineKeyboardMarkup(1)
    direct_bt = InlineKeyboardButton('НАПРАВЛЕНИЯ', callback_data='directs')
    points_bt = InlineKeyboardButton('НАСЕЛЁННЫЕ ПУНКТЫ', callback_data='points')
    return what_change_kb.add(direct_bt, points_bt)


def get_add_point_type_kb() -> InlineKeyboardMarkup:
    add_point_type_kb = InlineKeyboardMarkup(1)
    new_bt = InlineKeyboardButton('НОВАЯ ГРУППА', callback_data='new')
    old_bt = InlineKeyboardButton('УЖЕ ИМЯЮЩАЯСЯ', callback_data='old')
    return add_point_type_kb.add(new_bt, old_bt)


def get_points_group_kb(places: dict) -> InlineKeyboardMarkup:
    points_group_kb = InlineKeyboardMarkup(1)
    for point_group in list(places.keys())[1 : -1]:
        bt_text = '|'.join(places[point_group])
        group_bt = InlineKeyboardButton(bt_text, callback_data=f'gr_{point_group}')
        points_group_kb.add(group_bt)
    return points_group_kb
