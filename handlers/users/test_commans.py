from aiogram import types

from loader import dp, db


@dp.message_handler(commands='alitestpay')
async def bot_test_command(message: types.Message):
    try:
        db_request_ref = await db.select_students_one(message.chat.id)
        db_partner = await db.select_students_one(db_request_ref['referral_id'])
        await db.update_student_pay_status(telegram_id=message.chat.id,
                                           pay_status=1)
        calculator = int(db_partner['not_payment_refers']) + 1
        await db.update_not_payment_refers(telegram_id=int(db_request_ref['referral_id']),
                                           not_payment_refers=calculator)
        await message.answer(f"Done!{calculator}\n{db_partner['not_payment_refers']}\n")
    except Exception as er:
        await message.answer(f"{er}")
