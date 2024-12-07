import os
import pymysql
from aiomysql import create_pool
from aiomysql.pool import Pool

# Глобальна змінна для зберігання пулу з'єднань
db_pool: Pool | None = None  # Указан тип Pool для db_pool


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
    if db_pool:  # Проверяем, что пул инициализирован
        db_pool.close()
        await db_pool.wait_closed()
        print("Підключення до бази даних закрито")


def execute_query_sync(query, params=None):
    """Синхронне виконання SQL-запиту."""
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


async def execute_query(query, params=None):
    """Асинхронне виконання SQL-запиту."""
    global db_pool
    if not db_pool:
        raise RuntimeError("Database pool is not initialized")
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params or ())
            if query.strip().lower().startswith("select"):
                return await cur.fetchall()


async def create_tables():
    """Створюємо всі необхідні таблиці, якщо їх ще немає."""
    # Використовуємо синхронний метод для ініціалізації структури таблиць
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
    print("Таблиці створено або вже існують")