from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from model import DatabaseModel
from view import AirportFilterView
import sys


class AirportController:
    def __init__(self, view, model):
        """С помощью self._view.filter_button.clicked.connect(self.apply_filter) и
        self._view.fetch_routes_button.clicked.connect(self.fetch_routes) связываются методы apply_filter и fetch_routes
        с кнопками действия в программе"""
        self._view = view
        self._model = model
        self._view.filter_button.clicked.connect(self.apply_filter)
        self._view.fetch_routes_button.clicked.connect(self.fetch_routes)

    def apply_filter(self):
        """Значение координат, которые передаёт пользователь, переводятся в float, если он ввёл целые числа.
        Введённые пользователем данные обрабатываются и в случае, если он ввёл не числовое значение, то
        он получит окно предупреждения с просьбой ввести числовое значение"""
        try:
            min_lat = float(self._view.min_lat.text())
            max_lat = float(self._view.max_lat.text())
            min_lon = float(self._view.min_lon.text())
            max_lon = float(self._view.max_lon.text())
        except ValueError:
            QMessageBox.warning(self._view, 'Input Error', 'Please enter the numeric values')
            return
        airports = self._model.fetch_airports(min_lat, max_lat, min_lon, max_lon)

        # Таблица очищается перед добавлением новых данных
        self._view.table.setRowCount(0)

        # В цикле, из полученных данных создаётся новая строка в таблице и в неё добавляются
        # значения из словаря аэропорта
        for airport in airports:
            row_position = self._view.table.rowCount()
            self._view.table.insertRow(row_position)
            for column, value in enumerate(airport.values()):
                self._view.table.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(value)))
                self._view.table.setColumnWidth(column, 160)


    def fetch_routes(self):
        """С помощью этого метода извлекается текст, введённый пользователем.
        Далее метод проверяет, если были введены два города (отправления и назначения),
        то запрашивается маршруты между введёнными городами, а если был введён только
        один город, то запрашиваются все маршруты из этого города или в него"""
        origin_city = self._view.origin_city.text()
        destination_city = self._view.destination_city.text()
        if origin_city and destination_city:
            # Если указаны оба города, ищем рейсы между городами
            routes = self._model.fetch_routes_between_cities(origin_city, destination_city)
        else:
            # Если указан только один город, ищем рейсы из этого города и в этот город
            routes = self._model.fetch_routes_from_city(origin_city or destination_city)

        # Обновляет таблицы в интерфейсе
        self.update_routes_table(routes)

    def update_routes_table(self, routes):
        """Данный метод отвечает за обновление таблицы в интерфейсе"""

        # Удаляет все текущие данные из таблицы, чтобы потом заполнить её новыми данными
        self._view.table.clear()

        # Настраивает количество столбцов таблицы для трёх элементов - аэропорт отправления, аэропорт назначения и авикопмания
        self._view.table.setColumnCount(3)

        # Настраивает заголовки столбцов (названия)
        self._view.table.setHorizontalHeaderLabels(['Source Airport', 'Destination Airport', 'Airline'])

        # Настраивает количество строк, чтобы они были равны количеству маршрутов в списке routes
        self._view.table.setRowCount(len(routes))

        # Установил ширину на 160, чтобы названия авиакомпаний не обрывались троеточием
        for i, route in enumerate(routes):
            self._view.table.setItem(i, 0, QtWidgets.QTableWidgetItem(route['src_airport']))
            self._view.table.setColumnWidth(i, 160)
            self._view.table.setItem(i, 1, QtWidgets.QTableWidgetItem(route['dst_airport']))
            self._view.table.setColumnWidth(i, 160)
            self._view.table.setItem(i, 2, QtWidgets.QTableWidgetItem(route['airline']))
            self._view.table.setColumnWidth(i, 160)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    db_config = {
        'user': 'root',
        'password': 'Password2057',
        'host': 'localhost',
        'database': 'flights'
    }
    model = DatabaseModel(db_config)
    view = AirportFilterView()
    controller = AirportController(view, model)
    view.show()
    sys.exit(app.exec_())