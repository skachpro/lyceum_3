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

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("математичний", """
Якщо тебе захоплює світ чисел і точні науки, хочеш розв’язувати складні задачі та розвивати логічне мислення, математичний профіль — твій вибір! Це допоможе в кар'єрі програміста, аналітика, інженера чи фінансиста, де логіка — основа успіху.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("інформатичний", """
Якщо ти захоплюєшся комп'ютерами, програмуванням і хочеш створювати програми, розв’язувати технічні задачі та працювати з новітніми технологіями, інформаційний профіль — твій вибір! Це відкриє кар'єрні можливості в IT, програмуванні, аналізі даних та інженерії.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("історичний", """
Якщо ти цікавишся історією, хочеш розуміти, як події формували світ, історичний профіль — твій вибір! Тут ти навчишся критично оцінювати факти, досліджувати джерела та розвиватимеш навички для кар'єри журналіста, юриста чи аналітика.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("правовий", """
Якщо тебе цікавлять права людини, захист правопорядку, розбір в законах і правові питання, правовий профіль — для тебе! Тут ти дізнаєшся основи законодавства, судової системи та отримаєш досвід для кар'єри юриста, адвоката чи правозахисника.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("географічний", """
Якщо ти хочеш досліджувати планету, вивчати природні процеси, екологію та клімат, географічний профіль — для тебе! Навчишся аналізувати явища та ресурси, що відкриє кар'єрні можливості в екології, метеорології, географії та туризмі.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("хіміко-біологічний", """
Якщо ти хочеш вивчати живу природу, розуміти процеси в клітинах і хімічні реакції, хіміко-біологічний профіль — для тебе! Навчишся працювати в лабораторіях, досліджувати організми та взаємодію з середовищем для кар'єри в медицині чи екології.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("українська філологія", """
Якщо ти любиш українську мову та літературу, хочеш вивчати рідне слово, культурну спадщину та виражати думки грамотно, профіль української філології — для тебе! Це допоможе в кар'єрі журналіста, вчителя, редактора чи перекладача.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("іноземна філологія", """
Якщо ти мрієш володіти іноземними мовами, цікавишся культурами інших країн, профіль іноземної філології — твій вибір! Тут ти вивчиш граматику, спілкування та літературу інших народів, що відкриє кар'єрні можливості в перекладі, журналістиці та дипломатії.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("військово-спортивний", """
Якщо ти хочеш поєднати фізичну активність із військовими навичками, цінуєш командний дух, військово-спортивний профіль — для тебе! Розвинути фізичні здібності, освоїти тактику і стратегію для кар'єри в спорті, військовій службі або інших сферах.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("художньо-естетичний", """
Якщо ти любиш мистецтво, хочеш виразити емоції через творчість, художньо-естетичний профіль — для тебе! Опануєш техніки живопису, малювання, дизайну і станеш професіоналом у галузі мистецтва, дизайну чи критики.
"""))


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