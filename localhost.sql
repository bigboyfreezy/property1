-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 08, 2021 at 01:34 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `phpmyadmin`
--
CREATE DATABASE IF NOT EXISTS `phpmyadmin` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE `phpmyadmin`;

-- --------------------------------------------------------

--

--
-- Table structure for table `pma__central_columns`
--


--
-- Table structure for table `pma__column_info`
--

--
CREATE DATABASE IF NOT EXISTS `property` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `property`;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(50) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `active` varchar(100) NOT NULL DEFAULT 'Yes',
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `tel` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `fname`, `lname`, `email`, `password`, `active`, `reg_date`, `tel`) VALUES
(1, 'Abdi', 'Farah', 'abdifarah076@gmail.com', '4ce172517ca4678e62855b25ccfa60ceef6648ce66b15404ab84522c45f3643116e64b1531f879312f723b9fecee23ff6823f6b9d5343f5901babe3685b502b9b733fd6aec7537b49379b0db457eff25d7feeef638d57940285e25dc0fee31ba', 'Yes', '2021-09-13 11:04:29', '');

-- --------------------------------------------------------

--
-- Table structure for table `agency`
--

CREATE TABLE `agency` (
  `agency_id` int(50) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `active` varchar(100) NOT NULL DEFAULT 'Yes',
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `admin_id` int(50) NOT NULL,
  `tel_office` varchar(255) NOT NULL,
  `tel_personal` varchar(255) NOT NULL,
  `company_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `agency`
--

INSERT INTO `agency` (`agency_id`, `fname`, `lname`, `email`, `password`, `active`, `reg_date`, `admin_id`, `tel_office`, `tel_personal`, `company_name`) VALUES
(21, 'Callum', 'Wilsan', 'callum@gmail.com', '8dc34a5fd84f67cf3f1465d1d511b1571fc37880853bccf263bd910a2d8d2eedbe6aac5d648a54088e5edab8691966eb65cbd9a844afde072b83741b13ee899b49796c49ee97c772e8a9c0eed420059e37ef1a5c6a5c4cd5a9541f92d0cab113', 'Yes', '2021-09-23 09:41:17', 1, '+245722658975', '+254729225710', 'Callum Agency Ltd');

-- --------------------------------------------------------

--
-- Table structure for table `agent`
--

CREATE TABLE `agent` (
  `agent_id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `active` varchar(100) NOT NULL DEFAULT 'Yes',
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `agency_id` int(50) NOT NULL,
  `tel_office` varchar(255) NOT NULL,
  `tel_personal` varchar(255) NOT NULL,
  `company_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `agent`
--

INSERT INTO `agent` (`agent_id`, `fname`, `lname`, `email`, `password`, `active`, `reg_date`, `agency_id`, `tel_office`, `tel_personal`, `company_name`) VALUES
(5, 'Allan', 'Gray', 'allan@gmail.com', 'f895da1bf0950ab83c92814954219d131aea129e22ce19fcf980c93eab2c32366fba431cbd630aca4bec65fb34106770d92c539e96be2ef9b8914ac313e9f6ec0e9c9a819f7ba785eb1c51e030751a5d556d6aa8afeb6ba074e395e5d5fa79ce', 'Yes', '2021-09-28 09:10:29', 21, '+254812532578', '+254723326919', 'Allan Agency');

-- --------------------------------------------------------

--
-- Table structure for table `allocate_unit`
--

CREATE TABLE `allocate_unit` (
  `allocate_id` int(50) NOT NULL,
  `unit_id` int(50) NOT NULL,
  `tenant_id` int(50) NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'yes',
  `allocation_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `allocate_unit`
--

INSERT INTO `allocate_unit` (`allocate_id`, `unit_id`, `tenant_id`, `status`, `allocation_date`) VALUES
(5, 3, 2, 'yes', '2021-10-01 11:18:36'),
(6, 6, 4, 'yes', '2021-10-07 10:06:52'),
(7, 7, 4, 'yes', '2021-10-07 10:17:25');

-- --------------------------------------------------------

--
-- Table structure for table `landlord`
--

CREATE TABLE `landlord` (
  `lardlord_id` int(11) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `active` varchar(100) NOT NULL DEFAULT 'Yes',
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `agent_id` int(11) NOT NULL,
  `tel_office` varchar(255) NOT NULL,
  `tel_personal` varchar(255) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `bank_name` varchar(50) DEFAULT NULL,
  `bank_acc` varchar(50) DEFAULT NULL,
  `pin` varchar(50) DEFAULT NULL,
  `idno` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `landlord`
--

INSERT INTO `landlord` (`lardlord_id`, `fname`, `lname`, `email`, `password`, `active`, `reg_date`, `agent_id`, `tel_office`, `tel_personal`, `company_name`, `address`, `bank_name`, `bank_acc`, `pin`, `idno`) VALUES
(1, 'Karani', 'Mwangi', 'karani@gmail.com', '', 'Yes', '2021-09-23 10:31:56', 5, '', '+254789635822', '', 'CBD MOI AVENUE', 'EQUITY', '02545532689', '2589', '23566710'),
(2, 'Marcus', 'muinde', 'marcus@gmail.com', '0b19fb9b8610796be5de9e36197f263948a5dd94ce2efaa5e145c61a9c365c872c6a59b24ed3afea57beec300589d093e6b4137b6305daf35ae7090f28cba6af1dcc3de48692ab13eba873a48fbad72b123acd860161e4d9618104f4ff931096', 'Yes', '2021-09-24 09:12:41', 5, '+245722658975', '+254723326919', 'mulinge ltd', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `property`
--

CREATE TABLE `property` (
  `property_id` int(11) NOT NULL,
  `property_name` varchar(50) NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `agent_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `landlord_id` int(11) NOT NULL,
  `address` varchar(100) NOT NULL,
  `property_location` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `property`
--

INSERT INTO `property` (`property_id`, `property_name`, `reg_date`, `agent_id`, `category_id`, `landlord_id`, `address`, `property_location`) VALUES
(1, 'Hudson', '2021-09-24 09:01:36', 5, 2, 1, 'Waiyaki', 3),
(2, 'musau', '2021-09-24 11:39:22', 5, 1, 2, 'mulii road', 3),
(3, 'Lavingbon', '2021-09-27 10:16:40', 5, 1, 2, 'Near Kalulu road', 4);

-- --------------------------------------------------------

--
-- Table structure for table `property_category`
--

CREATE TABLE `property_category` (
  `category_id` int(50) NOT NULL,
  `category_name` varchar(50) NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `agency_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `property_category`
--

INSERT INTO `property_category` (`category_id`, `category_name`, `reg_date`, `agency_id`) VALUES
(1, 'Office Space', '2021-09-23 10:12:48', 21),
(2, 'Apartments', '2021-09-23 10:12:48', 21),
(3, 'Main House', '2021-09-28 08:56:35', 21);

-- --------------------------------------------------------

--
-- Table structure for table `property_location`
--

CREATE TABLE `property_location` (
  `category_id` int(11) NOT NULL,
  `location_name` varchar(50) NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `agency_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `property_location`
--

INSERT INTO `property_location` (`category_id`, `location_name`, `reg_date`, `agency_id`) VALUES
(3, 'Westlands', '2021-09-23 10:28:27', 21),
(4, 'Eastlands', '2021-09-23 10:28:27', 21),
(5, 'Kiambu', '2021-09-28 08:57:03', 21),
(6, 'Donholm', '2021-09-28 08:57:10', 21),
(7, 'Lavington', '2021-09-28 09:01:01', 21);

-- --------------------------------------------------------

--
-- Table structure for table `tenants`
--

CREATE TABLE `tenants` (
  `tenant_id` int(50) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `active` varchar(100) NOT NULL DEFAULT 'Yes',
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `agent_id` int(11) NOT NULL,
  `tel_office` varchar(255) NOT NULL,
  `tel_personal` varchar(255) NOT NULL,
  `company_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tenants`
--

INSERT INTO `tenants` (`tenant_id`, `fname`, `lname`, `email`, `password`, `active`, `reg_date`, `agent_id`, `tel_office`, `tel_personal`, `company_name`) VALUES
(3, 'kajose', 'kamulu', 'kamulu@gmail.com', '2838a8aace1b6e03f8ba3b4c5f05c42676d48db0fcd8d68fbccce7652ecb0a00600f7827239cbdafa58be9655cbe60feb0d41fd2d3c07e311948f3fb7d397d44717ff7f885d64fee598b07fd6af983f7971e66efc9bda14c0ded8997a87cab1c', 'Yes', '2021-09-30 09:00:57', 5, '+254812532578', '+254746736304', 'Kajose Ltd'),
(4, 'Malicha', 'hanifa', 'malicha@gmail.com', '97f47462157db83fb42502cf2c2558d1afb0485f71002a76d13883aa45088ab0483e3d976616254205869805594b28bbda683c4edcfb7749bf086fc10cefcae17516638aa0e415b1b6c96930a0fef2e73de02d8543d8c7ca8a950524ffd1016e', 'Yes', '2021-10-07 08:56:21', 5, '+245722658975', '+254723326919', 'Malicha ltd');

-- --------------------------------------------------------

--
-- Table structure for table `unit`
--

CREATE TABLE `unit` (
  `unit_id` int(50) NOT NULL,
  `unit_code` varchar(50) NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `agent_id` int(11) NOT NULL,
  `type_id` int(50) NOT NULL,
  `property_id` int(50) NOT NULL,
  `location_name` varchar(60) NOT NULL,
  `cost` varchar(100) NOT NULL,
  `description` varchar(5000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `unit`
--

INSERT INTO `unit` (`unit_id`, `unit_code`, `reg_date`, `agent_id`, `type_id`, `property_id`, `location_name`, `cost`, `description`) VALUES
(3, 'B3', '2021-09-29 12:42:02', 5, 3, 3, 'Eastlands', '10500', 'Magnificent'),
(6, 'A6', '2021-10-01 11:17:01', 5, 5, 1, 'Westlands', '5000', 'hot shower'),
(7, 'A10', '2021-10-01 11:17:35', 5, 6, 1, 'Westlands', '15000', 'KITCHEN'),
(8, 'A8', '2021-10-01 11:18:14', 5, 7, 1, 'Westlands', '20000', 'Four Nice Bedroooms');

-- --------------------------------------------------------

--
-- Table structure for table `unit_type`
--

CREATE TABLE `unit_type` (
  `type_id` int(50) NOT NULL,
  `type_name` varchar(50) NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `agency_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `unit_type`
--

INSERT INTO `unit_type` (`type_id`, `type_name`, `reg_date`, `agency_id`) VALUES
(3, 'One Bedroom', '2021-09-27 10:28:13', 21),
(4, 'Two Bedroom', '2021-09-27 10:28:13', 21),
(5, 'Bedsitter', '2021-09-27 11:07:59', 21),
(6, 'Three Bedroom', '2021-09-27 11:07:59', 21),
(7, 'Four Bedroom', '2021-09-28 08:56:54', 21);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `agency`
--
ALTER TABLE `agency`
  ADD PRIMARY KEY (`agency_id`),
  ADD KEY `agency_fk0` (`admin_id`);

--
-- Indexes for table `agent`
--
ALTER TABLE `agent`
  ADD PRIMARY KEY (`agent_id`),
  ADD KEY `agent_fk0` (`agency_id`);

--
-- Indexes for table `allocate_unit`
--
ALTER TABLE `allocate_unit`
  ADD PRIMARY KEY (`allocate_id`);

--
-- Indexes for table `landlord`
--
ALTER TABLE `landlord`
  ADD PRIMARY KEY (`lardlord_id`),
  ADD KEY `landlord_fk0` (`agent_id`);

--
-- Indexes for table `property`
--
ALTER TABLE `property`
  ADD PRIMARY KEY (`property_id`),
  ADD KEY `property_fk0` (`agent_id`),
  ADD KEY `property_fk1` (`category_id`),
  ADD KEY `property_fk2` (`landlord_id`);

--
-- Indexes for table `property_category`
--
ALTER TABLE `property_category`
  ADD PRIMARY KEY (`category_id`),
  ADD KEY `property_category_fk0` (`agency_id`);

--
-- Indexes for table `property_location`
--
ALTER TABLE `property_location`
  ADD PRIMARY KEY (`category_id`),
  ADD KEY `property_location_fk0` (`agency_id`);

--
-- Indexes for table `tenants`
--
ALTER TABLE `tenants`
  ADD PRIMARY KEY (`tenant_id`),
  ADD KEY `tenants_fk0` (`agent_id`);

--
-- Indexes for table `unit`
--
ALTER TABLE `unit`
  ADD PRIMARY KEY (`unit_id`),
  ADD KEY `unit_fk0` (`agent_id`),
  ADD KEY `unit_fk1` (`type_id`),
  ADD KEY `unit_fk2` (`property_id`);

--
-- Indexes for table `unit_type`
--
ALTER TABLE `unit_type`
  ADD PRIMARY KEY (`type_id`),
  ADD KEY `unit_type_fk0` (`agency_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `agency`
--
ALTER TABLE `agency`
  MODIFY `agency_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `agent`
--
ALTER TABLE `agent`
  MODIFY `agent_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `allocate_unit`
--
ALTER TABLE `allocate_unit`
  MODIFY `allocate_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `landlord`
--
ALTER TABLE `landlord`
  MODIFY `lardlord_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `property`
--
ALTER TABLE `property`
  MODIFY `property_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `property_category`
--
ALTER TABLE `property_category`
  MODIFY `category_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `property_location`
--
ALTER TABLE `property_location`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `tenants`
--
ALTER TABLE `tenants`
  MODIFY `tenant_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `unit`
--
ALTER TABLE `unit`
  MODIFY `unit_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `unit_type`
--
ALTER TABLE `unit_type`
  MODIFY `type_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `agency`
--
ALTER TABLE `agency`
  ADD CONSTRAINT `agency_fk0` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`);

--
-- Constraints for table `agent`
--
ALTER TABLE `agent`
  ADD CONSTRAINT `agent_fk0` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`agency_id`);

--
-- Constraints for table `landlord`
--
ALTER TABLE `landlord`
  ADD CONSTRAINT `landlord_fk0` FOREIGN KEY (`agent_id`) REFERENCES `agent` (`agent_id`);

--
-- Constraints for table `property`
--
ALTER TABLE `property`
  ADD CONSTRAINT `property_fk0` FOREIGN KEY (`agent_id`) REFERENCES `agent` (`agent_id`),
  ADD CONSTRAINT `property_fk1` FOREIGN KEY (`category_id`) REFERENCES `property_category` (`category_id`),
  ADD CONSTRAINT `property_fk2` FOREIGN KEY (`landlord_id`) REFERENCES `landlord` (`lardlord_id`);

--
-- Constraints for table `property_category`
--
ALTER TABLE `property_category`
  ADD CONSTRAINT `property_category_fk0` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`agency_id`);

--
-- Constraints for table `property_location`
--
ALTER TABLE `property_location`
  ADD CONSTRAINT `property_location_fk0` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`agency_id`);

--
-- Constraints for table `tenants`
--
ALTER TABLE `tenants`
  ADD CONSTRAINT `tenants_fk0` FOREIGN KEY (`agent_id`) REFERENCES `agent` (`agent_id`);

--
-- Constraints for table `unit`
--
ALTER TABLE `unit`
  ADD CONSTRAINT `unit_fk0` FOREIGN KEY (`agent_id`) REFERENCES `agent` (`agent_id`),
  ADD CONSTRAINT `unit_fk1` FOREIGN KEY (`type_id`) REFERENCES `unit_type` (`type_id`),
  ADD CONSTRAINT `unit_fk2` FOREIGN KEY (`property_id`) REFERENCES `property` (`property_id`);

--
-- Constraints for table `unit_type`
--
ALTER TABLE `unit_type`
  ADD CONSTRAINT `unit_type_fk0` FOREIGN KEY (`agency_id`) REFERENCES `agency` (`agency_id`);
--
-- Database: `test`
--
CREATE DATABASE IF NOT EXISTS `test` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `test`;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
