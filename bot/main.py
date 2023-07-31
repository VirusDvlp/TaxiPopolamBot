from aiogram import executor

from createBot import dp, db, scheduler
from handlers import register_all_handlers
from scheduler import add_jobs


async def on_startup(dp):
    add_jobs(scheduler)
    register_all_handlers(dp)
    print('Бот успешно запущен')


async def on_shutdown(dp):
    db.close_db()
    print('Бот завершил свою работу')


def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)