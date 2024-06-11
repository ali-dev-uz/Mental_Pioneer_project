from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

from handlers.users.done_message_sender import sender_done
from handlers.users.monthly_payment import monthly_payment_group
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    from handlers.users.channel_control import main_control
    scheduler = AsyncIOScheduler()
    await db.create()
    # await db.drop_users()
    await db.create_payment_users()
    await db.create_message_list()
    await db.create_done_message_admin()
    await db.create_chat_history()
    await db.create_message_list_ar()
    await db.create_chat_lifetime()
    dubai_tz = timezone('Asia/Dubai')
    scheduler.timezone = dubai_tz
    scheduler.add_job(main_control, trigger='cron', hour=9, minute=1)
    scheduler.add_job(sender_done, 'interval', minutes=10)
    scheduler.add_job(monthly_payment_group, 'interval', hours=12)


    # Start the scheduler
    scheduler.start()
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

