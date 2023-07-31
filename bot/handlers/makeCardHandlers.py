'''Handlers for searching companions'''
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ParseMode

from createBot import db
from FSM import MakeCardFSM
from texts import Texts
from keyboards import get_list_of_directions_kb, get_list_of_points_kb, get_cancel_search_kb, get_step_back_kb, get_main_kb
from utils import datetime_filter, get_trip_card


async def ask_where_from_direct(message: types.Message, state: FSMContext):
    await MakeCardFSM.whereFromDirectionState.set()

    await message.answer('⬇Создание карточки поездки⬇', reply_markup=get_step_back_kb())
    msg = await message.answer(
        Texts.makeCard1Text,
        reply_markup=get_list_of_directions_kb()
    )
    async with state.proxy() as data:
        data['message_id'] = msg.message_id


async def ask_where_from_point(callback: types.CallbackQuery, state: FSMContext):
    mess = callback.message
    async with state.proxy() as data:
        data['where_from_direct'] = callback.data.split('_')[1]
        await mess.bot.delete_message(mess.chat.id, data['message_id'])
        await MakeCardFSM.whereFromPointState.set()
        msg  = await mess.answer(
            Texts.makeCard2Text,
            reply_markup=get_list_of_points_kb(data['where_from_direct'])
        )
        data['message_id'] = msg.message_id
    await callback.answer()


async def ask_where_direct(callback: types.CallbackQuery, state: FSMContext):
    mess = callback.message
    async with state.proxy() as data:
        data['where_from_point'] = callback.data.split('_')[1]
        await mess.bot.delete_message(mess.chat.id, data['message_id'])
        await MakeCardFSM.whereDirectionState.set()
        msg = await mess.answer(
            Texts.makeCard3Text,
            reply_markup=get_list_of_directions_kb()
        )
        data['message_id'] = msg.message_id
    await callback.answer()


async def ask_where_point(callback: types.CallbackQuery, state: FSMContext):
    mess = callback.message
    async with state.proxy() as data:
        data['where_direct'] = callback.data.split('_')[1]
        await mess.bot.delete_message(mess.chat.id, data['message_id'])
        await MakeCardFSM.wherePointState.set()
        msg = await mess.answer(
            Texts.makeCard4Text,
            reply_markup=get_list_of_points_kb(data['where_direct'])
        )
        data['message_id'] = msg.message_id
        await callback.answer()


async def ask_datetime(callback: types.CallbackQuery, state: FSMContext):
    mess = callback.message
    async with state.proxy() as data:
        data['where_point'] = callback.data.split('_')[1]
        await mess.bot.delete_message(mess.chat.id, data['message_id'])
        await MakeCardFSM.dateTimeState.set()
        msg = await mess.answer(Texts.makeCard5Text)
        data['message_id'] = msg.message_id
    await callback.answer()

