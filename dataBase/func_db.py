from decouple import config

from mysql.connector import connect, Error

USER = config('USER', default='')
PASSWORD = config('PASSWORD', default='')


def exists_db():
    try:
        with connect(
            host="localhost",
            user=USER,
            password=PASSWORD,
        ) as connection:
            exists_db_query = 'USE awesome_app_KAI'
            with connection.cursor() as cursor:
                cursor.execute(exists_db_query)
            return True
    except Error as e:
        return False


def create_db():
    try:
        with connect(
            host="localhost",
            user=USER,
            password=PASSWORD,
        ) as connection:
            create_db_query = 'CREATE DATABASE awesome_app_KAI'
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)


def create_tables_db():
    try:
        with connect(
            host="localhost",
            user=USER,
            password=PASSWORD,
        ) as connection:
            create_table_query1 = '''CREATE TABLE IF NOT EXISTS users (ID int NOT NULL
            login TEXT,
            password TEXT)'''
            create_table_query2 = '''CREATE TABLE IF NOT EXISTS questions (ID int NOT NULL
            login TEXT,
            password TEXT)'''
            with connection.cursor() as cursor:
                cursor.execute(create_table_query1)
                cursor.execute(create_table_query2)
    except Error as e:
        print(e)

