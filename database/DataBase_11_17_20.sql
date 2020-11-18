CREATE DATABASE  IF NOT EXISTS `StockPortfolio` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `StockPortfolio`;
-- MySQL dump 10.13  Distrib 8.0.22, for macos10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: StockPortfolio
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `idcategory` int NOT NULL AUTO_INCREMENT,
  `name` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`idcategory`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `idproduct` int NOT NULL AUTO_INCREMENT,
  `fk_idcategory_product` int NOT NULL,
  `ticker` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`idproduct`,`fk_idcategory_product`),
  KEY `fk_idcategory_idx` (`fk_idcategory_product`),
  CONSTRAINT `fk_idcategory_product` FOREIGN KEY (`fk_idcategory_product`) REFERENCES `category` (`idcategory`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `realTime`
--

DROP TABLE IF EXISTS `realTime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `realTime` (
  `idrealTime` int NOT NULL AUTO_INCREMENT,
  `fk_idproduct_realTime` int NOT NULL,
  `observedPrice` decimal(10,0) NOT NULL,
  `observedTime` datetime NOT NULL,
  PRIMARY KEY (`idrealTime`,`fk_idproduct_realTime`),
  KEY `fk_idproduct_idx` (`fk_idproduct_realTime`),
  CONSTRAINT `fk_idproduct_realTime` FOREIGN KEY (`fk_idproduct_realTime`) REFERENCES `product` (`idproduct`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction` (
  `idtransaction` int NOT NULL AUTO_INCREMENT,
  `fk_idproduct_transaction` int NOT NULL,
  `transactionTime` datetime DEFAULT NULL,
  `buySell` tinyint(1) DEFAULT NULL,
  `price` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`idtransaction`,`fk_idproduct_transaction`),
  KEY `fk_idproduct_idx` (`fk_idproduct_transaction`),
  CONSTRAINT `fk_idproduct_transaction` FOREIGN KEY (`fk_idproduct_transaction`) REFERENCES `product` (`idproduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-17 20:20:58
