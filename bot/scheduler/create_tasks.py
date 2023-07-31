import os

from aiogram.types import InputFile

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from datetime import timezone, timedelta, datetime

from createBot import bot, ADMIN_ID
from utils import get_file
from .checkActiveTrips import check_active_trips


async def create_stat_for_admin(scheduler: AsyncIOScheduler):
    file = get_file()
    date = datetime.today() + timedelta(days=1)
    tz = timezone(timedelta(hours=5))
    scheduler.add_job(send_stat_to_admin, CronTrigger(date.year, date.month, date.day, 9, tz), file)



async def send_stat_to_admin(file):
    await bot.send_document(ADMIN_ID, file, caption='Отчет за сегодня')
    os.remove(f'bot\{file.filename}')


def add_jobs(scheduler: AsyncIOScheduler):
    scheduler.add_job(check_active_trips, IntervalTrigger(hours=1))
    scheduler.add_job(
        create_stat_for_admin,
        CronTrigger(hour=23, minute=59, timezone=timezone(timedelta(hours=5))),
        (scheduler,)
    )
    scheduler.start()
