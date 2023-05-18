-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 07, 2023 at 05:21 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `photo_chain`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `ds_contact`
--

CREATE TABLE `ds_contact` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `cname` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_contact`
--

INSERT INTO `ds_contact` (`id`, `uname`, `cname`, `status`, `date_time`) VALUES
(1, 'raj', 'dinesh', 1, '2023-02-04 17:46:51'),
(2, 'dinesh', 'raj', 1, '2023-02-04 17:47:07');

-- --------------------------------------------------------

--
-- Table structure for table `ds_face`
--

CREATE TABLE `ds_face` (
  `id` int(11) NOT NULL,
  `vid` int(11) NOT NULL,
  `vface` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_face`
--


-- --------------------------------------------------------

--
-- Table structure for table `ds_post`
--

CREATE TABLE `ds_post` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `detail` text NOT NULL,
  `photo` varchar(100) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `status` int(11) NOT NULL,
  `photo_mode` int(11) NOT NULL,
  `pimage` varchar(30) NOT NULL,
  `dstatus` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_post`
--

INSERT INTO `ds_post` (`id`, `uname`, `detail`, `photo`, `rdate`, `dtime`, `status`, `photo_mode`, `pimage`, `dstatus`) VALUES
(1, 'vijay', 'mobile', 'BP1soc.jpg', '04-02-2023', '2023-02-04 17:48:48', 0, 2, 'P1soc.jpg', 0),
(2, 'raj', 'my friends', 'FP2gf1.jpg', '04-02-2023', '2023-02-04 19:04:57', 0, 1, 'P2gf1.jpg', 0),
(3, 'dinesh', 'my post', 'FP3gf1.jpg', '05-02-2023', '2023-02-05 18:11:16', 0, 1, 'P3gf1.jpg', 0);

-- --------------------------------------------------------

--
-- Table structure for table `ds_register`
--

CREATE TABLE `ds_register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `aadhar` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `profile_st` int(11) NOT NULL,
  `block_key` varchar(20) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `dstatus` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_register`
--

INSERT INTO `ds_register` (`id`, `name`, `gender`, `dob`, `email`, `aadhar`, `uname`, `pass`, `create_date`, `profile_st`, `block_key`, `date_time`, `dstatus`) VALUES
(1, 'Raj', 'Male', '1995-08-15', 'raj@gmail.com', '246813571123', 'raj', '1234', '04-02-2023', 1, 'Ra181246', '2023-02-05 14:37:47', 0),
(2, 'Dinesh', 'Male', '1998-12-18', 'dinesh@gmail.com', '432156784321', 'dinesh', '1234', '04-02-2023', 0, 'Di278432', '2023-02-04 17:46:29', 0),
(3, 'Vijay', 'Male', '1992-04-22', 'vijay@gmail.com', '678967896789', 'vijay', '1234', '04-02-2023', 1, 'Vi389678', '2023-02-05 14:38:39', 0);

-- --------------------------------------------------------

--
-- Table structure for table `ds_request`
--

CREATE TABLE `ds_request` (
  `id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `cname` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ds_request`
--

INSERT INTO `ds_request` (`id`, `pid`, `uname`, `cname`, `status`, `dtime`) VALUES
(1, 2, 'vijay', 'raj', 1, '2023-02-05 16:34:22');
