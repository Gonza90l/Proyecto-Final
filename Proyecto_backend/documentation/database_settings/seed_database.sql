-- Insertar datos en `menu`
INSERT INTO `proyecto_informatico`.`menu` (`name`, `description`, `price`, `photo`, `deleted_flag`, `category_id`) VALUES
('Coca Cola', 'Bebida refrescante', 1.50, 'coca_cola.jpg', 0, 1),
('Pepsi', 'Bebida refrescante', 1.50, 'pepsi.jpg', 0, 1),
('Papas Fritas', 'Papas crujientes', 2.50, 'papas_fritas.jpg', 0, 2),
('Alitas de Pollo', 'Alitas picantes', 5.00, 'alitas_pollo.jpg', 0, 2),
('Hamburguesa', 'Jugosa hamburguesa de res', 8.00, 'hamburguesa.jpg', 0, 3),
('Pasta', 'Pasta italiana', 7.50, 'pasta.jpg', 0, 3),
('Tarta de Queso', 'Tarta de queso cremosa', 4.00, 'tarta_queso.jpg', 0, 4),
('Ensalada César', 'Ensalada César clásica', 5.50, 'ensalada_cesar.jpg', 0, 5),
('Sopa de Tomate', 'Sopa de tomate caliente', 3.50, 'sopa_tomate.jpg', 0, 6),
('Salmón a la Parrilla', 'Filete de salmón a la parrilla', 12.00, 'salmon_parrilla.jpg', 0, 7);

-- Insertar datos en `user`
INSERT INTO `proyecto_informatico`.`user` (`name`, `lastname`, `email`, `password`, `rol`) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', 'password123', 'USER'),
('Ana', 'García', 'ana.garcia@example.com', 'password123', 'USER'),
('Luis', 'Martínez', 'luis.martinez@example.com', 'password123', 'USER'),
('María', 'López', 'maria.lopez@example.com', 'password123', 'USER'),
('Carlos', 'González', 'carlos.gonzalez@example.com', 'password123', 'USER'),
('Elena', 'Rodríguez', 'elena.rodriguez@example.com', 'password123', 'USER'),
('Pedro', 'Hernández', 'pedro.hernandez@example.com', 'password123', 'USER'),
('Lucía', 'Fernández', 'lucia.fernandez@example.com', 'password123', 'USER'),
('Miguel', 'Sánchez', 'miguel.sanchez@example.com', 'password123', 'USER'),
('Laura', 'Ramírez', 'laura.ramirez@example.com', 'password123', 'ADMIN');

-- Insertar datos en `order`
INSERT INTO `proyecto_informatico`.`order` (`created_at`, `updated_at`, `total`, `status`, `user_id`) VALUES
('2023-01-01 10:00:00', NULL, 15.00, 'CREATED', 1),
('2023-01-02 11:00:00', NULL, 20.00, 'IN PROGRESS', 2),
('2023-01-03 12:00:00', NULL, 25.00, 'SEND', 3),
('2023-01-04 13:00:00', NULL, 30.00, 'ENTERGADO', 4),
('2023-01-05 14:00:00', NULL, 35.00, 'CANCELED', 5),
('2023-01-06 15:00:00', NULL, 40.00, 'CREATED', 6),
('2023-01-07 16:00:00', NULL, 45.00, 'IN PROGRESS', 7),
('2023-01-08 17:00:00', NULL, 50.00, 'SEND', 8),
('2023-01-09 18:00:00', NULL, 55.00, 'ENTERGADO', 9),
('2023-01-10 19:00:00', NULL, 60.00, 'CANCELED', 10);


-- Insertar datos en `payment`
INSERT INTO `proyecto_informatico`.`payment` (`created_at`, `order_id`) VALUES
('2023-01-01 10:30:00', 1),
('2023-01-02 11:30:00', 2),
('2023-01-03 12:30:00', 3),
('2023-01-04 13:30:00', 4),
('2023-01-05 14:30:00', 5),
('2023-01-06 15:30:00', 6),
('2023-01-07 16:30:00', 7),
('2023-01-08 17:30:00', 8),
('2023-01-09 18:30:00', 9),
('2023-01-10 19:30:00', 10);

-- Insertar datos en `notification`
INSERT INTO `proyecto_informatico`.`notification` (`created_at`, `read_at`, `subject`, `body`, `user_id`) VALUES
('2023-01-01 10:00:00', NULL, 'Bienvenido', '¡Bienvenido a nuestro servicio!', 1),
('2023-01-02 11:00:00', NULL, 'Actualización de Pedido', 'Tu pedido está en progreso.', 2),
('2023-01-03 12:00:00', NULL, 'Pedido Enviado', 'Tu pedido ha sido enviado.', 3),
('2023-01-04 13:00:00', NULL, 'Pedido Entregado', 'Tu pedido ha sido entregado.', 4),
('2023-01-05 14:00:00', NULL, 'Pedido Cancelado', 'Tu pedido ha sido cancelado.', 5),
('2023-01-06 15:00:00', NULL, 'Bienvenido', '¡Bienvenido a nuestro servicio!', 6),
('2023-01-07 16:00:00', NULL, 'Actualización de Pedido', 'Tu pedido está en progreso.', 7),
('2023-01-08 17:00:00', NULL, 'Pedido Enviado', 'Tu pedido ha sido enviado.', 8),
('2023-01-09 18:00:00', NULL, 'Pedido Entregado', 'Tu pedido ha sido entregado.', 9),
('2023-01-10 19:00:00', NULL, 'Pedido Cancelado', 'Tu pedido ha sido cancelado.', 10);

-- Insertar datos en `comment`
INSERT INTO `proyecto_informatico`.`comment` (`comment`, `rating`, `created_at`, `menu_id`, `order_id`) VALUES
('Cremoso y dulce', 5, '2023-01-07 16:00:00', 7, 7),
('Fresco y saludable', 4, '2023-01-08 17:00:00', 8, 8),
('Caliente y reconfortante', 5, '2023-01-09 18:00:00', 9, 9),
('Perfectamente a la parrilla', 5, '2023-01-10 19:00:00', 10, 10);


-- Insertar datos en `order_has_menu`
INSERT INTO `proyecto_informatico`.`order_has_menu` (`order_id`, `menu_id`) VALUES
(1, 1),
(1, 3),
(1, 5),
(2, 2),
(2, 4),
(2, 6),
(3, 1),
(3, 2),
(3, 3),
(4, 4),
(4, 5),
(4, 6),
(5, 1),
(5, 7),
(5, 8),
(6, 2),
(6, 9),
(6, 10),
(7, 3),
(7, 4),
(7, 5),
(8, 6),
(8, 7),
(8, 8),
(9, 9),
(9, 10),
(9, 1),
(10, 2),
(10, 3),
(10, 4);