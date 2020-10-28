from categories import Categories
from model import Exercise, Category
from aiogram import types

from exceptions import NotCorrectMessage


class MessageParser:
    def __init__(self, categories: Categories):
        self.categories = categories

    def parse_exercise(self, message: types.Message) -> Exercise:
        """Парсит текст пришедшего сообщения о новом подходе"""
        try:
            parsed_message = message.text.split()
            user_id = int(message.from_user.id)
            weight = int(parsed_message[0])
            repetitions = int(parsed_message[1])
            exercise_name = parsed_message[2]
            category: Category = self.categories.get_category_by_name(exercise_name)
            return Exercise(user_id=user_id,
                            weight=weight,
                            repetitions=repetitions,
                            category_codename=category.codename,
                            name=exercise_name)

        except Exception:
            raise NotCorrectMessage('Не могу понять сообщение. Напишите сообщение в формате, "например: 100 4 жим"')
