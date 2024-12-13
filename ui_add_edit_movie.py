from PyQt6 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 600)
        # Поля ввода
        self.lineEditTitle = QtWidgets.QLineEdit(Dialog)
        self.lineEditTitle.setGeometry(QtCore.QRect(20, 20, 360, 30))
        self.lineEditTitle.setObjectName("lineEditTitle")
        self.lineEditGenre = QtWidgets.QLineEdit(Dialog)
        self.lineEditGenre.setGeometry(QtCore.QRect(20, 70, 360, 30))
        self.lineEditGenre.setObjectName("lineEditGenre")
        self.spinBoxYear = QtWidgets.QSpinBox(Dialog)
        self.spinBoxYear.setGeometry(QtCore.QRect(20, 120, 360, 30))
        self.spinBoxYear.setRange(1900, 2100)
        self.spinBoxYear.setObjectName("spinBoxYear")
        self.lineEditDirector = QtWidgets.QLineEdit(Dialog)
        self.lineEditDirector.setGeometry(QtCore.QRect(20, 170, 360, 30))
        self.lineEditDirector.setObjectName("lineEditDirector")
        # Оценка
        self.spinBoxRating = QtWidgets.QSpinBox(Dialog)
        self.spinBoxRating.setGeometry(QtCore.QRect(20, 220, 360, 30))
        self.spinBoxRating.setRange(0, 10)
        self.spinBoxRating.setObjectName("spinBoxRating")
        # Статус просмотра
        self.comboBoxStatus = QtWidgets.QComboBox(Dialog)
        self.comboBoxStatus.setGeometry(QtCore.QRect(20, 270, 360, 30))
        self.comboBoxStatus.addItems(["в планах", "смотрю", "посмотрел", "брошено"])
        self.comboBoxStatus.setObjectName("comboBoxStatus")
        # Дата просмотра
        self.dateEditWatched = QtWidgets.QDateEdit(Dialog)
        self.dateEditWatched.setGeometry(QtCore.QRect(20, 320, 360, 30))
        self.dateEditWatched.setCalendarPopup(True)
        self.dateEditWatched.setDate(QtCore.QDate.currentDate())
        self.dateEditWatched.setObjectName("dateEditWatched")
        # Обложка фильма
        self.labelCover = QtWidgets.QLabel(Dialog)
        self.labelCover.setGeometry(QtCore.QRect(20, 370, 150, 200))
        self.labelCover.setObjectName("labelCover")
        self.btnChooseCover = QtWidgets.QPushButton(Dialog)
        self.btnChooseCover.setGeometry(QtCore.QRect(190, 370, 190, 30))
        self.btnChooseCover.setObjectName("btnChooseCover")
        # Ссылка на видеохостинг
        self.lineEditLink = QtWidgets.QLineEdit(Dialog)
        self.lineEditLink.setGeometry(QtCore.QRect(20, 580, 360, 30))
        self.lineEditLink.setObjectName("lineEditLink")
        # Комментарии
        self.textEditComments = QtWidgets.QTextEdit(Dialog)
        self.textEditComments.setGeometry(QtCore.QRect(20, 420, 360, 150))
        self.textEditComments.setObjectName("textEditComments")
        # Кнопки сохранения и отмены
        self.btnSave = QtWidgets.QPushButton(Dialog)
        self.btnSave.setGeometry(QtCore.QRect(220, 620, 75, 30))
        self.btnSave.setObjectName("btnSave")
        self.btnCancel = QtWidgets.QPushButton(Dialog)
        self.btnCancel.setGeometry(QtCore.QRect(305, 620, 75, 30))
        self.btnCancel.setObjectName("btnCancel")
        # Перевод UI
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Добавить/Редактировать фильм"))
        self.btnChooseCover.setText(_translate("Dialog", "Выбрать обложку"))
        self.btnSave.setText(_translate("Dialog", "Сохранить"))
        self.btnCancel.setText(_translate("Dialog", "Отмена"))
