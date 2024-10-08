import asyncio
from datetime import datetime

from handlers.users.button_builder import pay_select
from loader import db, dp


async def monthly_payment_group():
    today_date = await display_date()
    all_remover_lifetime = await db.select_lifetime(added_date=today_date)
    if all_remover_lifetime:
        for wise in all_remover_lifetime:
            member_data2 = await db.select_students_one(wise['user_id'])
            if wise['added_date'] == f"{today_date}":
                await remover_chat_group(wise['user_id'], wise['channel_id'])
                mon_buttons = await pay_select(member_data2['language'])
                new_message = await dp.bot.send_message(chat_id=wise['user_id'],
                                                        text=text_repaid[member_data2['language']],
                                                        reply_markup=mon_buttons)
                await db.update_student_pay_message(pay_message_id=new_message.message_id,
                                                    telegram_id=wise['user_id'])
                await db.delete_lifetime(wise['user_id'])


            else:
                pass
        await asyncio.sleep(1)


async def remover_chat_group(user_id, channel):
    hh = await dp.bot.get_chat_member(chat_id=channel, user_id=user_id)
    if hh['status'] == "member":
        await dp.bot.ban_chat_member(chat_id=channel,
                                     user_id=user_id,
                                     revoke_messages=True)


async def display_date():
    today = datetime.today()
    formatted_date = today.strftime("%d.%m.%Y")
    return formatted_date


text_repaid = {
    "ar": "لقد طردناك من المجموعة!\nللعودة إلى المجموعة، يجب عليك إكمال رسوم الاشتراك الشهري.\nالمبلغ - 9.99 دولارًا",
    "en": "We kicked you out of the group!\n"
          "To return to the group, you must make a monthly subscription payment\n"
          "Amount - $9.99"
}
