class BaseDTO:
    def __init__(self, **kwargs):
        """Constructor inicial que permite asignar campos opcionales sin requerir argumentos posicionales."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_required_fields(self):
        """Debe ser implementado por las clases hijas para especificar los campos requeridos y sus tipos."""
        raise NotImplementedError("Subclasses must implement get_required_fields method")

    def get_field_constraints(self):
        """Debe ser implementado por las clases hijas para especificar restricciones adicionales."""
        return {}

    @classmethod
    def from_json(cls, json_data):
        """Construye un DTO desde un diccionario JSON de forma segura."""
        if not isinstance(json_data, dict):
            return None, {"json_error": "Invalid JSON format"}

        errors = {}
        validated_data = {}
        required_fields = cls().get_required_fields()
        field_constraints = cls().get_field_constraints()

        # Verificar que solo los campos definidos en required_fields estén presentes
        for field in json_data.keys():
            if field not in required_fields:
                errors[field] = f"Field {field} is not allowed"

        # Validación de campos requeridos y tipos
        for field, field_type in required_fields.items():
            value = json_data.get(field, None)
            if value is None:
                errors[field] = f"Missing required field: {field}"
            elif not isinstance(value, field_type):
                errors[field] = f"Field {field} must be of type {field_type.__name__}"
            else:
                validated_data[field] = value  # Solo guardamos campos válidos

        # Validación de restricciones adicionales
        for field, constraints in field_constraints.items():
            value = validated_data.get(field)
            if value is not None:  # Solo valida si el campo fue validado previamente
                if 'min' in constraints and value < constraints['min']:
                    errors[field] = f"Field {field} must be greater than {constraints['min']}"
                if 'max' in constraints and value > constraints['max']:
                    errors[field] = f"Field {field} must be less than {constraints['max']}"
                # Otros constraints según sea necesario

        if errors:
            return None, errors

        # Asignación de los datos validados a la instancia
        instance = cls(**validated_data)
        return instance, None  # Sin errores, devuelve instancia y None