from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_admin_kb() -> ReplyKeyboardMarkup:
    main_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    mailing_bt = KeyboardButton('СОЗДАТЬ РАССЫЛКУ ПОЛЬЗОВАТЕЛЯМ✉️')
    edit_points_config_bt = KeyboardButton('ИЗМЕНИТЬ ПАРАМЕТРЫ КОНЕЧНЫХ ТОЧЕК⚙')
    stat_bt = KeyboardButton('СТАТИСТИКА ПО ПОЕЗДКАМ📊')
    exit_bt = KeyboardButton('ВЫЙТИ ИЗ РЕЖИМА АДМИНИСТРТАТОРА🔙')
    return main_admin_kb.add(mailing_bt, edit_points_config_bt, stat_bt, exit_bt)


def get_cancel_kb(input_data: str) -> ReplyKeyboardMarkup:
    cancel_bt = KeyboardButton(f'ОТМЕНИТЬ {input_data}✖️')
    mailing_kb = ReplyKeyboardMarkup().add(cancel_bt)
    return mailing_kb
