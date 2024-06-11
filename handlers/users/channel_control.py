import asyncio
import datetime
import logging


from states import Personaldata
import pytz
from handlers.users.button_builder import exam_builder

from handlers.users.exam import read_quiz_file
from handlers.users.words import test_description
from loader import dp, db


async def main_control():
    from handlers.users.day_1 import Monday_Cycle_Channel
    from handlers.users.day_2 import Tuesday_Cycle_Channel
    from handlers.users.day_3 import Wednesday_Cycle_Channel
    from handlers.users.day_4 import Thursday_Cycle_Channel
    from handlers.users.day_5 import Friday_Cycle_Channel
    from handlers.users.day_6 import Saturday_Cycle_Channel
    from handlers.users.day_7 import Sunday_Cycle_Channel
    from handlers.users.day_1ar import Monday_Cycle_Channel_ar
    from handlers.users.day_2ar import Tuesday_Cycle_Channel_ar
    from handlers.users.day_3ar import Wednesday_Cycle_Channel_ar
    from handlers.users.day_4ar import Thursday_Cycle_Channel_ar
    from handlers.users.day_5ar import Friday_Cycle_Channel_ar
    from handlers.users.day_6ar import Saturday_Cycle_Channel_ar
    from handlers.users.day_7ar import Sunday_Cycle_Channel_ar
    weekly_format, name_weekly = await get_day_of_week_and_data()
    try:
        await Monday_Cycle_Channel(weekly_format, name_weekly)
    except:
        pass
    try:
        await Tuesday_Cycle_Channel(weekly_format, name_weekly)
    except:
        pass
    try:
        await Wednesday_Cycle_Channel(weekly_format, name_weekly)
    except:
        pass
    try:
        await Thursday_Cycle_Channel(weekly_format, name_weekly)
    except:
        pass
    try:
        await Friday_Cycle_Channel(weekly_format, name_weekly)
    except:
        pass
    try:
        await Saturday_Cycle_Channel(weekly_format, name_weekly)
    except:
        pass
    try:
        await Sunday_Cycle_Channel(weekly_format, name_weekly)
    except:
        pass
    try:
        await Monday_Cycle_Channel_ar(weekly_format, name_weekly)
    except:
        pass
    try:
        await Tuesday_Cycle_Channel_ar(weekly_format, name_weekly)
    except:
        pass
    try:
        await Wednesday_Cycle_Channel_ar(weekly_format, name_weekly)
    except:
        pass
    try:
        await Thursday_Cycle_Channel_ar(weekly_format, name_weekly)
    except:
        pass
    try:
        await Friday_Cycle_Channel_ar(weekly_format, name_weekly)
    except:
        pass
    try:
        await Saturday_Cycle_Channel_ar(weekly_format, name_weekly)
    except:
        pass
    try:
        await Sunday_Cycle_Channel_ar(weekly_format, name_weekly)
    except:
        pass


async def get_day_of_week_and_data():
    uae_tz = pytz.timezone('Asia/Dubai')
    current_time = datetime.datetime.now(uae_tz)
    today_date_aue = datetime.datetime.now(uae_tz).date()
    formatted_date = today_date_aue.strftime('%d.%m.%Y')
    day_of_weekly = current_time.weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return formatted_date, days[day_of_weekly]



async def channel_cleaning(chat_id):
    channel_data = await db.select_chats_id_one(chat_id)
    start_message = int(channel_data['start_message_id'])
    end_message = int(channel_data['end_message_id'])
    range_call = abs(end_message - start_message)
    for check in range(range_call + 1):
        try:
            await dp.bot.delete_message(chat_id=chat_id,
                                        message_id=start_message)
            start_message += 1
            await asyncio.sleep(0.5)
        except:
            pass


async def remove_user_to_channel_and_send_test(chat_id, weekly_format, name_weekly):
    all_remover = await db.select_students_week_name(name_weekly)
    for remover in all_remover:
        if remover['added_time'] != f"{weekly_format}":
            try:
                hh = await dp.bot.get_chat_member(chat_id=chat_id, user_id=int(remover['telegram_id']))
                if hh['status'] == "member":
                    await dp.bot.ban_chat_member(chat_id=chat_id,
                                                 user_id=int(remover['telegram_id']),
                                                 revoke_messages=True)
                    filename = '/home/ubuntu/Direction_Droid/test.txt'  # Update with the correct file path
                    if remover['language'] == "ar":
                        filename = '/home/ubuntu/Direction_Droid/test2.txt'
                    questions = await read_quiz_file(filename)
                    keyword_inline = await exam_builder(user=int(remover['telegram_id']),
                                                        ques=questions)
                    question_order = int(remover['exam_answers'])
                    question_text = questions[question_order]['question']
                    try:
                        await dp.bot.send_message(chat_id=int(remover['telegram_id']),
                                                  text=f"{test_description[remover['language']]}")
                        await asyncio.sleep(0.2)
                        await dp.bot.send_message(chat_id=int(remover['telegram_id']),
                                                  text=f"<b>{question_text}</b>",
                                                  reply_markup=keyword_inline)
                    except Exception as e:
                        logging.exception(e)
            except:
                pass
        else:
            pass
        await asyncio.sleep(0.2)


