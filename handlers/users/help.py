from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from handlers.users.button_builder import languages, admin_panel
from handlers.users.words import select_language, support_text
from loader import dp, db


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    member_set = message.chat.id
    db_request = await db.select_students_one(member_set)
    try:
        await message.delete()
    except:
        pass

    await message.answer(support_text[f'{db_request["language"]}'])


@dp.message_handler(commands='languages')
async def setting_languages(message: types.Message):
    member_set = message.chat.id
    db_request = await db.select_students_one(member_set)
    try:
        await message.delete()
    except:
        pass
    keyboard = await languages()
    if str(member_set) not in ADMINS and db_request is not None:
        await message.answer(text=select_language[f"{db_request['language']}"],
                             reply_markup=keyboard)
    elif str(member_set) not in ADMINS and db_request is None:
        await message.answer(text=select_language['en'],
                             reply_markup=keyboard)
    elif str(member_set) in ADMINS:
        keyword_admin = await admin_panel()
        await message.answer("Sorry, But the ADMIN panel provides services only in English.",
                             reply_markup=keyword_admin)
