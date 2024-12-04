
from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import emoji
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Я навчаюсь в ліцеї 👨‍🎓')],
    [KeyboardButton(text='Я не навчаюсь в ліцеї ❌👨‍🎓')],
    [KeyboardButton(text='Я з адміністрації ліцею 🏫🧑‍💼')]
])

not_for_students = ReplyKeyboardMarkup(keyboard=[
    [ KeyboardButton(text="Контакти ☎️"), KeyboardButton(text=f"Про Ліцей {emoji.emojize(':school:')}")],
    
    [KeyboardButton(text=f"Обрати профіль у 10 класі 🔍")]
])

for_students = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f'Розклад 📋'),
    KeyboardButton(text="Дошка оголошень 📌")],
    [KeyboardButton(text="Запитання/Відповідь 💬")],
    [KeyboardButton(text="Меню їдальні 🍽️")]
])


select_num_of_class = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f"7-9 клас"), KeyboardButton(text=f'10-11 клас')]
])

kbd_for_young_stud = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f'Розклад 📋'),KeyboardButton(text="Дошка оголошень 📌")],
    [KeyboardButton(text="Запитання/Відповідь 💬")],
    [KeyboardButton(text="Меню їдальні 🍽️")],
    [KeyboardButton(text=f"Обрати профіль у 10 класі 🔍", url="https://t.me/Lyceum_Profile_Selection_bot")]
])

profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"Обрати профіль у 10 класі 🔍", url="https://t.me/Lyceum_Profile_Selection_bot")]
])

qa = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f'Запитати/Запроронувати 📝', callback_data="ask")],
    [InlineKeyboardButton(text=f'Переглянути відповіді 📖', callback_data="check_for_answer")]
])

admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f"Відповісти на питання")],
    [KeyboardButton(text=f'Дошка оголошень')],
    [KeyboardButton(text=f"Розклад дзвінків")],
    [KeyboardButton(text="Меню їдальні")]
])

qa_navigation = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="⬅️ Назад"),
                KeyboardButton(text="Далі ➡️"),
            ],
            [
                KeyboardButton(text="✏️ Відповісти"),
            ],
        ]
    )

answer_nav = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="prev"),
     InlineKeyboardButton(text="Вперед ➡️", callback_data="next")]
])

about = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f'Дізнатись більше...', url='http://tbl.km.ua/')]
])

skip_photo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пропустити дію.', callback_data='skip_photo')]
])

rozklad = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Розклад дзвінків 🔔', callback_data='alert_plan')],
    [InlineKeyboardButton(text='Розклад уроків 📋', callback_data='lesson_plan',url='https://client.rozklad.org/files/rozklad/rr/r_2755.html?1732728631375#c')]
])