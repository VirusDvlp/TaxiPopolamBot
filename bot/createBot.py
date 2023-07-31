import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from database import DataBase

load_dotenv() # Loading environment variables


TOKEN = os.getenv('TOKEN') # bot token
ADMIN_ID = os.getenv("ADMIN_ID")

db = DataBase()

scheduler = AsyncIOScheduler()

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
