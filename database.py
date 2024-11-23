import sqlite3

DB_NAME = "movies.db"

def get_connection():
    """Возвращает подключение к базе данных."""
    connection = sqlite3.connect(DB_NAME)
    return connection

def initialize_database():
    """Инициализирует базу данных, если это необходимо."""
    connection = get_connection()
    cursor = connection.cursor()
    # Создание таблицы, если она не существует
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT,
        year INTEGER,
        rating REAL,
        status TEXT,
        comment TEXT,
        cover_image TEXT,
        video_url TEXT
    )
    """)
    connection.commit()
    connection.close()
