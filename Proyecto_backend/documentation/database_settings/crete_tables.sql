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
ENGINE = InnoDB


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
  `created_at` DATETIME NOT NULL,
  `read_at` DATETIME NULL,
  `subject` VARCHAR(255) NOT NULL,
  `body` VARCHAR(500) NOT NULL,
  `user_id` BIGINT NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_notification_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `proyecto_informatico`.`user` (`id`)
    ON DELETE NO ACTION
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
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comment_order1`
    FOREIGN KEY (`order_id`)
    REFERENCES `proyecto_informatico`.`order` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB

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