import os
import pymysql
from aiomysql import create_pool
from aiomysql.pool import Pool
from datetime import *

db_pool: Pool | None = None


async def init_db():
    global db_pool
    db_pool = await create_pool(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        autocommit=True,
    )
    print("Підключення до бази даних встановлено")


async def close_db():
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()
        print("Підключення до бази даних закрито")


def execute_query_sync(query, params=None):
    connection = pymysql.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
    finally:
        connection.close()


async def execute_query(query, params=None, fetch="fetchall"):
    global db_pool
    if not db_pool:
        raise RuntimeError("Database pool is not initialized")
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params or ())
            if query.strip().lower().startswith("select") and fetch == "fetchall":
                return await cur.fetchall()
            elif query.strip().lower().startswith("select") and fetch == "fetchone":
                return await cur.fetchone()




async def create_tables():
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            educ_stage VARCHAR(255)
        )
    """)
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS call_schedule (
            id INT AUTO_INCREMENT PRIMARY KEY,
            photo_id VARCHAR(255)
        )
    """)
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS alert_desk (
            id INT AUTO_INCREMENT PRIMARY KEY,
            photo_id VARCHAR(255),
            text TEXT
        )
    """)
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS remember_me (
            user_id VARCHAR(255),
            user_class VARCHAR(255)
        )
    """)
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS eat (
            id INT AUTO_INCREMENT PRIMARY KEY,
            photo_id VARCHAR(255)
        )
    """)
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS question_answer (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            name VARCHAR(255),
            question TEXT,
            answer TEXT,
            time_que DATETIME
        )
    """)
    execute_query_sync("""
        CREATE TABLE IF NOT EXISTS profiles(
            id INT AUTO_INCREMENT PRIMARY KEY,
            profile_name VARCHAR(255),
            profile_info TEXT
        )
    """)
    print("Таблиці створено або вже існують")

async def remember_me(user_id, user_class):
    global db_pool
    if not db_pool:
        raise RuntimeError("Database pool is not initalized")
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                INSERT INTO users (user_id,educ_stage) VALUES(%s,%s)
            """, (user_id, user_class))

async def que_user(user_id,name,question):
    global db_pool
    if not db_pool:
        raise RuntimeError("Database pool is not initalized")
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                INSERT INTO question_answer(user_id,name,question,answer,time_que) VALUES(%s,%s,%s,%s,%s)
            """, (user_id,name,question,"None",time))
async def del_user(query,*users):
    global db_pool
    if not db_pool:
        raise RuntimeError("Database pool is not initalized")
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            for user in users:
                try:
                    await cur.execute(query, (user,))
                except Exception as e:
                    print(f"Помилка видалення користовача {user}: {e}")