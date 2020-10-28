from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""Кнопки для выпадающей клавиатуры"""
hi_btn = KeyboardButton('👋')
begin_btn = KeyboardButton('Начать тренировку✅')
menu_btn = KeyboardButton('МЕНЮ')
last_workout_button = KeyboardButton('/last_workout')
last_month_button = KeyboardButton("ВЫПОЛНЕНО ЗА МЕСЯЦ")
send_contact_btn = KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
send_location_btn = KeyboardButton('Отправить свою локацию 🗺️', request_location=True)

"""Структура выпадающей клавиатуры"""
screen_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
    .add(hi_btn)\
    .add(menu_btn)\
    .add(send_contact_btn)\
    .add(send_location_btn)\

"""Конструкция используемая для скрытия выпадающей клавиатуры"""
remove_kb = ReplyKeyboardRemove()

"""Кнопки инлайн-клавиатуры"""
get_plan_inline_btn = InlineKeyboardButton('Получить план тренировки на сегодня🗓', callback_data='start_training')
today_inline_btn = InlineKeyboardButton('Поднял сегодня💪', callback_data='today')
last_workout_inline_btn = InlineKeyboardButton('Последние записи🏁', callback_data='last_training')
month_inline_btn = InlineKeyboardButton('Статистика за месяц🌜', callback_data='month')
instagram_inline_btn = InlineKeyboardButton('Instagram🥇', url='https://www.instagram.com/oleg.akifjev/')
get_categories_inline_btn = InlineKeyboardButton('Справочник упражнений🔹', callback_data='categories')

"""Структура инлан-клавиатуры"""
inline_kb_full = InlineKeyboardMarkup(row_width=2)\
    .add(get_plan_inline_btn)\
    .add(today_inline_btn, last_workout_inline_btn, month_inline_btn)\
    .add(instagram_inline_btn).add(get_categories_inline_btn)

