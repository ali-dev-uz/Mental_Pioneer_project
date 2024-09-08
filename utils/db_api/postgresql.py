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
        language VARCHAR(10) NULL,
        pay_message_id BIGINT NULL
        );
        """
        await self.execute(sql, execute=True)


    async def add_student(self, telegram_id):
        sql = "INSERT INTO students (telegram_id) VALUES($1) returning *"
        return await self.execute(sql, telegram_id, fetchrow=True)


    async def select_students_one(self, telegram_id):
        sql = "SELECT * FROM students WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def select_students_all(self):
        sql = "SELECT * FROM students"
        return await self.execute(sql, fetch=True)


    async def update_student_language(self, language, telegram_id):
        sql = "UPDATE students SET language=$1 WHERE telegram_id=$2"
        return await self.execute(sql, language, telegram_id, execute=True)


    async def update_student_pay_message(self, pay_message_id, telegram_id):
        sql = "UPDATE students SET pay_message_id=$1 WHERE telegram_id=$2"
        return await self.execute(sql, pay_message_id, telegram_id, execute=True)






    async def create_training_courses(self):
        sql = """
        CREATE TABLE IF NOT EXISTS training_courses (
        id_course SERIAL PRIMARY KEY,
        course_name VARCHAR(50) NULL,
        course_price BIGINT NULL,
        course_id VARCHAR(50) NULL,
        course_channel BIGINT NULL
        );
        """
        await self.execute(sql, execute=True)


    async def add_training_course(self, course_name, course_price, course_channel, course_id):
        sql = "INSERT INTO training_courses (course_name, course_price, course_channel, course_id) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, course_name, course_price, course_channel, course_id, fetchrow=True)


    async def select_training_course_one(self, id_course):
        sql = "SELECT * FROM training_courses WHERE id_course=$1"
        return await self.execute(sql, id_course, fetchrow=True)

    async def select_training_courses_all(self):
        sql = "SELECT * FROM training_courses"
        return await self.execute(sql, fetch=True)

    async def delete_training_course(self, course_channel):
        sql = "DELETE FROM training_courses WHERE course_channel=$1"
        return await self.execute(sql, course_channel, fetchrow=True)


    async def create_training_courses_arabic(self):
        sql = """
        CREATE TABLE IF NOT EXISTS training_courses_arabic (
        id_course SERIAL PRIMARY KEY,
        course_name VARCHAR(50) NULL,
        course_price BIGINT NULL,
        course_id VARCHAR(50) NULL,
        course_channel BIGINT NULL
        );
        """
        await self.execute(sql, execute=True)


    async def add_training_course_arabic(self, course_name, course_price, course_channel, course_id):
        sql = "INSERT INTO training_courses_arabic (course_name, course_price, course_channel, course_id) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, course_name, course_price, course_channel, course_id, fetchrow=True)


    async def select_training_course_one_arabic(self, id_course):
        sql = "SELECT * FROM training_courses_arabic WHERE id_course=$1"
        return await self.execute(sql, id_course, fetchrow=True)

    async def select_training_courses_all_arabic(self):
        sql = "SELECT * FROM training_courses_arabic"
        return await self.execute(sql, fetch=True)

    async def delete_training_course_arabic(self):
        sql = "DELETE FROM training_courses_arabic"
        return await self.execute(sql, fetchrow=True)


    async def create_chat_lifetime(self):
        sql = """
        CREATE TABLE IF NOT EXISTS lifetime (
        user_id BIGINT NOT NULL,
        added_date VARCHAR(50) NULL,
        course_id VARCHAR(50) NULL,
        channel_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)


    async def add_lifetime(self, user_id, added_date, channel_id, course_id):
        sql = "INSERT INTO lifetime (user_id, added_date, channel_id, course_id) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, user_id, added_date, channel_id, course_id, fetchrow=True)


    async def select_lifetime(self, added_date):
        sql = "SELECT * FROM lifetime WHERE added_date=$1"
        return await self.execute(sql, added_date, fetch=True)

    async def select_lifetime_one(self, user_id):
        sql = "SELECT * FROM lifetime WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def delete_lifetime(self, user_id):
        sql = "DELETE FROM lifetime WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

