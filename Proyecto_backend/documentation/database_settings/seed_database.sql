
USE `proyecto_informatico` ;

-- Volcando datos para la tabla proyecto_informatico.category: ~4 rows (aproximadamente)
INSERT INTO `category` (`id`, `name`, `description`, `photo`) VALUES
	(1, 'Entradas', '', NULL),
	(2, 'Minutas', '', NULL),
	(3, 'Postres', NULL, NULL),
	(4, 'Bebidas', NULL, NULL),
	(5, 'Pastas', NULL, NULL);

-- Volcando datos para la tabla proyecto_informatico.menu: ~3 rows (aproximadamente)
INSERT INTO `menu` (`id`, `name`, `description`, `price`, `photo`, `deleted_flag`, `category_id`) VALUES
	(1, 'Empanadas de carne', 'Empanadas rellenas de carne especiada, cocidas al horno', 200.00, 'db3a3c0897704389a97ad44e3cdba066.jpg', 0, 1),
	(2, 'Bruschettas', 'Pan tostado con tomate fresco, albahaca y aceite de oliva', 150.00, '8aa32fd18684424885da9b684c8887c9.jpg', 0, 1),
	(3, 'Tabla de fiambres', 'Selección de quesos y embutidos artesanales', 500.00, '83a35dc8a8104d06b6f9148a10ff5239.jpg', 0, 1),
	(4, 'Patitas de pollo', 'Croquetas de pollo empanizado, servidas con salsas', 300.00, '12d465c2a7704010ab7bbbbd1efa9487.jpg', 0, 1),
	(5, 'Milanesa de ternera', 'Clásica milanesa de carne, servida con guarnición', 600.00, '00dca814e07642f38c951732c34948b7.jpg', 0, 2),
	(6, 'Papas fritas', 'Papas fritas caseras, crujientes y doradas', 350.00, '545dacd72c06457dbdc8bf4044a0d8f9.jpg', 0, 2),
	(7, 'Hamburguesa completa', 'Hamburguesa con queso, lechuga, tomate y aderezos', 750.00, '3a0985d3734d4de8b17283f13b343478.jpg', 0, 2),
	(8, 'Lomito completo', 'Sandwich de lomito con huevo, jamón, queso y vegetales', 900.00, 'f47d791f5db5483a95d68504eb6b316b.jpg', 0, 2),
	(9, 'Helado artesanal', 'Helado casero con sabores a elección', 250.00, 'c27b18c23e59465fbabd5d65a8375ef5.jpg', 0, 3),
	(10, 'Flan con crema y dulce de leche', 'Postre casero acompañado de crema y dulce de leche', 400.00, 'bb77f9b2e58448c880c9a3b3c919ed20.jpg', 0, 3),
	(11, 'Tiramisú', 'Postre italiano de mascarpone, café y cacao', 550.00, 'e66a02bd70f042369ec65a1e8f1e2216.jpg', 0, 3),
	(12, 'Cheesecake de frutos rojos', 'Tarta de queso con coulis de frutos rojos', 600.00, '52523da635cb47298fad9d2b5772c004.jpg', 0, 3),
	(13, 'Agua mineral', 'Botella de agua mineral natural o con gas', 150.00, 'b06b772ab46a473eab81fe71420427fd.jpg', 0, 4),
	(14, 'Refresco', 'Lata de refresco de cola o sabor a elección', 200.00, '079d91a2bbb24f1880ec57300189d090.jpg', 0, 4),
	(15, 'Cerveza artesanal', 'Pinta de cerveza artesanal, varios estilos disponibles', 350.00, '5cdef1f203a94b2c8f7d10d2d3ebceba.jpg', 0, 4),
	(16, 'Vino de autor', 'vino tinto o blanco, selección de la casa', 400.00, '0a5981032a774477b35fa63c9cb3ccc8.jpg', 0, 4),
	(42, 'Volcan de chocolate', 'relleno de chocolate, acompañado con frutos finos.', 5000.00, '6765d3e518f54843b03038b40fac766a.jpg', 0, 3),
	(43, 'Rabas', 'rabas recien pescadas del mar de MH', 4999.00, 'ac23b81708e146a7871d85f4f4bc8f07.jpg', 0, 1),
	(44, 'Ravioles con salsa elección', 'Ravioles rellenos de trucha o verdura', 870.00, '6ac7080920104ce0809d80b2bea3c4f1.jpg', 0, 5);

-- Volcando datos para la tabla proyecto_informatico.user: ~3 rows (aproximadamente)
INSERT INTO `user` (`id`, `name`, `lastname`, `email`, `password`, `role`, `deleted_flag`) VALUES
	(2, 'Admin', 'Administrador', 'admin@example.com', 'scrypt:32768:8:1$HoS5y8gmDmcZKeQJ$ee9745a9942b2b7d96d313de602148cf147a5dc5f1f6ce816765a56edbf334e9a4baabb59b306838217fe90fe47614f86ff1cc69b0944f78b9567463f6937e8e', 'ADMIN', 0),
	(3, 'User1', 'Dummy', 'user1@example.com', 'scrypt:32768:8:1$HoS5y8gmDmcZKeQJ$ee9745a9942b2b7d96d313de602148cf147a5dc5f1f6ce816765a56edbf334e9a4baabb59b306838217fe90fe47614f86ff1cc69b0944f78b9567463f6937e8e', 'USER', 0),
	(4, 'User2', 'Dummy', 'user2@example.com', 'scrypt:32768:8:1$HoS5y8gmDmcZKeQJ$ee9745a9942b2b7d96d313de602148cf147a5dc5f1f6ce816765a56edbf334e9a4baabb59b306838217fe90fe47614f86ff1cc69b0944f78b9567463f6937e8e', 'USER', 0);
