import asyncio
import datetime

import pytz
from aiogram import types
from cryptapi import CryptAPIHelper
from datetime import datetime, timedelta

from handlers.users.button_builder import invite_link_add, i_paid_button, pay_button, pay_stripe, pay_crypto, \
    invite_link_add_all
from handlers.users.monthly_payment import display_date
from handlers.users.words import successful_payment, already_paid, waiting_paid, bug_paid, re_start_text, next_start, \
    start_text, text_57_py, list_course, crypto_pay
from loader import dp, db


@dp.callback_query_handler(text='back')
async def crypto_checker_back(call: types.CallbackQuery):
    member = call.message.chat.id
    db_request = await db.select_students_one(member)
    lan = db_request["language"]
    keyword_but = await pay_button(lan)
    message_id = await call.message.answer(crypto_pay[lan], reply_markup=keyword_but)

    try:
        await call.message.delete()
    except:
        pass
    await db.update_student_pay_message(pay_message_id=message_id.message_id,
                                        telegram_id=member)


@dp.callback_query_handler(text='crypto')
async def crypto_checker_crypto(call: types.CallbackQuery):
    member = call.message.chat.id
    db_request = await db.select_students_one(member)
    lan = db_request["language"]
    try:
        await call.message.delete()
    except:
        pass
    keyboard = await pay_crypto(lan)
    await call.message.answer(text=f"{list_course[lan]}", reply_markup=keyboard)


@dp.callback_query_handler(text=['course1c', 'course2c', 'course3c', 'course4c', 'courseallc'])
async def crypto_checker_paid(call: types.CallbackQuery):
    db_request3 = await db.select_students_one(call.message.chat.id)
    ca = CryptAPIHelper(
        'bep20/usdt',
        '0x7292E1E11f5bfae961c4B1d4d4600385142e9c92',
        'https://webhook.site/test-bep202',
        {
            'order_id': f'crypto{call.message.chat.id}'
        },
        {
            'convert': 0,
            'multi_token': 0,
            'confirmations': 1,
            'pending': 1
        }
    )
    address_pay2 = ca.get_address()['address_in']
    data_api2 = ca.get_logs()
    chat_type = call.data
    db_request = await db.select_students_one(call.message.chat.id)
    if not data_api2['callbacks']:
        print("Address (BEP20): " + address_pay2)
        await call.answer(text=f"{waiting_paid[db_request3['language']]}", show_alert=True)
    else:
        if 9 <= float(data_api2['callbacks'][0]['value_coin']) <= 10:
            try:
                chat_select = {'course1c': {"ar": -1002245707991, "en": -1002193321511},
                               'course2c': {"ar": -1002213759182, "en": -1002246600813},
                               'course3c': {"ar": -1002222132173, "en": -1002215313141},
                               'course4c': {"ar": -1002153988064, "en": -1002216267911},
                               }
                await dp.bot.unban_chat_member(chat_id=chat_select[chat_type][db_request['language']],
                                               user_id=call.message.chat.id,
                                               only_if_banned=True)
                channel_link = await dp.bot.create_chat_invite_link(
                    chat_id=chat_select[chat_type][db_request['language']],
                    member_limit=1,
                    name=f"Repaid{call.message.chat.id}")
                keyword_button = await invite_link_add(channel_link['invite_link'], db_request['language'])
                await call.message.answer_photo(photo='https://t.me/bsbsi39idjdjxj/620',
                                                caption=f"{text_57_py[db_request['language']]}",
                                                reply_markup=keyword_button)
                today = datetime.today()
                future_date = today + timedelta(days=30)
                formatted_date = future_date.strftime("%d.%m.%Y")
                await db.add_lifetime(user_id=call.message.chat.id,
                                      added_date=f"{formatted_date}",
                                      channel_id=chat_select[chat_type][db_request['language']],
                                      course_id=chat_type)
                await dp.bot.send_message(chat_id=-1001871966486,
                                          text=f"🟢<b>Mental Pioneer</b>\n"
                                               f"💵Amount: {data_api2['callbacks'][0]['value_coin']}USDT\n"
                                               f"👤Payer: {call.message.chat.id}")
            except:
                pass
        elif 25 <= float(data_api2['callbacks'][0]['value_coin']) <= 30 and call.data == "courseallc":
            chat_select = {'course1c': {"ar": -1002245707991, "en": -1002193321511},
                           'course2c': {"ar": -1002213759182, "en": -1002246600813},
                           'course3c': {"ar": -1002222132173, "en": -1002215313141},
                           'course4c': {"ar": -1002153988064, "en": -1002216267911},
                           }
            keyword_buttons_link = []
            for one_one in chat_select.keys():
                await dp.bot.unban_chat_member(chat_id=chat_select[one_one][db_request['language']],
                                               user_id=call.message.chat.id,
                                               only_if_banned=True)
                channel_link = await dp.bot.create_chat_invite_link(
                    chat_id=chat_select[one_one][db_request['language']],
                    member_limit=1,
                    name=f"Repaid{call.message.chat.id}")
                keyword_buttons_link.append(channel_link['invite_link'])
                today = datetime.today()
                future_date = today + timedelta(days=30)
                formatted_date = future_date.strftime("%d.%m.%Y")
                await db.add_lifetime(user_id=call.message.chat.id,
                                      added_date=f"{formatted_date}",
                                      channel_id=chat_select[one_one][db_request['language']],
                                      course_id=one_one)
                await asyncio.sleep(0.001)
            keyword_button = await invite_link_add_all(keyword_buttons_link, db_request['language'])
            await call.message.answer_photo(photo='https://t.me/bsbsi39idjdjxj/620',
                                            caption=f"{text_57_py[db_request['language']]}",
                                            reply_markup=keyword_button)
            await dp.bot.send_message(chat_id=-1001871966486,
                                      text=f"🟢<b>Mental Pioneer</b>\n"
                                           f"💵Amount: {data_api2['callbacks'][0]['value_coin']}USDT\n"
                                           f"👤Payer: {call.message.chat.id}")
            try:
                await dp.bot.delete_message(chat_id=call.message.chat.id,
                                            message_id=int(db_request['pay_message_id']))
            except:
                pass
        else:
            await call.answer(text=f"{bug_paid[db_request3['language']]}", show_alert=True)


