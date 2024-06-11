from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:

                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_payment_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS students (
        telegram_id BIGINT NOT NULL UNIQUE,
        chat_id BIGINT NULL,
        week VARCHAR(30) NULL,
        pay_status BIGINT NULL,
        added_time VARCHAR(20) NULL,
        exam_result BIGINT NULL,
        language VARCHAR(10) NULL,
        pay_message_id BIGINT NULL,
        exam_answers BIGINT NULL,
        referral_id BIGINT NULL,
        repaid_referral_id BIGINT NULL,
        wallet_address VARCHAR(255) NULL,
        not_payment_refers BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_student(self, telegram_id, exam_result, exam_answers, not_payment_refers, repaid_referral_id):
        sql = "INSERT INTO students (telegram_id, exam_result, exam_answers, not_payment_refers, repaid_referral_id) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, telegram_id, exam_result, exam_answers, not_payment_refers, repaid_referral_id, fetchrow=True)


    async def select_students_one(self, telegram_id):
        sql = "SELECT * FROM students WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def select_students_all(self):
        sql = "SELECT * FROM students"
        return await self.execute(sql, fetch=True)

    async def select_students_week_name(self, week):
        sql = "SELECT * FROM students WHERE week=$1"
        return await self.execute(sql, week, fetch=True)

    async def update_student_language(self, language, telegram_id):
        sql = "UPDATE students SET language=$1 WHERE telegram_id=$2"
        return await self.execute(sql, language, telegram_id, execute=True)

    async def update_not_payment_refers(self, not_payment_refers, telegram_id):
        sql = "UPDATE students SET not_payment_refers=$1 WHERE telegram_id=$2"
        return await self.execute(sql, not_payment_refers, telegram_id, execute=True)

    async def update_repaid_referral_id(self, repaid_referral_id, telegram_id):
        sql = "UPDATE students SET repaid_referral_id=$1 WHERE telegram_id=$2"
        return await self.execute(sql, repaid_referral_id, telegram_id, execute=True)

    async def update_student_referral_id(self, referral_id, telegram_id):
        sql = "UPDATE students SET referral_id=$1 WHERE telegram_id=$2"
        return await self.execute(sql, referral_id, telegram_id, execute=True)

    async def update_student_week(self, week, telegram_id):
        sql = "UPDATE students SET week=$1 WHERE telegram_id=$2"
        return await self.execute(sql, week, telegram_id, execute=True)

    async def update_student_time(self, added_time, telegram_id):
        sql = "UPDATE students SET added_time=$1 WHERE telegram_id=$2"
        return await self.execute(sql, added_time, telegram_id, execute=True)

    async def update_student_exam_answers(self, exam_answers, telegram_id):
        sql = "UPDATE students SET exam_answers=$1 WHERE telegram_id=$2"
        return await self.execute(sql, exam_answers, telegram_id, execute=True)

    async def update_student_exam_result(self, exam_result, telegram_id):
        sql = "UPDATE students SET exam_result=$1 WHERE telegram_id=$2"
        return await self.execute(sql, exam_result, telegram_id, execute=True)

    async def update_student_chat_id(self, chat_id, telegram_id):
        sql = "UPDATE students SET chat_id=$1 WHERE telegram_id=$2"
        return await self.execute(sql, chat_id, telegram_id, execute=True)

    async def update_student_pay_status(self, pay_status, telegram_id):
        sql = "UPDATE students SET pay_status=$1 WHERE telegram_id=$2"
        return await self.execute(sql, pay_status, telegram_id, execute=True)

    async def update_student_pay_message(self, pay_message_id, telegram_id):
        sql = "UPDATE students SET pay_message_id=$1 WHERE telegram_id=$2"
        return await self.execute(sql, pay_message_id, telegram_id, execute=True)

    async def create_message_list(self):
        sql = """
        CREATE TABLE IF NOT EXISTS cycle (
        day_id BIGINT NULL,
        message_id BIGINT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_cycle_message(self, day_id, message_id):
        sql = "INSERT INTO cycle (day_id, message_id) VALUES($1, $2) returning *"
        return await self.execute(sql, day_id, message_id, fetchrow=True)

    async def select_cycle_message(self, day_id):
        sql = "SELECT * FROM cycle WHERE day_id=$1"
        return await self.execute(sql, day_id, fetch=True)

    async def delete_cycle_message(self, day_id):
        sql = "DELETE FROM cycle WHERE day_id=$1"
        return await self.execute(sql, day_id, fetch=True)

    async def create_message_list_ar(self):
        sql = """
        CREATE TABLE IF NOT EXISTS cycle_ar (
        day_id BIGINT NULL,
        message_id BIGINT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_cycle_message_ar(self, day_id, message_id):
        sql = "INSERT INTO cycle_ar (day_id, message_id) VALUES($1, $2) returning *"
        return await self.execute(sql, day_id, message_id, fetchrow=True)

    async def select_cycle_message_ar(self, day_id):
        sql = "SELECT * FROM cycle_ar WHERE day_id=$1"
        return await self.execute(sql, day_id, fetch=True)

    async def delete_cycle_message_ar(self, day_id):
        sql = "DELETE FROM cycle_ar WHERE day_id=$1"
        return await self.execute(sql, day_id, fetch=True)

    async def create_chat_history(self):
        sql = """
        CREATE TABLE IF NOT EXISTS history (
        chats_id BIGINT NOT NULL UNIQUE,
        start_message_id BIGINT NULL,
        end_message_id BIGINT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_start_and_end(self, start_message_id, end_message_id, chats_id):
        sql = "INSERT INTO history (start_message_id, end_message_id, chats_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, start_message_id, end_message_id, chats_id, fetchrow=True)

    async def update_start_message_id(self, start_message_id, chats_id):
        sql = "UPDATE history SET start_message_id=$1 WHERE chats_id=$2"
        return await self.execute(sql, start_message_id, chats_id, execute=True)

    async def update_end_message_id(self, end_message_id, chats_id):
        sql = "UPDATE history SET end_message_id=$1 WHERE chats_id=$2"
        return await self.execute(sql, end_message_id, chats_id, execute=True)

    async def select_chats_id_one(self, chats_id):
        sql = "SELECT * FROM history WHERE chats_id=$1"
        return await self.execute(sql, chats_id, fetchrow=True)

    async def create_done_message_admin(self):
        sql = """
        CREATE TABLE IF NOT EXISTS done (
        id BIGINT NULL,
        type INTEGER NULL,
        telegram_id BIGINT NULL,
        count BIGINT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())


    async def select_students_admin_done(self):
        sql = "SELECT * FROM done"
        return await self.execute(sql, fetch=True)

    async def delete_cycle_admin_done(self, telegram_id):
        sql = "DELETE FROM done WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetch=True)


    async def create_chat_lifetime(self):
        sql = """
        CREATE TABLE IF NOT EXISTS lifetime (
        chats_id BIGINT NOT NULL UNIQUE,
        added_date VARCHAR(50) NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_lifetime(self, chats_id, added_date):
        sql = "INSERT INTO lifetime (chats_id, added_date) VALUES($1, $2) returning *"
        return await self.execute(sql, chats_id, added_date, fetchrow=True)


    async def select_lifetime(self, added_date):
        sql = "SELECT * FROM lifetime WHERE added_date=$1"
        return await self.execute(sql, added_date, fetch=True)

    async def delete_lifetime(self, chats_id):
        sql = "DELETE FROM lifetime WHERE chats_id=$1"
        return await self.execute(sql, chats_id, fetch=True)

