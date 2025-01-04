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
Якщо тебе захоплює світ чисел, цікавлять точні науки, хочеш навчитися розв’язувати складні задачі, розвивати логічне мислення та знаходити рішення там, де інші бачать лише питання, тоді математичний профіль — твій ідеальний вибір! Ці знання допоможуть тобі в кар'єрі програміста, аналітика, інженера, фінансиста та багатьох інших професій, де логіка і математичне мислення — основа успіху.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("інформатичний", """
Якщо тебе захоплює світ чисел, цікавлять точні науки, хочеш навчитися розв’язувати складні задачі, розвивати логічне мислення та знаходити рішення там, де інші бачать лише питання, тоді математичний профіль — твій ідеальний вибір! Ці знання допоможуть тобі в кар'єрі програміста, аналітика, інженера, фінансиста та багатьох інших професій, де логіка і математичне мислення — основа успіху.
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("історичний", """
Якщо тобі цікаво досліджувати минуле, розуміти, як події формували світ, в якому ми живемо, аналізувати зв’язки між історією і сучасністю, тоді історичний профіль — твій вибір! Ти навчишся критично оцінювати факти, досліджувати історичні джерела, аргументувати свою думку, а також розвиватимеш навички, що знадобляться в кар'єрі журналіста, юриста, аналітика чи культуролога. Вибирай історичний профіль та розкрий таємниці людства разом з нами!
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("правовий", """
Якщо тебе цікавлять права людини, справедливість і захист правопорядку, якщо ти хочеш розбиратися в законах, вміти аргументувати свою позицію та вирішувати правові питання, тоді правовий профіль — саме для тебе! Тут ти здобудеш навички аналізу правових ситуацій, навчишся основам законодавства, дізнаєшся про роботу судової системи та отримаєш досвід, що стане корисним у кар'єрі юриста, адвоката, поліцейського чи правозахисника. Обирай правовий профіль та ставай захисником прав і справедливості!
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("географічний", """
Якщо тебе захоплює дослідження нашої планети, вивчення природних процесів і культур, ти хочеш розуміти, як взаємодіють природа і суспільство, і цікавишся питаннями екології та клімату — тоді географічний профіль саме для тебе! Тут ти навчишся орієнтуватися у складному світі природних ресурсів, картографії, аналізу природних явищ і глобальних змін. Ці знання відкриють тобі шлях до кар’єри еколога, метеоролога, географа чи спеціаліста з туризму. Обирай географічний профіль і досліджуй світ разом із нами!
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("хіміко-біологічний", """
Якщо тобі цікаво досліджувати живу природу, розуміти, з чого складається все навколо, вивчати процеси в клітинах і хімічні реакції, що формують життя, тоді хіміко-біологічний профіль саме для тебе! Ти навчишся працювати з лабораторними приладами, проводити експерименти, досліджувати організми та їх взаємодію із середовищем. Ці знання стануть основою для кар'єри в медицині, фармацевтиці, екології чи наукових дослідженнях. Обирай хіміко-біологічний профіль і розкривай таємниці живої природи!
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("українська філологія", """
Якщо ти любиш українську мову та літературу, цікавишся історією та культурою нашого народу, хочеш вивчати багатство рідного слова і виражати свої думки красиво та грамотно, тоді профіль української філології — саме для тебе! Тут ти опануєш навички аналізу текстів, вдосконалиш мовлення, відкриєш для себе творчість українських письменників і зможеш створювати власні літературні твори. Ці знання стануть тобі у пригоді в кар'єрі журналіста, вчителя, редактора чи перекладача. Обирай філологічний профіль і вдосконалюй свою українську!
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("іноземна філологія", """
Якщо ти мрієш вільно володіти іноземними мовами, цікавишся культурами інших країн і хочеш вивчати світ через слово, тоді профіль іноземної філології — твій ідеальний вибір! Тут ти зможеш опанувати граматику, розвинути навички спілкування, зануритися в літературу і традиції інших народів, а також навчитися тонкощам перекладу. Ці знання відкриють тобі шлях до кар'єри перекладача, журналіста, дипломата або викладача. Обирай профіль іноземної філології та відкривай для себе безмежний світ мов і культур!
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("військово-спортивний", """
Якщо ти прагнеш поєднати фізичну активність із військовими навичками, цінуєш командний дух і хочеш навчитися витримки та лідерства, тоді військово-спортивний профіль — це те, що тобі потрібно! Тут ти зможеш розвинути свої фізичні здібності, освоїти основи тактики і стратегії, навчитися працювати в команді та брати участь у змаганнях. Ці навички знадобляться не тільки в спорті, але й у військовій службі та інших сферах, де потрібні витривалість і рішучість. Обирай військово-спортивний профіль і готуйся до викликів з впевненістю та енергією!
"""))

execute_query("""
    INSERT INTO profiles (profile_name, profile_info)
    VALUES (%s, %s)
""", ("художньо-естетичний", """
Якщо ти любиш мистецтво, цінуєш красу навколишнього світу і прагнеш висловити свої емоції через творчість, тоді художньо-естетичний профіль — це твій шлях! Тут ти зможеш освоїти різні техніки живопису, малювання, скульптури та дизайну, а також навчишся аналізувати мистецькі твори та розуміти їхню глибину. Ці навички відкриють перед тобою двері в світ професій художника, дизайнера, ілюстратора чи арт-критика. Обирай художньо-естетичний профіль і дай волю своїй творчості!
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