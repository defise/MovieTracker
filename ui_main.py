from PyQt6 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        # Создание центрального виджета
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Список фильмов
        self.listWidgetMovies = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetMovies.setGeometry(QtCore.QRect(10, 10, 200, 540))
        self.listWidgetMovies.setObjectName("listWidgetMovies")
        # Поле поиска
        self.lineEditSearch = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditSearch.setGeometry(QtCore.QRect(10, 560, 200, 30))
        self.lineEditSearch.setObjectName("lineEditSearch")
        # Кнопки управления
        self.btnAddMovie = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddMovie.setGeometry(QtCore.QRect(220, 10, 100, 30))
        self.btnAddMovie.setObjectName("btnAddMovie")
        self.btnEditMovie = QtWidgets.QPushButton(self.centralwidget)
        self.btnEditMovie.setGeometry(QtCore.QRect(330, 10, 100, 30))
        self.btnEditMovie.setObjectName("btnEditMovie")
        self.btnDeleteMovie = QtWidgets.QPushButton(self.centralwidget)
        self.btnDeleteMovie.setGeometry(QtCore.QRect(440, 10, 100, 30))
        self.btnDeleteMovie.setObjectName("btnDeleteMovie")
        self.btnImportCSV = QtWidgets.QPushButton(self.centralwidget)
        self.btnImportCSV.setGeometry(QtCore.QRect(550, 10, 100, 30))
        self.btnImportCSV.setObjectName("btnImportCSV")
        self.btnImportSQL = QtWidgets.QPushButton(self.centralwidget)
        self.btnImportSQL.setGeometry(QtCore.QRect(660, 10, 100, 30))
        self.btnImportSQL.setObjectName("btnImportSQL")
        # Отображение деталей фильма
        self.labelCover = QtWidgets.QLabel(self.centralwidget)
        self.labelCover.setGeometry(QtCore.QRect(220, 50, 200, 300))
        self.labelCover.setObjectName("labelCover")
        self.labelTitle = QtWidgets.QLabel(self.centralwidget)
        self.labelTitle.setGeometry(QtCore.QRect(430, 50, 350, 30))
        self.labelTitle.setObjectName("labelTitle")
        self.labelGenre = QtWidgets.QLabel(self.centralwidget)
        self.labelGenre.setGeometry(QtCore.QRect(430, 90, 350, 30))
        self.labelGenre.setObjectName("labelGenre")
        self.labelYear = QtWidgets.QLabel(self.centralwidget)
        self.labelYear.setGeometry(QtCore.QRect(430, 130, 350, 30))
        self.labelYear.setObjectName("labelYear")
        self.labelDirector = QtWidgets.QLabel(self.centralwidget)
        self.labelDirector.setGeometry(QtCore.QRect(430, 170, 350, 30))
        self.labelDirector.setObjectName("labelDirector")
        self.labelRating = QtWidgets.QLabel(self.centralwidget)
        self.labelRating.setGeometry(QtCore.QRect(430, 210, 350, 30))
        self.labelRating.setObjectName("labelRating")
        self.labelStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelStatus.setGeometry(QtCore.QRect(430, 250, 350, 30))
        self.labelStatus.setObjectName("labelStatus")
        self.labelDateWatched = QtWidgets.QLabel(self.centralwidget)
        self.labelDateWatched.setGeometry(QtCore.QRect(430, 290, 350, 30))
        self.labelDateWatched.setObjectName("labelDateWatched")
        # Текстовое поле для комментариев
        self.textBrowserComments = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserComments.setGeometry(QtCore.QRect(220, 360, 560, 230))
        self.textBrowserComments.setObjectName("textBrowserComments")
        # Установка центрального виджета
        MainWindow.setCentralWidget(self.centralwidget)
        # Перевод UI
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MovieTracker"))
        self.btnAddMovie.setText(_translate("MainWindow", "Добавить"))
        self.btnEditMovie.setText(_translate("MainWindow", "Редактировать"))
        self.btnDeleteMovie.setText(_translate("MainWindow", "Удалить"))
        self.btnImportCSV.setText(_translate("MainWindow", "Импорт CSV"))
        self.btnImportSQL.setText(_translate("MainWindow", "Импорт SQL"))
