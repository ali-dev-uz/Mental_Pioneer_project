import aiofiles
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from handlers.users.button_builder import public_notice, admin_panel
from loader import dp
from states import Personaldata


@dp.message_handler(text="Arabic Exam")
async def add_ExamTest212(message: types.Message):
    if str(message.chat.id) in ADMINS:
        keyword_send = await public_notice()
        await message.answer("Send the questions file", reply_markup=keyword_send)
        await Personaldata.ExamTest2.tests2.set()


@dp.message_handler(state=Personaldata.ExamTest2.tests2, content_types=types.ContentType.DOCUMENT)
async def send_bax12(message: types.Message, state: FSMContext):
    menu = await admin_panel()
    # Download the file
    file_id = message.document.file_id
    file_path = "/home/ubuntu/Direction_Droid/test2.txt"
    file_info = await dp.bot.get_file(file_id)
    file = await dp.bot.download_file(file_info.file_path)
    # Check if the file is a text file (.txt)
    if file_info.file_path.endswith('.txt'):
        # Save the file to the specified address
        with open(file_path, 'wb') as new_file:
            new_file.write(file.read())
        len_ques = await main_test2()
        await message.reply(f"Questions file saved successfully.\n"
                            f"Questions found: {len_ques}", reply_markup=menu)
        await state.finish()
    else:
        await message.reply("Please send only .txt format file")


@dp.message_handler(state=Personaldata.ExamTest2.tests2, text="🔙Back")
async def back_key_ExamTest22(message: types.Message, state: FSMContext):
    if str(message.chat.id) in ADMINS:
        menu = await admin_panel()
        await message.answer("Main menu", reply_markup=menu)
        await state.finish()


async def read_quiz_file2(filename):
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


async def main_test2():
    try:
        filename = '/home/ubuntu/Direction_Droid/test2.txt'  # Update with the correct file path
        questions = await read_quiz_file2(filename)
        # print(questions)
        # for i, question in enumerate(questions, 1):
        #     print(f"{question['question']}")
        #     for j, answer in enumerate(question['answers'], 1):
        #         print(f"{'+' if answer['correct'] else '-'} {answer['text']}")
        return len(questions)
    except:
        return 0
