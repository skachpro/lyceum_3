from datetime import datetime, timedelta, date, time
from aiogram.filters.logic import or_f

import sqlite3 as sq
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InputFile

import app.keyboards as kb

from app import database as db
import os
from dotenv import load_dotenv
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.pygithub import upload_to_github
import aiohttp

load_dotenv()
bot = Bot(token=os.getenv('BOT_API'))

router = Router()

class RememberMe(StatesGroup):
    user_id = State()
    user_class = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await db.del_user("DELETE FROM remember_me WHERE user_id = %s", 6156445988, 1397873368)
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    user = await db.execute_query("SELECT * FROM remember_me WHERE user_id = %s", user_id,fetch="fetchone")

    print(user)
    answer = f'<b>Вітаємо </b>{user_name}!\nTelegram-bot Ліцею №3 імені Артема Мазура до ваших послуг!\nОберіть наступну дію ⬇️'

    try:
        if user[1] == "7-9 клас":
            await message.answer(answer, parse_mode='HTML', reply_markup=kb.kbd_for_young_stud)
        elif user[1] == '10-11 клас':
            await message.answer(answer, parse_mode='HTML', reply_markup=kb.for_students)
    except:
        await message.answer(answer, parse_mode='HTML', reply_markup=kb.start)

class Answers(StatesGroup):
    step = State()

@router.callback_query(F.data == 'check_for_answer')
async def check_for_answers(callback_query: CallbackQuery, state: FSMContext):

    questions = await db.execute_query("""SELECT id, name, question, answer 
        FROM question_answer 
        WHERE answer != %s 
        LIMIT 5
    """,("None",))
    if not questions:
        await callback_query.message.answer("Немає доступних відповідей на запитання.", parse_mode="html")
        return

    await state.set_state(Answers.step)
    await state.update_data(questions=questions, step=0)

    current_question = questions[0]
    response = (
        f"Запитання:\n<pre><code>{current_question[1]}:\n{current_question[2]}</code></pre>\n"
        f"Відповідь:\n<pre><code>{current_question[3]}</code></pre>"
    )
    await callback_query.message.edit_text(response, parse_mode="html", reply_markup=kb.answer_nav)


