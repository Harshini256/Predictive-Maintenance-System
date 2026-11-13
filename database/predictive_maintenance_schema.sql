-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: predictive_maintenance_db
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `dataqualityissue`
--

DROP TABLE IF EXISTS `dataqualityissue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dataqualityissue` (
  `issue_id` varchar(40) NOT NULL,
  `issue_type` varchar(60) NOT NULL,
  `related_record_id` varchar(250) DEFAULT NULL,
  `description` text NOT NULL,
  `detected_at` datetime NOT NULL,
  `ground_truth_label` varchar(50) NOT NULL,
  PRIMARY KEY (`issue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `failureevent`
--

DROP TABLE IF EXISTS `failureevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `failureevent` (
  `failure_id` varchar(40) NOT NULL,
  `machine_id` varchar(150) NOT NULL,
  `failure_time` datetime NOT NULL,
  `failure_type` varchar(100) NOT NULL,
  `severity` enum('LOW','MEDIUM','HIGH','CRITICAL') NOT NULL,
  `downtime_minutes` int NOT NULL,
  PRIMARY KEY (`failure_id`),
  KEY `idx_failure_machine_time` (`machine_id`,`failure_time`),
  CONSTRAINT `failureevent_ibfk_1` FOREIGN KEY (`machine_id`) REFERENCES `machine` (`machine_id`),
  CONSTRAINT `failureevent_chk_1` CHECK ((`downtime_minutes` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `machine`
--

DROP TABLE IF EXISTS `machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `machine` (
  `machine_id` varchar(150) NOT NULL,
  `line_id` varchar(100) NOT NULL,
  `machine_name` varchar(100) NOT NULL,
  `machine_type` varchar(50) NOT NULL,
  `installation_date` date NOT NULL,
  `status` enum('RUNNING','IDLE','STOPPED','MAINTENANCE') DEFAULT 'RUNNING',
  PRIMARY KEY (`machine_id`),
  KEY `idx_machine_line` (`line_id`),
  CONSTRAINT `machine_ibfk_1` FOREIGN KEY (`line_id`) REFERENCES `productionline` (`line_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `machinestatushistory`
--

DROP TABLE IF EXISTS `machinestatushistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `machinestatushistory` (
  `history_id` bigint NOT NULL AUTO_INCREMENT,
  `machine_id` varchar(150) NOT NULL,
  `old_status` varchar(30) DEFAULT NULL,
  `new_status` varchar(30) NOT NULL,
  `changed_at` datetime NOT NULL,
  PRIMARY KEY (`history_id`),
  KEY `machine_id` (`machine_id`),
  CONSTRAINT `machinestatushistory_ibfk_1` FOREIGN KEY (`machine_id`) REFERENCES `machine` (`machine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `maintenanceworkorder`
--

DROP TABLE IF EXISTS `maintenanceworkorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenanceworkorder` (
  `work_order_id` varchar(40) NOT NULL,
  `machine_id` varchar(150) NOT NULL,
  `technician_id` varchar(30) NOT NULL,
  `failure_id` varchar(40) DEFAULT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `maintenance_type` enum('PREVENTIVE','CORRECTIVE','INSPECTION') NOT NULL,
  `status` enum('OPEN','IN_PROGRESS','COMPLETED','CANCELLED') DEFAULT 'OPEN',
  `downtime_minutes` int DEFAULT '0',
  PRIMARY KEY (`work_order_id`),
  KEY `technician_id` (`technician_id`),
  KEY `failure_id` (`failure_id`),
  KEY `idx_workorder_machine` (`machine_id`),
  CONSTRAINT `maintenanceworkorder_ibfk_1` FOREIGN KEY (`machine_id`) REFERENCES `machine` (`machine_id`),
  CONSTRAINT `maintenanceworkorder_ibfk_2` FOREIGN KEY (`technician_id`) REFERENCES `technician` (`technician_id`),
  CONSTRAINT `maintenanceworkorder_ibfk_3` FOREIGN KEY (`failure_id`) REFERENCES `failureevent` (`failure_id`),
  CONSTRAINT `maintenanceworkorder_chk_1` CHECK (((`end_time` is null) or (`end_time` >= `start_time`)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `operatingshift`
--

DROP TABLE IF EXISTS `operatingshift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operatingshift` (
  `shift_id` varchar(30) NOT NULL,
  `plant_id` varchar(30) NOT NULL,
  `shift_name` varchar(30) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`shift_id`),
  KEY `plant_id` (`plant_id`),
  CONSTRAINT `operatingshift_ibfk_1` FOREIGN KEY (`plant_id`) REFERENCES `plant` (`plant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `part`
--

DROP TABLE IF EXISTS `part`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `part` (
  `part_id` varchar(30) NOT NULL,
  `part_name` varchar(100) NOT NULL,
  `part_type` varchar(50) NOT NULL,
  `unit_cost` decimal(12,2) NOT NULL,
  `stock_quantity` int NOT NULL,
  PRIMARY KEY (`part_id`),
  CONSTRAINT `part_chk_1` CHECK ((`unit_cost` >= 0)),
  CONSTRAINT `part_chk_2` CHECK ((`stock_quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plant`
--

DROP TABLE IF EXISTS `plant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plant` (
  `plant_id` varchar(30) NOT NULL,
  `plant_name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `capacity` int DEFAULT NULL,
  PRIMARY KEY (`plant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prediction`
--

DROP TABLE IF EXISTS `prediction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prediction` (
  `prediction_id` bigint NOT NULL AUTO_INCREMENT,
  `sensor_id` varchar(200) NOT NULL,
  `reading_value` decimal(14,4) NOT NULL,
  `predicted_label` enum('NORMAL','ABNORMAL') NOT NULL,
  `abnormal_probability` decimal(5,2) NOT NULL,
  `predicted_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `telemetry_id` varchar(250) NOT NULL,
  PRIMARY KEY (`prediction_id`),
  UNIQUE KEY `unique_telemetry_prediction` (`telemetry_id`),
  KEY `sensor_id` (`sensor_id`),
  CONSTRAINT `fk_prediction_telemetry` FOREIGN KEY (`telemetry_id`) REFERENCES `telemetryevent` (`telemetry_id`),
  CONSTRAINT `prediction_ibfk_1` FOREIGN KEY (`sensor_id`) REFERENCES `sensor` (`sensor_id`),
  CONSTRAINT `prediction_chk_1` CHECK ((`abnormal_probability` between 0 and 100))
) ENGINE=InnoDB AUTO_INCREMENT=10001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `productionline`
--

DROP TABLE IF EXISTS `productionline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productionline` (
  `line_id` varchar(100) NOT NULL,
  `plant_id` varchar(30) NOT NULL,
  `line_name` varchar(100) NOT NULL,
  `status` enum('ACTIVE','INACTIVE') DEFAULT 'ACTIVE',
  `production_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`line_id`),
  KEY `plant_id` (`plant_id`),
  CONSTRAINT `productionline_ibfk_1` FOREIGN KEY (`plant_id`) REFERENCES `plant` (`plant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sensor`
--

DROP TABLE IF EXISTS `sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor` (
  `sensor_id` varchar(200) NOT NULL,
  `machine_id` varchar(150) NOT NULL,
  `sensor_type` enum('TEMPERATURE','VIBRATION','PRESSURE','HUMIDITY','CURRENT') NOT NULL,
  `unit` varchar(20) NOT NULL,
  `min_range` decimal(12,2) NOT NULL,
  `max_range` decimal(12,2) NOT NULL,
  `installed_at` datetime NOT NULL,
  `status` enum('ACTIVE','INACTIVE','FAULTY') DEFAULT 'ACTIVE',
  PRIMARY KEY (`sensor_id`),
  KEY `idx_sensor_machine` (`machine_id`),
  CONSTRAINT `sensor_ibfk_1` FOREIGN KEY (`machine_id`) REFERENCES `machine` (`machine_id`),
  CONSTRAINT `sensor_chk_1` CHECK ((`min_range` < `max_range`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `technician`
--

DROP TABLE IF EXISTS `technician`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `technician` (
  `technician_id` varchar(30) NOT NULL,
  `technician_name` varchar(100) NOT NULL,
  `specialization` varchar(50) NOT NULL,
  `availability_status` enum('AVAILABLE','BUSY','INACTIVE') DEFAULT 'AVAILABLE',
  `experience_years` int DEFAULT NULL,
  PRIMARY KEY (`technician_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `telemetryevent`
--

DROP TABLE IF EXISTS `telemetryevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telemetryevent` (
  `telemetry_id` varchar(250) NOT NULL,
  `sensor_id` varchar(200) NOT NULL,
  `recorded_at` datetime NOT NULL,
  `reading_value` decimal(14,4) NOT NULL,
  `operating_state` enum('RUNNING','IDLE','STOPPED') NOT NULL DEFAULT 'RUNNING',
  `shift_id` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`telemetry_id`),
  UNIQUE KEY `sensor_id` (`sensor_id`,`recorded_at`),
  KEY `shift_id` (`shift_id`),
  CONSTRAINT `telemetryevent_ibfk_1` FOREIGN KEY (`sensor_id`) REFERENCES `sensor` (`sensor_id`),
  CONSTRAINT `telemetryevent_ibfk_2` FOREIGN KEY (`shift_id`) REFERENCES `operatingshift` (`shift_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workorderpart`
--

DROP TABLE IF EXISTS `workorderpart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workorderpart` (
  `work_order_id` varchar(40) NOT NULL,
  `part_id` varchar(30) NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`work_order_id`,`part_id`),
  KEY `part_id` (`part_id`),
  CONSTRAINT `workorderpart_ibfk_1` FOREIGN KEY (`work_order_id`) REFERENCES `maintenanceworkorder` (`work_order_id`),
  CONSTRAINT `workorderpart_ibfk_2` FOREIGN KEY (`part_id`) REFERENCES `part` (`part_id`),
  CONSTRAINT `workorderpart_chk_1` CHECK ((`quantity` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workorderstatushistory`
--

DROP TABLE IF EXISTS `workorderstatushistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workorderstatushistory` (
  `history_id` bigint NOT NULL AUTO_INCREMENT,
  `work_order_id` varchar(40) NOT NULL,
  `old_status` varchar(30) DEFAULT NULL,
  `new_status` varchar(30) NOT NULL,
  `changed_at` datetime NOT NULL,
  PRIMARY KEY (`history_id`),
  KEY `work_order_id` (`work_order_id`),
  CONSTRAINT `workorderstatushistory_ibfk_1` FOREIGN KEY (`work_order_id`) REFERENCES `maintenanceworkorder` (`work_order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-13 15:39:50
