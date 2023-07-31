from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext


from createBot import db, ADMIN_ID
from keyboards import get_tech_support_kb
from FSM import MakeCardFSM


async def succes_trip(callback: types.CallbackQuery):
    db.set_trip_success(callback.data.split('_')[1], True)
    await callback.message.answer('''Отлично! Если у вас есть 
пожелания по улучшению работы бота, напишите в техподдержку''', reply_markup=get_tech_support_kb())
    await callback.message.delete()
    await callback.answer()


async def unsuccess_trip(callback: types.CallbackQuery):
    db.set_trip_success(callback.data.split('_')[1], False)
    await callback.message.answer('''Мне очень жаль. Если у вас есть пожелания 
по улучшению работы бота, напишите в техподдержку''', reply_markup=get_tech_support_kb())
    await callback.message.delete()
    await callback.answer()


async def ask_message_to_admin(callback: types.CallbackQuery):
    await MakeCardFSM.techSupprotState.set()
    await callback.message.answer('''Пришлите сообщение, которое хотите отправить в тех. поддержку''')
    await callback.message.delete()
    await callback.answer()


async def get_message_to_admin(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        await message.bot.send_message(ADMIN_ID, f'Собщение от @{message.from_user.username}\n{message.text}')
    except:
        await message.answer('Что-то пошло не так')
    await message.answer('Ваше сообщение успешно отправлено в тех.поддержку')

def register_succes_trip_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(succes_trip, Text(startswith='yes'), state='*')
    dp.register_callback_query_handler(unsuccess_trip, Text(startswith='no'), state='*')
    dp.register_callback_query_handler(ask_message_to_admin, Text('tech_sup'), state='*')
    dp.register_message_handler(get_message_to_admin, state=MakeCardFSM.techSupprotState)
