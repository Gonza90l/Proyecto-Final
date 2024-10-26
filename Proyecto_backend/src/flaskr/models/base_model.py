from flask_mysqldb import MySQL

class BaseModel:
    def __init__(self, mysql: MySQL):
        self.mysql = mysql

    def execute_query(self, query, params=None):
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, params)
        self.mysql.connection.commit()
        cursor.close()

    def fetch_one(self, query, params=None):
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query, params=None):
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result