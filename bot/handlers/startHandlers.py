from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.storage import FSMContext

from texts import Texts
from keyboards import get_main_kb
from createBot import db, ADMIN_ID


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    if not db.check_user_exists(user_id):
        date = db.add_user(user_id, message.from_user.username)
        try:
            await message.bot.send_message(
                ADMIN_ID,
                f'Новый пользователь бота - {message.from_user.username}\nДата регистрации - {date}'
            )
        except:
            return None
    await message.answer(Texts.startText, reply_markup=get_main_kb(message.from_user.id))


def register_start_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start, CommandStart(), state='*')