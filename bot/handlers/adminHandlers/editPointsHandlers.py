import json

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text


from keyboards import get_cancel_kb, get_change_type_kb,get_what_change_kb, get_list_of_directions_kb, get_list_of_points_kb, get_add_point_type_kb, get_points_group_kb
from FSM import WhatFSM, AddFSM, DeleteFSM, MainAdminFSM
from utils import update_file


async def ask_change_type(message: types.Message):
    await WhatFSM.first()
    await message.answer('Редактирование конечных точек', reply_markup=get_cancel_kb('РЕДАКТИРОВАНИЕ'))
    await message.answer('Выберите, какое действие хотите совершить', reply_markup=get_change_type_kb())


async def ask_direct_or_points(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        action = callback.data
        data['action'] = action
        if action =='del':
            text = 'удалить'
        elif action == 'add':
            text = 'добавить'
        else:
            await callback.answer()
    await WhatFSM.next()
    await callback.message.answer(f'Выберите, что хотите {text}', reply_markup=get_what_change_kb())
    await callback.answer()


async def get_change_type(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        with open('bot\pointsInfo.json', 'r', encoding='utf-8') as file:
            data['places'] = json.load(file)
        what = callback.data
        data['what'] = what
        if data['action'] == 'del':
            await DeleteFSM.directState.set()
            if what == 'directs':
                await callback.message.answer('Выберите, какое направление хотите удалить', reply_markup=get_list_of_directions_kb())
            elif what == 'points':
                await callback.message.answer('Выберите, населённый пункт из какого направления вы хотите удалить', reply_markup=get_list_of_directions_kb())
            await callback.answer()        
        elif data['action'] == 'add':
            if what == 'directs':
                await AddFSM.directNameState.set()
                await callback.message.answer('Пришлите имя для нового напрвавления')
            elif what == 'points':
                await DeleteFSM.directState.set()
                await callback.message.answer('Выберите, в какое направление вы хотите добавить населённый пункт', reply_markup=get_list_of_directions_kb())
            await callback.answer()


async def get_deleting_direct(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['direct'] = callback.data.split('_')[1]
        if data['action'] == 'del':
            if data['what'] =='directs':
                del data['places'][data['direct']]
                update_file(data['places'])
                await callback.message.answer('Направление успешно удалено')
                await ask_change_type(callback.message)
            else:
                await DeleteFSM.pointState.set()
                await callback.message.answer('Выберите населённый пункт, который хотите удалить', reply_markup=get_list_of_points_kb(data['direct']))
        else:
            await AddFSM.addTypeState.set()
            await callback.message.answer('Вы хотите добавить населённый пункт уже в имющюся группу или создать новую', reply_markup=get_add_point_type_kb())
    await callback.answer()


async def get_direct_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keys_list = data['places'].keys()
        index = str(int(list(keys_list)[-1]) + 1)
        data['places'][index] = {'name': message.text}
        update_file(data['places'])
    await message.answer('Направление успешно добавлено')
    await ask_change_type(message)


async def get_deleting_point(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['point'] = callback.data
        deleting_item = data['point'].split('_')[1].split('*')
        del data['places'][data['direct']][deleting_item[0]][int(deleting_item[1])]
        update_file(data['places'])
        await callback.message.answer('Населённый пункт успешно удалён')
        await ask_change_type(callback.message)
        await callback.answer()

    
async def ask_point_group(callback: types.CallbackQuery, state: FSMContext):
    await AddFSM.pointState.set()
    async with state.proxy() as data:
        await callback.message.answer('Выберите в какую группу пунктов хотите добавить', reply_markup=get_points_group_kb(data['places'][data['direct']]))
    await callback.answer()


async def ask_point_name_1(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        keys_list = data['places'].keys()
        data['point_index'] = str(int(list(keys_list)[-1]) + 1)
    await AddFSM.pointNameState.set()
    await callback.message.answer('Пришлите имя для населённого пункта')


async def ask_point_name_2(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['point_index'] = callback.data.split('_')[1]
    await AddFSM.pointNameState.set()
    await callback.message.answer('Пришлите имя для населённого пункта')


async def get_point_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        point_name = message.text
        point = data['places'][data['direct']].get(data['point_index'])
        if point:
            point.append(point_name)
        else:
            data['places'][data['direct']][data['point_index']] = [point_name]
        update_file(data['places'])
        await message.answer('Населённый пункт успешно добавлен')
        await ask_change_type(message)


def register_points_config_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        ask_change_type,
        Text('ИЗМЕНИТЬ ПАРАМЕТРЫ КОНЕЧНЫХ ТОЧЕК⚙'),
        state=MainAdminFSM.adminState
    )
    dp.register_callback_query_handler(
        ask_direct_or_points,
        state=WhatFSM.typeState,
    )
    dp.register_callback_query_handler(
        get_change_type,
        state=WhatFSM.whatState
    )
    dp.register_callback_query_handler(
        get_deleting_direct,
        Text(startswith='direct_'),
        state=DeleteFSM.directState
    )
    dp.register_message_handler(
        get_direct_name,
        content_types=['text'],
        state=AddFSM.directNameState
    )
    dp.register_callback_query_handler(
        get_deleting_point,
        Text(startswith='point_'),
        state=DeleteFSM.pointState
    )
    dp.register_callback_query_handler(
        ask_point_group,
        Text('old'),
        state=AddFSM.addTypeState
    )
    dp.register_callback_query_handler(
        ask_point_name_1,
        Text('new'),
        state=AddFSM.addTypeState
    )
    dp.register_callback_query_handler(
        ask_point_name_2,
        Text(startswith=['gr_']),
        state=AddFSM.pointState
    )
    dp.register_message_handler(
        get_point_name,
        content_types=['text'],
        state=AddFSM.pointNameState
    )
