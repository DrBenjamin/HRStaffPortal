CREATE DATABASE  IF NOT EXISTS `benbox` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `benbox`;
-- MySQL dump 10.13  Distrib 8.0.28, for macos11 (x86_64)
--
-- Host: 127.0.0.1    Database: benbox
-- ------------------------------------------------------
-- Server version	8.0.29

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
-- Table structure for table `CATEGORIES`
--

DROP TABLE IF EXISTS `CATEGORIES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CATEGORIES` (
  `ID` int NOT NULL,
  `CATEGORY_ID` varchar(45) DEFAULT NULL,
  `CATEGORY_DESCRIPTION` varchar(45) DEFAULT NULL,
  `CATEGORY_SUB_ID` varchar(45) DEFAULT NULL,
  `CATEGORY_SUB_DESCRIPTION` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CATEGORIES`
--

LOCK TABLES `CATEGORIES` WRITE;
/*!40000 ALTER TABLE `CATEGORIES` DISABLE KEYS */;
INSERT INTO `CATEGORIES` VALUES (1,'00001','HR Staff Portal',NULL,NULL),(2,'00002','Workshops',NULL,NULL),(3,'00003','Car Fleet Management',NULL,NULL),(4,NULL,NULL,'00001','General'),(5,NULL,NULL,'00002','User Interface'),(6,NULL,NULL,'00003','Technical'),(7,NULL,NULL,'00004','Logical');
/*!40000 ALTER TABLE `CATEGORIES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FAQ`
--

DROP TABLE IF EXISTS `FAQ`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FAQ` (
  `ID` int NOT NULL,
  `QUESTION_ID` varchar(45) DEFAULT NULL,
  `HANDBOOK_ID` varchar(45) DEFAULT NULL,
  `FAQ_ID` varchar(45) DEFAULT NULL,
  `FAQ_ANSWER` varchar(4000) DEFAULT NULL,
  `FAQ_ANSWER_SUMMARY` varchar(200) DEFAULT NULL,
  `FAQ_ANSWER_LANGUAGE` varchar(45) DEFAULT NULL,
  `FAQ_HITS` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FAQ`
--

LOCK TABLES `FAQ` WRITE;
/*!40000 ALTER TABLE `FAQ` DISABLE KEYS */;
/*!40000 ALTER TABLE `FAQ` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HANDBOOK_ADMIN`
--

DROP TABLE IF EXISTS `HANDBOOK_ADMIN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HANDBOOK_ADMIN` (
  `ID` int NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HANDBOOK_ADMIN`
--

LOCK TABLES `HANDBOOK_ADMIN` WRITE;
/*!40000 ALTER TABLE `HANDBOOK_ADMIN` DISABLE KEYS */;
/*!40000 ALTER TABLE `HANDBOOK_ADMIN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HANDBOOK_STRUCTURE`
--

DROP TABLE IF EXISTS `HANDBOOK_STRUCTURE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HANDBOOK_STRUCTURE` (
  `ID` int NOT NULL,
  `HANDBOOK_CHAPTER_ID` varchar(45) DEFAULT NULL,
  `HANDBOOK_CHAPTER_DESCRIPTION` varchar(45) DEFAULT NULL,
  `HANDBOOK_PARAGRAPH_ID` varchar(45) DEFAULT NULL,
  `HANDBOOK_PARAGRAPH_DESCRIPTION` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HANDBOOK_STRUCTURE`
--

LOCK TABLES `HANDBOOK_STRUCTURE` WRITE;
/*!40000 ALTER TABLE `HANDBOOK_STRUCTURE` DISABLE KEYS */;
INSERT INTO `HANDBOOK_STRUCTURE` VALUES (1,'00001','Introduction',NULL,NULL),(2,'00002','User Interface',NULL,NULL),(3,'00003','Technical',NULL,NULL),(4,'00004','Logical',NULL,NULL),(5,NULL,NULL,'00001','Purpose'),(6,NULL,NULL,'00002','End User');
/*!40000 ALTER TABLE `HANDBOOK_STRUCTURE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HANDBOOK_USER`
--

DROP TABLE IF EXISTS `HANDBOOK_USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HANDBOOK_USER` (
  `ID` int NOT NULL,
  `HANDBOOK_ID` varchar(45) DEFAULT NULL,
  `CATEGORY_ID` varchar(45) DEFAULT NULL,
  `CATEGORY_SUB_ID` varchar(45) DEFAULT NULL,
  `HANDBOOK_CHAPTER` int DEFAULT NULL,
  `HANDBOOK_PARAGRAPH` int DEFAULT NULL,
  `HANDBOOK_KEYWORD1` varchar(45) DEFAULT NULL,
  `HANDBOOK_KEYWORD2` varchar(45) DEFAULT NULL,
  `HANDBOOK_KEYWORD3` varchar(45) DEFAULT NULL,
  `HANDBOOK_KEYWORD4` varchar(45) DEFAULT NULL,
  `HANDBOOK_KEYWORD5` varchar(45) DEFAULT NULL,
  `HANDBOOK_SUMMARY` varchar(200) DEFAULT NULL,
  `HANDBOOK_TEXT` varchar(4000) DEFAULT NULL,
  `HANDBOOK_TEXT_LANGUAGE` varchar(45) DEFAULT NULL,
  `HANDBOOK_HITS` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HANDBOOK_USER`
--

LOCK TABLES `HANDBOOK_USER` WRITE;
/*!40000 ALTER TABLE `HANDBOOK_USER` DISABLE KEYS */;
INSERT INTO `HANDBOOK_USER` VALUES (1,'00001','00001','00001',1,1,'Purpose','Functions','Tool','Data','Employee','Tool to view, analyze and alter employee data.','The HR Stafff Portal is a tool for Human Resource stafff to view, analyze and alter employee data. It contains master data like name, address and age. Because of this the employee data is protected. Just staff who have an account can login and use the data.','en',NULL);
/*!40000 ALTER TABLE `HANDBOOK_USER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `QUESTIONS`
--

DROP TABLE IF EXISTS `QUESTIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `QUESTIONS` (
  `ID` int NOT NULL,
  `QUESTION_ID` varchar(45) DEFAULT NULL,
  `QUESTION_CATEGORY` varchar(45) DEFAULT NULL,
  `QUESTION_CATEGORY_SUB` varchar(45) DEFAULT NULL,
  `QUESTION_KEYWORD1` varchar(45) DEFAULT NULL,
  `QUESTION_KEYWORD2` varchar(45) DEFAULT NULL,
  `QUESTION_KEYWORD3` varchar(45) DEFAULT NULL,
  `QUESTION_KEYWORD4` varchar(45) DEFAULT NULL,
  `QUESTION_KEYWORD5` varchar(45) DEFAULT NULL,
  `QUESTION_SUMMARY` varchar(200) DEFAULT NULL,
  `QUESTION_TEXT` varchar(4000) DEFAULT NULL,
  `QUESTION_TEXT_LANGUAGE` varchar(4000) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `QUESTIONS`
--

LOCK TABLES `QUESTIONS` WRITE;
/*!40000 ALTER TABLE `QUESTIONS` DISABLE KEYS */;
INSERT INTO `QUESTIONS` VALUES (1,'00001','00003','00002','Trips','Input','Find','Where','Do','Input Trips','Where do I find the Trips input?','en'),(2,'00002','00001','00001','Car','Fleet','System','Purpose','What','Manage car fleet','What is the purpose of the car fleet system?','en'),(3,'00003','00001','00001','Hr staff portal','Hr','HR','HR','Portal','Manage personnel data','What is thew purpose of the HR Staff Portal tool?','en'),(4,'00004','00001','00001','Hr staff portal','Hr','HR','HR','Portal','HR Staff Support','What is thew purpose of the HR Staff Portal tool?','en'),(5,'00005','00001','00001','Hr staff portal','Hr','HR','HR','Portal','Manage staff data','What is thew purpose of the HR Staff Portal tool?','en'),(6,'00006','00001','00001','Hr staff portal','Hr','HR','HR','Portal','HR staff support','What is thew purpose of the HR Staff Portal tool?','en'),(7,'00007','00001','00001','Hr staff portal','Hr','Portal','Functionality','Staff','HR staff access','What is the functionality of the HR Staff Portal?','en');
/*!40000 ALTER TABLE `QUESTIONS` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-21  4:03:06
