import mysql.connector

class DatabaseModel:
    def __init__(self, db_config):
        """Подключение к базе данных, входные данные для которой указаны в переменной db_config"""
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor(dictionary=True)

    def fetch_airports(self, min_lat, max_lat, min_lon, max_lon):
        """Метод принимает аргументы min_lat и max_lat, которые указываются
        пользователем как минимальная и максимальная широта, а также min_lon и max_lon
        которые указываются пользователем как минимальная и максимальная долгота.
        Переменная query содержит запрос, в соответствии с которым выюираются столбцы из базы данных
        city, country, latitude, longitude из таблицы airports, где значение latitude находится между
        min_lat и max_lat, а значение longitude находится между min_lon и max_lon
        self.cursor.execute(query, (min_lat, max_lat, min_lon, max_lon)) выполняет запрос к базе данных
        return self.cursor.fetchall() возвращает результат запроса"""
        query = """
        SELECT city, country, latitude, longitude FROM airports
        WHERE latitude BETWEEN %s AND %s AND longitude BETWEEN %s AND %s
        """
        self.cursor.execute(query, (min_lat, max_lat, min_lon, max_lon))
        return self.cursor.fetchall()

    def fetch_routes_from_city(self, city):
        """Метод позволяет получить информацию о всех маршрутах, вылетающих из переданного города,
        которая возвращает аиропорт отправления, аиропорт назначения и авиакомпанию.
        Метод принимает аргумент city, который является городов из которого осуществляется вылет.
        В query содержится запрос для выбора начального и конечного аэропортов, а также авиакомпании.
        self.cursor.execute(query, (city,)) выполняет запрос, передавая city в качестве параметра
        return self.cursor.fetchall() возвращает результат запроса"""
        query = """
        SELECT r.src_airport, r.dst_airport, a.name AS airline
        FROM routes r
        INNER JOIN airlines a ON r.airline_id = a.id
        INNER JOIN airports ap ON r.src_airport_id = ap.id
        WHERE ap.city = %s
        """
        self.cursor.execute(query, (city,))
        return self.cursor.fetchall()

    def fetch_routes_between_cities(self, origin_city, destination_city):
        """Метод позволяет получить информацию о маршрутах между двумя городами.
        origin_city - город отправления, destination_city - город назначения
        Запрос, указанный в переменной query, выбирает город отправления, город назначения и авиакомпанию
        совершающую перелёт.
        self.cursor.execute(query, (origin_city, destination_city)) выполняет запрос к базе данных
        return self.cursor.fetchall() возвращает результат запроса"""
        query = """
        SELECT r.src_airport, r.dst_airport, a.name AS airline
        FROM routes r
        INNER JOIN airlines a ON r.airline_id = a.id
        INNER JOIN airports ap1 ON r.src_airport_id = ap1.id
        INNER JOIN airports ap2 ON r.dst_airport_id = ap2.id
        WHERE ap1.city = %s AND ap2.city = %s
        """
        self.cursor.execute(query, (origin_city, destination_city))
        return self.cursor.fetchall()

    def __del__(self):
        """Метод закрывает соединение с базой данных."""
        self.conn.close()