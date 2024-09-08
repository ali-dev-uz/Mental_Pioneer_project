from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

from handlers.users.monthly_payment import monthly_payment_group
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    scheduler = AsyncIOScheduler()
    await db.create()
    # await db.drop_users()
    await db.create_payment_users()
    await db.create_chat_lifetime()
    await db.create_training_courses()
    await db.create_training_courses_arabic()
    dubai_tz = timezone('Asia/Dubai')
    scheduler.timezone = dubai_tz
    scheduler.add_job(monthly_payment_group, 'interval', hours=12)


    # Start the scheduler
    scheduler.start()
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

