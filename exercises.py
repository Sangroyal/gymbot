""" Работа с повторениями — их добавление, удалени и статистика"""
import datetime
from typing import List, NamedTuple

import pytz

import db
from parsers import MessageParser
import exceptions
from categories import Categories
from model import Exercise


week_days = {0: 'понедельник',
             1: 'вторник',
             2: 'среда',
             3: 'четверг',
             4: 'пятница',
             5: 'суббота',
             6: 'воскресенье'}

exercise_type = {0: 'грудь и бицепс',
                 1: 'спину и трицепс',
                 2: 'грудь и плечи',
                 3: 'спину и ноги',
                 4: 'грудь и ноги',
                 5: 'расслабься, сегодня выходной ;)',
                 6: 'мозг. Нет ну отдых то должен быть? ;)'}


def add_exercise(exercise: Exercise):
    (user_id, name, weight, repetitions, category_codename) = exercise
    db.insert("exercises",
              {"user_id": user_id,
               "weight": weight,
               "repetitions": repetitions,
               "created": _get_now_formatted(),
               "category_codename": category_codename,
               "name": name})


def delete_exercise(row_id: int) -> None:
    """Удаляет сообщение по его идентификатору"""
    db.delete("exercises", row_id)


def get__week_value():
    """Возвращает день текущий недели"""
    week_day_value = datetime.datetime.today().weekday()
    week_day = week_days[week_day_value]
    return week_day


def get_type_exercise_now():
    """Возвращает упражнение в зависимости от дня недели"""
    week_day_value = datetime.datetime.today().weekday()
    exercise_name = exercise_type[week_day_value]
    return exercise_name


def get_today_statistics(user_id) -> str:
    """Возвращает строкой статистику тренировки за сегодня"""
    cursor = db.get_cursor()
    cursor.execute('SELECT SUM(weight*repetitions) '
                   'FROM exercises '
                   'WHERE date(created)=date("now", "localtime") '
                   'AND user_id={user_id}'
                   .format(user_id=user_id))
    result = cursor.fetchone()
    if not result[0]:
        return "Ты сегодня еще и грамма не поднял. Бегом на тренировку"
    all_today_exercise = result[0]
    cursor.execute('SELECT SUM(weight) '
                   'FROM exercises '
                   'WHERE date(created)=date("now", "localtime") '
                   'AND user_id={user_id} '
                   'AND category_codename IN (SELECT codename '
                   'FROM category '
                   'WHERE is_base_exercise=true)'
                   .format(user_id=user_id))
    result = cursor.fetchone()
    base_today_exercise = result[0] if result[0] else 0
    return (f"Уже поднял сегодня:\n"
            f"всего — {all_today_exercise} кг.\n"
            f"базовые — {base_today_exercise} кг. из {_get_daily_volume()} кг.\n\n"
            f"За текущий месяц: /month")


def get_month_statistics(user_id) -> str:
    """Возвращает строкой статистику тренировок за текущий месяц"""
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute('SELECT SUM(weight*repetitions) '
                   'FROM exercises '
                   'WHERE date(created) >= {first_day_of_month} '
                   'AND user_id = {user_id}'
                   .format(user_id=user_id, first_day_of_month=first_day_of_month))
    result = cursor.fetchone()
    if not result[0]:
        return "В этом месяце ещё небыло тренировок"
    all_today_exercise = result[0]
    cursor.execute('SELECT SUM(weight*repetitions) '
                   'FROM exercises '
                   'WHERE date(created) >= {first_day_of_month} '
                   'AND user_id = {user_id} '
                   'AND category_codename in (select codename '
                   'FROM category WHERE is_base_exercise=true)'
                   .format(first_day_of_month=first_day_of_month, user_id=user_id))
    result = cursor.fetchone()
    base_today_exercise = result[0] if result[0] else 0
    return (f"В этом месяце ты поднял:\n"
            f"всего — {all_today_exercise} кг.\n"
            f"базовые — {base_today_exercise} кг. из "
            f"{now.day * _get_daily_volume()} кг.")


def last(user_id) -> List[Exercise]:
    """Возвращает последние несколько расходов"""
    cursor = db.get_cursor()
    cursor.execute('SELECT e.id, e.weight*e.repetitions, e.repetitions, e.name, c.name '
                   'FROM exercises e '
                   'LEFT JOIN category c '
                   'ON c.codename=e.category_codename '
                   'WHERE e.user_id={user_id} '
                   'ORDER BY created DESC limit 10'
                   .format(user_id=user_id))
    rows = cursor.fetchall()
    last_exercises = [Exercise(user_id=row[0], weight=row[1], repetitions=row[2], name=row[3], category_codename=row[4])
                      for row in rows]
    return last_exercises


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    time_zone = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(time_zone)
    return now


def _get_daily_volume() -> int:
    """Возвращает дневной объем повторений в кг."""
    return db.fetchall("training_plan", ["daily_volume"])[0]["daily_volume"]
