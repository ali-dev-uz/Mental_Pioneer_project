import asyncio

from handlers.users.channel_control import channel_cleaning
from loader import db, dp


async def on_startup2():
    await db.create()
    # await db.drop_users()
    await db.create_payment_users()
    await db.create_message_list()
    await db.create_chat_history()
    channel_ids = [-1002053101294, -1002137395521, -1002104317649, -1002009521367, -1002001918933, -1002050117788,
                   -1002025930027, -1001830011413, -1002139375128, -1002046248938, -1002105710154, -1001900177055, -1002047687481, -1002028676437]

    for i in channel_ids:
        # await db.update_start_message_id(start_message_id=1, chats_id=i)
        # await db.update_end_message_id(end_message_id=60, chats_id=i)
        await db.add_start_and_end(start_message_id=1, end_message_id=60, chats_id=i)
    print("bajarildi!")

if __name__ == '__main__':
    asyncio.run(on_startup2())
