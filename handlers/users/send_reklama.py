import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from data.config import ADMINS
from handlers.users.button_builder import public_notice, admin_panel
from loader import dp, db
from states import Personaldata


@dp.message_handler(text="📩Send message to all users")
async def add_market(message: types.Message):
    if str(message.chat.id) in ADMINS:
        keyword_send = await public_notice()
        await message.answer("Submit ad text...", reply_markup=keyword_send)
        await Personaldata.Market.media.set()


@dp.message_handler(state=Personaldata.Market.media, content_types=types.ContentType.ANY)
async def send_bax(message: types.Message, state: FSMContext):
    senders = await db.select_students_all()
    await state.finish()
    menu = await admin_panel()
    await message.reply("Messaging has started!", reply_markup=menu)
    for sender in senders:
        try:
            await dp.bot.copy_message(chat_id=int(sender['telegram_id']), from_chat_id=message.chat.id,
                                      message_id=message.message_id)
            await asyncio.sleep(0.8)
        except exceptions.ChatNotFound as e:
            logging.error(f"ChatNotFound error: {e}")
        except Exception as err:
            logging.error(f"All error: {err}")





@dp.message_handler(state=Personaldata.Market.media, text="🔙Back")
async def back_key_market(message: types.Message, state: FSMContext):
    if str(message.chat.id) in ADMINS:
        menu = await admin_panel()
        await message.answer("Main menu", reply_markup=menu)
        await state.finish()