@router.callback_query(F.data == "next")
async def next_answer(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    questions = data.get("questions", [])
    step = data.get("step", 0) + 1

    if step < len(questions):

        await state.update_data(step=step)
        current_question = questions[step]


        response = (
            f"Запитання:\n<pre><code>{current_question[1]}:\n{current_question[2]}</code></pre>\n"
            f"Відповідь:\n<pre><code>{current_question[3]}</code></pre>"
        )
        await callback_query.message.edit_text(response, parse_mode="html", reply_markup=kb.answer_nav)
    else:
        await callback_query.answer("Це був останній запис.")


@router.callback_query(F.data == "prev")
async def prev_answer(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    questions = data.get("questions", [])
    step = data.get("step", 0) - 1

    if step >= 0:

        await state.update_data(step=step)
        current_question = questions[step]


        response = (
            f"Запитання:\n<pre><code>{current_question[1]}:\n{current_question[2]}</code></pre>\n"
            f"Відповідь:\n<pre><code>{current_question[3]}</code></pre>"
        )
        await callback_query.message.edit_text(response, parse_mode="html", reply_markup=kb.answer_nav)
    else:
        await callback_query.answer("Це був перший запис.")




@router.message(F.text == 'Розклад 📋')
async def lesson_plan(message: Message):
    await message.answer("Ви можете <b>переглянути Розклад дзвінків,</b> або <b>Розклад уроків за посиланням.</b>", parse_mode="html",reply_markup=kb.rozklad)

@router.callback_query(F.data == 'alert_plan')
async def alert_plan(callback_query: CallbackQuery):

    data = await db.execute_query("SELECT photo_id FROM call_schedule ORDER BY id DESC LIMIT 1",fetch="fetchone")
    if data:
        photo_id = data[0]
        photo_url = f"https://raw.githubusercontent.com/skachpro/photos_lyceum_bot/refs/heads/main/photos/AgACAgIAAxkBAAIFjmdJ_SENu66ydLFppi5xgpJVTZpxAAIS4jEb1npRSizdC1npjreEAQADAgADeQADNgQ.jpg"
        await callback_query.message.delete()
        await callback_query.message.answer_photo(photo=photo_url, caption="Розклад дзвінків")
    else:
        await callback_query.message.answer("Фото не знайдено в базі")
#Не для Учнів
@router.message(F.text == 'Я не навчаюсь в ліцеї ❌👨‍🎓')
async def not_for_students(message: Message):
    await message.answer(f'Оберіть наступну дію!', reply_markup=kb.not_for_students)


@router.message(F.text == 'Контакти ☎️')
async def contacts(message: Message):
    await message.answer(
        (
            "<b>З нами можна зв'язатись:</b>\n\n"
            "<b>Email:</b> <a href='mailto:tbl@ua.fm'>tbl@ua.fm</a>\n"
            "<b>Номери телефону:</b>\n"
            "  • <a href='tel:+0382674323'>+0382674323</a>\n"
            "  • <a href='tel:+38067600920'>+38067600920</a>\n"
            "  • <a href='tel:+380975581966'>+380975581966</a>\n"
            "  • <a href='tel:+0967235770'>+0967235770</a>\n"
            "<b>Адреса:</b> <i>вул. Тернопільська 14/1</i>"
        ),
        parse_mode="html"
    )

#Для Учнів
@router.message(F.text == 'Я навчаюсь в ліцеї 👨‍🎓')
async def for_students(message: Message, state: FSMContext):
    await message.answer(f'Оберіть в якому ви класі ⬇️', reply_markup=kb.select_num_of_class)
    await state.set_state(RememberMe.user_id)
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(RememberMe.user_class)

@router.message(RememberMe.user_class)
async def class_choosed(message: Message, state: FSMContext):
    # Получаем данные от пользователя
    await state.update_data(user_class=message.text)
    data = await state.get_data()
    user_id = data["user_id"]
    user_class = data["user_class"]

    answer = f"Готово\nВаш Id: {user_id}\nВаш клас: {user_class}"

    await db.remember_me(user_id, user_class)
    try:
        if user_class == "7-9 клас":
            await message.answer(answer, parse_mode='HTML', reply_markup=kb.kbd_for_young_stud)
        elif user_class == '10-11 клас':
            await message.answer(answer, parse_mode='HTML', reply_markup=kb.for_students)
    except:
        await message.answer(answer, parse_mode='HTML', reply_markup=kb.start)
    await state.clear()

@router.message(F.text=='Обрати профіль у 10 класі 🔍')
async def select_profile(message: Message):
    await message.reply(f'Обрати профіль можна в іншому Телеграм-боті. Для переходу натисніть на кнопку під повідомленням.',reply_markup=kb.profile)

@router.message(F.text == 'Запитання/Відповідь 💬')
async def qa(message:Message):
    await message.answer(f"<b>Напишіть своє запитання/пропозицію.</b>\nАбо перегляньте запитання на які вже надали відповідь.",parse_mode="html",reply_markup=kb.qa)


@router.message(F.text == 'Про ліцей 🏫')
async def about_lyceum(message: Message):
    await message.answer_photo(photo="https://lh3.googleusercontent.com/p/AF1QipNxPlNdabKtiwUqr-0qGomj8XwD2bn0FURD-7Z7=s680-w680-h510",caption=f"""<b>Комунальний заклад загальної середньої освіти \n“Ліцей №3 імені Артема МазураХмельницької міської ради”</b>\n\nВ Ліцеї №3 імені Артема Мазура працюють відомі вчителі, автори підручників та посібників,\nнаставники переможців олімпіад,\nконкурсу-захисту МАН і спортивних змагань...<a href='http://tbl.km.ua/'>далі</a>\n\n""", parse_mode="html")

class QA(StatesGroup):
    name = State()
    que = State()

@router.callback_query(F.data == 'ask')
async def qa_run(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(QA.name)
    await callback_query.message.edit_text(
        "Ви зможете задати запитання після того як введете своє ім'я та прізвище:"
    )

@router.message(QA.name)
async def qa_que(message: Message, state: FSMContext):

    await state.update_data(name=message.text)
    await state.set_state(QA.que)
    await message.answer(
        "Дякуємо! Тепер напишіть своє запитання і ми обов'язково передамо його адміністрації школи:"
    )

@router.message(QA.que)
async def qa_res(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    name = data.get("name")
    question = message.text

    await db.que_user(user_id,name,question)

    await message.answer(
        f"Дякуємо, <b>{name}</b>! Ваше запитання отримано:\n\n{question}"
    ,parse_mode="HTML")
    await state.clear()

@router.message(or_f(Command("admin"),(F.text == "Я з адміністрації ліцею 🏫🧑‍💼")))
async def admin(message: Message):
    if message.from_user.id != 6156445988 and message.from_user.id != 1397873368 and message.from_user.id != 5832908779:
        return
    else:
        await message.answer(f"Адмінпанель до ваших послуг",reply_markup=kb.admin)


class Alert(StatesGroup):
    photo_id = State()
    text = State()

@router.message(F.text == 'Дошка оголошень')
async def al_desk_admin(message: Message,state:FSMContext):
    await state.set_state(Alert.photo_id)
    await message.answer(f'Пришліть фотографію.', reply_markup=kb.skip_photo)

@router.callback_query(F.data == 'skip_photo')
async def skip_photo(callback_query: CallbackQuery, state: FSMContext):

    await db.execute_query("""
        INSERT INTO alert_desk (photo_id) VALUES (%s)
    """, ("None",))
    await callback_query.message.edit_text("Введіть текст для дошки оголошень.")
    await state.set_state(Alert.text)


@router.message(Alert.photo_id, F.photo)
async def get_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await db.execute_query("""
        INSERT INTO alert_desk (photo_id) VALUES (%s)
    """,(photo_id,))
    await message.answer("Фото отримано!\nНапишіть текст оголошення")
    await state.set_state(Alert.text)

@router.message(Alert.text)
async def get_text_for_alert_desk(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    data = await state.get_data()
    photo_id = data.get("photo_id", "null")
    print("Фотка:",photo_id)

    await db.execute_query("""
        INSERT INTO alert_desk (photo_id, text) VALUES (%s,%s)
    """, (photo_id,text))

    file_info = await bot.get_file(photo_id)
    file_path = file_info.file_path

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.telegram.org/file/bot{os.getenv('BOT_API')}/{file_path}") as resp:
            if resp.status == 200:
                file_content = await resp.read()
                file_name = f"{photo_id}.jpg"

                result = upload_to_github(file_name, file_content)
                await message.answer(result)
                photo_url = f"https://raw.githubusercontent.com/skachpro/photos_lyceum_bot/refs/heads/main/photos/{photo_id}.jpg"
            else:
                await message.answer("Не вдалося завантажити фото.")

    await message.answer_photo(photo=photo_url, caption=text)

class Call_Schedule(StatesGroup):
    photo = State()
@router.message(F.text == 'Розкалд дзвінків')
async def call_schedule_admin(message: Message, state: FSMContext):
    await message.answer("Пришліть фото Розкладу дзвінків")
    await state.set_state(Call_Schedule.photo)

@router.message(Call_Schedule.photo)
async def call_schedule_set_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await db.execute_query("""INSERT INTO call_schedule(photo_id) VALUES (%s)""", (photo_id,))
    await state.clear()

    file_info = await bot.get_file(photo_id)
    file_path = file_info.file_path

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.telegram.org/file/bot{os.getenv('BOT_API')}/{file_path}") as resp:
            if resp.status == 200:
                file_content = await resp.read()
                file_name = f"{photo_id}.jpg"
                photo_url = f"https://raw.githubusercontent.com/skachpro/photos_lyceum_bot/refs/heads/main/photos/{photo_id}.jpg"
                result = upload_to_github(file_name, file_content)
                await message.answer_photo(photo=photo_url)
            else:
                await message.answer("Не вдалось скачати фото.")
    await message.answer("Фото збережено в базі")

@router.message(F.text == "Меню їдальні 🍽️")
async def stolovka(message: Message):
    photo_id = await db.execute_query("""SELECT photo_id FROM eat ORDER BY id DESC LIMIT 1""")


    print(photo_id)
    if photo_id:
        photo_url = f"https://raw.githubusercontent.com/skachpro/photos_lyceum_bot/refs/heads/main/photos/{photo_id[0][0]}.jpg"
        await message.answer_photo(photo=photo_url, caption='Меню ідальні')
    else:
        await message.answer("Меню не додано")

class Stolova(StatesGroup):
    photo = State()

@router.message(F.text == 'Меню їдальні')
async def stolovka_admin(message: Message, state: FSMContext):
    await state.set_state(Stolova.photo)
    await message.answer("Додайте фото Меню")

@router.message(Stolova.photo)
async def stolova_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    await db.execute_query("""
        INSERT INTO eat(photo_id) VALUES(%s)
    """, (photo_id,))
    await state.clear()
    file_info = await bot.get_file(photo_id)
    file_path = file_info.file_path

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.telegram.org/file/bot{os.getenv('BOT_API')}/{file_path}") as resp:
            if resp.status == 200:
                file_content = await resp.read()
                file_name = f"{photo_id}.jpg"
                photo_url = f"https://raw.githubusercontent.com/skachpro/photos_lyceum_bot/refs/heads/main/photos/{photo_id}.jpg"
                result = upload_to_github(file_name, file_content)
                if result:
                    await message.answer_photo(photo=photo_url)
            else:
                await message.answer("Не вдалося скачати фото.")
    await message.answer("Фото збережено в базі")
    await message.answer_photo(photo=photo_url)


@router.message(F.text=='Дошка оголошень 📌')
async def alert_desk(message: Message):
    al_desk = await db.execute_query("SELECT photo_id,text FROM alert_desk ORDER BY id DESC LIMIT 1")
    #print(al_desk)
    if al_desk:
        photo_id = al_desk[0][0]
        text = al_desk[0][1]
        photo_url = f"https://raw.githubusercontent.com/skachpro/photos_lyceum_bot/refs/heads/main/photos/{photo_id}.jpg"
        await message.answer_photo(photo=photo_url, caption=text)
    else:
        await message.answer("Наразі оголошень немає")


class QAstep(StatesGroup):
    step = State()
    questions = State()

@router.message(F.text == "Відповісти на питання")
async def qa_answ(message: Message, state: FSMContext):

    questions = await db.execute_query("SELECT id, name, question FROM question_answer WHERE answer = 'None'")
    await state.update_data(step=0)
    if questions:
        question = questions[0]
        await message.answer(
            f'Звернувся:\n<b>{question[1]}</b>\n\nТекст:\n{question[2]}',
            parse_mode="html",
            reply_markup=kb.qa_navigation
        )
        await state.update_data(questions=questions)
    else:
        await message.answer("Немає доступних питань.")

@router.message(F.text == 'Далі ➡️')
async def next_que(message: Message, state: FSMContext):
    data = await state.get_data()
    step = data.get("step", 0) + 1
    questions = data.get("questions", [])
    if not questions:
        await message.answer("Немає доступних питань.")
        return
    if step < 0 or step >= len(questions):
        await message.answer("Немає більше питань.")
        return
    await state.update_data(step=step)
    question = questions[step]
    await message.answer(
        f'Звернувся:\n<b>{question[1]}</b>\n\nТекст:\n{question[2]}',
        parse_mode="html",
        reply_markup=kb.qa_navigation
    )

@router.message(F.text == '⬅️ Назад')
async def prev_que(message: Message, state: FSMContext):
    data = await state.get_data()
    step = data.get("step", 0)
    questions = data.get("questions", [])
    step = max(step - 1, 0)
    await state.update_data(step=step)
    if step < len(questions):
        question = questions[step]
        await message.answer(
            f'Звернувся:\n<b>{question[1]}</b>\n\nТекст:\n{question[2]}',
            parse_mode="html",
            reply_markup=kb.qa_navigation
        )

class Answer(StatesGroup):
    answer = State()

@router.message(F.text == '✏️ Відповісти')
async def que_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    step = data.get("step", 0)
    questions = data.get("questions", [])
    if step < len(questions):
        question = questions[step]
        await message.answer(
            f'Повідомлення:\n<pre>Від: {question[1]}\nТекст: {question[2]}</pre>\nПишіть відповідь:',

            parse_mode="html"
        )
        await state.update_data(current_question_id=question[0])
    await state.set_state(Answer.answer)

@router.message(Answer.answer)
async def answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    answer = data['answer']
    question_id = data.get("current_question_id")
    await db.execute_query("UPDATE question_answer SET answer = %s WHERE id = %s", (answer, question_id))
    await message.answer("Відповідь збережено.",reply_markup=kb.admin)
    await state.clear()

