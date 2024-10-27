

# ItemMenuDTO
# Clase que representa un ítem del menú
class ItemMenuDTO:
    def __init__(self, id, name, description, price, image, category_id):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.image = image
        self.category_id = category_id

# CategoryDTO
# Clase que representa una categoría
class CategoryDTO:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# OrderDTO
# Clase que representa una orden
class OrderDTO:
    def __init__(self, id, user_id, date_time, status, total_price, items):
        self.id = id
        self.user_id = user_id
        self.date_time = date_time
        self.status = status
        self.total_price = total_price
        self.items = items  # Lista de OrderHasItemDTO

# OrderHasItemDTO
# Clase que representa la relación entre una orden y un ítem
class OrderHasItemDTO:
    def __init__(self, order_id, item_id, quantity):
        self.item_id = item_id
        self.quantity = quantity

# CommentDTO
# Clase que representa un comentario
class CommentDTO:
    def __init__(self, id, user_id, order_id, item_id, comment, rating, date_time):
        self.id = id
        self.user_id = user_id
        self.order_id = order_id
        self.item_id = item_id
        self.comment = comment
        self.rating = rating
        self.date_time = date_time

# PaymentDTO
# Clase que representa un pago
class PaymentDTO:
    def __init__(self, id, order_id, payment_method, payment_status, date_time):
        self.id = id
        self.order_id = order_id
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.date_time = date_time

# NotificationDTO
# Clase que representa una notificación
class NotificationDTO:
    def __init__(self, id, user_id, message, date_time):
        self.id = id
        self.user_id = user_id
        self.message = message
        self.date_time = date_time

# LoginDTO
# Clase que representa un login
class LoginDTO:
    def __init__(self, email, password):
        self.email = email
        self.password = password

# RegisterDTO
# Clase que representa un registro
class RegisterDTO:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

# LoginResponseDTO
# Clase que representa la respuesta de un login
class LoginResponseDTO:
    def __init__(self, user, token):
        self.user = user
        self.token = token

# RegisterResponseDTO
# Clase que representa la respuesta de un registro
class RegisterResponseDTO:
    def __init__(self, user):
        self.user = user

# UpdateUserDTO
# Clase que representa la actualización de un usuario
class UpdateUserDTO:
    def __init__(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
