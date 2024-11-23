from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QLabel
from PyQt6.QtCore import Qt


class Ui_MainWindow:
    def setup_ui(self, MainWindow):
        """Настраивает интерфейс окна."""
        MainWindow.setWindowTitle("MovieTracker")
        MainWindow.setFixedSize(900, 600)

        # Центровой виджет
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.layout = QVBoxLayout(self.centralwidget)

        # Верхняя панель
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск фильмов...")
        self.btn_add = QPushButton("Добавить фильм")
        self.btn_import = QPushButton("Импорт из SQL")
        self.btn_refresh = QPushButton("Обновить")

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.search_input)
        top_layout.addWidget(self.btn_add)
        top_layout.addWidget(self.btn_import)
        top_layout.addWidget(self.btn_refresh)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Название", "Жанр", "Год", "Рейтинг", "Статус"])
        self.table.horizontalHeader().setStretchLastSection(True)

        # Кнопка для открытия карточки
        self.btn_open_card = QPushButton("Открыть карточку фильма")

        # Основной макет
        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btn_open_card)
