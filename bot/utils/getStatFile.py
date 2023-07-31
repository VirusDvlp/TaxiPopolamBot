import openpyxl
from datetime import date
from aiogram.types import InputFile

from createBot import db
from utils import get_trip_card


def get_file():
    today = date.today()
    file_name = f'Отчёт_{today}.xlsx'
    fp = f'bot\{file_name}'
    drives = db.get_all_today_drives(today)
    file = openpyxl.Workbook(write_only=True)
    file.create_sheet('main', 0)
    page = file.get_sheet_by_name('main')
    page.column_dimensions['A'].width = 16
    page.column_dimensions['B'].width = 12
    page.column_dimensions['C'].width = 7
    page.column_dimensions['D'].width = 40
    page.column_dimensions['E'].width = 40
    page.column_dimensions['F'].width = 24
    page.column_dimensions['G'].width = 10
    page.append(['Дата', 'Никнейм', 'Статус', 'откуда', 'Куда', 'Дата, время поездки', 'Успешно?'])
    for drive in drives:
        user = get_trip_card(
            str(drive['from_direct']),
            drive['from_point'],
            str(drive['where_direct']),
            drive['where_point'],
            [drive['date'], drive['time']],
            drive['user_name'],
            drive['active'],
            drive['success']
        )['values']
        page.append(
            [
                user['datetime'],
                user['userName'],
                user['status'],
                f'{user["fromDirect"]}, {user["fromPoint"]}',
                f'{user["whereDirect"]}, {user["wherePoint"]}',
                today,
                user['success']
            ]
        )
    file.save(fp)
    file.close()
    sending_file = InputFile(fp)
    return sending_file