import os
from typing import Dict, List, Tuple
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = str(tuple(column_values.values()))
    cursor.execute(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES " + values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int):
    row_id = int(row_id)
    cursor.execute(f"DELETE FROM {table} WHERE id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as script:
        sql = script.read()
    cursor.execute(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT table_name FROM information_schema.tables "
                   "WHERE table_schema NOT IN ('information_schema', 'pg_catalog');")
    table_exists = cursor.fetchall()
    if not table_exists:
        _init_db()


check_db_exists()
