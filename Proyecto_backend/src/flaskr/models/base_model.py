class BaseModel:
    def __init__(self, mysql, table, fields):
        self.mysql = mysql
        self.table = table
        self.fields = fields  # Campos específicos del modelo derivado
        self.data = {}  # Almacena los valores de los campos

    def __getattr__(self, name):
        """Permite acceder a un campo como una propiedad"""
        if name in self.fields:
            return self.data.get(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """Permite establecer un valor en un campo como una propiedad"""
        if name in ['mysql', 'table', 'fields', 'data']:  # Atributos internos
            super().__setattr__(name, value)
        elif name in self.fields:
            self.data[name] = value
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def set(self, **kwargs):
        """Permite establecer múltiples valores de una vez, solo en campos permitidos."""
        for key, value in kwargs.items():
            if key in self.fields:
                self.data[key] = value
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def insert(self):
        """Inserta un nuevo registro en la base de datos usando `self.data`."""
        columns = ', '.join(self.data.keys())
        placeholders = ', '.join(['%s'] * len(self.data))
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(self.data.values()))

    def update(self):
        """Actualiza el registro en la base de datos usando `self.data`. Requiere que `id` esté en `self.data`."""
        if 'id' not in self.data:
            raise ValueError("El campo 'id' debe estar definido para actualizar un registro.")
        set_clause = ', '.join([f"{key} = %s" for key in self.data.keys()])
        query = f"UPDATE {self.table} SET {set_clause} WHERE id = %s"
        params = tuple(self.data.values()) + (self.data['id'],)
        self.execute_query(query, params)

    def delete(self):
        """Elimina el registro de la base de datos usando el `id` en `self.data`."""
        if 'id' not in self.data:
            raise ValueError("El campo 'id' debe estar definido para eliminar un registro.")
        query = f"DELETE FROM {self.table} WHERE id = %s"
        self.execute_query(query, (self.data['id'],))

    def find_by_id(self, record_id):
        """Encuentra un registro por su `id` y carga los valores en `self.data`."""
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self.fetch_one(query, (record_id,))
        if result:
            self.set(**result)
        return result

    def find_all(self):
        """Recupera todos los registros de la tabla."""
        query = f"SELECT * FROM {self.table}"
        return self.fetch_all(query)

    # Métodos de utilidad para consultas SQL
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
