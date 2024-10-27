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

    def insert(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))

    def update(self, table, data, where_clause, where_params):
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        self.execute_query(query, tuple(data.values()) + tuple(where_params))

    def delete(self, table, where_clause, where_params):
        query = f"DELETE FROM {table} WHERE {where_clause}"
        self.execute_query(query, where_params)

    def find_by_id(self, table, id):
        query = f"SELECT * FROM {table} WHERE id = %s"
        return self.fetch_one(query, (id,))

    def find_all(self, table):
        query = f"SELECT * FROM {table}"
        return self.fetch_all(query)