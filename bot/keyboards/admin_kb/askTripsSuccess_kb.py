from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_trip_succes_kb(trip_id) -> InlineKeyboardMarkup:
    trip_succes_kb = InlineKeyboardMarkup(2)
    yes_bt = InlineKeyboardButton('ДА✅', callback_data=f'yes_{trip_id}')
    no_bt = InlineKeyboardButton('НЕТ❌', callback_data=f'no_{trip_id}')
    return trip_succes_kb.add(yes_bt, no_bt)


def get_tech_support_kb() -> InlineKeyboardMarkup:
    tech_support_kb = InlineKeyboardMarkup(1)
    admin_bt = InlineKeyboardButton('НАПИСАТЬ В ТЕХ.ПОДДЕРЖКУ', callback_data='tech_sup')
    return tech_support_kb.add(admin_bt)
