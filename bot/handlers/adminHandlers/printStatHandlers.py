import os

from aiogram import types, Dispatcher

from aiogram.dispatcher.filters import Text

from datetime import date

from createBot import db, ADMIN_ID
from utils import get_trip_card, get_file
from FSM import MainAdminFSM


async def send_stat(message = types.Message):
    file = get_file()
    await message.answer_document(file, caption='Отчет за сеодня')
    os.remove(f'bot\{file.filename}')    

        
def register_stat_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(send_stat, Text('СТАТИСТИКА ПО ПОЕЗДКАМ📊'), state=MainAdminFSM.adminState)
