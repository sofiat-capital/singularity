-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema sofiat
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `sofiat` ;

-- -----------------------------------------------------
-- Schema sofiat
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sofiat` DEFAULT CHARACTER SET utf8 ;
USE `sofiat` ;

-- -----------------------------------------------------
-- Table `sofiat`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`category` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`category` (
  `idcategory` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(25) NULL DEFAULT NULL,
  PRIMARY KEY (`idcategory`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sofiat`.`product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`product` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`product` (
  `idproduct` INT NOT NULL AUTO_INCREMENT,
  `fk_idcategory_product` INT NOT NULL,
  `ticker` VARCHAR(15) NULL DEFAULT NULL,
  PRIMARY KEY (`idproduct`, `fk_idcategory_product`),
  INDEX `fk_idcategory_idx` (`fk_idcategory_product` ASC) VISIBLE,
  CONSTRAINT `fk_idcategory_product`
    FOREIGN KEY (`fk_idcategory_product`)
    REFERENCES `sofiat`.`category` (`idcategory`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sofiat`.`binanceOrder`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`binanceOrder` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`binanceOrder` (
  `idbinanceOrder` INT NOT NULL,
  `fk_idproduct_binanceOrder` INT NOT NULL,
  `orderListId` INT NULL DEFAULT NULL,
  `clientOrderId` VARCHAR(25) NULL DEFAULT NULL,
  `transactTime` DATETIME NULL DEFAULT NULL,
  `price` DECIMAL(20,12) NULL DEFAULT NULL,
  `origQty` DECIMAL(20,12) NULL DEFAULT NULL,
  `executedQty` DECIMAL(20,12) NULL DEFAULT NULL,
  `cummulativeQuoteQty` DECIMAL(20,12) NULL DEFAULT NULL,
  `status` VARCHAR(15) NULL DEFAULT NULL,
  `timeInForce` VARCHAR(15) NULL DEFAULT NULL,
  `type` VARCHAR(8) NULL DEFAULT NULL,
  `side` VARCHAR(5) NULL DEFAULT NULL,
  PRIMARY KEY (`idbinanceOrder`, `fk_idproduct_binanceOrder`),
  INDEX `fk_idproduct_binanceOrder_idx` (`fk_idproduct_binanceOrder` ASC) VISIBLE,
  CONSTRAINT `fk_idproduct_binanceOrder`
    FOREIGN KEY (`fk_idproduct_binanceOrder`)
    REFERENCES `sofiat`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sofiat`.`binanceFill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`binanceFill` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`binanceFill` (
  `idbinanceFill` INT NOT NULL AUTO_INCREMENT,
  `fk_idbinanceorder_binanceFill` INT NOT NULL,
  `price` DECIMAL(20,12) NULL DEFAULT NULL,
  `qty` DECIMAL(20,12) NULL DEFAULT NULL,
  `commission` DECIMAL(20,12) NULL DEFAULT NULL,
  `commissionAsset` VARCHAR(15) NULL DEFAULT NULL,
  PRIMARY KEY (`idbinanceFill`, `fk_idbinanceorder_binanceFill`),
  INDEX `fk_idbinanceorder_binanceFill` (`fk_idbinanceorder_binanceFill` ASC) VISIBLE,
  CONSTRAINT `fk_idbinanceorder_binanceFill`
    FOREIGN KEY (`fk_idbinanceorder_binanceFill`)
    REFERENCES `sofiat`.`binanceOrder` (`idbinanceOrder`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sofiat`.`dayCandle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`dayCandle` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`dayCandle` (
  `iddayCandle` INT NOT NULL AUTO_INCREMENT,
  `fk_idproduct_dayCandle` INT NOT NULL,
  `date` DATE NULL DEFAULT NULL,
  `open` DECIMAL(20,12) NULL DEFAULT NULL,
  `hi` DECIMAL(20,12) NULL DEFAULT NULL,
  `low` DECIMAL(20,12) NULL DEFAULT NULL,
  `close` DECIMAL(20,12) NULL DEFAULT NULL,
  `volume` DECIMAL(20,12) NULL DEFAULT NULL,
  `numTrades` INT NULL DEFAULT NULL,
  PRIMARY KEY (`iddayCandle`, `fk_idproduct_dayCandle`),
  INDEX `fk_idproduct_dayCandle` (`fk_idproduct_dayCandle` ASC) VISIBLE,
  CONSTRAINT `fk_idproduct_dayCandle`
    FOREIGN KEY (`fk_idproduct_dayCandle`)
    REFERENCES `sofiat`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 501
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sofiat`.`realTime`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`realTime` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`realTime` (
  `idrealTime` INT NOT NULL AUTO_INCREMENT,
  `fk_idproduct_realTime` INT NOT NULL,
  `observedPrice` DECIMAL(20,12) NOT NULL,
  `observedTime` DATETIME NOT NULL,
  PRIMARY KEY (`idrealTime`, `fk_idproduct_realTime`),
  INDEX `fk_idproduct_idx` (`fk_idproduct_realTime` ASC) VISIBLE,
  CONSTRAINT `fk_idproduct_realTime`
    FOREIGN KEY (`fk_idproduct_realTime`)
    REFERENCES `sofiat`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
