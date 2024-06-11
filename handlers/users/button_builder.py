import asyncio

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from data.config import STRIPE_TOKEN
from handlers.users.words import pay_button_text, stripe_data, join_button, detail_button, i_paid_button_name, \
    back_paid_button
from loader import dp, db


async def languages():
    markup = InlineKeyboardMarkup(row_width=2)
    arabic = InlineKeyboardButton("🇦🇪Arabic", callback_data='ar')
    english = InlineKeyboardButton("🇺🇸English", callback_data='en')
    markup.add(arabic, english)
    return markup


async def details_button_user(lan):
    markup = InlineKeyboardMarkup(row_width=1)
    creat_keyboard = InlineKeyboardButton(text="Learn more",
                                          web_app=WebAppInfo(url='https://akobir.co/referraluser'))
    if lan == "ar":
        creat_keyboard = InlineKeyboardButton(text="يتعلم أكثر",
                                              web_app=WebAppInfo(url='https://akobir.co/referraluser'))
    markup.add(creat_keyboard)
    return markup


async def details_button_admin():
    markup = InlineKeyboardMarkup(row_width=1)
    creat_keyboard = InlineKeyboardButton(text="🗄Panel",
                                          web_app=WebAppInfo(url='https://akobir.co/referraladmin'))
    markup.add(creat_keyboard)
    return markup


async def referral_pay_button(lan):
    markup = InlineKeyboardMarkup(row_width=1)
    pay_out = InlineKeyboardButton("🇦🇪Arabic", callback_data='ar_ref')
    if lan == "ar":
        pay_out = InlineKeyboardButton("🇦🇪Arabic", callback_data='ar_ref')

    markup.add(pay_out)
    return markup


async def offer():
    markup = InlineKeyboardMarkup(row_width=1)
    agree = InlineKeyboardButton("I agree", callback_data='agree')
    back = InlineKeyboardButton("🔙Back", callback_data='back')
    markup.add(agree, back)
    return markup


async def pay_button(lan):
    prices2 = [types.LabeledPrice(label=f"{stripe_data[lan]['label']}", amount=25700)]
    invoice2 = await dp.bot.create_invoice_link(title="Consultant Droid course",
                                                description=f"{stripe_data[lan]['description']}",
                                                payload="invoice-stripe-link",
                                                provider_token=STRIPE_TOKEN,
                                                currency="USD",
                                                prices=prices2,
                                                is_flexible=False)
    markup = InlineKeyboardMarkup(row_width=2)
    stripe2 = InlineKeyboardButton(f"{pay_button_text[lan]['stripe']}-257$", url=invoice2)
    crypto2 = InlineKeyboardButton(f"{pay_button_text[lan]['crypto']}-257USDT", callback_data='crypto')
    markup.add(stripe2, crypto2)
    prices = [types.LabeledPrice(label=f"{stripe_data[lan]['label']}", amount=5700)]
    invoice = await dp.bot.create_invoice_link(title="Consultant Droid course",
                                               description=f"{stripe_data[lan]['description']}",
                                               payload="invoice-stripe-link",
                                               provider_token=STRIPE_TOKEN,
                                               currency="USD",
                                               prices=prices,
                                               is_flexible=False)
    stripe = InlineKeyboardButton(f"{pay_button_text[lan]['stripe']}-57$", url=invoice)
    crypto = InlineKeyboardButton(f"{pay_button_text[lan]['crypto']}-57USDT", callback_data='cryptoz')
    markup.add(stripe, crypto)
    return markup


async def pay_button_monthly(lan):
    prices = [types.LabeledPrice(label=f"{stripe_data[lan]['label']}", amount=5700)]
    invoice = await dp.bot.create_invoice_link(title="Direction Droid course",
                                               description=f"{stripe_data[lan]['description']}",
                                               payload="invoice-stripe-link",
                                               provider_token=STRIPE_TOKEN,
                                               currency="USD",
                                               prices=prices,
                                               is_flexible=False)
    markup = InlineKeyboardMarkup(row_width=1)
    stripe = InlineKeyboardButton(f"{pay_button_text[lan]['stripe']}", url=invoice)
    crypto = InlineKeyboardButton(f"{pay_button_text[lan]['crypto']}", callback_data='crypto')
    markup.add(stripe)
    markup.add(crypto)
    return markup


