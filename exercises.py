""" Работа с повторениями — их добавление, удаление, статистики"""
import datetime
import re
from typing import List, NamedTuple, Optional
from aiogram import Bot, Dispatcher, executor, types

import pytz

import db
import exceptions
from categories import Categories


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом повторении"""
    user_id: int
    weight: int
    reiteration: int
    category_text: str


class Exercise(NamedTuple):
    """Структура добавленного нового выполненного упражнения в БД"""
    user_id: int
    weight: int
    reiteration: int
    category_name: str


def _parse_message(message) -> Message:
    """Парсит текст пришедшего сообщения о новом подходе"""
    regexp_result = re.match(r"([\d ]+)(.*)", message.text)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n100 4 жим")

    user_id = message.from_user.id
    weight = int(regexp_result.group(1).replace(" ", ""))
    reiteration = int(regexp_result.group(1).replace(" ", ""))
    category_text = regexp_result.group(2).strip().lower()
    return Message(user_id=user_id, weight=weight, reiteration=reiteration, category_text=category_text)


def add_exercise(message) -> Exercise:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(message)
    user_id = Message.user_id
    reiteration = Message.reiteration
    category = Categories().get_category(
        parsed_message.category_text)
    inserted_row_id = db.insert("exercises", {
        "user_id": user_id,
        "weight": parsed_message.weight,
        "reiteration": parsed_message.reiteration,
        "created": _get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": message.text
    })
    return Exercise(user_id=user_id, weight=parsed_message.weight, reiteration=reiteration, category_name=category.name)


def delete_exercise(row_id: int) -> None:
    """Удаляет сообщение по его идентификатору"""
    db.delete("exercises", row_id)


def get_today_statistics() -> str:
    """Возвращает строкой статистику тренировки за сегодня"""
    cursor = db.get_cursor()
    cursor.execute("select sum(weight)"
                   "from exercises where date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "Ты сегодня еще и грамма не поднял. Бегом на тренировку"
    all_today_exercise = result[0]
    cursor.execute("select sum(weight) "
                   "from exercises where date(created)=date('now', 'localtime') "
                   "and category_codename in (select codename "
                   "from category where is_base_exercise=true)")
    result = cursor.fetchone()
    base_today_exercise = result[0] if result[0] else 0
    return (f"Уже поднял сегодня:\n"
            f"всего — {all_today_exercise} кг.\n"
            f"базовые — {base_today_exercise} кг. из {_get_daily_volume()} кг.\n\n"
            f"За текущий месяц: /month")


def get_month_statistics() -> str:
    """Возвращает строкой статистику тренировок за текущий месяц"""
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select sum(weight) "
                   f"from exercises where date(created) >= '{first_day_of_month}'")
    result = cursor.fetchone()
    if not result[0]:
        return "В этом месяце ещё небыло тренировок"
    all_today_exercise = result[0]
    cursor.execute(f"select sum(weight) "
                   f"from exercises where date(created) >= '{first_day_of_month}' "
                   f"and category_codename in (select codename "
                   f"from category where is_base_exercise=true)")
    result = cursor.fetchone()
    base_today_exercise = result[0] if result[0] else 0
    return (f"В этом месяце ты поднял:\n"
            f"всего — {all_today_exercise} кг.\n"
            f"базовые — {base_today_exercise} кг. из "
            f"{now.day * _get_daily_volume()} кг.")


def last() -> List[Exercise]:
    """Возвращает последние несколько расходов"""
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.weight, c.name "
        "from exercises e left join category c "
        "on c.codename=e.category_codename "
        "order by created desc limit 10")
    rows = cursor.fetchall()
    last_exercises = [Exercise(user_id=row[0], weight=row[1], reiteration=row[2], category_name=row[3]) for row in rows]
    return last_exercises


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _get_daily_volume() -> int:
    """Возвращает дневной объем повторений в кг."""
    return db.fetchall("training_plan", ["daily_volume"])[0]["daily_volume"]
