import asyncio

from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from handlers.users.button_builder import admin_panel, offer, submit_message
from handlers.users.channel_control import channel_cleaning, remove_user_to_channel_and_send_test
from loader import dp, db
from states import Personaldata


@dp.message_handler(
    text=["Forth-Arabic Message"])
async def daily_message_set_ar(msg: types.Message):
    timer = await msg.answer(text=".", reply_markup=ReplyKeyboardRemove())
    await timer.delete()
    keyword_agree = await offer()
    await msg.answer(text=f"{msg.text} CYCLE!\n\n"
                          f"<i>To change course materials at this stage, submit new all materials to the bot (you can submit them in any format).</i>\n"
                          f"<b>Important!</b><i>: As soon as you click 'I agree' button, the old materials in this step will be deleted.</i>",
                     reply_markup=keyword_agree)
    await Personaldata.Daily4Messages_ar.manual_done.set()


@dp.callback_query_handler(state=Personaldata.Daily4Messages_ar.manual_done, text=['agree', 'back'])
async def manual_done_callback_ar(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        keyword_admin = await admin_panel()
        await call.message.answer("Admin panel", reply_markup=keyword_admin)
        await call.message.delete()
        await state.finish()
    else:
        await call.message.delete()
        button_agree = await submit_message()
        await call.message.answer(text=f"⬇️<b>Submit all course materials.\n"
                                       f"(Click 'Save' button after submitting all materials)</b>",
                                  reply_markup=button_agree)
        await db.delete_cycle_message_ar(day_id=4)
        await Personaldata.Daily4Messages_ar.input_message.set()


@dp.message_handler(state=Personaldata.Daily4Messages_ar.input_message, content_types=types.ContentType.ANY)
async def input_message_handler_ar(messages: types.Message):
    send_message = await dp.bot.copy_message(chat_id=-1001899486063,
                                             from_chat_id=messages.chat.id,
                                             message_id=messages.message_id)
    await db.add_cycle_message_ar(day_id=4, message_id=send_message.message_id)





async def Thursday_Cycle_Channel_ar(weekly_format, name_weekly):
    if name_weekly == "Friday":
        all_content = await db.select_cycle_message_ar(day_id=2)
        for mass in all_content:
            await dp.bot.copy_message(chat_id=-1001830011413,
                                      from_chat_id=-1001899486063,
                                      message_id=int(mass['message_id']))
            await asyncio.sleep(0.1)
    elif name_weekly == "Saturday":
        all_content = await db.select_cycle_message_ar(day_id=3)
        for mass in all_content:
            await dp.bot.copy_message(chat_id=-1001830011413,
                                      from_chat_id=-1001899486063,
                                      message_id=int(mass['message_id']))
            await asyncio.sleep(0.1)
    elif name_weekly == "Sunday":
        all_content = await db.select_cycle_message_ar(day_id=4)
        for mass in all_content:
            await dp.bot.copy_message(chat_id=-1001830011413,
                                      from_chat_id=-1001899486063,
                                      message_id=int(mass['message_id']))
            await asyncio.sleep(0.1)
    elif name_weekly == "Monday":
        all_content = await db.select_cycle_message_ar(day_id=5)
        for mass in all_content:
            await dp.bot.copy_message(chat_id=-1001830011413,
                                      from_chat_id=-1001899486063,
                                      message_id=int(mass['message_id']))
            await asyncio.sleep(0.1)

    elif name_weekly == "Tuesday":
        all_content = await db.select_cycle_message_ar(day_id=6)
        for mass in all_content:
            await dp.bot.copy_message(chat_id=-1001830011413,
                                      from_chat_id=-1001899486063,
                                      message_id=int(mass['message_id']))
            await asyncio.sleep(0.1)
    elif name_weekly == "Wednesday":
        all_content = await db.select_cycle_message_ar(day_id=7)
        for mass in all_content:
            channel_smg = await dp.bot.copy_message(chat_id=-1001830011413,
                                                    from_chat_id=-1001899486063,
                                                    message_id=int(mass['message_id']))
            await db.update_end_message_id(end_message_id=channel_smg.message_id,
                                           chats_id=-1001830011413)
            await asyncio.sleep(0.1)
    elif name_weekly == "Thursday":
        all_content = await db.select_cycle_message_ar(day_id=1)
        await channel_cleaning(-1001830011413)
        await remove_user_to_channel_and_send_test(chat_id=-1001830011413,
                                                   weekly_format=weekly_format,
                                                   name_weekly=name_weekly)
        await asyncio.sleep(0.1)
        a_index = 0
        for mass in all_content:
            channel_smg = await dp.bot.copy_message(chat_id=-1001830011413,
                                                    from_chat_id=-1001899486063,
                                                    message_id=int(mass['message_id']))
            if a_index == 0:
                await db.update_start_message_id(start_message_id=channel_smg.message_id,
                                                 chats_id=-1001830011413)
                a_index = 1
            await asyncio.sleep(0.1)



