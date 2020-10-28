"""Работа с категориями упражнений"""
from typing import Dict, List
from model import Category

import db


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Возвращает справочник категорий упражнений"""
        categories = db.fetchall("category", "codename name is_base_exercise aliases".split())
        categories = self._fill_aliases(categories)
        return categories

    @staticmethod
    def _fill_aliases(categories: List[Dict]) -> List[Category]:
        """Заполняет по каждой категории aliases, то есть возможные
        названия этой категории, которые можем писать в тексте сообщения.
        Например, категория «жим штанги лежа» может быть написана как "жим",
        "bench press" и тд."""
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                is_base_exercise=category['is_base_exercise'],
                aliases=aliases
            ))
        return categories_result

    def get_all_categories(self) -> List[Category]:
        """Возвращает справочник категорий упражнений"""
        return self._categories

    def get_category_by_name(self, category_name: str) -> Category:
        """Возвращает категорию по одному из её алиасов."""
        found = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    found = category
        if not found:
            found = other_category
        return found
