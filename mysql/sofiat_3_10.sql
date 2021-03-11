-- MySQL dump 10.13  Distrib 8.0.22, for macos10.15 (x86_64)
--
-- Host: localhost    Database: sofiat
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
-- Table structure for table `binanceFill`
--

DROP TABLE IF EXISTS `binanceFill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `binanceFill` (
  `idbinanceFill` int NOT NULL AUTO_INCREMENT,
  `fk_idorderQueue_binanceOrder_binanceFill` int NOT NULL,
  `price` decimal(20,12) NOT NULL,
  `qty` decimal(20,12) NOT NULL,
  `commission` decimal(20,12) DEFAULT NULL,
  `commissionAsset` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`idbinanceFill`,`fk_idorderQueue_binanceOrder_binanceFill`),
  KEY `fk_idorderQueue_binanceOrder_binanceFill_idx` (`fk_idorderQueue_binanceOrder_binanceFill`),
  CONSTRAINT `fk_idorderQueue_binanceOrder_binanceFill` FOREIGN KEY (`fk_idorderQueue_binanceOrder_binanceFill`) REFERENCES `binanceOrder` (`fk_idorderQueue_binanceOrder`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `binanceOrder`
--

DROP TABLE IF EXISTS `binanceOrder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `binanceOrder` (
  `fk_idorderQueue_binanceOrder` int NOT NULL,
  `fk_idproduct_binanceOrder` int NOT NULL,
  `orderListId` int NOT NULL,
  `transactTime` datetime NOT NULL,
  `price` decimal(20,12) NOT NULL,
  `origQty` decimal(20,12) DEFAULT NULL,
  `executedQty` decimal(20,12) DEFAULT NULL,
  `cummulativeQuoteQty` decimal(20,12) DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  `timeInForce` varchar(15) DEFAULT NULL,
  `type` varchar(8) NOT NULL,
  `side` varchar(5) NOT NULL,
  PRIMARY KEY (`fk_idproduct_binanceOrder`,`fk_idorderQueue_binanceOrder`),
  KEY `fk_idproduct_binanceOrder_idx` (`fk_idproduct_binanceOrder`),
  KEY `fk_clientOrderId_idx` (`fk_idorderQueue_binanceOrder`),
  CONSTRAINT `fk_idorderQueue_binanceOrder` FOREIGN KEY (`fk_idorderQueue_binanceOrder`) REFERENCES `orderQueue` (`idorderQueue`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_idproduct_binanceOrder` FOREIGN KEY (`fk_idproduct_binanceOrder`) REFERENCES `product` (`idproduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `idcategory` int NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  PRIMARY KEY (`idcategory`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gains`
--

DROP TABLE IF EXISTS `gains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gains` (
  `idgainstable` int NOT NULL AUTO_INCREMENT,
  `fk_idproduct_gainsTable` int NOT NULL,
  `symbol` varchar(10) NOT NULL,
  `cycleTime` datetime NOT NULL,
  `gainPercent` decimal(20,12) NOT NULL,
  `gainAmount` decimal(10,3) NOT NULL,
  PRIMARY KEY (`idgainstable`,`fk_idproduct_gainsTable`),
  KEY `fk_idproduct_gainsTable` (`fk_idproduct_gainsTable`),
  CONSTRAINT `fk_idproduct_gainsTable` FOREIGN KEY (`fk_idproduct_gainsTable`) REFERENCES `product` (`idproduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orderQueue`
--

DROP TABLE IF EXISTS `orderQueue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderQueue` (
  `idorderQueue` int NOT NULL AUTO_INCREMENT,
  `fk_idproduct_orderQueue` int NOT NULL,
  `side` varchar(45) NOT NULL,
  `timeCreated` datetime NOT NULL,
  `price` decimal(20,12) NOT NULL,
  `executed` tinyint NOT NULL DEFAULT '0',
  `type` varchar(25) NOT NULL,
  PRIMARY KEY (`idorderQueue`,`fk_idproduct_orderQueue`),
  KEY `fk_idproduct_orderQueue_idx` (`fk_idproduct_orderQueue`),
  KEY `fk_idbinanceOrder_orderQueue_idx` (`executed`),
  CONSTRAINT `fk_idproduct_orderQueue` FOREIGN KEY (`fk_idproduct_orderQueue`) REFERENCES `product` (`idproduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=242 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `portfolio`
--

DROP TABLE IF EXISTS `portfolio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `portfolio` (
  `idportfolio` int NOT NULL AUTO_INCREMENT,
  `asOfDate` datetime NOT NULL,
  `valuation` decimal(20,2) NOT NULL,
  `USD` decimal(10,2) DEFAULT NULL,
  `BTC` decimal(10,6) DEFAULT NULL,
  `ETH` decimal(10,6) DEFAULT NULL,
  `LTC` decimal(10,6) DEFAULT NULL,
  `BNB` decimal(10,6) DEFAULT NULL,
  PRIMARY KEY (`idportfolio`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
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
  `ticker` varchar(15) NOT NULL,
  PRIMARY KEY (`idproduct`,`fk_idcategory_product`),
  KEY `fk_idcategory_idx` (`fk_idcategory_product`),
  CONSTRAINT `fk_idcategory_product` FOREIGN KEY (`fk_idcategory_product`) REFERENCES `category` (`idcategory`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-10 19:29:57
