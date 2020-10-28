from typing import NamedTuple, List


class Exercise(NamedTuple):
    """Структура добавленного упражнения"""
    user_id: int
    name: str
    weight: int
    repetitions: int
    category_codename: str

'''
class Message(NamedTuple):
    """Структура распаршенного сообщения о новом повторении"""
    user_id: int
    weight: int
    repetitions: int
    category_codename: str
'''


class Category(NamedTuple):
    """Структура категории"""
    codename: str
    name: str
    is_base_exercise: bool
    aliases: List[str]