@dp.callback_query_handler(text=['course1', 'course2', 'course3', 'course4', 'courseall'])
async def cryptos_checker(call: types.CallbackQuery):
    db_request2 = await db.select_students_one(call.message.chat.id)
    cost = 9.99
    if call.data == "courseall":
        cost = 27.1
    ca = CryptAPIHelper(
        'bep20/usdt',
        '0x7292E1E11f5bfae961c4B1d4d4600385142e9c92',
        'https://webhook.site/test-bep202',
        {
            'order_id': f'crypto{call.message.chat.id}'
        },
        {
            'convert': 0,
            'multi_token': 0,
            'confirmations': 1,
            'pending': 1
        }
    )
    address_pay = ca.get_address()['address_in']
    data_api = ca.get_logs()
    en_text = (f"<b>🪙 Amount:</b>  {cost} USDT\n"
               f"Please send exact amount (after fees).\n\n"
               f"⚡ <b>Network:</b> (BSC)/ BEP20\n\n"
               f"🏦 <b>Deposit Address (Tap to copy):</b>\n"
               f"<code>{address_pay}</code>\n\n"
               f"⚠ Sending any other currency to this address may result in the loss of your deposit.\n\n"
               f"<b>Please note, After making the payment, click the 'I paid' button below. Please keep this page open during payment processing, which may take up to 15 minutes.\n"
               f"Tap the message to copy the wallet address.</b>")

    ar_text = (f"<b>🪙 المبلغ:</b>  {cost} USDT\n"
               f"يرجى إرسال المبلغ الدقيق (بعد الرسوم).\n\n"
               f"⚡ <b>الشبكة:</b> (BSC)/ BEP20\n\n"
               f"🏦 <b>عنوان الإيداع (انقر للنسخ):</b>\n"
               f"<code>{address_pay}</code>\n\n"
               f"⚠ إرسال أي عملة أخرى إلى هذا العنوان قد يؤدي إلى فقدان إيداعك.\n\n"
               "<b>يرجى ملاحظة، بعد إتمام الدفع، انقر على زر 'لقد دفعت' أدناه. يرجى الاحتفاظ بهذه الصفحة مفتوحة أثناء معالجة الدفع، والتي قد تستغرق ما يصل إلى 15 دقيقة.</b>\nانقر على الرسالة لنسخ عنوان المحفظة.")

    keyboard_paid = await i_paid_button(db_request2['language'], f"{call.data}c")
    if not data_api['callbacks']:
        print("Address (BEP20): " + address_pay)
        if db_request2['language'] == "en":
            try:
                await call.message.delete()
            except:
                pass
            hey_py = await call.message.answer(text=f"{en_text}",
                                               reply_markup=keyboard_paid)
        else:
            try:
                await call.message.delete()
            except:
                pass
            hey_py = await call.message.answer(text=f"{ar_text}",
                                               reply_markup=keyboard_paid)
        await db.update_student_pay_message(pay_message_id=hey_py.message_id,
                                            telegram_id=call.message.chat.id)
    else:
        await call.answer(text=f"{already_paid[db_request2['language']]}✅", show_alert=True)


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre: types.PreCheckoutQuery):
    await dp.bot.answer_pre_checkout_query(pre.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def payment(message: types.Message):
    db_request = await db.select_students_one(message.chat.id)
    chat_type = message.successful_payment.invoice_payload
    if 9 <= float(message.successful_payment.total_amount / 100) <= 10:
        try:
            chat_select = {'course1': {"ar": -1002245707991, "en": -1002193321511},
                           'course2': {"ar": -1002213759182, "en": -1002246600813},
                           'course3': {"ar": -1002222132173, "en": -1002215313141},
                           'course4': {"ar": -1002153988064, "en": -1002216267911},
                           }
            await dp.bot.unban_chat_member(chat_id=chat_select[chat_type][db_request['language']],
                                           user_id=message.chat.id,
                                           only_if_banned=True)
            channel_link = await dp.bot.create_chat_invite_link(chat_id=chat_select[chat_type][db_request['language']],
                                                                member_limit=1,
                                                                name=f"Repaid{message.chat.id}")
            keyword_button = await invite_link_add(channel_link['invite_link'], db_request['language'])
            await message.answer_photo(photo='https://t.me/bsbsi39idjdjxj/620',
                                       caption=f"{text_57_py[db_request['language']]}",
                                       reply_markup=keyword_button)
            today = datetime.today()
            future_date = today + timedelta(days=30)
            formatted_date = future_date.strftime("%d.%m.%Y")
            await db.add_lifetime(user_id=message.chat.id,
                                  added_date=f"{formatted_date}",
                                  channel_id=chat_select[chat_type][db_request['language']],
                                  course_id=chat_type)
            await dp.bot.send_message(chat_id=-1001871966486,
                                      text=f"🟢<b>Mental Pioneer</b>\n"
                                           f"💵Amount: {message.successful_payment.total_amount / 100}{message.successful_payment.currency}\n"
                                           f"👤Payer: {message.chat.id}")
        except:
            pass
    elif 25 <= float(message.successful_payment.total_amount / 100) <= 30 and chat_type == "all_course":
        chat_select = {'course1': {"ar": -1002245707991, "en": -1002193321511},
                       'course2': {"ar": -1002213759182, "en": -1002246600813},
                       'course3': {"ar": -1002222132173, "en": -1002215313141},
                       'course4': {"ar": -1002153988064, "en": -1002216267911},
                       }
        keyword_buttons_link = []
        for one_one in chat_select.keys():
            await dp.bot.unban_chat_member(chat_id=chat_select[one_one][db_request['language']],
                                           user_id=message.chat.id,
                                           only_if_banned=True)
            channel_link = await dp.bot.create_chat_invite_link(chat_id=chat_select[one_one][db_request['language']],
                                                                member_limit=1,
                                                                name=f"Repaid{message.chat.id}")
            keyword_buttons_link.append(channel_link['invite_link'])
            today = datetime.today()
            future_date = today + timedelta(days=30)
            formatted_date = future_date.strftime("%d.%m.%Y")
            await db.add_lifetime(user_id=message.chat.id,
                                  added_date=f"{formatted_date}",
                                  channel_id=chat_select[one_one][db_request['language']],
                                  course_id=one_one)
            await asyncio.sleep(0.001)
        keyword_button = await invite_link_add_all(keyword_buttons_link, db_request['language'])
        await message.answer_photo(photo='https://t.me/bsbsi39idjdjxj/620',
                                   caption=f"{text_57_py[db_request['language']]}",
                                   reply_markup=keyword_button)
        await dp.bot.send_message(chat_id=-1001871966486,
                                  text=f"🟢<b>Mental Pioneer</b>\n"
                                       f"💵Amount: {message.successful_payment.total_amount / 100}{message.successful_payment.currency}\n"
                                       f"👤Payer: {message.chat.id}")
    try:
        await dp.bot.delete_message(chat_id=message.chat.id,
                                    message_id=int(db_request['pay_message_id']))
    except:
        pass


async def get_day_of_week(lan):
    uae_tz = pytz.timezone('Asia/Dubai')
    current_time = datetime.datetime.now(uae_tz)
    day_of_weekly = current_time.weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    channel_ids = {
        "Monday": {"en": -1002053101294,
                   "ar": -1002137395521},
        "Tuesday": {"en": -1002104317649,
                    "ar": -1002009521367},
        "Wednesday": {"en": -1002001918933,
                      "ar": -1002050117788},
        "Thursday": {"en": -1002025930027,
                     "ar": -1001830011413},
        "Friday": {"en": -1002139375128,
                   "ar": -1002046248938},
        "Saturday": {"en": -1002105710154,
                     "ar": -1001900177055},
        "Sunday": {"en": -1002047687481,
                   "ar": -1002028676437}
    }
    return channel_ids[days[day_of_weekly]][lan], days[day_of_weekly]


async def get_today_date():
    uae_tz = pytz.timezone('Asia/Dubai')

    # Get the current date in the UAE time zone
    today_date_aue = datetime.datetime.now(uae_tz).date()

    # Format the date as required (DD.MM.YYYY)
    formatted_date = today_date_aue.strftime('%d.%m.%Y')

    return formatted_date
