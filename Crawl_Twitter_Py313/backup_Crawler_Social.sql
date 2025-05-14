-- MySQL dump 10.13  Distrib 9.3.0, for Linux (x86_64)
--
-- Host: localhost    Database: Crawler_Social
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `data_keywords`
--

DROP TABLE IF EXISTS `data_keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_keywords` (
  `id` int NOT NULL AUTO_INCREMENT,
  `keyword` varchar(255) DEFAULT NULL,
  `status` int DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_keywords`
--

LOCK TABLES `data_keywords` WRITE;
/*!40000 ALTER TABLE `data_keywords` DISABLE KEYS */;
INSERT INTO `data_keywords` VALUES (1,'banker',1),(2,'techcombank',1),(3,'xe scooter',1);
/*!40000 ALTER TABLE `data_keywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_posts_twitter`
--

DROP TABLE IF EXISTS `data_posts_twitter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_posts_twitter` (
  `post_id` varchar(100) NOT NULL,
  `keyword` varchar(255) DEFAULT NULL,
  `user_id` varchar(100) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `content_created` timestamp NULL DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `url_post` varchar(300) DEFAULT NULL,
  `content` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`post_id`),
  UNIQUE KEY `unique_url_post` (`url_post`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_posts_twitter`
--

LOCK TABLES `data_posts_twitter` WRITE;
/*!40000 ALTER TABLE `data_posts_twitter` DISABLE KEYS */;
INSERT INTO `data_posts_twitter` VALUES ('1920443787618496711','banker','MaiHanh64481','LÊ THỊ MAI HẠNH','2025-05-08 18:40:53','0','1','/1900113226869960704/status/1920443787618496711','Anh chị Banker có kinh nghiệm cho em hỏi, nếu làm Sales BĐS dự án, và làm sales tín dụng ngân hàng thì cái nào hơn ạ.','2025-05-15 01:24:41'),('1920456777554145749','banker','phucc2banker','Van Phuc','2025-05-08 19:32:30','0','1','/1635154068460163072/status/1920456777554145749','@HeyTaiZen Cảm ơn anh Tài - Billion Dollar Boy ✊','2025-05-15 01:24:41'),('1920506852300742916','banker','Dani4375','Civil','2025-05-08 22:51:29','0','1','/1835310415565230080/status/1920506852300742916','@HalimaS01 Banker tu nh','2025-05-15 01:24:41'),('1920657125996437820','banker','NguynTi00401700','Hieuthuhai A.K.A','2025-05-09 08:48:37','0','1','/1366664935250399235/status/1920657125996437820','@AzuraETH @Scallop_io Banker dự án này ấn tượng quá nè 👍👍','2025-05-15 01:24:41'),('1920693681872413092','banker','longbanker66','Long Banker','2025-05-09 11:13:53','0','1','/1886611975863721984/status/1920693681872413092','@easyforshopping @suidefai @CoinTerminalCom Xin gửi lời chúc mừng đến tập thể đã tạo nên điều kỳ diệu!','2025-05-15 01:24:41'),('1920694128255381913','banker','thuybankerr','Thùy Banker','2025-05-09 11:15:39','0','1','/1886687935308947457/status/1920694128255381913','@easyforshopping @suidefai @CoinTerminalCom Một bước tiến lớn trong sự nghiệp – xin chúc mừng dự án!','2025-05-15 01:24:41'),('1921243550198473212','banker','longbanker66','Long Banker','2025-05-10 23:38:52','0','1','/1886611975863721984/status/1921243550198473212','@TronDao_VIE @justinsuntron Ngày : 30/08/2025 @justinsuntron @trondao #TRON #USDT','2025-05-15 01:24:41'),('1921243955296866608','banker','thuybankerr','Thùy Banker','2025-05-10 23:40:28','0','1','/1886687935308947457/status/1921243955296866608','@TronDao_VIE @justinsuntron Ngày : 11/10/2025 @justinsuntron @trondao #TRON #USDT','2025-05-15 01:24:41'),('1921367540753727843','banker','phucc2banker','Van Phuc','2025-05-11 07:51:33','0','1','/1635154068460163072/status/1921367540753727843','@Dantienacademy Mọi thứ đều đã được cảnh bảo cảnh báo trước khi nó xảy ra vài tuần vài tháng vài năm 👍','2025-05-15 01:24:41'),('1921418278301241433','banker','nhacaiuytinwin','Top Nhà Cái Uy Tín Nhất','2025-05-11 11:13:10','0','1','/1897201093790326787/status/1921418278301241433','Super 6 Baccarat – Kinh nghiệm chơi từ cao thủ lâu năm - Nhà Cái Uy Tín\nSuper 6 Baccarat là biến thể hấp dẫn của trò chơi baccarat truyền thống, nổi bật với tỷ lệ trả thưởng cao khi người chơi cược vào cửa Banker thắng \nNew: https://t.co/8gJaBLoQhQ https://t.co/O7myQle5rE','2025-05-15 01:24:41'),('1921810577355059667','banker','luv_myseltf','Banker','2025-05-12 13:12:01','0','1','/1383778397038399497/status/1921810577355059667','@ThenaFi_ @ThenaCN Giờ không bay được thì khi nào mới bay được nữa.','2025-05-15 01:24:41'),('1921810771895320717','banker','luv_myseltf','Banker','2025-05-12 13:12:48','0','1','/1383778397038399497/status/1921810771895320717','@ThenaFi_ @ThenaCN Hay là thôi. Kiếm coin khác cho nhanh','2025-05-15 01:24:41'),('1922166924059758666','banker','traviscremin68','𝑻𝒓𝒂𝒗𝒊𝒔','2025-05-13 12:48:01','0','1','/1577839463065358336/status/1922166924059758666','@Lecter_XFinance Đại gia banker mà than!','2025-05-15 01:24:41'),('1922190500066464031','banker','longbanker66','Long Banker','2025-05-13 14:21:42','0','1','/1886611975863721984/status/1922190500066464031','@bitgetvietnam Giá dự đoán 0.0191 UID : 1195681588','2025-05-15 01:24:41'),('1922191062132490316','banker','thuybankerr','Thùy Banker','2025-05-13 14:23:56','0','1','/1886687935308947457/status/1922191062132490316','@bitgetvietnam Giá dự đoán 0.0212 UID : 2525757114','2025-05-15 01:24:41'),('1922269055823618058','banker','july_2000_w','July béo','2025-05-13 19:33:51','0','1','/1575147275944308737/status/1922269055823618058','Tìm banker SG ạ','2025-05-15 01:24:41'),('1922269675351654442','banker','july_2000_w','July béo','2025-05-13 19:36:19','0','1','/1575147275944308737/status/1922269675351654442','Tìm nam banker ạ','2025-05-15 01:24:41');
/*!40000 ALTER TABLE `data_posts_twitter` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-14 18:44:14
