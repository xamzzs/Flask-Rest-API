-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: esportsdb
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game` (
  `game_id` int NOT NULL AUTO_INCREMENT,
  `game_name` varchar(50) NOT NULL,
  `game_type` varchar(45) NOT NULL,
  PRIMARY KEY (`game_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `game` VALUES (1,'Mobile Legends','MOBA'),(2,'Dota 2','MOBA'),(3,'Valorant','FPS'),(4,'League of Legends','MOBA'),(5,'Call of Duty: Mobile','FPS'),(6,'PUBG Mobile','Battle Royale'),(7,'Wild Rift','MOBA'),(8,'Free Fire','Battle Royale'),(9,'CS:GO','FPS'),(10,'Fortnite','Battle Royale'),(11,'Apex Legends','Battle Royale'),(12,'Overwatch','FPS'),(13,'Genshin Impact','RPG'),(14,'FIFA 24','Sports'),(15,'NBA 2K24','Sports'),(16,'Among Us','Social Deduction'),(17,'Clash Royale','Strategy'),(18,'Hearthstone','Card Game'),(19,'Minecraft','Sandbox'),(20,'League of Legends: Wild Rift','MOBA');
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `player_id` int NOT NULL AUTO_INCREMENT,
  `ingame_name` varchar(50) NOT NULL,
  `gaming_role` varchar(50) NOT NULL,
  `team_id` int NOT NULL,
  `joined_date` date NOT NULL,
  `real_name` varchar(45) NOT NULL,
  PRIMARY KEY (`player_id`),
  KEY `players_ibfk_1` (`team_id`),
  CONSTRAINT `players_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (1,'Inferno Crimson','Top Laner',1,'2022-01-15','Yodj Estares'),(2,'Paalee','Top Laner',2,'2021-07-10','Ralph Angelo Badang'),(3,'Baji','Gold Laner',3,'2022-03-22','Russel Cabailo'),(4,'DatuJustineNabuntoran','Rizzler',4,'2023-01-05','Datu James Lachica'),(5,'Hesuyasu','Jungler',5,'2021-11-11','Edrian Bantog'),(6,'Ji-Ar','Jack Of All Trades',6,'2022-06-18','Jon Vitug'),(7,'Agonie','Top Laner',7,'2023-02-14','Carl De Castro'),(8,'BananaPeel','Carry',8,'2021-12-10','Miguel Ramos'),(9,'KeyboardWarrior','Support',9,'2022-08-25','Andres Santos'),(10,'PotatoAim','DPS',10,'2023-03-05','Daniel Reyes'),(11,'LagMaster','Tank',11,'2022-05-30','Erik Tan'),(12,'ChickenLover','Mid Laner',12,'2021-09-12','Luis Fernandez'),(13,'PizzaSlicer','Sniper',13,'2023-04-01','Ramon Cruz'),(14,'CouchPotato','Carry',14,'2022-02-11','Victor Morales'),(15,'AFKWizard','Support',15,'2021-08-28','Henry Lim'),(16,'SpamLord','DPS',16,'2020-09-15','Carlos Mendoza'),(17,'Duckinator','Tank',17,'2023-06-09','Julian Perez'),(18,'CheeseWizard','Mid Laner',18,'2022-12-12','Antonio Flores'),(19,'LaggingLegend','Sniper',19,'2021-07-19','Miguel Santos'),(20,'SausageKing','Carry',20,'2023-01-01','Ricardo Bautista');
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team` (
  `team_id` int NOT NULL AUTO_INCREMENT,
  `team_name` varchar(50) NOT NULL,
  `game_id` int NOT NULL,
  `active_players` int NOT NULL,
  PRIMARY KEY (`team_id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `team_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `game` (`game_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES (1,'Bren Esports',1,5),(2,'OMEGA Esports',2,5),(3,'Blacklist International',1,5),(4,'Execration',2,5),(5,'TNC Predator',2,5),(6,'Shadow Wolves',3,5),(7,'Iron Titans',4,6),(8,'Crimson Hawks',1,10),(9,'Golden Dragons',2,7),(10,'Phantom Ninjas',3,5),(11,'Storm Breakers',4,10),(12,'Cyber Spartans',1,10),(13,'Fury Kings',2,7),(14,'Night Owls',3,6),(15,'Venom Vipers',4,6),(16,'Titan Slayers',1,6),(17,'Lunar Wolves',2,6),(18,'Solar Phoenix',3,6),(19,'Obsidian Knights',4,7),(20,'Crimson Serpents',1,8);
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-23 14:13:14
