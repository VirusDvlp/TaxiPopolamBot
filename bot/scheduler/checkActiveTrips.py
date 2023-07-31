from createBot import db, bot
from texts import Texts
from keyboards import get_trip_succes_kb

async def check_active_trips():
    users = db.check_active_trips()
    for user in users:
        try:
            await bot.send_message(
                user['user_id'],
                Texts.askTripSuccesText,
                reply_markup=get_trip_succes_kb(user['id'])
            )
        except Exception:
            continue