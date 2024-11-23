import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from ui_mainwindow import Ui_MainWindow
from database import get_connection, initialize_database
from sql_import import import_sql
from movie_card_dialog import MovieCardDialog
from add_movie_dialog import AddMovieDialog  # Мы создадим это ниже


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setup_ui(self)

        # Подключаем кнопки
        self.ui.btn_refresh.clicked.connect(self.refresh_table)
        self.ui.btn_add.clicked.connect(self.add_movie)
        self.ui.btn_import.clicked.connect(self.import_from_sql)
        self.ui.btn_open_card.clicked.connect(self.open_movie_card)

        # Инициализация базы данных
        initialize_database()
        self.refresh_table()

    def refresh_table(self):
        """Обновляет данные в таблице."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT title, genre, year, rating, status FROM movies")
        rows = cursor.fetchall()
        connection.close()

        self.ui.table.setRowCount(0)
        for row_data in rows:
            row = self.ui.table.rowCount()
            self.ui.table.insertRow(row)
            for col, data in enumerate(row_data):
                self.ui.table.setItem(row, col, QTableWidgetItem(str(data)))

    def add_movie(self):
        """Открывает диалог для добавления нового фильма."""
        dialog = AddMovieDialog(self)
        if dialog.exec():
            data = dialog.get_movie_data()
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
            INSERT INTO movies (title, genre, year, rating, status)
            VALUES (?, ?, ?, ?, ?)
            """, (data["title"], data["genre"], data["year"], data["rating"], data["status"]))

            connection.commit()
            connection.close()
            self.refresh_table()

    def import_from_sql(self):
        """Открывает диалог для выбора SQL-файла и импортирует данные."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите SQL файл", "", "SQL Files (*.sql *.sqlite)")
        if file_path:
            import_sql(file_path)
            self.refresh_table()

    def open_movie_card(self):
        """Открывает карточку выбранного фильма."""
        selected_row = self.ui.table.currentRow()
        if selected_row != -1:
            movie_id_item = self.ui.table.item(selected_row, 0)
            if movie_id_item:
                movie_id = int(movie_id_item.text())
                dialog = MovieCardDialog(movie_id, self)
                dialog.exec()
                self.refresh_table()

def open_movie_card(self):
    """Открывает карточку выбранного фильма."""
    selected_row = self.ui.table.currentRow()
    if selected_row != -1:
        movie_id_item = self.ui.table.item(selected_row, 0)
        if movie_id_item:
            movie_id = int(movie_id_item.text())
            dialog = MovieCardDialog(movie_id, self)
            dialog.exec()
            self.refresh_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
