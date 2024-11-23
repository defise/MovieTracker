import sqlite3
from database import get_connection

def import_sql(file_path):
    """Импортирует данные из указанного SQL-файла в базу данных."""
    try:
        source_connection = sqlite3.connect(file_path)
        source_cursor = source_connection.cursor()
        source_cursor.execute("SELECT * FROM movies")  # Измените таблицу на нужную

        rows = source_cursor.fetchall()
        source_connection.close()

        # Вставка данных в локальную базу
        target_connection = get_connection()
        target_cursor = target_connection.cursor()

        for row in rows:
            target_cursor.execute("""
            INSERT INTO movies (title, genre, year, rating, status)
            VALUES (?, ?, ?, ?, ?)
            """, row[:5])  # Убедитесь, что столбцы совпадают

        target_connection.commit()
        target_connection.close()
        print("Импорт завершён успешно!")
    except Exception as e:
        print(f"Ошибка импорта: {e}")
