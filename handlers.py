import datetime

from aiogram import types

import keyboards as kb
import exceptions
import exercises
from categories import Categories


class Handlers:
    def __init__(self, dp, bot):
        dp = dp
        bot = bot

        week_day = {0: 'понедельник', 1: 'вторник', 2: 'среда',
                    3: 'четверг', 4: 'пятница', 5: 'суббота', 6: 'воскресенье'}

        exercise_type = {0: 'грудь и бицепс', 1: 'спину и трицепс', 2: 'грудь и плечи', 3: 'спину и ноги',
                         4: 'грудь и ноги', 5: 'расслабься, сегодня выходной ;)',
                         6: 'мозг. Нет ну отдых то должен быть? ;)'}

        week_day_value = datetime.datetime.today().weekday()
        today = week_day[week_day_value]
        exercise_name = exercise_type[week_day_value]

        @dp.callback_query_handler(lambda c: c.data == 'start_training')
        async def process_callback_button1(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, 'Выложись по полной', reply_markup=kb.inline_kb_full)

        @dp.callback_query_handler(lambda c: c.data == '/today')
        async def process_callback_button1(callback_query: types.CallbackQuery):
            answer_message = exercises.get_today_statistics()
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, answer_message, reply_markup=kb.inline_kb_full)

        @dp.callback_query_handler(lambda c: c.data == 'month')
        async def process_callback_button1(callback_query: types.CallbackQuery):
            answer_message = exercises.get_month_statistics()
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, answer_message, reply_markup=kb.inline_kb_full)

        @dp.callback_query_handler(lambda c: c.data == 'last_training')
        async def process_callback_button1(callback_query: types.CallbackQuery):
            last_exercises = exercises.last()
            if not last_exercises:
                await bot.send_message(callback_query.from_user.id,
                                       "Вы еще не вносили данные о тренировках", reply_markup=kb.inline_kb_full)
                return
            last_exercises_rows = [
                f"{exercise.weight} кг. - {exercise.category_name} — нажми "
                f"/del{exercise.user_id} для удаления"
                for exercise in last_exercises]
            answer_message = "Последние сохранённые данные:\n\n➕ " + "\n\n➕ " \
                .join(last_exercises_rows)
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, answer_message, reply_markup=kb.inline_kb_full)

        @dp.callback_query_handler(lambda c: c.data == 'categories')
        async def categories_list(callback_query: types.CallbackQuery):
            """Отправляет справочник упражнений"""
            categories = Categories().get_all_categories()
            answer_message = "Справочник упражнений:\n\n🔹 " + \
                             ("\n🔹 ".join([c.name + ' - (' + ", ".join(c.aliases) + ')' for c in categories]))
            await bot.send_message(callback_query.from_user.id, answer_message, reply_markup=kb.inline_kb_full)

        @dp.callback_query_handler(lambda c: c.data == 'help')
        async def send_menu(callback_query: types.CallbackQuery):
            """Отправляет приветственное сообщение и помощь по боту"""
            await bot.send_message(callback_query.from_user.id,
                                   f"Привет👋, {callback_query.from_user.first_name}!\n"
                                   f"Cегодня - {today}, а значит\n"
                                   f"пришло время качать {exercise_name}\n\n", reply_markup=kb.markup1)

        @dp.message_handler(commands=['start', 'hi', 'привет'])
        async def send_welcome(message: types.Message):
            """Отправляет приветственное сообщение и помощь по боту"""
            await message.answer(f"Привет👋, {message.from_user.first_name}!\n"
                                 "Я рад что ты теперь с нами!\n"
                                 "Я постараюсь быть максимально эффективным.\n"
                                 "Вместе мы сможем!!!\n\n",
                                 reply_markup=kb.markup1)

        @dp.message_handler(lambda message: message.text == '👋')
        async def exercises_plan(message: types.Message):
            """Отправляет план тренировки на сегодня"""
            week_day_value = datetime.datetime.today().weekday()
            today = week_day[week_day_value]
            exercise_name = exercise_type[week_day_value]
            await message.answer(f"Cегодня - {today}, а значит\n"
                                 f"пришло время качать {exercise_name}\n\n", reply_markup=kb.inline_kb_full)

        @dp.message_handler(lambda message: message.text == 'МЕНЮ')
        async def exercises_plan(message: types.Message):
            """Отправляет меню"""
            await message.answer('Ок, вот тебе меню:', reply_markup=kb.inline_kb_full)

        @dp.message_handler(lambda message: message.text.startswith('/del'))
        async def del_exercise(message: types.Message):
            """Удаляет одну запись об подходе по её идентификатору"""
            row_id = int(message.text[4:])
            exercises.delete_exercise(row_id)
            answer_message = "Удалил"
            await message.answer(answer_message)

        @dp.message_handler(commands=['month'])
        async def month_statistics(message: types.Message):
            """Отправляет статистику поднятого веса текущего месяца"""
            answer_message = exercises.get_month_statistics()
            await message.answer(answer_message)

        @dp.message_handler()
        async def add_exercise(message: types.Message):
            """Добавляет новую запись о подходе"""
            try:
                exercise = exercises.add_exercise(message)
                print(exercise)
            except exceptions.NotCorrectMessage as e:
                await message.answer(str(e))
                return
            answer_message = (
                f"Добавлено в зачёт:\n"
                f"{exercise.weight} кг - на {exercise.reiteration} повторений - {exercise.category_name}.\n\n"
                f"{exercises.get_today_statistics()}")
            await message.answer(answer_message)
