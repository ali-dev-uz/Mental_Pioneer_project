from aiogram import types

from data.config import ADMINS
from handlers.users.button_builder import details_button_user, details_button_admin
from handlers.users.words import referral_system_start, pay_refer
from loader import dp, db


@dp.message_handler(commands='referrals')
async def bot_referral(message: types.Message):
    member_ref = message.chat.id
    db_request_ref = await db.select_students_one(member_ref)
    if str(member_ref) not in ADMINS:
        keyboard_ref = await details_button_user(db_request_ref['language'])
        await message.answer(text=f"{referral_system_start[db_request_ref['language']]}\n"
                                  f"{pay_refer[db_request_ref['language']]}\n"
                                  f"https://t.me/ConsuItantbot?start={message.chat.id}",
                             reply_markup=keyboard_ref)
    else:
        keyboard_ref = await details_button_admin()
        await message.answer(text=f"<b>Hello admin.</b>\nYou can check the referrals through the Panel below",
                             reply_markup=keyboard_ref)


