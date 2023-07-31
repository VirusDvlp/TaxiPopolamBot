from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.storage import FSMContext


from FSM import MainAdminFSM
from keyboards import get_main_admin_kb, get_main_kb
from createBot import ADMIN_ID, db


async def set_admin_mode(message: types.Message):
    await MainAdminFSM.adminState.set()
    await message.answer('Открыта панель администратора', reply_markup=get_main_admin_kb())


async def exit_admin_mode(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Панель администратора закрыта', reply_markup=get_main_kb(message.from_user.id))


async def cancel_admin_action(message: types.Message):
    await MainAdminFSM.adminState.set()
    await message.answer(f'{message.text.split(" ")[1][0 : -1].lower()} отменено', reply_markup=get_main_admin_kb())


def register_main_admin_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        set_admin_mode,
        Text('АДМИН-ПАНЕЛЬ'),
        IDFilter(int(ADMIN_ID))
    )
    dp.register_message_handler(
        exit_admin_mode,
        Text('ВЫЙТИ ИЗ РЕЖИМА АДМИНИСТРТАТОРА🔙'),
        state=MainAdminFSM.adminState
    )
    dp.register_message_handler(cancel_admin_action, Text(startswith='ОТМЕНИТЬ'), IDFilter(ADMIN_ID), state='*')
