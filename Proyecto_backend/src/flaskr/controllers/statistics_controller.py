from flask_injector import inject
from flaskr.controllers.base_controller import BaseController
from flaskr.database.database_interface import IDatabase
from flaskr.auth import role_required

# no utilizamos el patron service en este caso, ya que es una consulta simple

class StatisticsController(BaseController):
    @inject
    def __init__(self, mysql: IDatabase):
        """
        Constructor de la clase StatisticsController.
        
        :param mysql: Servicio de base de datos inyectado.
        """
        self._mysql = mysql

    @role_required('ADMIN')
    def get_statistics(self):
        # Consulta para obtener la cantidad de pedidos excepto los que están en estado 'CREATED' o 'CANCELED'
        query_count = """
            SELECT COUNT(*) as total_orders 
            FROM orders 
            WHERE status NOT IN ('CREATED', 'CANCELED')
        """
        result_count = self._mysql.select(query_count)
        total_orders = result_count[0]['total_orders'] if result_count else 0

        # Consulta para obtener la suma total de los pedidos excepto los que están en estado 'CREATED' o 'CANCELED'
        query_sum = """
            SELECT SUM(total_amount) as total_amount 
            FROM orders 
            WHERE status NOT IN ('CREATED', 'CANCELED')
        """
        result_sum = self._mysql.select(query_sum)
        total_amount = result_sum[0]['total_amount'] if result_sum else 0

        # Consulta para obtener la cantidad de pedidos pendientes (no 'DELIVERED')
        query_pending = """
            SELECT COUNT(*) as pending_orders 
            FROM orders 
            WHERE status NOT IN ('DELIVERED')
        """
        result_pending = self._mysql.select(query_pending)
        pending_orders = result_pending[0]['pending_orders'] if result_pending else 0

        # Devolver las estadísticas
        return {
            'total_orders': total_orders,
            'total_amount': total_amount,
            'pending_orders': pending_orders
        }