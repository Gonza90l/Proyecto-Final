from flask import Blueprint
from flaskr.controllers.users_controller import UsersController
from flaskr.controllers.menu_controller import MenuController
from flaskr.controllers.menu_category_controller import MenuCategoryController
from flaskr.controllers.order_controller import OrderController
from flaskr.controllers.image_controller import ImageController
from flaskr.controllers.review_controller import ReviewController
from flaskr.controllers.ipn_controller import ipnController
from flaskr.controllers.notification_controller import NotificationController
from flaskr.controllers.statistics_controller import StatisticsController
from flask_injector import inject

# Definir el Blueprint
main = Blueprint('main', __name__)

base_url = '' #'/api/v1'

############################################################################################################
# Rutas para el login, registro y verificación de token

@main.route(base_url + '/login', methods=['POST'])
@inject
def login(users_controller: UsersController):
    """
    Endpoint de inicio de sesión
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Login
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: El nombre de usuario
            password:
              type: string
              description: La contraseña del usuario
    responses:
      200:
        description: Inicio de sesión exitoso
      401:
        description: No autorizado
    """
    return users_controller.login()

@main.route(base_url + '/register', methods=['POST'])
@inject
def register(users_controller: UsersController):
    return users_controller.register()

# verificación de token
@main.route(base_url + '/verify_token', methods=['POST'])
@inject
def verify_token(users_controller: UsersController):
    return users_controller.verify_token()

############################################################################################################

# Rutas para obtener usuarios

@main.route(base_url + '/users', methods=['GET'])
@inject
def get_users(users_controller: UsersController):
    return users_controller.get_users()

@main.route(base_url + '/users/<int:user_id>', methods=['GET'])
@inject
def get_user(users_controller: UsersController, user_id):
    return users_controller.get_user(user_id)


############################################################################################################

# Rutas CRUD para Menús

# FETCH ALL
@main.route(base_url + '/menus', methods=['GET'])
@inject
def get_menus(menu_controller: MenuController):
    return menu_controller.get_menus()

# FETCH ONE
@main.route(base_url + '/menus/<int:menu_id>', methods=['GET'])
@inject
def get_menu(menu_controller: MenuController, menu_id):
    return menu_controller.get_menu(menu_id)

# CREATE 
@main.route(base_url + '/menus', methods=['POST'])
@inject
def create_menu(menu_controller: MenuController):
    return menu_controller.create_menu()

# UPDATE
@main.route(base_url + '/menus/<int:menu_id>', methods=['PUT'])
@inject
def update_menu(menu_controller: MenuController, menu_id):
    return menu_controller.update_menu(menu_id)

# DELETE
@main.route(base_url + '/menus/<int:menu_id>', methods=['DELETE'])
@inject
def delete_menu(menu_controller: MenuController, menu_id):
    return menu_controller.delete_menu(menu_id)
    
############################################################################################################

# Rutas CRUD para Categorías

# FETCH ALL
@main.route(base_url + '/categories', methods=['GET'])
@inject
def get_categories(menu_category_controller: MenuCategoryController):
    return menu_category_controller.get_categories()

# FETCH ONE
@main.route(base_url + '/categories/<int:category_id>', methods=['GET'])
@inject
def get_category(menu_category_controller: MenuCategoryController, category_id):
    return menu_category_controller.get_category(category_id)

# CREATE
@main.route(base_url + '/categories', methods=['POST'])
@inject
def create_category(menu_category_controller: MenuCategoryController):
    return menu_category_controller.create_category()

# UPDATE
@main.route(base_url + '/categories/<int:category_id>', methods=['PUT'])
@inject
def update_category(menu_category_controller: MenuCategoryController, category_id):
    return menu_category_controller.update_category(category_id)

# DELETE
@main.route(base_url + '/categories/<int:category_id>', methods=['DELETE'])
@inject
def delete_category(menu_category_controller: MenuCategoryController, category_id):
    return menu_category_controller.delete_category(category_id)

############################################################################################################

# Rutas CRUD para Ordenes

# FETCH ALL
@main.route(base_url + '/orders', methods=['GET'])
@inject
def get_orders(order_controller: OrderController):
    return order_controller.get_orders()

# FETCH ONE
@main.route(base_url + '/orders/<int:order_id>', methods=['GET'])
@inject
def get_order(order_controller: OrderController, order_id):
    return order_controller.get_order(order_id)

# CREATE
@main.route(base_url + '/orders', methods=['POST'])
@inject
def create_order(order_controller: OrderController):
    return order_controller.create_order()

# UPDATE
@main.route(base_url + '/orders/<int:order_id>', methods=['PUT'])
@inject
def update_order(order_controller: OrderController, order_id):
    return order_controller.update_order(order_id)

# DELETE
@main.route(base_url + '/orders/<int:order_id>', methods=['DELETE'])
@inject
def delete_order(order_controller: OrderController, order_id):
    return order_controller.delete_order(order_id)

############################################################################################################

#rutas para las reviews
@main.route(base_url + '/reviews/<int:id>', methods=['GET'])
@inject
def get_review_by_id(review_controller: ReviewController, id):
    return review_controller.get_review_by_id(id)

@main.route(base_url + '/reviews', methods=['POST'])
@inject
def create_review(review_controller: ReviewController):
    return review_controller.create_review()

#las rutas restantes del crud devuelven metodo no soportado
@main.route(base_url + '/reviews/<int:id>', methods=['PUT'])
@inject
def update_review(review_controller: ReviewController, id):
    return "Method not supported", 405

@main.route(base_url + '/reviews/<int:id>', methods=['DELETE'])
@inject
def delete_review(review_controller: ReviewController, id):
    return "Method not supported", 405

@main.route(base_url + '/reviews', methods=['GET'])
@inject
def get_all_reviews(review_controller: ReviewController):
    return "Method not supported", 405

############################################################################################################



# reutas para cargar las imagen de los menus
@main.route(base_url + '/images', methods=['POST'])
@inject
def upload_image(image_controller: ImageController):
    return image_controller.upload_image()

@main.route(base_url + '/images/<string:filename>', methods=['GET'])
@inject
def get_image(image_controller: ImageController, filename):
    return image_controller.get_image(filename)

@main.route(base_url + '/images/<string:filename>', methods=['DELETE'])
@inject
def delete_image(image_controller: ImageController, filename):
    return image_controller.delete_image(filename)


############################################################################################################

#rutas para el IPN
@main.route(base_url + '/ipn', methods=['POST'])
@inject
def ipn(ipn_controller: ipnController):
    return ipn_controller.post()

#ruta para verificar si una orden posee una review
@main.route(base_url + '/orders/<int:id>/review', methods=['GET'])
@inject
def get_review_by_order_id(review_controller: ReviewController, id):
    return review_controller.get_review_by_order_id(id)
    

#rutas para las notifaciones
@main.route(base_url + '/notifications', methods=['GET'])
@inject
def get_notifications(notification_controller: NotificationController):
    return notification_controller.get_notifications()

@main.route(base_url + '/notifications/<int:notification_id>', methods=['GET'])
@inject
def get_notification(notification_controller: NotificationController, notification_id):
    return notification_controller.get_notification(notification_id)

#amrcar la notificacion como leida
@main.route(base_url + '/notifications/<int:notification_id>/read', methods=['PUT'])
@inject
def set_as_read(notification_controller: NotificationController, notification_id):
    return notification_controller.set_as_read(notification_id)


#rutas para las estadisticas
@main.route(base_url + '/statistics', methods=['GET'])
@inject
def get_statistics(statistics_controller: StatisticsController):
    return statistics_controller.get_statistics()