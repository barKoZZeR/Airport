from PyQt5 import QtWidgets

class AirportFilterView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Создаём заголовок окна программы
        self.setWindowTitle('Airport Filter')
        self.layout = QtWidgets.QGridLayout(self)

        # Создание интерфейса
        self.min_lat = QtWidgets.QLineEdit(self)
        self.max_lat = QtWidgets.QLineEdit(self)
        self.min_lon = QtWidgets.QLineEdit(self)
        self.max_lon = QtWidgets.QLineEdit(self)
        self.filter_button = QtWidgets.QPushButton('Apply Filter', self)
        self.table = QtWidgets.QTableWidget(self)
        self.origin_city = QtWidgets.QLineEdit(self)
        self.destination_city = QtWidgets.QLineEdit(self)
        self.fetch_routes_button = QtWidgets.QPushButton('Fetch Routes', self)

        # Настройка таблицы - для отображение четырех столбцов
        # с названиями City, Country, latitude и Longitude
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['City', 'Country', 'Latitude', 'Longitude'])

        # Размещение полей для ввода, кнопок и таблицы в определённых местах
        self.layout.addWidget(QtWidgets.QLabel('Min Latitude:'), 0, 0)
        self.layout.addWidget(self.min_lat, 0, 1)
        self.layout.addWidget(QtWidgets.QLabel('Max Latitude:'), 1, 0)
        self.layout.addWidget(self.max_lat, 1, 1)
        self.layout.addWidget(QtWidgets.QLabel('Min Longitude:'), 2, 0)
        self.layout.addWidget(self.min_lon, 2, 1)
        self.layout.addWidget(QtWidgets.QLabel('Max Longitude:'), 3, 0)
        self.layout.addWidget(self.max_lon, 3, 1)
        self.layout.addWidget(self.filter_button, 4, 0, 1, 2)
        self.layout.addWidget(self.table, 5, 0, 1, 2)
        self.layout.addWidget(QtWidgets.QLabel('Origin City:'), 6, 0)
        self.layout.addWidget(self.origin_city, 6, 1)
        self.layout.addWidget(QtWidgets.QLabel('Destination City:'), 7, 0)
        self.layout.addWidget(self.destination_city, 7, 1)
        self.layout.addWidget(self.fetch_routes_button, 8, 0, 1, 2)

        #Установка размеров окна приложения
        self.setFixedSize(750, 400)
