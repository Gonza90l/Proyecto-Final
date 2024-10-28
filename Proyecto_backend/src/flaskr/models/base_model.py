import importlib
from flask_mysqldb import MySQL
import json

class BaseModel():
    def __init__(self, mysql: MySQL, table: str, fields: list, deleted_flag: str = None):
        self._mysql = mysql
        self._table = table
        self._fields = fields  # Campos específicos del modelo derivado
        self._data = {}  # Almacenamos los valores de los campos
        self._deleted_flag = deleted_flag  # Campo de bandera de eliminación

    def __getattr__(self, name):
        """Permite acceder a un campo como una propiedad"""
        if name in self._fields:
            return self._data.get(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """Permite establecer un valor en un campo como una propiedad"""
        if name in ['_mysql', '_table', '_fields', '_data', '_deleted_flag']:  # Atributos internos
            super().__setattr__(name, value)
        elif name in self._fields: # Campos permitidos para el modelo 
            self._data[name] = value
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def set(self, **kwargs):
        """Permite establecer múltiples valores de una vez, solo en campos permitidos."""
        for key, value in kwargs.items():
            if key in self._fields:
                self._data[key] = value
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def insert(self):
        """Inserta un nuevo registro en la base de datos usando `self._data`."""
        columns = ', '.join(self._data.keys())
        placeholders = ', '.join(['%s'] * len(self._data))
        query = f"INSERT INTO {self._table} ({columns}) VALUES ({placeholders})"
        cursor = self.execute_query(query, tuple(self._data.values()), return_cursor=True)
        # Obtener el ID del nuevo registro
        new_id = cursor.lastrowid
        cursor.close()  # Cerrar el cursor después de obtener el ID

        #si existe un campo id en el modelo, lo seteamos con el id generado
        if 'id' in self._fields:
            self._data['id'] = new_id
            # Cargar los datos del registro insertado
            self.find_by_id(new_id)

        return new_id

    def update(self):
        """Actualiza el registro en la base de datos usando `self._data`. Requiere que `id` esté en `self._data`."""
        if 'id' not in self._data:
            raise ValueError("El campo 'id' debe estar definido para actualizar un registro.")
        set_clause = ', '.join([f"{key} = %s" for key in self._data.keys()])
        query = f"UPDATE {self._table} SET {set_clause} WHERE id = %s"
        params = tuple(self._data.values()) + (self._data['id'],)
        self.execute_query(query, params)

    def delete(self):
        """Elimina el registro de la base de datos usando el `id` en `self._data`."""
        if 'id' not in self._data:
            raise ValueError("El campo 'id' debe estar definido para eliminar un registro.")
        if self._deleted_flag:
            query = f"UPDATE {self._table} SET {self._deleted_flag} = 1 WHERE id = %s"
        else:
            query = f"DELETE FROM {self._table} WHERE id = %s"
        self.execute_query(query, (self._data['id'],))

    def find_by_id(self, record_id):
        """Encuentra un registro por su `id` y carga los valores en `self._data`."""
        query = f"SELECT * FROM {self._table} WHERE id = %s"
        if self._deleted_flag:
            query += f" AND {self._deleted_flag} = 0"
        result = self.fetch_one(query, (record_id,))
        if result:
            self.set(**result)
        return result

    def find_all(self):
        """Recupera todos los registros de la tabla y los convierte en instancias del modelo."""
        query = f"SELECT * FROM {self._table}"
        if self._deleted_flag:
            query += f" WHERE {self._deleted_flag} = 0"
        results = self.fetch_all(query)
        
        # Convertir cada resultado en una instancia del modelo actual
        model_instances = []
        for result in results:
            instance = self.__class__(self._mysql, self._table, self._fields, self._deleted_flag)  # Crear una instancia del modelo
            instance.set(**result)  # Cargar los datos en la instancia
            model_instances.append(instance)
        
        return model_instances

    # Métodos de utilidad para consultas SQL
    def execute_query(self, query, params=None, return_cursor=False):
        cursor = self._mysql.connection.cursor()
        cursor.execute(query, params)
        self._mysql.connection.commit()
        if return_cursor:
            return cursor
        cursor.close()

    def fetch_one(self, query, params=None):
        cursor = self._mysql.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query, params=None):
        cursor = self._mysql.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    def __str__(self):
        return str(self._data)

    # Método para convertir el objeto a un DTO y serializarlo a JSON
    # Requiere que exista un módulo DTO correspondiente en el directorio dtos
    # Usamos  reflection para importar dinámicamente el módulo DTO correspondiente
    def to_json_dto(self):
        dto_class_name = f"{self.__class__.__name__}DTO"
        try:
            # Importar dinámicamente el módulo DTO correspondiente
            dto_module = importlib.import_module(f"flaskr.dtos.{self.__class__.__name__.lower()}_dto")
            # Obtener la clase DTO
            dto_class = getattr(dto_module, dto_class_name)
            # Crear una instancia del DTO
            dto_instance = dto_class()
            # Copiar los atributos del modelo al DTO
            for field in self._fields:
                if hasattr(dto_instance, field):
                    setattr(dto_instance, field, self._data.get(field))
            # Serializar el DTO a JSON
            return json.dumps(dto_instance.__dict__)
        except (ModuleNotFoundError, AttributeError) as e:
            raise ImportError(f"DTO class '{dto_class_name}' not found for model '{self.__class__.__name__}'") from e

    def from_dto(self, dto):
        """Convierte un DTO a un modelo."""
        try:
            for key, value in dto.__dict__.items():
                if key in self._fields:
                    self._data[key] = value
                else:
                    raise AttributeError(f"DTO has no attribute '{key}'")
        except Exception as e:
            raise ValueError("Invalid DTO format") from e

    def from_dict(self, data):
        """Convierte un diccionario a un modelo."""
        for key, value in data.items():
            if key in self._fields:
                self._data[key] = value
            else:
                raise AttributeError(f"Dictionary has no attribute '{key}'")