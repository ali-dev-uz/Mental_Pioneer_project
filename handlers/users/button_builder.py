import asyncio

from aiogram import types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from data.config import STRIPE_TOKEN
from handlers.users.words import pay_button_text, stripe_data, join_button, detail_button, i_paid_button_name, \
    back_paid_button, pay_all_course, paid_type_name_stripe, paid_type_name_crypto
from loader import dp, db


async def languages():
    markup = InlineKeyboardMarkup(row_width=2)
    arabic = InlineKeyboardButton("🇦🇪Arabic", callback_data='ar')
    english = InlineKeyboardButton("🇺🇸English", callback_data='en')
    markup.add(arabic, english)
    return markup


async def pay_select(lan):
    markup = InlineKeyboardMarkup(row_width=1)
    stripe = InlineKeyboardButton(f'{paid_type_name_stripe[lan]}', callback_data='stripe')
    crypto = InlineKeyboardButton(f'{paid_type_name_crypto[lan]}', callback_data='crypto')
    markup.add(stripe, crypto)
    return markup


async def pay_crypto(lan):
    list_c = ['course1', 'course2', 'course3', 'course4']
    markup = InlineKeyboardMarkup(row_width=1)
    all_c = await db.select_training_courses_all()
    all_price = 2710
    list_index = 0
    if lan == "ar":
        all_c = await db.select_training_courses_all_arabic()
    for in_c in all_c:
        crypto = InlineKeyboardButton(f"{in_c['course_name']}-{in_c['course_price'] / 100}USDT",
                                      callback_data=f'{list_c[list_index]}')
        markup.add(crypto)
        list_index += 1
        await asyncio.sleep(0.001)

    crypto = InlineKeyboardButton(f"{pay_all_course[lan]}-{all_price / 100}USDT",
                                  callback_data='courseall')
    markup.add(crypto)
    back = InlineKeyboardButton(f"🔙Back", callback_data='back')
    markup.add(back)
    return markup


async def pay_stripe(lan):
    markup = InlineKeyboardMarkup(row_width=1)
    all_c = await db.select_training_courses_all()
    all_price = 2710
    if lan == "ar":
        all_c = await db.select_training_courses_all_arabic()
    for in_c in all_c:
        prices2 = [types.LabeledPrice(label=f"{stripe_data[lan]['label']}", amount=in_c['course_price'])]
        invoice2 = await dp.bot.create_invoice_link(title="Mental Pioneer",
                                                    description=f"{stripe_data[lan]['description']}",
                                                    payload=f"{in_c['course_id']}",
                                                    provider_token=STRIPE_TOKEN,
                                                    currency="USD",
                                                    prices=prices2,
                                                    is_flexible=False)
        stripe = InlineKeyboardButton(f"{in_c['course_name']}-{in_c['course_price'] / 100}$",
                                      url=invoice2)
        markup.add(stripe)
        await asyncio.sleep(0.001)
    prices2 = [types.LabeledPrice(label=f"{stripe_data[lan]['label']}", amount=all_price)]
    invoice2 = await dp.bot.create_invoice_link(title="Mental Pioneer",
                                                description=f"{stripe_data[lan]['description']}",
                                                payload=f"all_course",
                                                provider_token=STRIPE_TOKEN,
                                                currency="USD",
                                                prices=prices2,
                                                is_flexible=False)
    stripe = InlineKeyboardButton(f"{pay_all_course[lan]}-{all_price / 100}$", url=invoice2)
    markup.add(stripe)
    back = InlineKeyboardButton(f"🔙Back", callback_data='back')
    markup.add(back)
    return markup


async def pay_button(lan):
    markup = InlineKeyboardMarkup(row_width=1)
    stripe = InlineKeyboardButton(f'{paid_type_name_stripe[lan]}', callback_data='stripe')
    crypto = InlineKeyboardButton(f'{paid_type_name_crypto[lan]}', callback_data='crypto')
    markup.add(stripe, crypto)
    return markup


# async def pay_button_monthly(user):
#     prices = [types.LabeledPrice(label=f"{stripe_data[lan]['label']}", amount=5700)]
#     invoice = await dp.bot.create_invoice_link(title="Direction Droid course",
#                                                description=f"{stripe_data[lan]['description']}",
#                                                payload="invoice-stripe-link",
#                                                provider_token=STRIPE_TOKEN,
#                                                currency="USD",
#                                                prices=prices,
#                                                is_flexible=False)
#     markup = InlineKeyboardMarkup(row_width=1)
#     stripe = InlineKeyboardButton(f"{pay_button_text[lan]['stripe']}", url=invoice)
#     crypto = InlineKeyboardButton(f"{pay_button_text[lan]['crypto']}", callback_data='crypto')
#     markup.add(stripe)
#     markup.add(crypto)
#     return markup


async def invite_link_add(link, lan):
    markup = InlineKeyboardMarkup(row_width=1)
    link_group = InlineKeyboardButton(f"{join_button[lan]}", url=f"{link}")
    markup.add(link_group)
    return markup


async def invite_link_add_all(link, lan):
    markup = InlineKeyboardMarkup(row_width=1)
    member = 1
    for one_link in link:
        link_group = InlineKeyboardButton(f"{join_button[lan]} | {member}", url=f"{one_link}")
        markup.add(link_group)
        member += 1
        await asyncio.sleep(0.001)

    return markup


async def detail_button_builder(lan, url):
    markup = InlineKeyboardMarkup(row_width=1)
    link_group = InlineKeyboardButton(f"{detail_button[lan]}", url=f"{url}")
    markup.add(link_group)
    return markup


async def admin_panel():
    markup = ReplyKeyboardMarkup(row_width=1)
    all_send = KeyboardButton("📩Send message to all users")
    markup.add(all_send)

    return markup


async def public_notice():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    message = KeyboardButton("🔙Back")
    markup.add(message)

    return markup


async def i_paid_button(lan, call_data):
    markup = InlineKeyboardMarkup(row_width=1)
    link_group = InlineKeyboardButton(f"{i_paid_button_name[lan]}", callback_data=call_data)
    link_back = InlineKeyboardButton(f"{back_paid_button[lan]}", callback_data="back")

    markup.add(link_group)
    markup.add(link_back)
    return markup

# [{'question': '1. What is your name?', 'answers': [{'text': 'A) Correct answer', 'correct': True}, {'text': 'B) Wrong answer', 'correct': False}, {'text': 'C) Wrong answer', 'correct': False}, {'text': 'D) Okay', 'correct': False}]}, {'question': '2. Which country are you a citizen of?', 'answers': [{'text': 'A) Canada', 'correct': False}, {'text': 'B) Uzbekistan', 'correct': True}, {'text': 'C) America', 'correct': False}, {'text': 'D) Africa', 'correct': False}]}]
