import sqlite3
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect("students.db")
            cls._instance.connection.row_factory = sqlite3.Row
            cls._instance.cursor = cls._instance.connection.cursor()
            # Создание таблицы, если она не существует
            cls._instance.create_table()
        return cls._instance

    def create_table(self):
        # Создаем таблицу студентов, если она еще не существует
        self.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone_number TEXT NOT NULL UNIQUE,
                group_name TEXT NOT NULL
            )
        """)

    def execute(self, query, params=None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        # Применяем изменения к базе данных
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()



