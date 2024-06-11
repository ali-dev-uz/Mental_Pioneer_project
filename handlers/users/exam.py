import asyncio
import logging
import re

import aiofiles
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from handlers.users.button_builder import public_notice, admin_panel, exam_builder, invite_link_add
from handlers.users.words import exam_done, exam_none
from loader import dp, db
from states import Personaldata

exam_limit = 5


@dp.message_handler(commands='set')
async def delete_movie(message: types.Message):
    try:
        global exam_limit
        msg_number = re.sub(r'/set\s', '', message.text)
        exam_limit = int(msg_number)
        await message.answer(f"Setup done")
    except:
        pass


@dp.callback_query_handler(text="True")
@dp.callback_query_handler(text="False1")
@dp.callback_query_handler(text="False2")
@dp.callback_query_handler(text="False3")
@dp.callback_query_handler(text="False")
async def test_check(call: types.CallbackQuery, state: FSMContext):
    logging.error(call.data)
    count_test = int(await main_test())
    await call.answer(cache_time=1)
    member_data = await db.select_students_one(call.message.chat.id)
    await db.update_student_exam_answers(telegram_id=call.message.chat.id,
                                         exam_answers=int(member_data['exam_answers']) + 1)
    member_data = await db.select_students_one(call.message.chat.id)
    if member_data['exam_answers'] >= count_test:
        await state.finish()
        if member_data['exam_result'] >= exam_limit:
            chat_select = {
                "ar": -1002076053983,
                "en": -1002037504841
            }
            channel_link = await dp.bot.create_chat_invite_link(chat_id=chat_select[member_data['language']],
                                                                member_limit=1,
                                                                name=f"Link{call.message.chat.id}")
            keyword_button = await invite_link_add(channel_link['invite_link'], member_data['language'])
            await asyncio.sleep(0.02)
            await call.message.answer(f"{exam_done[member_data['language']]}",
                                      reply_markup=keyword_button)
            await dp.bot.delete_message(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id)
        else:
            await call.message.answer(f"{exam_none[member_data['language']]}")

    else:
        filename = '/home/ubuntu/Direction_Droid/test.txt'  # Update with the correct file path
        if member_data['language'] == "ar":
            filename = '/home/ubuntu/Direction_Droid/test2.txt'
        questions = await read_quiz_file(filename)
        keyword_inline = await exam_builder(user=call.message.chat.id,
                                            ques=questions)
        question_order = int(member_data['exam_answers'])
        question_text = questions[question_order]['question']
        try:

            await dp.bot.edit_message_text(chat_id=int(call.message.chat.id),
                                           text=f"<b>{question_text}</b>",
                                           message_id=call.message.message_id,
                                           inline_message_id=call.inline_message_id)
            await asyncio.sleep(0.02)
            await dp.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                   message_id=call.message.message_id,
                                                   inline_message_id=call.inline_message_id,
                                                   reply_markup=keyword_inline)
        except Exception as err:
            logging.exception(err)
        if call.data == "True":
            await db.update_student_exam_result(telegram_id=call.message.chat.id,
                                                exam_result=int(member_data['exam_result']) + 1)
        else:
            pass


@dp.message_handler(text="English Exam")
async def add_ExamTest1(message: types.Message):
    if str(message.chat.id) in ADMINS:
        keyword_send = await public_notice()
        await message.answer("Send the questions file", reply_markup=keyword_send)
        await Personaldata.ExamTest.tests.set()


@dp.message_handler(state=Personaldata.ExamTest.tests, content_types=types.ContentType.DOCUMENT)
async def send_bax1(message: types.Message, state: FSMContext):
    menu = await admin_panel()
    # Download the file
    file_id = message.document.file_id
    file_path = "/home/ubuntu/Direction_Droid/test.txt"
    file_info = await dp.bot.get_file(file_id)
    file = await dp.bot.download_file(file_info.file_path)
    # Check if the file is a text file (.txt)
    if file_info.file_path.endswith('.txt'):
        # Save the file to the specified address
        with open(file_path, 'wb') as new_file:
            new_file.write(file.read())
        len_ques = await main_test()
        await message.reply(f"Questions file saved successfully.\n"
                            f"Questions found: {len_ques}", reply_markup=menu)
        await state.finish()
    else:
        await message.reply("Please send only .txt format file")


@dp.message_handler(state=Personaldata.ExamTest.tests, text="🔙Back")
async def back_key_ExamTest(message: types.Message, state: FSMContext):
    if str(message.chat.id) in ADMINS:
        menu = await admin_panel()
        await message.answer("Main menu", reply_markup=menu)
        await state.finish()


async def read_quiz_file(filename):
    async with aiofiles.open(filename, mode='r') as file:
        questions = []
        current_question = None
        async for line in file:
            line = line.strip()
            if line.startswith('?'):
                if current_question:
                    questions.append(current_question)
                current_question = {'question': line[2:].strip(), 'answers': []}
            elif line.startswith(('+', '-')):
                is_correct = line.startswith('+')
                answer_text = line[2:].strip()
                current_question['answers'].append({'text': answer_text, 'correct': is_correct})
        if current_question:
            questions.append(current_question)
    return questions


async def main_test():
    try:
        filename = '/home/ubuntu/Direction_Droid/test.txt'  # Update with the correct file path
        questions = await read_quiz_file(filename)
        # print(questions)
        # for i, question in enumerate(questions, 1):
        #     print(f"{question['question']}")
        #     for j, answer in enumerate(question['answers'], 1):
        #         print(f"{'+' if answer['correct'] else '-'} {answer['text']}")
        return len(questions)
    except:
        return 0
