-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: db_alpha
-- ------------------------------------------------------
-- Server version	8.0.17

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
-- Table structure for table `tbl_admin`
--

DROP TABLE IF EXISTS `tbl_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_admin` (
  `username` varchar(40) NOT NULL,
  `password` varchar(30) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_admin`
--

LOCK TABLES `tbl_admin` WRITE;
/*!40000 ALTER TABLE `tbl_admin` DISABLE KEYS */;
INSERT INTO `tbl_admin` VALUES ('alpha_squad','alpha');
/*!40000 ALTER TABLE `tbl_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_feedbackdata`
--

DROP TABLE IF EXISTS `tbl_feedbackdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_feedbackdata` (
  `fd_id` int(11) NOT NULL AUTO_INCREMENT,
  `fd_name` varchar(50) NOT NULL,
  `fd_img` varchar(250) DEFAULT NULL,
  `td_id` int(11) NOT NULL,
  `fd_file` varchar(250) NOT NULL,
  `fd_desc` varchar(200) DEFAULT NULL,
  `upload_date` date NOT NULL,
  `result_page` varchar(250) NOT NULL,
  PRIMARY KEY (`fd_id`),
  KEY `td_id` (`td_id`),
  CONSTRAINT `tbl_feedbackdata_ibfk_1` FOREIGN KEY (`td_id`) REFERENCES `tbl_trainingdata` (`td_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_feedbackdata`
--

LOCK TABLES `tbl_feedbackdata` WRITE;
/*!40000 ALTER TABLE `tbl_feedbackdata` DISABLE KEYS */;
INSERT INTO `tbl_feedbackdata` VALUES (17,'Simple','IMG20200626211826.png',42,'TD20200626211826.json','Just for debugging','2020-06-26','sample.json');
/*!40000 ALTER TABLE `tbl_feedbackdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_trainingdata`
--

DROP TABLE IF EXISTS `tbl_trainingdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_trainingdata` (
  `td_id` int(11) NOT NULL AUTO_INCREMENT,
  `td_name` varchar(50) NOT NULL,
  `td_img` varchar(250) DEFAULT NULL,
  `td_file` varchar(250) NOT NULL,
  `storage_type` int(11) NOT NULL DEFAULT '0',
  `td_desc` varchar(200) DEFAULT NULL,
  `td_model` varchar(250) DEFAULT NULL,
  `upload_date` date DEFAULT NULL,
  `model_accuracy` float DEFAULT NULL,
  PRIMARY KEY (`td_id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_trainingdata`
--

LOCK TABLES `tbl_trainingdata` WRITE;
/*!40000 ALTER TABLE `tbl_trainingdata` DISABLE KEYS */;
INSERT INTO `tbl_trainingdata` VALUES (42,'Amazon','IMG20200309210544.png','TD20200309210544.json',0,'This is DEFAULT dataset','sample.pkl','2020-03-09',97.65),(65,'Test Upload1','IMG20200725173301.png','TD20200725173301.json',0,'khuhnj','TD20200725173301.h5','2020-07-25',60.2);
/*!40000 ALTER TABLE `tbl_trainingdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_users`
--

DROP TABLE IF EXISTS `tbl_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_users` (
  `u_username` varchar(30) NOT NULL,
  `u_pwd` varchar(20) NOT NULL,
  `u_name` varchar(50) NOT NULL,
  `u_dept` varchar(20) NOT NULL DEFAULT 'N/A',
  `u_email` varchar(100) NOT NULL,
  `u_phone` varchar(15) NOT NULL,
  PRIMARY KEY (`u_username`),
  UNIQUE KEY `u_email` (`u_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_users`
--

LOCK TABLES `tbl_users` WRITE;
/*!40000 ALTER TABLE `tbl_users` DISABLE KEYS */;
INSERT INTO `tbl_users` VALUES ('asim123','0000','Asim Naqvi','Algorithms ','asim@gmail.com','9876543210'),('basant123','0000','Basant Mangal','Database','basant@gmail.com','9012457496'),('bhanu123','0000','Bhanu Chauhan','Cloud-AWS','bhanu@gmail.com','9340590344'),('gaurav123','0000','Gaurav Shukla','UI/UX','gaurav@gmail.com','9340680375'),('mimansha123','0000','Mimansha Agrawal','HR Tech','mimansha@gmail.com','8967456231');
/*!40000 ALTER TABLE `tbl_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-29 20:45:15
