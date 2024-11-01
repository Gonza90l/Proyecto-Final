import importlib
from flask_mysqldb import MySQL
import json
from decimal import Decimal
from flask_injector import inject
from flaskr.database.database_interface import IDatabase

class BaseModel():
    _deleted_flag = None  # definimos en NONE para que no se aplique en los modelos que no lo requieran
    _relationships = {}  # Define relationships in subclasses

    @inject
    def __init__(self, mysql: IDatabase, **kwargs):
        self._mysql = mysql
        self._table = self._table  # Debe ser definido en la subclase
        self._fields = self._fields  # Debe ser definido en la subclase
        self._data = kwargs  # Almacenamos los valores de los campos
        self._deleted_flag = getattr(self, '_deleted_flag', None)  # Campo de bandera de eliminación
        self._related_data = {}  # Store related data

    def __getattr__(self, name):
        """Permite acceder a un campo como una propiedad"""
        if name in self._fields:
            return self._data.get(name)
        if name in self._relationships:
            return self._related_data.get(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """Permite establecer un valor en un campo como una propiedad"""
        if name in ['_mysql', '_table', '_fields', '_data', '_deleted_flag', '_related_data', '_relationships']:  # Atributos internos
            super().__setattr__(name, value)
        elif name in self._fields:  # Campos permitidos para el modelo 
            self._data[name] = value
        elif name in self._relationships:
            self._related_data[name] = value
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def set(self, **kwargs):
        """Permite establecer múltiples valores de una vez, solo en campos permitidos."""
        for key, value in kwargs.items():
            if key in self._fields:
                self._data[key] = value
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    @classmethod
    def find_by_id(cls, mysql, record_id):
        """Encuentra un registro por su `id` y devuelve una instancia del modelo."""
        query = f"SELECT * FROM {cls._table} WHERE id = %s"
        if cls._deleted_flag:
            query += f" AND {cls._deleted_flag} = 0"
        result = cls.fetch_one(mysql, query, (record_id,))
        if result:
            instance = cls(mysql, **result)
            instance.load_related_data()
            return instance
        return None

    @classmethod
    def find_all(cls, mysql: IDatabase):
        """Retrieve all records from the table and convert them into model instances."""
        query = f"SELECT * FROM {cls._table}"
        if cls._deleted_flag:
            query += f" WHERE {cls._deleted_flag} = 0"
        results = cls.fetch_all(mysql, query)
        
        # Convert each result into an instance of the current model
        instances = [cls(mysql, **result) for result in results]
        for instance in instances:
            instance.load_related_data()
        return instances

    def insert(self):
        """Inserta un nuevo registro en la base de datos usando `self._data`."""
        columns = ', '.join(self._data.keys())
        placeholders = ', '.join(['%s'] * len(self._data))
        print(self._data)
        query = f"INSERT INTO {self._table} ({columns}) VALUES ({placeholders})"
        cursor = self.execute_query(self._mysql, query, tuple(self._data.values()), return_cursor=True)
        # Obtener el ID del nuevo registro
        new_id = cursor.lastrowid
        cursor.close()  # Cerrar el cursor después de obtener el ID

        # Si existe un campo id en el modelo, lo seteamos con el id generado
        if 'id' in self._fields:
            self._data['id'] = new_id
            # Cargar los datos del registro insertado
            self.find_by_id(self._mysql, new_id)

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

    @staticmethod
    def execute_query(mysql, query, params=None, return_cursor=False):
        cursor = mysql.connection.cursor()
        cursor.execute(query, params)
        mysql.connection.commit()
        if return_cursor:
            return cursor
        cursor.close()

    @staticmethod
    def fetch_one(mysql, query, params=None):
        cursor = mysql.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    @staticmethod
    def fetch_all(mysql, query, params=None):
        cursor = mysql.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    def __str__(self):
        return str(self._data)

    # Método para convertir el objeto a un DTO y convertirlo a diccionario
    # Requiere que exista un módulo DTO correspondiente en el directorio dtos
    # Usamos reflexión para importar dinámicamente el módulo DTO correspondiente
    def to_dict_dto(self):
        def serialize_instance(instance):
            dto_class_name = f"{instance.__class__.__name__}DTO"
            try:
                # Importar dinámicamente el módulo DTO correspondiente
                module_name = f"flaskr.dtos.{self._to_snake_case(instance.__class__.__name__)}_dto"
                dto_module = importlib.import_module(module_name)
                # Obtener la clase DTO
                dto_class = getattr(dto_module, dto_class_name)
                # Crear una instancia del DTO
                dto_instance = dto_class()
                # Copiar los atributos del modelo al DTO
                for field in instance._fields:
                    if hasattr(dto_instance, field):
                        value = instance._data.get(field)
                        if isinstance(value, Decimal):
                            value = str(value)
                        setattr(dto_instance, field, value)
                # Convertir el DTO a diccionario
                dto_dict = dto_instance.__dict__
                # Serializar datos relacionados
                for relation, related_instances in instance._related_data.items():
                    if isinstance(related_instances, list):
                        dto_dict[relation] = [serialize_instance(related_instance) for related_instance in related_instances]
                    else:
                        dto_dict[relation] = serialize_instance(related_instances)
                return dto_dict
            except (ModuleNotFoundError, AttributeError) as e:
                raise ImportError(f"DTO class '{dto_class_name}' not found for model '{instance.__class__.__name__}'") from e

        if isinstance(self, list):
            return [serialize_instance(instance) for instance in self]
        else:
            return serialize_instance(self)

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

    def load_related_data(self):
        """Load related data for the model instance."""
        for relation, details in self._relationships.items():
            related_class_name = details['class']
            foreign_key = details['foreign_key']
            
            # Convert class name to snake_case to match the file name
            module_name = f"flaskr.models.{self._to_snake_case(related_class_name)}"
            related_class = getattr(importlib.import_module(module_name), related_class_name)
            
            related_instances = related_class.find_all_by_foreign_key(self._mysql, foreign_key, self._data['id'])
            self._related_data[relation] = related_instances

    @classmethod
    def find_all_by_foreign_key(cls, mysql, foreign_key, value):
        """Find all records by foreign key."""
        query = f"SELECT * FROM {cls._table} WHERE {foreign_key} = %s"
        results = cls.fetch_all(mysql, query, (value,))
        return [cls(mysql, **result) for result in results]

    def _to_snake_case(self, name):
        """Convert CamelCase to snake_case."""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()