async def finish_card(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.bot.delete_message(message.chat.id, data['message_id'])
        datetime = message.text.split(' ')
        from_direct = data['where_from_direct']
        from_point = data['where_from_point']
        where_direct = data['where_direct']
        where_point = data['where_point']

    trip_id = db.add_trip(
        message.from_user.id,
        from_direct,
        from_point,
        where_direct,
        where_point,
        datetime[0],
        datetime[1]
    )
    await message.answer(
        '''Поздравляем! Ваша поездка создана. ✅.
Когда попутчик будет найден, он напишет вам в личку.
Также бот будет присылать вам подходящих попутчиков на эту дату. Вы сможете написать им самостоятельно.
Когда наступит время вашей поездки, она удалится из системы, чтобы никто не беспокоил вас.
Создавайте несколько поездок, чтобы увеличить шансы в поиске попутчика!
Ниже показана ваша карточка поездки, какой ее видят другие пользователи:''',
        reply_markup=get_main_kb(message.from_user.id)
    )
    card = get_trip_card(
            from_direct,
            from_point,
            where_direct,
            where_point,
            datetime,
            message.from_user.username
        )['card']
    await message.answer(
        card,
        parse_mode=ParseMode().HTML,
        reply_markup=get_cancel_search_kb(trip_id)
    )
    users = db.get_passengers(message.from_user.id, from_direct, from_point, datetime[0])
    if users:
        await message.answer('Мы нашли тебе попутчиков')
        for user in users:
            await message.answer(
                get_trip_card(
                    user['from_direct'],
                    user['from_point'],
                    user['where_direct'],
                    user['where_point'],
                    [user['date'], user['time']],
                    db.get_user_name(user['user_id'])
                )['card'],
                parse_mode=ParseMode.HTML
            )
            try:
                await message.bot.send_message(user['user_id'], card, parse_mode=ParseMode.HTML)
            except:
                continue
    else:
        await message.answer('''На текущий момент нет подходящих попутчиков.
Вам придет уведомление, когда попутчик будет найден 🚕''')
    await state.finish()  
    

async def get_wrong_date(message: types.Message):
    await message.answer('Дата и время поездки указаны неверно, попробуйте еще раз')


async def step_back(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    async with state.proxy() as data:
        await message.bot.delete_message(message.chat.id, data['message_id'])
        if curr_state == 'MakeCardFSM:whereFromPointState':
            await MakeCardFSM.whereFromDirectionState.set()
            msg = await message.answer(Texts.makeCard1Text, reply_markup=get_list_of_directions_kb())
        elif curr_state == 'MakeCardFSM:whereDirectionState':
            await MakeCardFSM.whereFromPointState.set()
            msg = await message.answer(Texts.makeCard2Text, reply_markup=get_list_of_points_kb(data['where_from_direct']))
        elif curr_state == 'MakeCardFSM:wherePointState':
            await MakeCardFSM.whereDirectionState.set()
            msg = await message.answer(Texts.makeCard3Text, reply_markup=get_list_of_directions_kb())
        elif curr_state == 'MakeCardFSM:dateTimeState':
            await MakeCardFSM.wherePointState.set()
            msg = await message.answer(Texts.makeCard4Text, reply_markup=get_list_of_points_kb(data['where_direct']))
        else:
            return None
        data['message_id'] = msg.message_id


async def cancel_search(callback: types.CallbackQuery):
    trip_id = callback.data.split('_')[1]
    db.cancel_search_for_pass(trip_id)
    await callback.answer('Поиск попутчиков по этому маршруту отменён')


async def cancel_making_card(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Создание поездки отменено', reply_markup=get_main_kb(message.from_user.id))


def register_make_card_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(step_back, Text('ВЕРНУТЬСЯ НА ШАГ НАЗАД🔙'), state=MakeCardFSM.all_states)
    dp.register_message_handler(cancel_making_card, Text('ВЕРНУТЬСЯ В МЕНЮ'), state=MakeCardFSM.all_states)
    dp.register_message_handler(ask_where_from_direct, Text('НАЙТИ ПОПУТЧИКА🔎'))
    dp.register_callback_query_handler(
        ask_where_from_point,
        Text(startswith='direct_'),
        state=MakeCardFSM.whereFromDirectionState
    )
    dp.register_callback_query_handler(
        ask_where_direct,
        Text(startswith='point_'), 
        state=MakeCardFSM.whereFromPointState
    )
    dp.register_callback_query_handler(
        ask_where_point,
        Text(startswith='direct_'),
        state=MakeCardFSM.whereDirectionState
    )
    dp.register_callback_query_handler(
        ask_datetime,
        Text(startswith='point_'),
        state=MakeCardFSM.wherePointState
    )
    dp.register_message_handler(
        finish_card,
        lambda message: datetime_filter(message),
        state=MakeCardFSM.dateTimeState
    )
    dp.register_message_handler(get_wrong_date, state=MakeCardFSM.dateTimeState)
    dp.register_callback_query_handler(cancel_search, Text(startswith='cancel_'), state='*')
