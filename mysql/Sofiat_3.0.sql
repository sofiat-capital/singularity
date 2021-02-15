-- MySQL dump 10.13  Distrib 5.7.19, for macos10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: sofiat_test
-- ------------------------------------------------------
-- Server version	5.7.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `BinanceFill`
--
use sofiat_test;
DROP TABLE IF EXISTS `BinanceFill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BinanceFill` (
  `idBinanceFill` int(11) NOT NULL AUTO_INCREMENT,
  `fk_idOrderQueue_BinanceOrder_BinanceFill` int(11) NOT NULL,
  `price` decimal(20,12) NOT NULL,
  `qty` decimal(20,12) NOT NULL,
  `commission` decimal(20,12) DEFAULT NULL,
  `commissionAsset` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`idBinanceFill`,`fk_idOrderQueue_BinanceOrder_BinanceFill`),
  KEY `fk_idOrderQueue_BinanceOrder_BinanceFill_idx` (`fk_idOrderQueue_BinanceOrder_BinanceFill`),
  CONSTRAINT `fk_idOrderQueue_BinanceOrder_BinanceFill` FOREIGN KEY (`fk_idOrderQueue_BinanceOrder_BinanceFill`) REFERENCES `BinanceOrder` (`fk_idOrderQueue_BinanceOrder`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `BinanceOrder`
--

DROP TABLE IF EXISTS `BinanceOrder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BinanceOrder` (
  `fk_idOrderQueue_BinanceOrder` int(11) NOT NULL,
  `fk_idProduct_BinanceOrder` int(11) NOT NULL,
  `orderListId` int(11) NOT NULL,
  `transactTime` datetime NOT NULL,
  `price` decimal(20,12) NOT NULL,
  `origQty` decimal(20,12) DEFAULT NULL,
  `executedQty` decimal(20,12) DEFAULT NULL,
  `cummulativeQuoteQty` decimal(20,12) DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  `timeInForce` varchar(15) DEFAULT NULL,
  `type` varchar(8) NOT NULL,
  `side` varchar(5) NOT NULL,
  PRIMARY KEY (`fk_idProduct_BinanceOrder`,`fk_idOrderQueue_BinanceOrder`),
  KEY `fk_idProduct_BinanceOrder_idx` (`fk_idProduct_BinanceOrder`),
  KEY `fk_clientOrderId_idx` (`fk_idOrderQueue_BinanceOrder`),
  CONSTRAINT `fk_idOrderQueue_BinanceOrder` FOREIGN KEY (`fk_idOrderQueue_BinanceOrder`) REFERENCES `OrderQueue` (`idOrderQueue`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_idProduct_BinanceOrder` FOREIGN KEY (`fk_idProduct_BinanceOrder`) REFERENCES `Product` (`idProduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Category`
--

DROP TABLE IF EXISTS `Category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Category` (
  `idCategory` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  PRIMARY KEY (`idCategory`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DayCandle`
--

DROP TABLE IF EXISTS `DayCandle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DayCandle` (
  `idDayCandle` int(11) NOT NULL AUTO_INCREMENT,
  `fk_idProduct_DayCandle` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `open` decimal(20,12) DEFAULT NULL,
  `hi` decimal(20,12) DEFAULT NULL,
  `low` decimal(20,12) DEFAULT NULL,
  `close` decimal(20,12) DEFAULT NULL,
  `volume` decimal(20,12) DEFAULT NULL,
  `numTrades` int(11) DEFAULT NULL,
  PRIMARY KEY (`idDayCandle`,`fk_idProduct_DayCandle`),
  KEY `fk_idProduct_DayCandle_idx` (`fk_idProduct_DayCandle`),
  CONSTRAINT `fk_idProduct_DayCandle` FOREIGN KEY (`fk_idProduct_DayCandle`) REFERENCES `Product` (`idProduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3331706 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `OrderQueue`
--

DROP TABLE IF EXISTS `OrderQueue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OrderQueue` (
  `idOrderQueue` int(11) NOT NULL AUTO_INCREMENT,
  `fk_idProduct_OrderQueue` int(11) NOT NULL,
  `side` varchar(45) NOT NULL,
  `timeCreated` datetime NOT NULL,
  `price` decimal(20,12) NOT NULL,
  `type` varchar(25) NOT NULL,
  `executed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idOrderQueue`,`fk_idProduct_OrderQueue`),
  KEY `fk_idProduct_OrderQueue_idx` (`fk_idProduct_OrderQueue`),
  KEY `fk_idBinanceOrder_OrderQueue_idx` (`executed`),
  CONSTRAINT `fk_idProduct_OrderQueue` FOREIGN KEY (`fk_idProduct_OrderQueue`) REFERENCES `Product` (`idProduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Portfolio`
--

DROP TABLE IF EXISTS `Portfolio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Portfolio` (
  `idPortfolio` int(11) NOT NULL AUTO_INCREMENT,
  `asOfDate` datetime NOT NULL,
  `valuation` decimal(20,2) NOT NULL,
  `USD` decimal(12,2) DEFAULT NULL,
  `BTC` decimal(20,12) DEFAULT NULL,
  `ETH` decimal(20,12) DEFAULT NULL,
  `LTC` decimal(20,12) DEFAULT NULL,
  PRIMARY KEY (`idPortfolio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Product` (
  `idProduct` int(11) NOT NULL AUTO_INCREMENT,
  `fk_idCategory_Product` int(11) NOT NULL,
  `ticker` varchar(15) NOT NULL,
  PRIMARY KEY (`idProduct`,`fk_idCategory_Product`),
  KEY `fk_idCategory_idx` (`fk_idCategory_Product`),
  CONSTRAINT `fk_idCategory_Product` FOREIGN KEY (`fk_idCategory_Product`) REFERENCES `Category` (`idCategory`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RealTime`
--

DROP TABLE IF EXISTS `RealTime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RealTime` (
  `idRealTime` int(11) NOT NULL AUTO_INCREMENT,
  `fk_idProduct_RealTime` int(11) NOT NULL,
  `observedPrice` decimal(20,12) NOT NULL,
  `observedTime` datetime NOT NULL,
  PRIMARY KEY (`idRealTime`,`fk_idProduct_RealTime`),
  KEY `fk_idProduct_idx` (`fk_idProduct_RealTime`),
  CONSTRAINT `fk_idProduct_RealTime` FOREIGN KEY (`fk_idProduct_RealTime`) REFERENCES `Product` (`idProduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Dumping routines for database 'sofiat_test'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-14 16:46:15
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

TRUNCATE sofiat_test.BinanceFill;
TRUNCATE sofiat_test.BinanceOrder;
TRUNCATE sofiat_test.Category;
TRUNCATE sofiat_test.DayCandle;
TRUNCATE sofiat_test.OrderQueue;
TRUNCATE sofiat_test.Portfolio;
TRUNCATE sofiat_test.Product;
TRUNCATE sofiat_test.RealTime;


/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=1 */;

