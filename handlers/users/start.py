import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import asyncio
from data.config import ADMINS
from handlers.users.button_builder import languages, pay_button, admin_panel, pay_select, pay_stripe
from handlers.users.words import select_language, start_text, re_start_text, next_start, list_course, crypto_pay
from loader import dp, db


@dp.callback_query_handler(text='stripe')
async def crypto_type(calls: types.CallbackQuery):
    member = calls.message.chat.id
    db_request = await db.select_students_one(member)
    lan = db_request["language"]
    try:
        await calls.message.delete()
    except:
        pass
    keyboard = await pay_stripe(lan)
    logging.exception(keyboard)
    await calls.message.answer(text=f"{list_course[lan]}", reply_markup=keyboard)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    member = message.chat.id
    db_request = await db.select_students_one(member)
    if str(member) not in ADMINS and db_request is not None:
        lan = db_request["language"]
        await message.answer(f"{re_start_text[lan]}{message.from_user.get_mention(as_html=True)}")
        keyword_but = await pay_select(lan)
        message_id = await message.answer(start_text[lan], reply_markup=keyword_but)

        try:
            pay_ids = await db.select_students_one(telegram_id=member)
            await dp.bot.delete_message(chat_id=member,
                                        message_id=int(pay_ids['pay_message_id']))
        except:
            pass
        await db.update_student_pay_message(pay_message_id=message_id.message_id,
                                            telegram_id=member)
    elif str(member) not in ADMINS and db_request is None:
        keyboard = await languages()
        await db.add_student(telegram_id=member)

        await message.answer(text=select_language['en'],
                             reply_markup=keyboard)
    elif str(member) in ADMINS:
        keyword_admin = await admin_panel()
        await message.answer("Welcome Admin!", reply_markup=keyword_admin)


@dp.callback_query_handler(text=['en', 'ar'])
async def language_checker(calls: types.CallbackQuery):
    call = calls
    member_call = call.message.chat.id
    try:
        await call.answer(cache_time=1)
        await calls.message.delete()
    except:
        pass
    db_request_call = await db.select_students_one(member_call)
    if str(member_call) not in ADMINS and db_request_call["language"] is not None:
        await db.update_student_language(telegram_id=member_call,
                                         language=f"{call.data}")
    elif str(member_call) not in ADMINS and db_request_call["language"] is None:
        await asyncio.sleep(0.1)
        await db.update_student_language(telegram_id=member_call,
                                         language=f"{call.data}")
        await call.message.answer(start_text[f"{call.data}"])
        await asyncio.sleep(0.1)
        keyword_but = await pay_select(call.data)
        message_id = await call.message.answer(crypto_pay[call.data], reply_markup=keyword_but)
        await db.update_student_pay_message(pay_message_id=message_id.message_id,
                                            telegram_id=member_call)
    try:
        await call.message.delete()
    except:
        pass
