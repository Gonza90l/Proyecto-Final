from flask_injector import inject
from flaskr.controllers.base_controller import BaseController
from flaskr.database.database_interface import IDatabase
from flaskr.auth import role_required

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
        try:
            # Consulta para obtener la cantidad de pedidos excepto los que están en estado 'CREATED' o 'CANCELED'
            query_count = """
                SELECT COUNT(*) as total_orders 
                FROM `order`
                WHERE status NOT IN ('CREATED', 'CANCELED')
            """
            result_count = self.execute_query(query_count)
            total_orders = result_count[0]['total_orders'] if result_count else 0

            # Consulta para obtener la suma total de los pedidos excepto los que están en estado 'CREATED' o 'CANCELED'
            query_sum = """
                SELECT SUM(total) as total_amount 
                FROM `order`
                WHERE status NOT IN ('CREATED', 'CANCELED')
            """
            result_sum = self.execute_query(query_sum)
            total_amount = result_sum[0]['total_amount'] if result_sum else 0

            # Consulta para obtener la cantidad de pedidos pendientes (no 'DELIVERED')
            query_pending = """
                SELECT COUNT(*) as pending_orders 
                FROM `order`
                WHERE status NOT IN ('DELIVERED')
            """
            result_pending = self.execute_query(query_pending)
            pending_orders = result_pending[0]['pending_orders'] if result_pending else 0

            # Devolver las estadísticas
            return self.respond_success({
                'total_orders': total_orders,
                'total_amount': total_amount,
                'pending_orders': pending_orders
            })
        except Exception as e:
            return self.respond_error(str(e))

    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta en la base de datos y devuelve los resultados.
        
        :param query: La consulta SQL a ejecutar.
        :param params: Parámetros para la consulta SQL.
        :return: Resultados de la consulta.
        """
        connection = self._mysql.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result