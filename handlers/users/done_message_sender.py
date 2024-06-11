import asyncio

from handlers.users.words import referral_all_count
from loader import dp, db


async def sender_done():
    search_done = await db.select_students_admin_done()
    if search_done is None:
        pass
    else:
        for sends in search_done:
            db_request = await db.select_students_one(sends['telegram_id'])
            await dp.bot.send_message(chat_id=sends['telegram_id'], text=f"{referral_all_count[db_request['language']]}")
            await db.delete_cycle_admin_done(sends['telegram_id'])
            await asyncio.sleep(1)
