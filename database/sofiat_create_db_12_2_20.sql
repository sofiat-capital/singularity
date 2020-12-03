-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema sofiat
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `sofiat` ;

-- -----------------------------------------------------
-- Schema sofiat
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sofiat` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema sofiat
-- -----------------------------------------------------
-- This schema was created for a stub table
DROP SCHEMA IF EXISTS `sofiat` ;

-- -----------------------------------------------------
-- Schema sofiat
--
-- This schema was created for a stub table
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sofiat` ;
USE `sofiat` ;

-- -----------------------------------------------------
-- Table `sofiat`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`category` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`category` (
  `idcategory` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(25) NULL,
  PRIMARY KEY (`idcategory`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sofiat`.`product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`product` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`product` (
  `idproduct` INT NOT NULL AUTO_INCREMENT,
  `fk_idcategory_product` INT NOT NULL,
  `ticker` VARCHAR(15) NULL,
  PRIMARY KEY (`idproduct`, `fk_idcategory_product`),
  CONSTRAINT `fk_idcategory_product`
    FOREIGN KEY (`fk_idcategory_product`)
    REFERENCES `sofiat`.`category` (`idcategory`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `fk_idcategory_idx` ON `sofiat`.`product` (`fk_idcategory_product` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `sofiat`.`transaction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`transaction` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`transaction` (
  `idtransaction` INT NOT NULL AUTO_INCREMENT,
  `fk_idproduct_transaction` INT NOT NULL,
  `transactionTime` DATETIME NULL,
  `buySell` TINYINT(1) NULL,
  `price` DECIMAL(15,8) NULL,
  `quantity` DECIMAL(15,8) NULL,
  PRIMARY KEY (`idtransaction`, `fk_idproduct_transaction`),
  CONSTRAINT `fk_idproduct_transaction`
    FOREIGN KEY (`fk_idproduct_transaction`)
    REFERENCES `sofiat`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `fk_idproduct_idx` ON `sofiat`.`transaction` (`fk_idproduct_transaction` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `sofiat`.`dayCandle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`dayCandle` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`dayCandle` (
  `iddayCandle` INT NOT NULL AUTO_INCREMENT,
  `fk_idproduct_dayCandle` INT NOT NULL,
  `date` DATE NULL,
  `low` DECIMAL(15,8) NULL,
  `hi` DECIMAL(15,8) NULL,
  `open` DECIMAL(15,8) NULL,
  `close` DECIMAL(15,8) NULL,
  `volume` DECIMAL(15,8) NULL,
  PRIMARY KEY (`iddayCandle`, `fk_idproduct_dayCandle`),
  CONSTRAINT `fk_idproduct_dayCandle`
    FOREIGN KEY (`fk_idproduct_dayCandle`)
    REFERENCES `sofiat`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sofiat`.`realTime`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`realTime` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`realTime` (
  `idrealTime` INT NOT NULL AUTO_INCREMENT,
  `fk_idproduct_realTime` INT NOT NULL,
  `observedPrice` DECIMAL(6,2) NOT NULL,
  `observedTime` DATETIME NOT NULL,
  PRIMARY KEY (`idrealTime`, `fk_idproduct_realTime`),
  CONSTRAINT `fk_idproduct_realTime`
    FOREIGN KEY (`fk_idproduct_realTime`)
    REFERENCES `sofiat`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

CREATE INDEX `fk_idproduct_idx` ON `sofiat`.`realTime` (`fk_idproduct_realTime` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `sofiat`.`binanceOrder`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`binanceOrder` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`binanceOrder` (
  `idbinanceOrder` INT NOT NULL,
  `fk_idproduct_binanceOrder` INT NOT NULL,
  `orderListId` INT NOT NULL,
  `clientOrderId` VARCHAR(25) NOT NULL,
  `transactTime` DATETIME NOT NULL,
  `price` DECIMAL(20,12) NOT NULL,
  `origQty` DECIMAL(20,12) NOT NULL,
  `executedQty` DECIMAL(20,12) NOT NULL,
  `cummulativeQuoteQty` DECIMAL(20,12) NOT NULL,
  `status` VARCHAR(15) NOT NULL,
  `timeInForce` VARCHAR(15) NOT NULL,
  `type` VARCHAR(8) NOT NULL,
  `side` VARCHAR(5) NOT NULL,
  `realTime_idrealTime` INT NOT NULL,
  `realTime_fk_idproduct_realTime` INT NOT NULL,
  PRIMARY KEY (`idbinanceOrder`, `realTime_idrealTime`, `realTime_fk_idproduct_realTime`, `fk_idproduct_binanceOrder`),
  CONSTRAINT `fk_idproduct_binanceOrder`
    FOREIGN KEY (`fk_idproduct_binanceOrder`)
    REFERENCES `sofiat`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `fk_idproduct_binanceOrder_idx` ON `sofiat`.`binanceOrder` (`fk_idproduct_binanceOrder` ASC) VISIBLE;

USE `sofiat` ;

-- -----------------------------------------------------
-- Table `sofiat`.`binanceFill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sofiat`.`binanceFill` ;

CREATE TABLE IF NOT EXISTS `sofiat`.`binanceFill` (
  `idbinanceFill` INT NOT NULL AUTO_INCREMENT,
  `fk_idbinanceOrder_idbinanceFill` INT NOT NULL,
  `price` DECIMAL(20,12) NULL,
  `qty` DECIMAL(20,12) NULL,
  `commission` DECIMAL(20,12) NULL,
  `commissionAsset` VARCHAR(15) NULL,
  PRIMARY KEY (`idbinanceFill`, `fk_idbinanceOrder_idbinanceFill`),
  CONSTRAINT `fk_idbinanceOrder_idbinanceFill`
    FOREIGN KEY (`fk_idbinanceOrder_idbinanceFill`)
    REFERENCES `sofiat`.`binanceOrder` (`idbinanceOrder`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `fk_idbinanceOrder_idbinanceFill_idx` ON `sofiat`.`binanceFill` (`fk_idbinanceOrder_idbinanceFill` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
