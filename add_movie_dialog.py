from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class AddMovieDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить фильм")
        self.setFixedSize(400, 300)

        self.layout = QVBoxLayout(self)

        # Поля ввода
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название фильма")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Жанр")
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год")
        self.rating_input = QLineEdit()
        self.rating_input.setPlaceholderText("Рейтинг (0-10)")
        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Статус")

        self.layout.addWidget(QLabel("Название:"))
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(QLabel("Жанр:"))
        self.layout.addWidget(self.genre_input)
        self.layout.addWidget(QLabel("Год:"))
        self.layout.addWidget(self.year_input)
        self.layout.addWidget(QLabel("Рейтинг:"))
        self.layout.addWidget(self.rating_input)
        self.layout.addWidget(QLabel("Статус:"))
        self.layout.addWidget(self.status_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.btn_save = QPushButton("Сохранить")
        self.btn_cancel = QPushButton("Отмена")
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)

        self.layout.addLayout(button_layout)

        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_movie_data(self):
        """Возвращает данные из полей ввода."""
        return {
            "title": self.title_input.text(),
            "genre": self.genre_input.text(),
            "year": self.year_input.text(),
            "rating": self.rating_input.text(),
            "status": self.status_input.text()
        }
