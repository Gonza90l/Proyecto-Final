# dtos/base_dto.py
class BaseDTO:
    def validate(self):
        """Valida que el DTO tenga los campos requeridos y sean del tipo especificado."""
        errors = []
        required_fields = self.get_required_fields()
        field_constraints = self.get_field_constraints()

        for field, field_type in required_fields.items():
            value = getattr(self, field, None)
            if value is None:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(value, field_type):
                errors.append(f"Field {field} must be of type {field_type.__name__}")

        for field, constraints in field_constraints.items():
            value = getattr(self, field, None)
            if value is not None:
                if 'min' in constraints and value < constraints['min']:
                    errors.append(f"Field {field} must be greater than {constraints['min']}")
                if 'max' in constraints and value > constraints['max']:
                    errors.append(f"Field {field} must be less than {constraints['max']}")
                if 'before' in constraints and value >= constraints['before']:
                    errors.append(f"Field {field} must be before {constraints['before']}")
                if 'after' in constraints and value <= constraints['after']:
                    errors.append(f"Field {field} must be after {constraints['after']}")
                if 'allowed_values' in constraints and value not in constraints['allowed_values']:
                    errors.append(f"Field {field} must be one of {constraints['allowed_values']}")
                if isinstance(value, str):
                    if 'min_length' in constraints and len(value) < constraints['min_length']:
                        errors.append(f"Field {field} must be at least {constraints['min_length']} characters long")
                    if 'max_length' in constraints and len(value) > constraints['max_length']:
                        errors.append(f"Field {field} must be at most {constraints['max_length']} characters long")
                    if 'must_contain_special' in constraints and not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
                        errors.append(f"Field {field} must contain at least one special character")

        return errors

    def get_required_fields(self):
        """Debe ser implementado por las clases hijas para especificar los campos requeridos y sus tipos."""
        raise NotImplementedError("Subclasses must implement get_required_fields method")

    def get_field_constraints(self):
        """Debe ser implementado por las clases hijas para especificar restricciones adicionales."""
        return {}