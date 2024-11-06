// UserDTO
// Clase que representa un usuario
export class UserDTO {
    constructor(id, name, email, password, role) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.password = password;
        this.role = role;
    }
}

// ItemMenuDTO
// Clase que representa un ítem del menú
export class ItemMenuDTO {
    constructor(id, name, description, price, image, categoryId) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.price = price;
        this.image = image;
        this.categoryId = categoryId;
    }
}

// CategoryDTO
// Clase que representa una categoría
export class CategoryDTO {
    constructor(id, name) {
        this.id = id;
        this.name = name;
    }
}

// OrderDTO
// Clase que representa una orden
export class OrderDTO {
    constructor(id, userId, dateTime, status, totalPrice, items) {
        this.id = id;
        this.userId = userId;
        this.dateTime = dateTime;
        this.status = status;
        this.totalPrice = totalPrice;
        this.items = items; // Array de OrderHasItemDTO
    }
}

// OrderHasItemDTO
// Clase que representa la relación entre una orden y un ítem
export class OrderHasItemDTO {
    constructor(orderId, itemId, quantity) {
        this.itemId = itemId;
        this.quantity = quantity;
    }
}

// CommentDTO
// Clase que representa un comentario
export class CommentDTO {
    constructor(id, userId, orderId, itemId, comment, rating, dateTime) {
        this.id = id;
        this.userId = userId;
        this.orderId = orderId;
        this.itemId = itemId;
        this.comment = comment;
        this.rating = rating;
        this.dateTime = dateTime;
    }
}

// PaymentDTO
// Clase que representa un pago
export class PaymentDTO {
    constructor(id, orderId, paymentMethod, paymentStatus, dateTime) {
        this.id = id;
        this.orderId = orderId;
        this.paymentMethod = paymentMethod;
        this.paymentStatus = paymentStatus;
        this.dateTime = dateTime;
    }
}

// NotificationDTO
// Clase que representa una notificación
export class NotificationDTO {
    constructor(id, userId, message, dateTime) {
        this.id = id;
        this.userId = userId;
        this.message = message;
        this.dateTime = dateTime;
    }
}



