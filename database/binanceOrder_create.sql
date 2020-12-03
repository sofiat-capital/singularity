CREATE TABLE `binanceOrder` (
  `idbinanceOrder` int NOT NULL,
  `fk_idproduct_binanceOrder` int NOT NULL,
  `orderListId` int NOT NULL,
  `clientOrderId` varchar(15) DEFAULT NULL,
  `transactTime` datetime DEFAULT NULL,
  `price` decimal(20, 12) DEFAULT NULL,
  `origQty` decimal(20, 12) DEFAULT NULL,
  `executedQty` decimal(20, 12) DEFAULT NULL,
  `cummulativeQuoteQty` decimal(20, 12) DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  `timeInForce` varchar(15) DEFAULT NULL,
  `type` varchar(8) DEFAULT NULL,
  `side` varchar(8) DEFAULT NULL,

  PRIMARY KEY (`idbinanceOrder`),
  KEY `fk_idproduct_dayTrade` (`fk_idproduct_dayCandle`),
  CONSTRAINT `fk_idproduct_dayTrade` FOREIGN KEY (`fk_idproduct_dayCandle`) REFERENCES `product` (`idproduct`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5007 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--