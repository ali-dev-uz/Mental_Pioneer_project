import asyncio
import logging
import time

from handlers.users.button_builder import invite_link_add, pay_button, detail_button_builder
from handlers.users.words import successful_payment, crypto_pay, next_start, start_text
from loader import db, dp
from handlers.users.pyCoinPayments import CryptoPayments


# Loading configuration file using configparser with API Keys for CoinPayments.net

async def crypto_request_getaway(user_id, chat_id, language_code):
    create_transaction_params = {
        'amount': 36.99,
        'currency1': 'USDT.BEP20',
        'currency2': 'USDT.BEP20',
        'buyer_email': 'buyer@example.com',
        'buyer_name': user_id,
    }
    # Client instance
    client = CryptoPayments()
    db_request1 = await db.select_students_one(chat_id)
    # make the call to createTransaction crypto payments API
    transaction = client.createTransaction(create_transaction_params)

    if transaction['error'] == 'ok':  # check error status 'ok' means the API returned with desired result
        keyword_more = await detail_button_builder(lan=language_code,
                                                   url=transaction['status_url'])
        message_id = await dp.bot.send_photo(chat_id=chat_id,
                                             photo=transaction['qrcode_url'],
                                             caption=f"{crypto_pay[language_code]}<code>{transaction['address']}</code>",
                                             reply_markup=keyword_more)
        try:
            await dp.bot.delete_message(chat_id=chat_id,
                                        message_id=int(db_request1['pay_message_id']))
        except:
            pass
        task = asyncio.create_task(cycle_check_out(txn_id=transaction['txn_id'],
                                                   message_id=message_id.message_id, chat_id=chat_id))
        await asyncio.gather(task, return_exceptions=True)
    else:
        logging.exception(transaction)


async def cycle_check_out(txn_id, message_id, chat_id):
    from handlers.users.pay_button import get_day_of_week, get_today_date

    post_params1 = {
        'txid': txn_id,
    }
    db_request = await db.select_students_one(chat_id)
    start_time = time.time()
    asd = 0
    while True:
        client = CryptoPayments()
        if time.time() - start_time >= 10790:
            try:
                await dp.bot.delete_message(chat_id=chat_id,
                                            message_id=message_id)
            except:
                pass
            keyword_but = await pay_button(db_request['language'])
            await dp.bot.send_message(chat_id=chat_id,
                                      text=start_text[db_request['language']],
                                      reply_markup=keyword_but)
            break
        transactionInfo = client.getTransactionInfo(post_params1)

        if transactionInfo['error'] == 'ok':  # check error status 'ok' means the API returned with desired result
            if transactionInfo['status_text'] == "Complete":
                asd = 1
                channel_number, days_week = await get_day_of_week(db_request['language'])
                data_today_now = await get_today_date()
                await db.update_student_time(added_time=f"{data_today_now}",
                                             telegram_id=chat_id)
                await db.update_student_week(week=days_week, telegram_id=chat_id)
                await db.update_student_chat_id(chat_id=channel_number, telegram_id=chat_id)
                channel_link = await dp.bot.create_chat_invite_link(chat_id=channel_number,
                                                                    member_limit=1,
                                                                    name=f"Link{chat_id}")
                keyword_button = await invite_link_add(channel_link['invite_link'], db_request['language'])
                await asyncio.sleep(0.1)
                await dp.bot.send_photo(chat_id=chat_id,
                                        photo='https://t.me/bsbsi39idjdjxj/620',
                                        caption=f"{successful_payment[db_request['language']]}",
                                        reply_markup=keyword_button)
                await asyncio.sleep(0.1)
                await dp.bot.send_message(chat_id=-1001871966486,
                                          text=f"🟢<b>New Paid Bot 2</b>\n"
                                               f"💵Amount: 36.99USDT"
                                               f"👤Payer: {chat_id}")
                await db.update_student_pay_status(pay_status=1,
                                                   telegram_id=chat_id)
                db_partner = await db.select_students_one(db_request['referral_id'])
                await db.update_not_payment_refers(telegram_id=int(db_request['referral_id']),
                                                   not_payment_refers=int(db_partner['not_payment_refers']) + 1)

                await asyncio.sleep(1)
                try:
                    await dp.bot.delete_message(chat_id=chat_id,
                                                message_id=message_id)
                except:
                    pass
                break
        else:
            logging.exception(transactionInfo)
        await asyncio.sleep(10)
    # if asd == 0:
    #     keyword_but = await pay_button(db_request['language'])
    #     await dp.bot.send_message(chat_id=chat_id,
    #                               text=next_start[db_request['language']],
    #                               reply_markup=keyword_but)
