USE `proyecto_informatico` ;

-- -----------------------------------------------------
-- Table `proyecto_informatico`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_informatico`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(500) NULL,
  `photo` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_informatico`.`menu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_informatico`.`menu` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(500) NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `photo` VARCHAR(255) NULL,
  `deleted_flag` TINYINT(1) NOT NULL DEFAULT 0,
  `category_id` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_menu_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_menu_category_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_menu_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `proyecto_informatico`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_informatico`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_informatico`.`user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` ENUM('USER', 'ADMIN') NOT NULL,
  `deleted_flag` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_informatico`.`order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_informatico`.`order` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NULL,
  `total` DECIMAL(10,2) NULL,
  `status` ENUM('CREATED', 'PAID', 'IN PROGRESS', 'SEND', 'DELIVERED', 'CANCELED') NOT NULL DEFAULT 'CREATED',
  `user_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_order_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `proyecto_informatico`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_informatico`.`payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_informatico`.`payment` (
  `created_at` DATETIME NOT NULL,
  `order_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`order_id`),
  INDEX `fk_payment_order1_idx` (`order_id` ASC) VISIBLE,
  CONSTRAINT `fk_payment_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `proyecto_informatico`.`order` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `proyecto_informatico`.`notification`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_informatico`.`notification` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NOT NULL,
  `read_at` DATETIME NULL,
  `subject` VARCHAR(255) NOT NULL,
  `body` VARCHAR(500) NOT NULL,
  `user_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_notification_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_notification_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `proyecto_informatico`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_informatico`.`comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_informatico`.`comment` (
  `comment` VARCHAR(500) NOT NULL,
  `rating` TINYINT(2) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `menu_id` BIGINT UNSIGNED NOT NULL,
  `order_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`menu_id`, `order_id`),
  INDEX `fk_comment_menu1_idx` (`menu_id` ASC) VISIBLE,
  INDEX `fk_comment_order1_idx` (`order_id` ASC) VISIBLE,
  CONSTRAINT `fk_comment_menu1`
    FOREIGN KEY (`menu_id`)
    REFERENCES `proyecto_informatico`.`menu` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comment_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `proyecto_informatico`.`order` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `proyecto_informatico`.`order_has_menu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_informatico`.`order_has_menu` (
  `order_id` BIGINT UNSIGNED NOT NULL,
  `menu_id` BIGINT UNSIGNED NOT NULL,
  `quantity` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`order_id`, `menu_id`),
  INDEX `fk_order_has_menu_menu1_idx` (`menu_id` ASC) VISIBLE,
  INDEX `fk_order_has_menu_order1_idx` (`order_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_has_menu_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `proyecto_informatico`.`order` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_has_menu_menu1`
    FOREIGN KEY (`menu_id`)
    REFERENCES `proyecto_informatico`.`menu` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

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