async def invite_link_add(link, lan):
    markup = InlineKeyboardMarkup(row_width=1)
    link_group = InlineKeyboardButton(f"{join_button[lan]}", url=f"{link}")
    markup.add(link_group)
    return markup


async def detail_button_builder(lan, url):
    markup = InlineKeyboardMarkup(row_width=1)
    link_group = InlineKeyboardButton(f"{detail_button[lan]}", url=f"{url}")
    markup.add(link_group)
    return markup


async def admin_panel():
    markup = ReplyKeyboardMarkup(row_width=3)
    day_1_ar = KeyboardButton("First-Arabic Message")
    day_2_ar = KeyboardButton("Second-Arabic Message")
    day_3_ar = KeyboardButton("Third-Arabic Message")
    markup.add(day_1_ar, day_2_ar, day_3_ar)
    day_4_ar = KeyboardButton("Forth-Arabic Message")
    day_5_ar = KeyboardButton("Fifth-Arabic Message")
    day_6_ar = KeyboardButton("Sixth-Arabic Message")
    markup.add(day_4_ar, day_5_ar, day_6_ar)
    day_7_ar = KeyboardButton("Seventh-Arabic Message")
    markup.add(day_7_ar)

    day_1 = KeyboardButton("First Message")
    day_2 = KeyboardButton("Second Message")
    day_3 = KeyboardButton("Third Message")
    markup.add(day_1, day_2, day_3)
    day_4 = KeyboardButton("Forth Message")
    day_5 = KeyboardButton("Fifth Message")
    day_6 = KeyboardButton("Sixth Message")
    markup.add(day_4, day_5, day_6)
    day_7 = KeyboardButton("Seventh Message")
    day_8 = KeyboardButton("English Exam")
    day_9 = KeyboardButton("Arabic Exam")

    markup.add(day_7)
    markup.add(day_8, day_9)
    all_send = KeyboardButton("📩Send message to all users")
    markup.add(all_send)

    return markup


async def submit_message():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    message = KeyboardButton("Save")
    markup.add(message)

    return markup


async def public_notice():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    message = KeyboardButton("🔙Back")
    markup.add(message)

    return markup


async def exam_builder(user, ques):
    user_data = await db.select_students_one(user)
    question_order = int(user_data['exam_answers'])
    markup = InlineKeyboardMarkup(row_width=1)
    a = 1
    for button_answer in ques[question_order]['answers']:
        if button_answer['correct'] == "False":
            button_variant = InlineKeyboardButton(f"{button_answer['text']}",
                                                  callback_data=f"{button_answer['correct']}{a}")
            markup.add(button_variant)
            a += 1
        else:
            button_variant = InlineKeyboardButton(f"{button_answer['text']}",
                                                  callback_data=f"{button_answer['correct']}")
            markup.add(button_variant)
        await asyncio.sleep(0.01)
    return markup


async def i_paid_button(lan):
    markup = InlineKeyboardMarkup(row_width=1)
    link_group = InlineKeyboardButton(f"{i_paid_button_name[lan]}", callback_data="paid")
    link_back = InlineKeyboardButton(f"{back_paid_button[lan]}", callback_data="back")

    markup.add(link_group)
    markup.add(link_back)
    return markup

# [{'question': '1. What is your name?', 'answers': [{'text': 'A) Correct answer', 'correct': True}, {'text': 'B) Wrong answer', 'correct': False}, {'text': 'C) Wrong answer', 'correct': False}, {'text': 'D) Okay', 'correct': False}]}, {'question': '2. Which country are you a citizen of?', 'answers': [{'text': 'A) Canada', 'correct': False}, {'text': 'B) Uzbekistan', 'correct': True}, {'text': 'C) America', 'correct': False}, {'text': 'D) Africa', 'correct': False}]}]
