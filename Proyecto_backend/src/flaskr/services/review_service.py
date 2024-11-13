from flask_injector import inject
from flaskr.database.database import IDatabase
from datetime import datetime

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

    # crear review
    def create_review(self, product_id, order_id, rating, comment):

        #averiguamos si existe el producto
        query = "SELECT * FROM menu WHERE id = %s"
        params = (product_id,)
        cursor = self._mysql.connection.cursor()
        cursor.execute(query, params)
        product = cursor.fetchone()
        cursor.close()


        #averiguamos si el usuario ya ha hecho una review para ese producto y esa orden
        query = "SELECT * FROM comment WHERE menu_id = %s AND order_id = %s"
        params = (product_id, order_id)

        cursor = self._mysql.connection.cursor()
        cursor.execute(query, params)
        review = cursor.fetchone()
        cursor.close()

        if review:
            raise Exception("This user has already made a review for this product")

        #averiguamos si la orden es del usuario que está intentando hacer la review
        query = "SELECT * FROM `order` WHERE id = %s AND user_id = (SELECT user_id FROM `order` WHERE id = %s)"
        params = (order_id, order_id)

        cursor = self._mysql.connection.cursor()
        cursor.execute(query, params)
        order = cursor.fetchone()
        cursor.close()

        if not order:
            raise Exception("This order does not belong to the user")

        #validamios que el rating sea un número entre 1 y 5
        if rating < 1 or rating > 5:
            raise Exception("Rating must be between 1 and 5")
                     
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO comment (menu_id, order_id, rating, comment, created_at) VALUES (%s, %s, %s, %s, %s)"
        params = (product_id, order_id, rating, comment, created_at)
        
        cursor = self._mysql.connection.cursor()
        cursor.execute(query, params)
        self._mysql.connection.commit()
        cursor.close()

        return True

    def order_has_review(self, order_id):
        query = "SELECT * FROM comment WHERE order_id = %s"
        params = (order_id,)
        
        cursor = self._mysql.connection.cursor()
        cursor.execute(query, params)
        review = cursor.fetchone()
        cursor.close()

        if review:
            return True
        else:
            return False