import re
import sys
from datetime import datetime

from PyQt6 import QtWidgets, QtGui, QtCore

from database import Database
from ui_add_edit_movie import Ui_Dialog as Ui_AddEditMovieDialog
from ui_main import Ui_MainWindow


class AddEditMovieDialog(QtWidgets.QDialog):
    def __init__(self, db, movie=None):
        super().__init__()
        self.ui = Ui_AddEditMovieDialog()
        self.ui.setupUi(self)
        self.db = db
        self.movie = movie
        self.cover_image_path = ''
        self.init_ui()

    def init_ui(self):
        if self.movie:
            self.ui.lineEditTitle.setText(self.movie['title'])
            self.ui.lineEditGenre.setText(self.movie['genre'])
            self.ui.spinBoxYear.setValue(self.movie['year'] or 2000)
            self.ui.lineEditDirector.setText(self.movie['director'])
            self.ui.spinBoxRating.setValue(self.movie['rating'] or 0)
            self.ui.comboBoxStatus.setCurrentText(self.movie['status'])
            if self.movie['date_watched']:
                date = QtCore.QDate.fromString(self.movie['date_watched'], 'yyyy-MM-dd')
                self.ui.dateEditWatched.setDate(date)
            self.ui.lineEditLink.setText(self.movie['link'])
            self.cover_image_path = self.movie['cover_image_path']
            if self.cover_image_path and QtCore.QFile.exists(self.cover_image_path):
                pixmap = QtGui.QPixmap(self.cover_image_path)
                self.ui.labelCover.setPixmap(pixmap.scaled(150, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            notes = self.db.get_notes(self.movie['id'])
            comments = '\n'.join([note['comment_text'] for note in notes])
            self.ui.textEditComments.setPlainText(comments)

        self.ui.btnChooseCover.clicked.connect(self.choose_cover_image)
        self.ui.btnSave.clicked.connect(self.save_movie)
        self.ui.btnCancel.clicked.connect(self.reject)

    def choose_cover_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать обложку", "",
                                                             "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.cover_image_path = f"resources/images/{QtCore.QFileInfo(file_path).fileName()}"
            QtCore.QFile.copy(file_path, self.cover_image_path)
            pixmap = QtGui.QPixmap(self.cover_image_path)
            self.ui.labelCover.setPixmap(pixmap.scaled(150, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

    def save_movie(self):
        movie_data = {
            'title': self.ui.lineEditTitle.text(),
            'genre': self.ui.lineEditGenre.text(),
            'year': self.ui.spinBoxYear.value(),
            'director': self.ui.lineEditDirector.text(),
            'rating': self.ui.spinBoxRating.value(),
            'status': self.ui.comboBoxStatus.currentText(),
            'date_watched': self.ui.dateEditWatched.date().toString('yyyy-MM-dd'),
            'cover_image_path': self.cover_image_path,
            'link': self.ui.lineEditLink.text()
        }

        if self.movie:
            self.db.update_movie(self.movie['id'], movie_data)
            movie_id = self.movie['id']
        else:
            movie_id = self.db.add_movie(movie_data)

        # Сохранение комментариев
        comment_text = self.ui.textEditComments.toPlainText()
        if comment_text:
            note_data = {
                'movie_id': movie_id,
                'comment_text': comment_text,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.db.add_note(note_data)

        self.accept()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database()
        self.selected_movie = None
        self.init_ui()

    def init_ui(self):
        self.load_movies()

        self.ui.lineEditSearch.textChanged.connect(self.search_movies)
        self.ui.listWidgetMovies.itemSelectionChanged.connect(self.display_movie_details)
        self.ui.btnAddMovie.clicked.connect(self.add_movie)
        self.ui.btnEditMovie.clicked.connect(self.edit_movie)
        self.ui.btnDeleteMovie.clicked.connect(self.delete_movie)
        self.ui.btnImportCSV.clicked.connect(self.import_csv)
        self.ui.btnImportSQL.clicked.connect(self.import_sql)

    def load_movies(self, search_query=''):
        movies = self.db.get_movies(search_query=search_query)
        self.ui.listWidgetMovies.clear()
        for movie in movies:
            item = QtWidgets.QListWidgetItem(movie['title'])
            item.setData(QtCore.Qt.ItemDataRole.UserRole, movie)
            self.ui.listWidgetMovies.addItem(item)

    def search_movies(self):
        query = self.ui.lineEditSearch.text()
        self.load_movies(search_query=query)

    def display_movie_details(self):
        selected_items = self.ui.listWidgetMovies.selectedItems()
        if selected_items:
            item = selected_items[0]
            self.selected_movie = item.data(QtCore.Qt.ItemDataRole.UserRole)
            movie = self.selected_movie

            self.ui.labelTitle.setText(movie['title'])
            self.ui.labelGenre.setText(f"Жанр: {movie['genre']}")
            self.ui.labelYear.setText(f"Год: {movie['year']}")
            self.ui.labelDirector.setText(f"Режиссёр: {movie['director']}")
            self.ui.labelRating.setText(f"Оценка: {movie['rating']}")
            self.ui.labelStatus.setText(f"Статус: {movie['status']}")
            self.ui.labelDateWatched.setText(f"Дата просмотра: {movie['date_watched']}")
            if movie['cover_image_path'] and QtCore.QFile.exists(movie['cover_image_path']):
                pixmap = QtGui.QPixmap(movie['cover_image_path'])
                self.ui.labelCover.setPixmap(pixmap.scaled(200, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.ui.labelCover.setPixmap(QtGui.QPixmap())

            # Отображение комментариев с тайм-кодами
            notes = self.db.get_notes(movie['id'])
            comments_html = ''
            for note in notes:
                comment = self.parse_timecodes(note['comment_text'], movie['link'])
                comments_html += f"<p>{comment}</p>"
            self.ui.textBrowserComments.setHtml(comments_html)
        else:
            self.selected_movie = None
            self.clear_movie_details()

    def clear_movie_details(self):
        self.ui.labelTitle.setText('')
        self.ui.labelGenre.setText('')
        self.ui.labelYear.setText('')
        self.ui.labelDirector.setText('')
        self.ui.labelRating.setText('')
        self.ui.labelStatus.setText('')
        self.ui.labelDateWatched.setText('')
        self.ui.labelCover.setPixmap(QtGui.QPixmap())
        self.ui.textBrowserComments.setHtml('')

    def parse_timecodes(self, text, base_link):
        pattern = r'(\d+:\d{2}:\d{2}|\d+:\d{2})'

        def replace(match):
            time_str = match.group(0)
            seconds = self.time_to_seconds(time_str)
            url = f"{base_link}?t={seconds}s"
            return f'<a href="{url}">{time_str}</a>'

        return re.sub(pattern, replace, text)

    def time_to_seconds(self, time_str):
        parts = list(map(int, time_str.split(':')))
        if len(parts) == 3:
            h, m, s = parts
        else:
            h = 0
            m, s = parts
        return h * 3600 + m * 60 + s

    def add_movie(self):
        dialog = AddEditMovieDialog(self.db)
        if dialog.exec():
            self.load_movies()

    def edit_movie(self):
        if self.selected_movie:
            dialog = AddEditMovieDialog(self.db, movie=self.selected_movie)
            if dialog.exec():
                self.load_movies()

    def delete_movie(self):
        if self.selected_movie:
            reply = QtWidgets.QMessageBox.question(self, 'Удаление фильма',
                                                   f"Вы действительно хотите удалить '{self.selected_movie['title']}'?",
                                                   QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.db.delete_movie(self.selected_movie['id'])
                self.load_movies()
                self.clear_movie_details()

    def import_csv(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Импортировать из CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.db.import_from_csv(file_path)
            self.load_movies()
            QtWidgets.QMessageBox.information(self, 'Импорт завершён', 'Импорт из CSV успешно завершён.')

    def import_sql(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Импортировать из SQL", "",
                                                             "SQLite Files (*.db *.sqlite)")
        if file_path:
            table_name, ok = QtWidgets.QInputDialog.getText(self, 'Импорт из SQL', 'Введите имя таблицы:')
            if ok and table_name:
                self.db.import_from_sql(file_path, table_name=table_name)
                self.load_movies()
                QtWidgets.QMessageBox.information(self, 'Импорт завершён', 'Импорт из SQL успешно завершён.')

    def closeEvent(self, event):
        self.db.close()
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
