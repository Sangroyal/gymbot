from aiogram.types \
    import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

button_hi = KeyboardButton('👋')
button1 = KeyboardButton('Начать тренировку✅')
button2 = KeyboardButton('МЕНЮ')
button3 = KeyboardButton('/last_workout')
button4 = KeyboardButton("ВЫПОЛНЕНО ЗА МЕСЯЦ")
button5 = KeyboardButton('')
button6 = KeyboardButton('')

markup1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True). \
    add(button_hi).add(button2). \
    add(KeyboardButton('Отправить свой контакт ☎️', request_contact=True)). \
    add(KeyboardButton('Отправить свою локацию 🗺️', request_location=True))

markup_kb_remove = ReplyKeyboardRemove()

inline_btn_1 = InlineKeyboardButton('🗓Получить план тренировки на сегодня🗓', callback_data='start_training')
inline_btn_3 = InlineKeyboardButton('💪Поднял сегодня💪', callback_data='/today')
inline_btn_4 = InlineKeyboardButton('🏁Последняя тренировка🏁', callback_data='last_training')
inline_btn_5 = InlineKeyboardButton('🌜Статистика за месяц🌜', callback_data='month')

inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)

inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
# inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
# inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
# inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
# inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
inline_kb_full.add(InlineKeyboardButton('🥇Instagram лучшего тренера🥇', url='https://www.instagram.com/oleg.akifjev/'))
inline_kb_full.add(InlineKeyboardButton('Справочник упражнений', callback_data='categories'))
