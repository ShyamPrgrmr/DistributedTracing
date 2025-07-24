from mysql.connector import Error # type: ignore
import mysql.connector  # type: ignore




class MysqlService:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def get_data(self, query, params=None):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        if self.connection is None:
            return None
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()