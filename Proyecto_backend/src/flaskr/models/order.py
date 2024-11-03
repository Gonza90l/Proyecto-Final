from .base_model import BaseModel
import importlib


class Order(BaseModel):
    _table = '`order`'
    _fields = ['id', 'created_at', 'updated_at', 'user_id', 'total', 'status']
    _relationships = {'order_items': {'class': 'OrderHasMenu', 'foreign_key': 'order_id'}}

    def from_dto(self, dto):
        """Convert a DTO to an Order model instance."""
        for key, value in dto.__dict__.items():
            if key in self._fields:
                self._data[key] = value
            elif key == 'order_items':
                # Skip order_items as it is not a field in the orders table
                continue
            else:
                raise AttributeError(f"DTO has no attribute '{key}'")

    def load_related_data(self):
        """Load related data for the Order instance."""
        for relation, details in self._relationships.items():
            related_class_name = details['class']
            foreign_key = details['foreign_key']
            
            # Convert class name to snake_case to match the file name
            module_name = f"flaskr.models.{self._to_snake_case(related_class_name)}"
            related_class = getattr(importlib.import_module(module_name), related_class_name)
            
            related_instances = related_class.find_all_by_foreign_key(self._mysql, foreign_key, self._data['id'])
            self._related_data[relation] = related_instances