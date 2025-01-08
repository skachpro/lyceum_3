
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
    [KeyboardButton(text=f"Обрати профіль у 10 класі 🔍",callback_data="choose_the_profile")]
])

# profile = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text=f"Обрати профіль у 10 класі 🔍",callback_data="choose_the_profile")]
# ])
start_chooing_profiles= InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Почати тестування 💼",callback_data="start_testing_profiles")]
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

profile_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Перелік Профілів 📋", callback_data="profile_catalog")],
    [InlineKeyboardButton(text="Взнати ваш профіль 🤔", callback_data="check_my_profile")]
])

# Анкета
test_subj = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Українська мова', callback_data="ukr_philo"),
     InlineKeyboardButton(text='Українська література', callback_data="ukr_philo")],
    [InlineKeyboardButton(text='Математика', callback_data="math"),
     InlineKeyboardButton(text='Фізика', callback_data="physics")],
    [InlineKeyboardButton(text='Хімія', callback_data="chem-bio"),
     InlineKeyboardButton(text='Біологія', callback_data="chem-bio")],
    [InlineKeyboardButton(text='Зарубіжна література', callback_data="foreign_philo")],
    [InlineKeyboardButton(text='Інформатика', callback_data="it")],
    [InlineKeyboardButton(text='Основи правознавства', callback_data='law')]
])

skills = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Розв'язання задач", callback_data="math"),
     InlineKeyboardButton(text="Робота з комп'ютером", callback_data="it")],
    [InlineKeyboardButton(text="Історичний аналіз", callback_data="history"),
     InlineKeyboardButton(text="Права та закони", callback_data="law")],
    [InlineKeyboardButton(text="Природні науки", callback_data="geography"),
     InlineKeyboardButton(text="Дослідження природи", callback_data="chem_bio")],
    [InlineKeyboardButton(text="Письмо та текст", callback_data="ukr_philo"),
     InlineKeyboardButton(text="Іноземні мови", callback_data="foreign_philo")],
    [InlineKeyboardButton(text="Спорт", callback_data="sports_military"),
     InlineKeyboardButton(text="Творчість", callback_data="art")]
])

develop_skills = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Логіка та обчислення", callback_data="math"),
     InlineKeyboardButton(text="Програмування", callback_data="it")],
    [InlineKeyboardButton(text="Історичний аналіз", callback_data="history"),
     InlineKeyboardButton(text="Правознавство", callback_data="law")],
    [InlineKeyboardButton(text="Географія та екологія", callback_data="geography"),
     InlineKeyboardButton(text="Хімічні дослідження", callback_data="chem_bio")],
    [InlineKeyboardButton(text="Письмо та мовлення", callback_data="ukr_philo")],
    [InlineKeyboardButton(text="Культурологія та мови", callback_data="foreign_philo")],
    [InlineKeyboardButton(text="Спортивні навички", callback_data="sports_military"),
     InlineKeyboardButton(text="Художня творчість", callback_data="art")]
])

favorite_tasks = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Аналітичні завдання", callback_data="math"),
     InlineKeyboardButton(text="Творчі проєкти", callback_data="art")],
    [InlineKeyboardButton(text="Практичні експерименти", callback_data="chem_bio")],
    [InlineKeyboardButton(text="Написання текстів", callback_data="ukr_philology")],
    [InlineKeyboardButton(text="Вирішення логічних задач", callback_data="math")],
    [InlineKeyboardButton(text="Комунікація з людьми", callback_data="foreign_philo")],
    [InlineKeyboardButton(text="Дослідження законів", callback_data="law")],
    [InlineKeyboardButton(text="Поглиблене вивчення історії", callback_data="history")],
    [InlineKeyboardButton(text="Вивчення природних явищ", callback_data="geography")],
    [InlineKeyboardButton(text="Аналіз інформації", callback_data="it")]
])

free_time = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Розв'язую задачі", callback_data="math"),
     InlineKeyboardButton(text="Ігри / ІТ", callback_data="it")],
    [InlineKeyboardButton(text="Історія / документалістика", callback_data="history"),
     InlineKeyboardButton(text="Читаю про права", callback_data="law")],
    [InlineKeyboardButton(text="Природа / подорожі", callback_data="geography"),
     InlineKeyboardButton(text="Наукові дослідження", callback_data="chem_bio")],
    [InlineKeyboardButton(text="Пишу тексти", callback_data="ukr_philo"),
     InlineKeyboardButton(text="Читаю іноземною", callback_data="foreign_philo")],
    [InlineKeyboardButton(text="Займаюсь спортом", callback_data="sports_military"),
     InlineKeyboardButton(text="Малюю / музика", callback_data="art")]
])

future_profession = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Математик / аналітик", callback_data="math"),
     InlineKeyboardButton(text="Програміст", callback_data="it")],
    [InlineKeyboardButton(text="Історик", callback_data="historian"),
     InlineKeyboardButton(text="Юрист", callback_data="lawyer")],
    [InlineKeyboardButton(text="Географ / еколог", callback_data="geography"),
     InlineKeyboardButton(text="Біолог / хімік", callback_data="bio_chem")],
    [InlineKeyboardButton(text="Філолог (укр. мова)", callback_data="ukr_philo"),
     InlineKeyboardButton(text="Лінгвіст", callback_data="foreign_philo")],
    [InlineKeyboardButton(text="Військовий / спортсмен", callback_data="sports_military")],
    [InlineKeyboardButton(text="Художник / дизайнер", callback_data="art")]
])

# анкета закінчилась
profile_catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="◀️", callback_data="back"), InlineKeyboardButton(text="▶️", callback_data="next")],
    [InlineKeyboardButton(text="Дізнатися більше", url="http://tbl.km.ua/")]
])