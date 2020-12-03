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
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'crypto');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `dayCandle`
--

LOCK TABLES `dayCandle` WRITE;
/*!40000 ALTER TABLE `dayCandle` DISABLE KEYS */;
/*!40000 ALTER TABLE `dayCandle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,1,'BTCUSDT');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `realTime`
--

LOCK TABLES `realTime` WRITE;
/*!40000 ALTER TABLE `realTime` DISABLE KEYS */;
INSERT INTO `realTime` VALUES (2,1,17824.33475294,'2020-11-18 22:48:06'),(3,1,17825.13141198,'2020-11-18 22:48:17'),(4,1,17827.41370118,'2020-11-18 22:48:28'),(5,1,17828.87832574,'2020-11-18 22:48:39'),(6,1,17829.52918992,'2020-11-18 22:48:50'),(7,1,17830.98075096,'2020-11-18 22:49:01'),(8,1,17833.99567976,'2020-11-18 22:49:11'),(9,1,17835.05844709,'2020-11-18 22:49:22'),(10,1,17836.45379089,'2020-11-18 22:49:33'),(11,1,17837.24348763,'2020-11-18 22:49:44'),(12,1,17838.78099640,'2020-11-18 22:49:55'),(13,1,17838.92562456,'2020-11-18 22:50:06'),(14,1,17839.17362335,'2020-11-18 22:50:17'),(15,1,17842.29533612,'2020-11-18 22:50:28'),(16,1,17843.22894401,'2020-11-18 22:50:39'),(17,1,17844.94119290,'2020-11-18 22:50:50'),(18,1,17845.46927884,'2020-11-18 22:51:01'),(19,1,17845.65050007,'2020-11-18 22:51:12'),(20,1,17846.01190825,'2020-11-18 22:51:23'),(21,1,17845.93986895,'2020-11-18 22:51:34'),(22,1,17844.75944565,'2020-11-18 22:51:45'),(23,1,17844.35642996,'2020-11-18 22:51:55'),(24,1,18636.06709261,'2020-11-20 17:58:38');
/*!40000 ALTER TABLE `realTime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-20 19:08:02