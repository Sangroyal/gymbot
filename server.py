import logging
import os
import datetime

from aiogram import Bot, Dispatcher, executor, types

from categories import Categories
import exceptions
import exercises
import keyboards as kb
from parsers import MessageParser

logging.basicConfig(level=logging.INFO)

# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
API_TOKEN = '1202070076:AAHCDBf0bIm4A9xmqRKf5726Ux9EKS0gYok'
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
# ACCESS_ID = '545679284'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
categories = Categories()
parser = MessageParser(categories)


@dp.callback_query_handler(lambda c: c.data == 'today')
async def get_today_stats(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    answer_message = exercises.get_today_statistics(user_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(user_id, answer_message, reply_markup=kb.inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'start_training')
async def start_training(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(user_id, "Вот что тебе предстоит выполнить:",
                           reply_markup=kb.inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'last_training')
async def get_last_training_stats(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    last_exercises = exercises.last(user_id)
    if not last_exercises:
        await bot.send_message(callback_query.from_user.id,
                               "Вы еще не вносили данные о тренировках", reply_markup=kb.inline_kb_full)
        return
    last_exercises_rows = [
        f"{exercise.weight} кг. - {exercise.category_codename} — нажми "
        f"/del{exercise.user_id} для удаления"
        for exercise in last_exercises]
    answer_message = "Последние сохранённые данные:\n\n➕ " + "\n\n➕ " \
        .join(last_exercises_rows)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, answer_message, reply_markup=kb.inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'month')
async def get_month_stats(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    answer_message = exercises.get_month_statistics(user_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(user_id, answer_message, reply_markup=kb.inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'categories')
async def categories_list(callback_query: types.CallbackQuery):
    """Отправляет справочник упражнений"""
    all_categories = categories.get_all_categories()
    answer_message = "Справочник упражнений:\n\n🔹 " + \
                     ("\n🔹 ".join([c.name + ' - (' + ", ".join(c.aliases) + ')' for c in all_categories]))
    await bot.send_message(callback_query.from_user.id, answer_message, reply_markup=kb.inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'help')
async def send_menu(callback_query: types.CallbackQuery):
    """Отправляет приветственное сообщение и помощь по боту"""
    await bot.send_message(callback_query.from_user.id,
                           "Если ты чувствуешь что готов повысить эффективность тренировок,\n"
                           "разобраться с планом питания и создать индивидуальную программу,\n"
                           f"то смело жми на эту кнопку\n", reply_markup=kb.screen_keyboard)


@dp.message_handler(commands=['start', 'hi', 'привет'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(f"Привет👋, {message.from_user.first_name}!\n"
                         "Я рад что ты теперь с нами!\n"
                         "Я постараюсь быть максимально эффективным помошником.\n",
                         reply_markup=kb.screen_keyboard)


@dp.message_handler(lambda message: message.text == '👋')
async def exercises_plan(message: types.Message):
    """Отправляет план тренировки на сегодня"""
    await message.answer(f"Cегодня - {exercises.get__week_value()}, а значит\n"
                         f"пришло время качать {exercises.get_type_exercise_now()}\n\n",
                         reply_markup=kb.inline_kb_full)


@dp.message_handler(lambda message: message.text == 'МЕНЮ')
async def menu_text_btn(message: types.Message):
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
    user_id = message.from_user.id
    answer_message = exercises.get_month_statistics(user_id)
    await message.answer(answer_message)


@dp.message_handler()
async def add_exercise(message: types.Message):
    """Добавляет новую запись о подходе"""
    try:
        user_id = message.from_user.id
        exercise = parser.parse_exercise(message)
        exercises.add_exercise(exercise)
        answer_message = (
            f"Добавлено в зачёт:\n"
            f"{exercise.weight} кг - на {exercise.repetitions} повторений - {exercise.category_codename}.\n\n"
            f"{exercises.get_today_statistics(user_id)}")
        await message.answer(answer_message)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
