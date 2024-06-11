from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.button_builder import admin_panel
from loader import dp
from states import Personaldata


@dp.message_handler(state=Personaldata.Daily7Messages_ar.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily6Messages_ar.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily5Messages_ar.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily4Messages_ar.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily3Messages_ar.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily2Messages_ar.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily1Messages_ar.input_message, text='Save')
async def manual_done_callback2(msg: types.Message, state: FSMContext):
    menu = await admin_panel()
    await msg.answer(text="<b>All materials saved</b>", reply_markup=menu)
    await state.finish()


@dp.message_handler(state=Personaldata.Daily7Messages.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily6Messages.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily5Messages.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily4Messages.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily3Messages.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily2Messages.input_message, text='Save')
@dp.message_handler(state=Personaldata.Daily1Messages.input_message, text='Save')
async def manual_done_callback(msg: types.Message, state: FSMContext):
    menu = await admin_panel()
    await msg.answer(text="<b>All materials saved</b>", reply_markup=menu)
    await state.finish()
