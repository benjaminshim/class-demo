-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 23, 2023 at 04:38 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `csv_db 6`
--

-- --------------------------------------------------------

--
-- Table structure for table `one_star_michelin_restaurants`
--

CREATE TABLE `one_star_michelin_restaurants` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(51) DEFAULT NULL,
  `Year` varchar(4) DEFAULT NULL,
  `City` varchar(30) DEFAULT NULL,
  `Region` varchar(14) DEFAULT NULL,
  `Zip` varchar(8) DEFAULT NULL,
  `Cuisine` varchar(21) DEFAULT NULL,
  `Price` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `one_star_michelin_restaurants`
--

INSERT INTO `one_star_michelin_restaurants` (`Name`, `Year`, `City`, `Region`, `Zip`, `Cuisine`, `Price`) VALUES
('name', 'year', 'city', 'region', 'zipCode', 'cuisine', 'price'),
('Kilian Stuba', '2019', 'Kleinwalsertal', 'Austria', '87568', 'Creative', '$$$$$'),
('Pfefferschiff', '2019', 'Hallwang', 'Austria', '5300', 'Classic cuisine', '$$$$$'),
('Esszimmer', '2019', 'Salzburg', 'Austria', '5020', 'Creative', '$$$$$'),
('Carpe Diem', '2019', 'Salzburg', 'Austria', '5020', 'Market cuisine', '$$$$$'),
('Edvard', '2019', 'Wien', 'Austria', '1010', 'Modern cuisine', '$$$$'),
('Das Loft', '2019', 'Wien', 'Austria', '1020', 'Modern cuisine', '$$$$$'),
('Pramerl & the Wolf', '2019', 'Wien', 'Austria', '1090', 'Creative', '$$$$$'),
('Walter Bauer', '2019', 'Wien', 'Austria', '1010', 'Classic cuisine', '$$$$$'),
('SHIKI', '2019', 'Wien', 'Austria', '1010', 'Japanese', '$$$$$'),
('Tian', '2019', 'Wien', 'Austria', '1010', 'Vegetarian', '$$$$$'),
('aend', '2019', 'Wien', 'Austria', '1010', 'Modern cuisine', '$$$$$'),
('Le Ciel by Toni Mörwald', '2019', 'Wien', 'Austria', '1010', 'Classic cuisine', '$$$$$'),
('Chez TJ', '2019', 'South San Francisco', 'California', '94041', 'Contemporary', '$$$$'),
('Protégé', '2019', 'South San Francisco', 'California', '94301', 'Contemporary', '$$$'),
('Madera', '2019', 'San Francisco', 'California', '94025', 'Contemporary', '$$$'),
('The Village Pub', '2019', 'San Francisco', 'California', '94062', 'Contemporary', '$$$'),
('Plumed Horse', '2019', 'South San Francisco', 'California', '95070', 'Contemporary', '$$$$'),
('Wakuriya', '2019', 'San Francisco', 'California', '94402', 'Japanese', '$$$$'),
('Sushi Yoshizumi', '2019', 'San Francisco', 'California', '94401', 'Japanese', '$$$$'),
('Rasa', '2019', 'San Francisco', 'California', '94010', 'Indian', '$$'),
('Maum', '2019', 'South San Francisco', 'California', '94101', 'Korean', '$$$$'),
('Al\'s Place', '2019', 'San Francisco', 'California', '94110', 'Californian', '$$'),
('Aster', '2019', 'San Francisco', 'California', '94110', 'Californian', '$$$'),
('Omakase', '2019', 'San Francisco', 'California', '94103', 'Japanese', '$$$$'),
('Commonwealth', '2019', 'San Francisco', 'California', '94110', 'Contemporary', '$$'),
('Luce', '2019', 'San Francisco', 'California', '94103', 'Contemporary', '$$$'),
('Birdsong', '2019', 'San Francisco', 'California', '94101', 'American', '$$$$'),
('In Situ', '2019', 'San Francisco', 'California', '94103', 'International', '$$$$'),
('Mourad', '2019', 'San Francisco', 'California', '94105', 'Moroccan', '$$$'),
('Hashiri', '2019', 'San Francisco', 'California', '94103', 'Japanese', '$$$$'),
('Angler', '2019', 'San Francisco', 'California', '94101', 'Contemporary', '$$$$'),
('Rich Table', '2019', 'San Francisco', 'California', '94102', 'Contemporary', '$$$'),
('Kin Khao', '2019', 'San Francisco', 'California', '94102', 'Thai', '$$'),
('Michael Mina', '2019', 'San Francisco', 'California', '94102', 'Contemporary', '$$$$'),
('Sons & Daughters', '2019', 'San Francisco', 'California', '94108', 'Contemporary', '$$$$'),
('Mister Jiu\'s', '2019', 'San Francisco', 'California', '94108', 'Chinese', '$$$'),
('Nico', '2019', 'San Francisco', 'California', '94101', 'Contemporary', '$$$'),
('jū-ni', '2019', 'San Francisco', 'California', '94117', 'Japanese', '$$$$'),
('Keiko à Nob Hill', '2019', 'San Francisco', 'California', '94109', 'Fusion', '$$$$'),
('The Progress', '2019', 'San Francisco', 'California', '94115', 'Californian', '$$$'),
('State Bird Provisions', '2019', 'San Francisco', 'California', '94115', 'American', '$$'),
('Octavia', '2019', 'San Francisco', 'California', '94109', 'Californian', '$$$'),
('SPQR', '2019', 'San Francisco', 'California', '94115', 'Italian', '$$$'),
('Lord Stanley', '2019', 'San Francisco', 'California', '94109', 'Californian', '$$$'),
('Kinjo', '2019', 'San Francisco', 'California', '94109', 'Japanese', '$$$$'),
('Sorrel', '2019', 'San Francisco', 'California', '94101', 'Californian', '$$$'),
('Gary Danko', '2019', 'San Francisco', 'California', '94109', 'Contemporary', '$$$$'),
('Bar Crenn', '2019', 'San Francisco', 'California', '94101', 'French', '$$$'),
('Spruce', '2019', 'San Francisco', 'California', '94118', 'Californian', '$$$');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
