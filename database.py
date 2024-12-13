import sqlite3

import pandas as pd


class Database:
    def __init__(self, db_path='movies.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        # Таблица фильмов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT,
                year INTEGER,
                director TEXT,
                rating INTEGER,
                status TEXT,
                date_watched TEXT,
                cover_image_path TEXT,
                link TEXT
            )
        ''')

        # Таблица заметок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                comment_text TEXT,
                timestamp TEXT,
                FOREIGN KEY(movie_id) REFERENCES movies(id)
            )
        ''')

        self.connection.commit()

    def add_movie(self, movie_data):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO movies (title, genre, year, director, rating, status, date_watched, cover_image_path, link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            movie_data['title'],
            movie_data['genre'],
            movie_data['year'],
            movie_data['director'],
            movie_data['rating'],
            movie_data['status'],
            movie_data['date_watched'],
            movie_data['cover_image_path'],
            movie_data['link']
        ))
        self.connection.commit()
        return cursor.lastrowid

    def update_movie(self, movie_id, movie_data):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE movies
            SET title = ?, genre = ?, year = ?, director = ?, rating = ?, status = ?, date_watched = ?, cover_image_path = ?, link = ?
            WHERE id = ?
        ''', (
            movie_data['title'],
            movie_data['genre'],
            movie_data['year'],
            movie_data['director'],
            movie_data['rating'],
            movie_data['status'],
            movie_data['date_watched'],
            movie_data['cover_image_path'],
            movie_data['link'],
            movie_id
        ))
        self.connection.commit()

    def delete_movie(self, movie_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
        cursor.execute('DELETE FROM notes WHERE movie_id = ?', (movie_id,))
        self.connection.commit()

    def get_movie(self, movie_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
        row = cursor.fetchone()
        if row:
            return self.row_to_dict(cursor, row)
        return None

    def get_movies(self, search_query='', filters={}):
        cursor = self.connection.cursor()
        query = 'SELECT * FROM movies WHERE 1=1'
        params = []

        if search_query:
            query += ' AND title LIKE ?'
            params.append(f'%{search_query}%')

        # Фильтры могут быть расширены по необходимости

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [self.row_to_dict(cursor, row) for row in rows]

    def add_note(self, note_data):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO notes (movie_id, comment_text, timestamp)
            VALUES (?, ?, ?)
        ''', (
            note_data['movie_id'],
            note_data['comment_text'],
            note_data['timestamp']
        ))
        self.connection.commit()

    def get_notes(self, movie_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM notes WHERE movie_id = ?', (movie_id,))
        rows = cursor.fetchall()
        return [self.row_to_dict(cursor, row) for row in rows]

    def row_to_dict(self, cursor, row):
        return {description[0]: value for description, value in zip(cursor.description, row)}

    def import_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            movie_data = {
                'title': row.get('title'),
                'genre': row.get('genre'),
                'year': row.get('year'),
                'director': row.get('director'),
                'rating': row.get('rating', 0),
                'status': row.get('status', 'в планах'),
                'date_watched': row.get('date_watched', ''),
                'cover_image_path': '',
                'link': row.get('link', '')
            }
            self.add_movie(movie_data)

    def import_from_sql(self, sql_file_path, table_name='movies'):
        external_conn = sqlite3.connect(sql_file_path)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", external_conn)
        for _, row in df.iterrows():
            movie_data = {
                'title': row.get('title') or row.get('movie_name'),
                'genre': row.get('genre'),
                'year': row.get('year'),
                'director': row.get('director'),
                'rating': row.get('rating', 0),
                'status': row.get('status', 'в планах'),
                'date_watched': row.get('date_watched', ''),
                'cover_image_path': '',
                'link': row.get('link', '')
            }
            self.add_movie(movie_data)
        external_conn.close()

    def close(self):
        self.connection.close()
