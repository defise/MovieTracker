from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QPixmap
from database import get_connection


class MovieCardDialog(QDialog):
    def __init__(self, movie_id, parent=None):
        super().__init__(parent)
        self.movie_id = movie_id
        self.setWindowTitle("Карточка фильма")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout(self)

        # Обложка
        self.cover_label = QLabel("Обложка фильма:")
        self.cover_image_label = QLabel()
        self.cover_image_label.setFixedSize(150, 200)  # Размер для обложки
        self.cover_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Кнопка для загрузки обложки
        self.btn_load_cover = QPushButton("Загрузить обложку")
        self.btn_load_cover.clicked.connect(self.load_cover_image)

        # Комментарии
        self.comment_label = QLabel("Комментарии:")
        self.comment_input = QTextEdit()

        # Ссылка на видео
        self.video_url_label = QLabel("Ссылка на видео (YouTube/Rutube):")
        self.video_url_input = QLineEdit()

        # Кнопка для сохранения изменений
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_movie_data)

        layout.addWidget(self.cover_label)
        layout.addWidget(self.cover_image_label)
        layout.addWidget(self.btn_load_cover)
        layout.addWidget(self.comment_label)
        layout.addWidget(self.comment_input)
        layout.addWidget(self.video_url_label)
        layout.addWidget(self.video_url_input)
        layout.addWidget(self.save_button)

        self.load_movie_data()

    def load_cover_image(self):
        """Загружает изображение обложки."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            self.cover_image_label.setPixmap(
                QPixmap(file_path).scaled(self.cover_image_label.size(), aspectRatioMode=1))
            self.cover_image_path = file_path

    def load_movie_data(self):
        """Загружает данные фильма из базы данных."""
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT title, comment, cover_image, video_url FROM movies WHERE id = ?", (self.movie_id,))
            row = cursor.fetchone()
            connection.close()

            if row:
                title, comment, cover_image, video_url = row
                self.setWindowTitle(f"Карточка фильма: {title}")
                self.comment_input.setText(comment if comment else "")
                self.video_url_input.setText(video_url if video_url else "")

                if cover_image:
                    self.cover_image_label.setPixmap(
                        QPixmap(cover_image).scaled(self.cover_image_label.size(), aspectRatioMode=1))
                    self.cover_image_path = cover_image
                else:
                    self.cover_image_path = None
            else:
                print("Фильм не найден в базе данных.")
        except Exception as e:
            print(f"Ошибка при загрузке данных фильма: {e}")

    def save_movie_data(self):
        """Сохраняет изменения данных фильма."""
        try:
            comment = self.comment_input.toPlainText()
            video_url = self.video_url_input.text()
            cover_image = self.cover_image_path if hasattr(self, 'cover_image_path') else None

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
            UPDATE movies 
            SET comment = ?, video_url = ?, cover_image = ? 
            WHERE id = ?
            """, (comment, video_url, cover_image, self.movie_id))

            connection.commit()
            connection.close()
            self.accept()
        except Exception as e:
            print(f"Ошибка при сохранении данных фильма: {e}")
