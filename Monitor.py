import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel, QDateEdit,
                             QMessageBox)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor

# Установка переменной окружения для платформы
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\astel\Desktop\Питон\hotel\.venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms'

class ChessBoardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Шахматка для бронирования комнат")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        # Календарь для выбора дат
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("dd.MM.yyyy")

        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setDate(QDate.currentDate().addDays(1))
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("dd.MM.yyyy")

        self.book_button = QPushButton("Забронировать", self)
        self.book_button.clicked.connect(self.book_room)

        self.cancel_button = QPushButton("Отменить бронирование", self)
        self.cancel_button.clicked.connect(self.cancel_booking)

        self.layout.addWidget(QLabel("Дата начала:"))
        self.layout.addWidget(self.start_date_edit)
        self.layout.addWidget(QLabel("Дата окончания:"))
        self.layout.addWidget(self.end_date_edit)
        self.layout.addWidget(self.book_button)
        self.layout.addWidget(self.cancel_button)

        # Таблица для отображения комнат
        self.table = QTableWidget(20, 30, self)  # 20 комнат и 30 дней (пример)
        self.table.setHorizontalHeaderLabels([f"День {i + 1}" for i in range(30)])  # 30 дней
        self.table.setVerticalHeaderLabels([f"Комната {i + 1}" for i in range(20)])  # 20 комнат

        # Устанавливаем размеры ячеек
        for i in range(30):
            self.table.setColumnWidth(i, 50)  # Установим ширину всех столбцов

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.init_table()

        # Список выбранных комнат
        self.selected_rooms = []

        # Подключаем обработчик щелчка по ячейкам
        self.table.cellClicked.connect(self.select_room)

    def init_table(self):
        # Инициализация таблицы значениями по умолчанию
        for i in range(20):  # 20 комнат
            for j in range(30):  # 30 дней
                item = QTableWidgetItem("Свободна")
                item.setBackground(QColor(173, 216, 230))  # Цвет для свободных комнат
                self.table.setItem(i, j, item)

    def select_room(self, row, column):
        """Обработчик выбора комнаты."""
        item = self.table.item(row, column)
        if item:
            if item.text() == "Свободна":
                # Если ячейка свободна, добавляем её в выбранные
                if row not in self.selected_rooms:
                    self.selected_rooms.append(row)
            elif item.text() == "Забронирована":
                QMessageBox.warning(self, "Ошибка", f"Комната {row + 1} уже забронирована!")

    def book_room(self):
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()

        if start_date >= end_date:
            QMessageBox.warning(self, "Ошибка", "Дата окончания должна быть позже даты начала.")
            return

        start_day = start_date.day() - 1
        end_day = end_date.day() - 1

        if not self.selected_rooms:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите номера для бронирования.")
            return

        # Проверяем и окрашиваем выбранные номера
        for room in self.selected_rooms:
            for j in range(start_day, end_day + 1):
                item = self.table.item(room, j)
                if item and item.text() == "Забронирована":
                    QMessageBox.warning(self, "Ошибка", f"Номер {room + 1} уже забронирован в день {j + 1}.")
                    return

        # Если все номера свободны, забронируем их
        for room in self.selected_rooms:
            for j in range(start_day, end_day + 1):
                item = self.table.item(room, j)
                item.setText("Забронирована")
                item.setBackground(QColor(255, 99, 71))  # Цвет для забронированных номеров

        QMessageBox.information(self, "Успех", "Номера успешно забронированы!")
        self.selected_rooms.clear()  # Очищаем список выбранных номеров

    def cancel_booking(self):
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()

        if start_date >= end_date:
            QMessageBox.warning(self, "Ошибка", "Дата окончания должна быть позже даты начала.")
            return

        start_day = start_date.day() - 1
        end_day = end_date.day() - 1

        if not self.selected_rooms:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите номера для отмены бронирования.")
            return

        # Проверяем и отменяем выбранные номера
        for room in self.selected_rooms:
            for j in range(start_day, end_day + 1):
                item = self.table.item(room, j)
                if item and item.text() == "Забронирована":
                    item.setText("Свободна")
                    item.setBackground(QColor(173, 216, 230))  # Возвращаем цвет свободной комнаты
                else:
                    QMessageBox.warning(self, "Ошибка", f"Номер {room + 1} не забронирован в день {j + 1}.")
                    return

        QMessageBox.information(self, "Успех", "Бронирование успешно отменено!")
        self.selected_rooms.clear()  # Очищаем список выбранных номеров


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessBoardApp()
    window.show()
    sys.exit(app.exec_())
