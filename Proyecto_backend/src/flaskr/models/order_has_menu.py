from flaskr.models.base_model import BaseModel
import importlib

class OrderHasMenu(BaseModel):
    _table = '`order_has_menu`'
    _fields = ['menu_id', 'order_id', 'quantity']
    _relationships = {'item': {'class': 'Menu', 'foreign_key': 'menu_id'}}

    def load_related_data(self):
        """Load related data for the OrderHasMenu instance."""
        for relation, details in self._relationships.items():
            related_class_name = details['class']
            foreign_key = details['foreign_key']
            
            # Convert class name to snake_case to match the file name
            module_name = f"flaskr.models.{self._to_snake_case(related_class_name)}"
            related_class = getattr(importlib.import_module(module_name), related_class_name)
            
            related_instance = related_class.find_by_id(self._mysql, self._data[foreign_key])
            self._related_data[relation] = related_instance