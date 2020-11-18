-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema StockPortfolio
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `StockPortfolio` ;

-- -----------------------------------------------------
-- Schema StockPortfolio
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `StockPortfolio` DEFAULT CHARACTER SET utf8 ;
USE `StockPortfolio` ;

-- -----------------------------------------------------
-- Table `StockPortfolio`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `StockPortfolio`.`category` ;

CREATE TABLE IF NOT EXISTS `StockPortfolio`.`category` (
  `idcategory` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(25) NULL,
  PRIMARY KEY (`idcategory`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `StockPortfolio`.`product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `StockPortfolio`.`product` ;

CREATE TABLE IF NOT EXISTS `StockPortfolio`.`product` (
  `idproduct` INT NOT NULL AUTO_INCREMENT,
  `fk_idcategory_product` INT NOT NULL,
  `ticker` VARCHAR(15) NULL,
  PRIMARY KEY (`idproduct`, `fk_idcategory_product`),
  CONSTRAINT `fk_idcategory_product`
    FOREIGN KEY (`fk_idcategory_product`)
    REFERENCES `StockPortfolio`.`category` (`idcategory`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `fk_idcategory_idx` ON `StockPortfolio`.`product` (`fk_idcategory_product` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `StockPortfolio`.`transaction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `StockPortfolio`.`transaction` ;

CREATE TABLE IF NOT EXISTS `StockPortfolio`.`transaction` (
  `idtransaction` INT NOT NULL AUTO_INCREMENT,
  `fk_idproduct_transaction` INT NOT NULL,
  `transactionTime` DATETIME NULL,
  `buySell` TINYINT(1) NULL,
  `price` DECIMAL(15,8) NULL,
  `quantity` DECIMAL(15,8) NULL,
  PRIMARY KEY (`idtransaction`, `fk_idproduct_transaction`),
  CONSTRAINT `fk_idproduct_transaction`
    FOREIGN KEY (`fk_idproduct_transaction`)
    REFERENCES `StockPortfolio`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `fk_idproduct_idx` ON `StockPortfolio`.`transaction` (`fk_idproduct_transaction` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `StockPortfolio`.`dayCandle`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `StockPortfolio`.`dayCandle` ;

CREATE TABLE IF NOT EXISTS `StockPortfolio`.`dayCandle` (
  `iddayCandle` INT NOT NULL AUTO_INCREMENT,
  `fk_idproduct_dayCandle` INT NOT NULL,
  `date` DATE NULL,
  `low` DECIMAL(15,8) NULL,
  `hi` DECIMAL(15,8) NULL,
  `open` DECIMAL(15,8) NULL,
  `close` DECIMAL(15,8) NULL,
  `volume` DECIMAL(15,8) NULL,
  PRIMARY KEY (`iddayCandle`, `fk_idproduct_dayCandle`),
  CONSTRAINT `fk_idproduct_dayTrade`
    FOREIGN KEY (`fk_idproduct_dayCandle`)
    REFERENCES `StockPortfolio`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `StockPortfolio`.`realTime`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `StockPortfolio`.`realTime` ;

CREATE TABLE IF NOT EXISTS `StockPortfolio`.`realTime` (
  `idrealTime` INT NOT NULL AUTO_INCREMENT,
  `fk_idproduct_realTime` INT NOT NULL,
  `observedPrice` DECIMAL(6,2) NOT NULL,
  `observedTime` DATETIME NOT NULL,
  PRIMARY KEY (`idrealTime`, `fk_idproduct_realTime`),
  CONSTRAINT `fk_idproduct_realTime`
    FOREIGN KEY (`fk_idproduct_realTime`)
    REFERENCES `StockPortfolio`.`product` (`idproduct`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

CREATE INDEX `fk_idproduct_idx` ON `StockPortfolio`.`realTime` (`fk_idproduct_realTime` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
