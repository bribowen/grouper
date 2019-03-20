-- MySQL dump 10.13  Distrib 8.0.15, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: grouper
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interest`
--

DROP TABLE IF EXISTS `interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `interest` (
  `interest_id` int(11) NOT NULL AUTO_INCREMENT,
  `interest_name` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`interest_id`),
  UNIQUE KEY `interest_name` (`interest_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interest`
--

LOCK TABLES `interest` WRITE;
/*!40000 ALTER TABLE `interest` DISABLE KEYS */;
INSERT INTO `interest` VALUES (4,'Art/Media/Communication'),(3,'Emerging Technology'),(8,'Event Management'),(2,'Finance'),(5,'Healthcare'),(1,'Marketing'),(7,'Science'),(6,'Student Affairs');
/*!40000 ALTER TABLE `interest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participation`
--

DROP TABLE IF EXISTS `participation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `participation` (
  `project_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `role` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`project_id`,`member_id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `participation_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `profile` (`uin`),
  CONSTRAINT `participation_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participation`
--

LOCK TABLES `participation` WRITE;
/*!40000 ALTER TABLE `participation` DISABLE KEYS */;
INSERT INTO `participation` VALUES (1,1,'Member'),(1,2,'Member'),(1,3,'Member'),(1,4,'Leader'),(1,73,'Advisor'),(2,5,'Member'),(2,7,'Leader'),(2,64,'Advisor'),(3,6,'Member'),(3,15,'Leader'),(3,65,'Advisor'),(4,7,'Member'),(4,8,'Member'),(4,9,'Member'),(4,32,'Leader'),(4,66,'Advisor'),(5,54,'Leader'),(5,55,'Member'),(5,67,'Advisor'),(6,46,'Leader'),(6,47,'Member'),(6,48,'Member'),(6,68,'Advisor');
/*!40000 ALTER TABLE `participation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `profile` (
  `uin` int(11) NOT NULL AUTO_INCREMENT,
  `email_address` varchar(120) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `first_name` varchar(120) DEFAULT NULL,
  `last_name` varchar(120) DEFAULT NULL,
  `user_persona_type` varchar(60) DEFAULT NULL,
  `primary_contact` varchar(60) DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `about_me` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`uin`),
  UNIQUE KEY `email_address` (`email_address`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile`
--

LOCK TABLES `profile` WRITE;
/*!40000 ALTER TABLE `profile` DISABLE KEYS */;
INSERT INTO `profile` VALUES (1,'brianbowen@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Brian','Bowen','Admin','9992112228','2019-03-17 19:40:13','Donkeys'),(2,'apooravjain@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Apoorav','Jain','Student','4850285869',NULL,NULL),(3,'harikrishnan@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Hari','Krishnan','Student','3906964929',NULL,NULL),(4,'joshuamohan@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Joshua','Mohan','Student','3959104950',NULL,NULL),(5,'sahilsarvadeva@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Sahil','Sarvadeva','Student','5967905932',NULL,NULL),(6,'siddharthmurali@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Siddharth','Murali','Student','2304858606',NULL,NULL),(7,'amishabattha@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Amisha','Battha','Student','2945690810',NULL,NULL),(8,'aishwaryahabib@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Aishwarya','Habib','Student','3980681848',NULL,NULL),(9,'violinmohandas@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Violin','Mohandas','Student','5291948591',NULL,NULL),(10,'amitmendiratta@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Amit','Mendiratta','Student','3904857191',NULL,NULL),(11,'shreyashpatmase@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Shreyash','Patmase','Student','3450381909',NULL,NULL),(12,'sumeerangra@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Sumeer','Angra','Student','9309999222',NULL,NULL),(13,'divyeshbatra@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Divyesh','Batra','Student','5520192444',NULL,NULL),(14,'abolimahajan@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Aboli','Mahajan','Student','3948111122',NULL,NULL),(15,'shikhakhandelwal@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Shikha','Khandelwal','Student','9992112222',NULL,NULL),(16,'sateendradey@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Sateendra','Dey','Student','9992112223',NULL,NULL),(17,'neeleshjayaraman@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Neelesh','Jayaraman','Student','9992112224',NULL,NULL),(18,'namithasreenatha@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Namitha','Sreenatha','Student','9992112225',NULL,NULL),(19,'swatigangwani@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Swati','Gangwani','Student','9992112226',NULL,NULL),(20,'yeshwanthnagaraja@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Yeshwanth','Nagaraja','Student','9992112227',NULL,NULL),(21,'debparnadas@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Debparna','Das','Student','9992112229',NULL,NULL),(22,'puneetgupta@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Puneet','Gupta','Student','9992112230',NULL,NULL),(23,'ashimasharma@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Ashima','Sharma','Student','9992112231',NULL,NULL),(24,'prashanthijawahar@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Prashanthi','Jawahar','Student','9992112232',NULL,NULL),(25,'pranjalgururani@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Pranjal','Gururani','Student','9992112233',NULL,NULL),(26,'swapnil@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Swapnil','','Student','9992112234',NULL,NULL),(27,'markwang@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Mark','Wang','Student','9992112235',NULL,NULL),(28,'tejasivashishtha@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Tejasi','Vashishtha','Student','9992112236',NULL,NULL),(29,'subodhghuge@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Subodh','Ghuge','Student','9992112237',NULL,NULL),(30,'vertikasharma@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Vertika','Sharma','Student','9992112238',NULL,NULL),(31,'abhishakedixit@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Abhishake','Dixit','Student','9992112239',NULL,NULL),(32,'amitamenon@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Amita','Menon','Student','9992112240',NULL,NULL),(33,'kripadixit@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Kripa','Dixit','Student','9992112241',NULL,NULL),(34,'ramyashrimartha@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Ramyashri','Martha','Student','9992112242',NULL,NULL),(35,'sumithasrajani@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Sumit','Hasrajani','Student','9992112243',NULL,NULL),(36,'swatiawasthi@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Swati','Awasthi','Student','9992112244',NULL,NULL),(37,'varshakampli@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Varsha','Kampli','Student','9992112245',NULL,NULL),(38,'mravi@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','M','Ravi','Student','9992112246',NULL,NULL),(39,'nikhilgupta@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Nikhil','Gupta','Student','9992112247',NULL,NULL),(40,'varunsood@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Varun','Sood','Student','9992112248',NULL,NULL),(41,'nehadeshpande@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Neha','Deshpande','Student','9992112249',NULL,NULL),(42,'harshikathusu@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Harshika','Thusu','Student','9992112250',NULL,NULL),(43,'shantanutiwari@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Shantanu','Tiwari','Student','9992112251',NULL,NULL),(44,'shivanisharma@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Shivani','Sharma','Student','9992112252',NULL,NULL),(45,'himanshikhandelwal@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Himanshi','Khandelwal','Student','9992112253',NULL,NULL),(46,'nupursinha@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Nupur','Sinha','Student','9992112254',NULL,NULL),(47,'sushreejena@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Sushree','Jena','Student','9992112255',NULL,NULL),(48,'nayanpramod@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Nayan','Pramod','Student','9992112256',NULL,NULL),(49,'shilpasubramanian@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Shilpa','Subramanian','Student','9992112257',NULL,NULL),(50,'sudeeptadas@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Sudeepta','Das','Student','9992112258',NULL,NULL),(51,'nehagarg@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Neha','Garg','Student','9992112259',NULL,NULL),(52,'akshatverma@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Akshat','Verma','Student','9992112260',NULL,NULL),(53,'valliappanpethaperumal@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Valliappan','Pethaperumal','Student','9992112261',NULL,NULL),(54,'jennafranz@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Jenna','Franz','Student','9992112262',NULL,NULL),(55,'ayushdubey@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Ayush','Dubey','Student','9992112263',NULL,NULL),(56,'poojaraj@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Pooja','Raj','Student','9992112264',NULL,NULL),(57,'prekshabeohar@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Preksha','Beohar','Student','9992112265',NULL,NULL),(58,'saniashetty@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Sania','Shetty','Student','9992112266',NULL,NULL),(59,'poojawalia@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Pooja','Walia','Student','9992112267',NULL,NULL),(60,'ankittripathi@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Ankit','Tripathi','Student','9992112268',NULL,NULL),(61,'ninadsapate@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Ninad','Sapate','Student','9992112269',NULL,NULL),(62,'bisweshpachauli@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Biswesh','Pachauli','Student','9992112270',NULL,NULL),(63,'aaronbecker@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Aaron','Becker','Faculty','9992112271',NULL,NULL),(64,'matthewmanley@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Matthew','Manley','Faculty','9992112272',NULL,NULL),(65,'dwaynewhitten@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Dwayne','Whitten','Faculty','9992112273',NULL,NULL),(66,'davidgomillion@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','David','Gomillion','Faculty','9992112274',NULL,NULL),(67,'arunsen@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Arun','Sen','Faculty','9992112275',NULL,NULL),(68,'ravisen@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Ravi','Sen','Faculty','9992112276',NULL,NULL),(69,'mikyoungjung@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Mikyoung','Jung','Faculty','9992112277',NULL,NULL),(70,'nazou@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Na','Zou','Faculty','9992112278',NULL,NULL),(71,'faronkincheloe@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Faron','Kincheloe','Faculty','9992112279',NULL,NULL),(72,'thomasjamieson@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Thomas','Jamieson','Faculty','9992112280',NULL,NULL),(73,'andrearaujo@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Andre','Araujo','Faculty','9992112281',NULL,NULL),(74,'courtneyfoster@tamu.edu','xxxxxxxxxxxxxxxxxxxxxxx','Courtney','Foster','Faculty','9992112282',NULL,NULL);
/*!40000 ALTER TABLE `profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_interest`
--

DROP TABLE IF EXISTS `profile_interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `profile_interest` (
  `interest_id` int(11) NOT NULL,
  `uin` int(11) NOT NULL,
  PRIMARY KEY (`interest_id`,`uin`),
  KEY `uin` (`uin`),
  CONSTRAINT `profile_interest_ibfk_1` FOREIGN KEY (`interest_id`) REFERENCES `interest` (`interest_id`),
  CONSTRAINT `profile_interest_ibfk_2` FOREIGN KEY (`uin`) REFERENCES `profile` (`uin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_interest`
--

LOCK TABLES `profile_interest` WRITE;
/*!40000 ALTER TABLE `profile_interest` DISABLE KEYS */;
INSERT INTO `profile_interest` VALUES (1,1),(7,1),(1,2),(1,3),(2,3),(1,4),(1,5),(4,5),(1,6),(1,7),(2,7),(1,8),(6,8),(1,9),(1,10),(3,10),(6,10),(1,11),(3,11),(1,12),(1,13),(2,13),(7,13),(1,14),(3,14),(1,15),(3,15),(6,15),(1,16),(4,16),(1,17),(6,17),(1,18),(2,18),(3,18),(1,19),(3,19),(1,20),(1,21),(5,21),(1,22),(3,22),(6,22),(1,23),(2,23),(3,23),(1,24),(7,25),(3,26),(3,27),(4,27),(2,29),(6,29),(3,30),(3,31),(2,33),(6,33),(8,33),(3,34),(3,35),(6,36),(7,37),(3,38),(4,38),(3,39),(2,40),(8,41),(3,42),(5,42),(2,43),(3,43),(6,43),(3,46),(4,49),(3,50),(6,50),(2,51),(2,53),(3,54),(6,57),(3,58),(4,60),(2,62),(3,62),(2,63),(5,63),(6,64),(4,65),(3,66),(3,68),(3,70),(4,71),(6,71),(2,73),(3,74);
/*!40000 ALTER TABLE `profile_interest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile_skill`
--

DROP TABLE IF EXISTS `profile_skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `profile_skill` (
  `skill_id` int(11) NOT NULL,
  `uin` int(11) NOT NULL,
  PRIMARY KEY (`skill_id`,`uin`),
  KEY `uin` (`uin`),
  CONSTRAINT `profile_skill_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skill` (`skill_id`),
  CONSTRAINT `profile_skill_ibfk_2` FOREIGN KEY (`uin`) REFERENCES `profile` (`uin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile_skill`
--

LOCK TABLES `profile_skill` WRITE;
/*!40000 ALTER TABLE `profile_skill` DISABLE KEYS */;
INSERT INTO `profile_skill` VALUES (1,1),(1,2),(1,3),(2,3),(1,4),(1,5),(4,5),(1,6),(1,7),(2,7),(1,8),(6,8),(1,9),(1,10),(3,10),(6,10),(1,11),(3,11),(1,12),(1,13),(2,13),(1,14),(3,14),(1,15),(3,15),(6,15),(1,16),(4,16),(1,17),(6,17),(1,18),(2,18),(3,18),(1,19),(3,19),(1,20),(1,21),(5,21),(1,22),(3,22),(6,22),(1,23),(2,23),(3,23),(1,24),(3,26),(3,27),(4,27),(2,29),(6,29),(3,30),(3,31),(2,33),(6,33),(3,34),(3,35),(6,36),(3,38),(4,38),(3,39),(2,40),(3,42),(5,42),(2,43),(3,43),(6,43),(3,46),(4,49),(3,50),(6,50),(2,51),(2,53),(3,54),(6,57),(3,58),(4,60),(2,62),(3,62),(2,63),(5,63),(6,64),(4,65),(3,66),(3,68),(3,70),(4,71),(6,71),(2,73),(3,74);
/*!40000 ALTER TABLE `profile_skill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `project` (
  `project_id` int(11) NOT NULL AUTO_INCREMENT,
  `original_poster` int(11) DEFAULT NULL,
  `project_name` varchar(120) DEFAULT NULL,
  `project_type` varchar(120) DEFAULT NULL,
  `project_description` varchar(500) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  KEY `ix_project_original_poster` (`original_poster`),
  KEY `ix_project_timestamp` (`timestamp`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`original_poster`) REFERENCES `profile` (`uin`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,4,'Grouper','Application Development','Application to assist in forming project group',NULL),(2,7,'PostIt','Online Retail','Website to buy bike posters',NULL),(3,15,'RentAHome','Database Mangement','Building a database to track properties for rent',NULL),(4,32,'TagAlong','Application Development','Ride sharing service',NULL),(5,54,'MixItUp','Machine Learning','Application to recommend local bars',NULL),(6,46,'InstaExplore','Database Mangement','Service to track trending posts',NULL);
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skill`
--

DROP TABLE IF EXISTS `skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `skill` (
  `skill_id` int(11) NOT NULL AUTO_INCREMENT,
  `skill_name` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`skill_id`),
  UNIQUE KEY `skill_name` (`skill_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skill`
--

LOCK TABLES `skill` WRITE;
/*!40000 ALTER TABLE `skill` DISABLE KEYS */;
INSERT INTO `skill` VALUES (4,'App Programming'),(2,'Data Analysis'),(1,'Database Design'),(5,'Documentation'),(6,'Presentation'),(3,'Web Development');
/*!40000 ALTER TABLE `skill` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-18 10:35:54
