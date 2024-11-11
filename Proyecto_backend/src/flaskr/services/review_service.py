from flask_injector import inject
from flaskr.database.database import IDatabase

class ReviewService:

    @inject
    def __init__(self, mysql: IDatabase):
        self._mysql = mysql

    # obtener reviews de un producto
    def get_review_by_id(self, product_id):
        query = "SELECT * FROM comment WHERE menu_id = %s"
        params = (product_id,)
        
        cursor = self._mysql.connection.cursor()
        cursor.execute(query, params)
        reviews = cursor.fetchall()
        cursor.close()

        # buscamos el usuario que hizo la review, sabiendo que el id del usuario está en la tabla de orders
        for review in reviews:
            query = "SELECT user_id FROM `order` WHERE id = %s"
            params = (review['order_id'],)
            cursor = self._mysql.connection.cursor()
            cursor.execute(query, params)
            user_id = cursor.fetchone()
            cursor.close()
            review['user_id'] = user_id['user_id']

        # eliminamos la data como menu_id y order_id
        for review in reviews:
            review.pop('order_id')

        # retornamos un diccionario con la información de las reviews y un promedio de estrellas
        #OJO, debemos respetar el formato de respuesta implicado en review_dto
        if len(reviews) == 0:
            return {
                "reviews": [],
                "count": len(reviews),
                "average": 0
            }
        else:
            total = 0
            for review in reviews:
                total += review['rating']
            average = total / len(reviews)
            return {
                "reviews": reviews,
                "count": len(reviews),
                "average": average
            }