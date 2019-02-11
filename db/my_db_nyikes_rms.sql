-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 10, 2019 at 02:43 AM
-- Server version: 5.5.54
-- PHP Version: 5.4.45-4+deprecated+dontuse+deb.sury.org~precise+1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `db_nyikes_rms`
--

-- --------------------------------------------------------

--
-- Table structure for table `campaign`
--
-- Creation: Feb 09, 2019 at 10:25 PM
--

DROP TABLE IF EXISTS `campaign`;
CREATE TABLE IF NOT EXISTS `campaign` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status_id` int(11) NOT NULL,
  `target_amount` float NOT NULL,
  `campaign_name` varchar(75) NOT NULL,
  `campaign_description` varchar(75) DEFAULT NULL,
  `notes` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_campaign_campaign_name` (`campaign_name`),
  KEY `campaign_id_index` (`id`),
  KEY `campaign_status_id_index` (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `campaign`:
--   `status_id`
--       `campaign_status` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `campaign_contributions`
--
-- Creation: Feb 09, 2019 at 10:53 PM
--

DROP TABLE IF EXISTS `campaign_contributions`;
CREATE TABLE IF NOT EXISTS `campaign_contributions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `split_txn_id` int(11) NOT NULL,
  `campaign_id` int(11) NOT NULL,
  `contrib_amount` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `campaign_contributions_id_index` (`id`),
  KEY `campaign_contributions_campaign_id_index` (`campaign_id`),
  KEY `campaign_contributions_split_txn_id_index` (`split_txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `campaign_contributions`:
--   `split_txn_id`
--       `credit_transaction_split` -> `id`
--   `campaign_id`
--       `campaign` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `campaign_status`
--
-- Creation: Feb 09, 2019 at 10:24 PM
--

DROP TABLE IF EXISTS `campaign_status`;
CREATE TABLE IF NOT EXISTS `campaign_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status_name` varchar(75) NOT NULL,
  `status_description` varchar(75) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_campaignstatus_status` (`status_name`),
  KEY `campaign_status_id_index` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `credit_transaction`
--
-- Creation: Feb 09, 2019 at 10:48 PM
--

DROP TABLE IF EXISTS `credit_transaction`;
CREATE TABLE IF NOT EXISTS `credit_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `holding_acc_id` int(11) NOT NULL,
  `txn_mode_id` int(11) NOT NULL,
  `transacting_member_id` int(11) NOT NULL,
  `reference_no` varchar(75) DEFAULT NULL,
  `amount` float NOT NULL,
  `txn_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `remarks` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `credit_transaction_id_index` (`id`),
  KEY `credit_transaction_holding_acc_id_index` (`holding_acc_id`),
  KEY `credit_transaction_txn_mode_id_index` (`txn_mode_id`),
  KEY `credit_transaction_transacting_member_id_index` (`transacting_member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `credit_transaction`:
--   `transacting_member_id`
--       `member` -> `id`
--   `holding_acc_id`
--       `nyikes_holding_account` -> `id`
--   `txn_mode_id`
--       `transaction_mode` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `credit_transaction_split`
--
-- Creation: Feb 09, 2019 at 10:51 PM
--

DROP TABLE IF EXISTS `credit_transaction_split`;
CREATE TABLE IF NOT EXISTS `credit_transaction_split` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `credit_txn_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `txn_amount` float NOT NULL,
  `remarks` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `credit_transaction_split_id_index` (`id`),
  KEY `credit_transaction_split_credit_txn_id_index` (`credit_txn_id`),
  KEY `fk_credittransactionsplit_member_id` (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `credit_transaction_split`:
--   `member_id`
--       `member` -> `id`
--   `credit_txn_id`
--       `credit_transaction` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `debit_transaction`
--
-- Creation: Feb 09, 2019 at 11:07 PM
--

DROP TABLE IF EXISTS `debit_transaction`;
CREATE TABLE IF NOT EXISTS `debit_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `holding_acc_id` int(11) NOT NULL,
  `txn_mode_id` int(11) NOT NULL,
  `campaign_id` int(11) DEFAULT NULL,
  `fund_account_id` int(11) DEFAULT NULL,
  `reference_no` varchar(75) DEFAULT NULL,
  `amount` float NOT NULL,
  `authorized` tinyint(1) NOT NULL,
  `authorized_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `txn_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `debit_transaction_id_index` (`id`),
  KEY `debit_transaction_txn_mode_id_index` (`txn_mode_id`),
  KEY `fk_debittransaction_nyikesholdingaccount_id` (`holding_acc_id`),
  KEY `fk_debittransaction_campaign_id` (`campaign_id`),
  KEY `fk_debittransaction_fundaccount_id` (`fund_account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `debit_transaction`:
--   `fund_account_id`
--       `fund_account` -> `id`
--   `campaign_id`
--       `campaign` -> `id`
--   `holding_acc_id`
--       `nyikes_holding_account` -> `id`
--   `txn_mode_id`
--       `transaction_mode` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `debit_txn_authorization`
--
-- Creation: Feb 09, 2019 at 11:08 PM
--

DROP TABLE IF EXISTS `debit_txn_authorization`;
CREATE TABLE IF NOT EXISTS `debit_txn_authorization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `debit_txn_id` int(11) NOT NULL,
  `holding_acc_signatory_id` int(11) NOT NULL,
  `authorization_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `authorizes` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `debit_txn_authorization_id_index` (`id`),
  KEY `fk_debittxnauthorization_debittransaction_id` (`debit_txn_id`),
  KEY `fk_debittxnauthorization_nyikesholdingaccsignatory_id` (`holding_acc_signatory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `debit_txn_authorization`:
--   `holding_acc_signatory_id`
--       `nyikes_holding_acc_signatory` -> `id`
--   `debit_txn_id`
--       `debit_transaction` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `debit_txn_cost`
--
-- Creation: Feb 09, 2019 at 11:09 PM
--

DROP TABLE IF EXISTS `debit_txn_cost`;
CREATE TABLE IF NOT EXISTS `debit_txn_cost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `debit_txn_id` int(11) NOT NULL,
  `cost_name` varchar(75) NOT NULL,
  `cost_amount` float NOT NULL,
  `cost_description` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `debit_txn_cost_id_index` (`id`),
  KEY `fk_debittxncost_debittransaction_id` (`debit_txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `debit_txn_cost`:
--   `debit_txn_id`
--       `debit_transaction` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `fund`
--
-- Creation: Feb 09, 2019 at 10:25 PM
--

DROP TABLE IF EXISTS `fund`;
CREATE TABLE IF NOT EXISTS `fund` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fund_name` varchar(75) NOT NULL,
  `fund_description` varchar(75) DEFAULT NULL,
  `fund_balance` float NOT NULL,
  `balance_last_update_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_fund_fund_name` (`fund_name`),
  KEY `fund_id_index` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `fund_account`
--
-- Creation: Feb 09, 2019 at 11:04 PM
--

DROP TABLE IF EXISTS `fund_account`;
CREATE TABLE IF NOT EXISTS `fund_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `holding_acc_id` int(11) NOT NULL,
  `fund_id` int(11) NOT NULL,
  `fund_balance` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fund_account_id_index` (`id`),
  KEY `fund_account_holding_acc_id_index` (`holding_acc_id`),
  KEY `fk_fund_id` (`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `fund_account`:
--   `fund_id`
--       `fund` -> `id`
--   `holding_acc_id`
--       `nyikes_holding_account` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `fund_contributions`
--
-- Creation: Feb 09, 2019 at 10:56 PM
--

DROP TABLE IF EXISTS `fund_contributions`;
CREATE TABLE IF NOT EXISTS `fund_contributions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fund_id` int(11) NOT NULL,
  `split_txn_id` int(11) DEFAULT NULL,
  `welfare_contribution_id` int(11) DEFAULT NULL,
  `contrib_amount` float NOT NULL,
  `fund_running_balance` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fund_contributions_id_index` (`id`),
  KEY `fund_contributions_fund_id_index` (`fund_id`),
  KEY `fund_contributions_welfare_contribution_id_index` (`welfare_contribution_id`),
  KEY `fund_contributions_split_txn_id_index` (`split_txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `fund_contributions`:
--   `split_txn_id`
--       `credit_transaction_split` -> `id`
--   `fund_id`
--       `fund` -> `id`
--   `welfare_contribution_id`
--       `welfare_contributions` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `holding_account_type`
--
-- Creation: Feb 09, 2019 at 10:26 PM
--

DROP TABLE IF EXISTS `holding_account_type`;
CREATE TABLE IF NOT EXISTS `holding_account_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(75) NOT NULL,
  `description` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_holdingaccounttype_type_name` (`type_name`),
  KEY `holding_account_type_id_index` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `member`
--
-- Creation: Feb 09, 2019 at 10:28 PM
--

DROP TABLE IF EXISTS `member`;
CREATE TABLE IF NOT EXISTS `member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_id` int(11) NOT NULL,
  `first_name` varchar(75) NOT NULL,
  `middle_name` varchar(75) NOT NULL,
  `surname` varchar(75) NOT NULL,
  `email` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `member_id_index` (`id`),
  KEY `member_class_id_index` (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `member`:
--   `class_id`
--       `membership_class` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `membership_class`
--
-- Creation: Feb 09, 2019 at 10:27 PM
--

DROP TABLE IF EXISTS `membership_class`;
CREATE TABLE IF NOT EXISTS `membership_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_name` varchar(75) NOT NULL,
  `monthly_contribution_amount` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_membershipclass_class_name` (`class_name`),
  KEY `membership_class_id_index` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `nyikes_holding_account`
--
-- Creation: Feb 09, 2019 at 10:36 PM
--

DROP TABLE IF EXISTS `nyikes_holding_account`;
CREATE TABLE IF NOT EXISTS `nyikes_holding_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_type_id` int(11) NOT NULL,
  `account_number` varchar(75) NOT NULL,
  `account_name` varchar(75) NOT NULL,
  `account_balance` float NOT NULL,
  `notes` varchar(75) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `nyikes_holding_account_id_index` (`id`),
  KEY `nyikes_holding_account_account_type_id_index` (`account_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `nyikes_holding_account`:
--   `account_type_id`
--       `holding_account_type` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `nyikes_holding_acc_signatory`
--
-- Creation: Feb 09, 2019 at 11:22 PM
--

DROP TABLE IF EXISTS `nyikes_holding_acc_signatory`;
CREATE TABLE IF NOT EXISTS `nyikes_holding_acc_signatory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `holding_acc_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `nyikes_holding_acc_signatory_id_index` (`id`),
  KEY `fk_nyikesholdingaccsignatory_nyikesholdingaccount_id` (`holding_acc_id`),
  KEY `fk_nyikesholdingaccsignatory_member_id` (`member_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `nyikes_holding_acc_signatory`:
--   `member_id`
--       `member` -> `id`
--   `holding_acc_id`
--       `nyikes_holding_account` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `transaction_mode`
--
-- Creation: Feb 09, 2019 at 10:28 PM
--

DROP TABLE IF EXISTS `transaction_mode`;
CREATE TABLE IF NOT EXISTS `transaction_mode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(75) NOT NULL,
  `description` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_transactionmode_name` (`name`),
  KEY `transaction_mode_id_index` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `welfare_contributions`
--
-- Creation: Feb 09, 2019 at 10:55 PM
--

DROP TABLE IF EXISTS `welfare_contributions`;
CREATE TABLE IF NOT EXISTS `welfare_contributions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `split_txn_id` int(11) NOT NULL,
  `welfare_contrib_schedule_id` int(11) NOT NULL,
  `contrib_amount` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `welfare_contributions_id_index` (`id`),
  KEY `welfare_contributions_split_txn_id_index` (`split_txn_id`),
  KEY `welfare_contributions_welfare_contrib_schedule_id_index` (`welfare_contrib_schedule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `welfare_contributions`:
--   `welfare_contrib_schedule_id`
--       `welfare_contrib_schedule` -> `id`
--   `split_txn_id`
--       `credit_transaction_split` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `welfare_contrib_alloc_reference`
--
-- Creation: Feb 09, 2019 at 11:14 PM
--

DROP TABLE IF EXISTS `welfare_contrib_alloc_reference`;
CREATE TABLE IF NOT EXISTS `welfare_contrib_alloc_reference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fund_id` int(11) NOT NULL,
  `percent_to_allocate` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `welfare_contrib_alloc_reference_id_index` (`id`),
  KEY `fk_welfarecontriballocreference_fund_id` (`fund_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- RELATIONS FOR TABLE `welfare_contrib_alloc_reference`:
--   `fund_id`
--       `fund` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `welfare_contrib_schedule`
--
-- Creation: Feb 09, 2019 at 10:29 PM
--

DROP TABLE IF EXISTS `welfare_contrib_schedule`;
CREATE TABLE IF NOT EXISTS `welfare_contrib_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contrib_month` varchar(75) NOT NULL,
  `contrib_year` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `welfare_contrib_schedule_id_index` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `campaign`
--
ALTER TABLE `campaign`
  ADD CONSTRAINT `fk_campaignstatus_id` FOREIGN KEY (`status_id`) REFERENCES `campaign_status` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `campaign_contributions`
--
ALTER TABLE `campaign_contributions`
  ADD CONSTRAINT `fk_campaigncontribution_credittransactionsplit_id` FOREIGN KEY (`split_txn_id`) REFERENCES `credit_transaction_split` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_campaigncontribution_campaign_id` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `credit_transaction`
--
ALTER TABLE `credit_transaction`
  ADD CONSTRAINT `fk_credittransaction_member_id` FOREIGN KEY (`transacting_member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_creditransaction_nyikesholdingaccount_id` FOREIGN KEY (`holding_acc_id`) REFERENCES `nyikes_holding_account` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_credittransaction_transactionmode_id` FOREIGN KEY (`txn_mode_id`) REFERENCES `transaction_mode` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `credit_transaction_split`
--
ALTER TABLE `credit_transaction_split`
  ADD CONSTRAINT `fk_credittransactionsplit_member_id` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_credittransactionsplit_credittransaction_id` FOREIGN KEY (`credit_txn_id`) REFERENCES `credit_transaction` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `debit_transaction`
--
ALTER TABLE `debit_transaction`
  ADD CONSTRAINT `fk_debittransaction_fundaccount_id` FOREIGN KEY (`fund_account_id`) REFERENCES `fund_account` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_debittransaction_campaign_id` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_debittransaction_nyikesholdingaccount_id` FOREIGN KEY (`holding_acc_id`) REFERENCES `nyikes_holding_account` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_debittransaction_transactionmode_id` FOREIGN KEY (`txn_mode_id`) REFERENCES `transaction_mode` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `debit_txn_authorization`
--
ALTER TABLE `debit_txn_authorization`
  ADD CONSTRAINT `fk_debittxnauthorization_nyikesholdingaccsignatory_id` FOREIGN KEY (`holding_acc_signatory_id`) REFERENCES `nyikes_holding_acc_signatory` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_debittxnauthorization_debittransaction_id` FOREIGN KEY (`debit_txn_id`) REFERENCES `debit_transaction` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `debit_txn_cost`
--
ALTER TABLE `debit_txn_cost`
  ADD CONSTRAINT `fk_debittxncost_debittransaction_id` FOREIGN KEY (`debit_txn_id`) REFERENCES `debit_transaction` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `fund_account`
--
ALTER TABLE `fund_account`
  ADD CONSTRAINT `fk_fund_id` FOREIGN KEY (`fund_id`) REFERENCES `fund` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_nyikesholdingaccount_id` FOREIGN KEY (`holding_acc_id`) REFERENCES `nyikes_holding_account` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `fund_contributions`
--
ALTER TABLE `fund_contributions`
  ADD CONSTRAINT `fk_credittransactionsplit_id` FOREIGN KEY (`split_txn_id`) REFERENCES `credit_transaction_split` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_fundcontributions_fund_id` FOREIGN KEY (`fund_id`) REFERENCES `fund` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_fundcontributions_welfarecontributions_id` FOREIGN KEY (`welfare_contribution_id`) REFERENCES `welfare_contributions` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `member`
--
ALTER TABLE `member`
  ADD CONSTRAINT `fk_membershipclass_id` FOREIGN KEY (`class_id`) REFERENCES `membership_class` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `nyikes_holding_account`
--
ALTER TABLE `nyikes_holding_account`
  ADD CONSTRAINT `fk_holdingaccounttype_id` FOREIGN KEY (`account_type_id`) REFERENCES `holding_account_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `nyikes_holding_acc_signatory`
--
ALTER TABLE `nyikes_holding_acc_signatory`
  ADD CONSTRAINT `fk_nyikesholdingaccsignatory_member_id` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_nyikesholdingaccsignatory_nyikesholdingaccount_id` FOREIGN KEY (`holding_acc_id`) REFERENCES `nyikes_holding_account` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `welfare_contributions`
--
ALTER TABLE `welfare_contributions`
  ADD CONSTRAINT `fk_welfarecontributions_welfarecontrib_id` FOREIGN KEY (`welfare_contrib_schedule_id`) REFERENCES `welfare_contrib_schedule` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_welfarecontributions_credittransactionsplit_id` FOREIGN KEY (`split_txn_id`) REFERENCES `credit_transaction_split` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `welfare_contrib_alloc_reference`
--
ALTER TABLE `welfare_contrib_alloc_reference`
  ADD CONSTRAINT `fk_welfarecontriballocreference_fund_id` FOREIGN KEY (`fund_id`) REFERENCES `fund` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
