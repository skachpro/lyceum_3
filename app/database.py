# import sqlite3 as sq
# import asyncio
#
# with sq.connect("app/lyceum.db") as con:
#     cur = con.cursor()
#
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id TEXT,
#     educ_stage TEXT
#     )
#     """)
#
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS call_schedule(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         photo_id TEXT
#         )
#     """)
#
#
#     cur.execute("""
#             CREATE TABLE IF NOT EXISTS alert_desk(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             photo_id TEXT,
#             text TEXT
#             )
#     """)
#
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS remember_me(
#     user_id TEXT,
#     user_class TEXT
#     )
#     """)
#
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS eat(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         photo_id TEXT
#         )
#     """)
#
#
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS question_answer(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id TEXT,
#             name TEXT,
#             question TEXT,
#             answer TEXT,
#             time_que TEXT
#         )
#     """)
#
#     # cur.execute("""
#     #     INSERT INTO alert_desk (photo_id,text) VALUES(?,?)
#     # """,("AgACAgIAAxkBAAMuZxaN9-2Lpwgcag93VdxwGV5OI8IAAnflMRvoY7FIdOlv1gS78HYBAAMCAAN5AAM2BA","ТЕКСТ ТЕКСТ текст текст текст текст текст текст текст текст"))
#
#     # cur.execute("DELETE FROM remember_me WHERE user_id = ?", ("6156445988",))
#     # cur.execute("DELETE FROM remember_me WHERE user_id = ?", ("1397873368",))
#     #cur.execute("DELETE FROM alert_desk WHERE id = ?", ("44",))
#
#
#
#
#
# #
# # async def alert_desk(photo, text):
# #     cur.execute("""
# #     INSERT INTO alert_desk(photo_id, text) VALUES(?,?)
# #     """, (photo, text))
#
#
# async def remember_me(user_id, user_class):
#     with sq.connect("app/lyceum.db") as con:
#         cur = con.cursor()
#         user = cur.execute("SELECT * FROM remember_me WHERE user_id = ?", (user_id,)).fetchone()
#
#         if not user:
#             cur.execute("""
#                 INSERT INTO remember_me (user_id, user_class) VALUES (?, ?)
#             """, (user_id, user_class))
#             con.commit()
#             return False
#
#         if user[1] is None and user_class is not None:
#             cur.execute("""
#                 UPDATE remember_me SET user_class = ? WHERE user_id = ?
#             """, (user_class, user_id))
#
#     return user_class
#
#
#
# async def que_user(user_id,name,que,time,answer="None"):
#     with sq.connect("app/lyceum.db") as con:
#         cur = con.cursor()
#         cur.execute("""
#             INSERT INTO question_answer(
#                 user_id,
#                 name,
#                 question,
#                 answer,
#                 time_que) VALUES(?,?,?,?,?)
#         """, (user_id,name,que,answer,time))
#     return 0
import os
from aiomysql import create_pool

# Глобальна змінна для зберігання пулу з'єднань
db_pool = None


async def init_db():
    """Ініціалізуємо з'єднання з базою даних."""
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
    """Закриваємо пул з'єднань з базою даних."""
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()
        print("Підключення до бази даних закрито")


async def execute_query(query, params=None):
    """Виконуємо SQL-запит з параметрами."""
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params or ())
            if query.strip().lower().startswith("select"):
                return await cur.fetchall()


async def create_tables():
    """Створюємо всі необхідні таблиці, якщо їх ще немає."""
    await execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            educ_stage VARCHAR(255)
        )
    """)
    await execute_query("""
        CREATE TABLE IF NOT EXISTS call_schedule (
            id INT AUTO_INCREMENT PRIMARY KEY,
            photo_id VARCHAR(255)
        )
    """)
    await execute_query("""
        CREATE TABLE IF NOT EXISTS alert_desk (
            id INT AUTO_INCREMENT PRIMARY KEY,
            photo_id VARCHAR(255),
            text TEXT
        )
    """)
    await execute_query("""
        CREATE TABLE IF NOT EXISTS remember_me (
            user_id VARCHAR(255),
            user_class VARCHAR(255)
        )
    """)
    await execute_query("""
        CREATE TABLE IF NOT EXISTS eat (
            id INT AUTO_INCREMENT PRIMARY KEY,
            photo_id VARCHAR(255)
        )
    """)
    await execute_query("""
        CREATE TABLE IF NOT EXISTS question_answer (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            name VARCHAR(255),
            question TEXT,
            answer TEXT,
            time_que DATETIME
        )
    """)
    print("Таблиці створено або вже існують")
