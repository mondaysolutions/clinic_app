PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE ab_permission (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO ab_permission VALUES(1,'can_this_form_post');
INSERT INTO ab_permission VALUES(2,'can_this_form_get');
INSERT INTO ab_permission VALUES(3,'can_edit');
INSERT INTO ab_permission VALUES(4,'can_show');
INSERT INTO ab_permission VALUES(5,'can_delete');
INSERT INTO ab_permission VALUES(6,'can_download');
INSERT INTO ab_permission VALUES(7,'can_userinfo');
INSERT INTO ab_permission VALUES(8,'can_list');
INSERT INTO ab_permission VALUES(9,'can_add');
INSERT INTO ab_permission VALUES(10,'muldelete');
INSERT INTO ab_permission VALUES(11,'resetmypassword');
INSERT INTO ab_permission VALUES(12,'resetpasswords');
INSERT INTO ab_permission VALUES(13,'userinfoedit');
INSERT INTO ab_permission VALUES(14,'menu_access');
INSERT INTO ab_permission VALUES(15,'copyrole');
INSERT INTO ab_permission VALUES(16,'can_chart');
INSERT INTO ab_permission VALUES(17,'can_get');
INSERT INTO ab_permission VALUES(18,'preview_receipt');
INSERT INTO ab_permission VALUES(19,'receipt');
INSERT INTO ab_permission VALUES(20,'download_receipt');
INSERT INTO ab_permission VALUES(21,'download_certificate');
INSERT INTO ab_permission VALUES(22,'preview_certificate');
INSERT INTO ab_permission VALUES(23,'can_calendar');
INSERT INTO ab_permission VALUES(24,'customer');
INSERT INTO ab_permission VALUES(25,'return_to_list');
INSERT INTO ab_permission VALUES(26,'can_action_post');
INSERT INTO ab_permission VALUES(27,'can_action');
INSERT INTO ab_permission VALUES(28,'appointment');
INSERT INTO ab_permission VALUES(29,'package');
INSERT INTO ab_permission VALUES(30,'can_search');
CREATE TABLE ab_view_menu (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO ab_view_menu VALUES(1,'CustomIndexView');
INSERT INTO ab_view_menu VALUES(2,'UtilView');
INSERT INTO ab_view_menu VALUES(3,'LocaleView');
INSERT INTO ab_view_menu VALUES(4,'SecurityApi');
INSERT INTO ab_view_menu VALUES(5,'ResetPasswordView');
INSERT INTO ab_view_menu VALUES(6,'ResetMyPasswordView');
INSERT INTO ab_view_menu VALUES(7,'UserInfoEditView');
INSERT INTO ab_view_menu VALUES(8,'AuthDBView');
INSERT INTO ab_view_menu VALUES(9,'MyUserDBView');
INSERT INTO ab_view_menu VALUES(10,'List Users');
INSERT INTO ab_view_menu VALUES(11,'Security');
INSERT INTO ab_view_menu VALUES(12,'RoleModelView');
INSERT INTO ab_view_menu VALUES(13,'List Roles');
INSERT INTO ab_view_menu VALUES(14,'UserStatsChartView');
INSERT INTO ab_view_menu VALUES(15,'User''s Statistics');
INSERT INTO ab_view_menu VALUES(16,'PermissionModelView');
INSERT INTO ab_view_menu VALUES(17,'Base Permissions');
INSERT INTO ab_view_menu VALUES(18,'ViewMenuModelView');
INSERT INTO ab_view_menu VALUES(19,'Views/Menus');
INSERT INTO ab_view_menu VALUES(20,'PermissionViewModelView');
INSERT INTO ab_view_menu VALUES(21,'Permission on Views/Menus');
INSERT INTO ab_view_menu VALUES(22,'OpenApi');
INSERT INTO ab_view_menu VALUES(23,'ReceiptView');
INSERT INTO ab_view_menu VALUES(24,'ReceiptItemView');
INSERT INTO ab_view_menu VALUES(25,'PatientDocumentView');
INSERT INTO ab_view_menu VALUES(26,'MedicalHistoryView');
INSERT INTO ab_view_menu VALUES(27,'PatientView');
INSERT INTO ab_view_menu VALUES(28,'Patients (Physician)');
INSERT INTO ab_view_menu VALUES(29,'Patient');
INSERT INTO ab_view_menu VALUES(30,'PatientStaffView');
INSERT INTO ab_view_menu VALUES(31,'Patients (Staff)');
INSERT INTO ab_view_menu VALUES(32,'AppointmentView');
INSERT INTO ab_view_menu VALUES(33,'Appointments');
INSERT INTO ab_view_menu VALUES(34,'Appointment');
INSERT INTO ab_view_menu VALUES(35,'AppointmentCalendarView');
INSERT INTO ab_view_menu VALUES(36,'Appointment Calendar');
INSERT INTO ab_view_menu VALUES(37,'CouponView');
INSERT INTO ab_view_menu VALUES(38,'Coupons');
INSERT INTO ab_view_menu VALUES(39,'Coupon');
INSERT INTO ab_view_menu VALUES(40,'CustomerDocumentView');
INSERT INTO ab_view_menu VALUES(41,'CustomerView');
INSERT INTO ab_view_menu VALUES(42,'Customers (Physician)');
INSERT INTO ab_view_menu VALUES(43,'Customer');
INSERT INTO ab_view_menu VALUES(44,'CustomerStaffView');
INSERT INTO ab_view_menu VALUES(45,'Customers (Staff)');
INSERT INTO ab_view_menu VALUES(46,'ReportView');
INSERT INTO ab_view_menu VALUES(47,'Reports');
INSERT INTO ab_view_menu VALUES(48,'Report');
INSERT INTO ab_view_menu VALUES(49,'Categories');
INSERT INTO ab_view_menu VALUES(50,'Category');
INSERT INTO ab_view_menu VALUES(51,'CategoryView');
INSERT INTO ab_view_menu VALUES(52,'Settings');
INSERT INTO ab_view_menu VALUES(53,'AppointmentReceiptView');
INSERT INTO ab_view_menu VALUES(54,'PackageReceiptView');
INSERT INTO ab_view_menu VALUES(55,'PackageView');
INSERT INTO ab_view_menu VALUES(56,'Receipts');
INSERT INTO ab_view_menu VALUES(57,'Receipt');
INSERT INTO ab_view_menu VALUES(58,'PackageTicketView');
INSERT INTO ab_view_menu VALUES(59,'ReceiptCustomerView');
INSERT INTO ab_view_menu VALUES(60,'ReceiptNoCustomerView');
INSERT INTO ab_view_menu VALUES(61,'ReceiptAdhocView');
INSERT INTO ab_view_menu VALUES(62,'ReceiptGeneralView');
INSERT INTO ab_view_menu VALUES(63,'ReceiptGeneralItemView');
INSERT INTO ab_view_menu VALUES(64,'ReceiptCustomerItemView');
CREATE TABLE ab_role (
	id INTEGER NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO ab_role VALUES(1,'Staff');
INSERT INTO ab_role VALUES(2,'Physician');
INSERT INTO ab_role VALUES(3,'Admin');
INSERT INTO ab_role VALUES(4,'Public');
CREATE TABLE ab_register_user (
	id INTEGER NOT NULL, 
	first_name VARCHAR(64) NOT NULL, 
	last_name VARCHAR(64) NOT NULL, 
	username VARCHAR(64) NOT NULL, 
	password VARCHAR(256), 
	email VARCHAR(64) NOT NULL, 
	registration_date DATETIME, 
	registration_hash VARCHAR(256), 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
CREATE TABLE ab_permission_view (
	id INTEGER NOT NULL, 
	permission_id INTEGER, 
	view_menu_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (permission_id, view_menu_id), 
	FOREIGN KEY(permission_id) REFERENCES ab_permission (id), 
	FOREIGN KEY(view_menu_id) REFERENCES ab_view_menu (id)
);
INSERT INTO ab_permission_view VALUES(1,1,5);
INSERT INTO ab_permission_view VALUES(2,2,5);
INSERT INTO ab_permission_view VALUES(3,1,6);
INSERT INTO ab_permission_view VALUES(4,2,6);
INSERT INTO ab_permission_view VALUES(5,1,7);
INSERT INTO ab_permission_view VALUES(6,2,7);
INSERT INTO ab_permission_view VALUES(7,3,9);
INSERT INTO ab_permission_view VALUES(8,4,9);
INSERT INTO ab_permission_view VALUES(9,5,9);
INSERT INTO ab_permission_view VALUES(10,6,9);
INSERT INTO ab_permission_view VALUES(11,7,9);
INSERT INTO ab_permission_view VALUES(12,8,9);
INSERT INTO ab_permission_view VALUES(13,9,9);
INSERT INTO ab_permission_view VALUES(14,10,9);
INSERT INTO ab_permission_view VALUES(15,11,9);
INSERT INTO ab_permission_view VALUES(16,12,9);
INSERT INTO ab_permission_view VALUES(17,13,9);
INSERT INTO ab_permission_view VALUES(18,14,10);
INSERT INTO ab_permission_view VALUES(19,14,11);
INSERT INTO ab_permission_view VALUES(20,3,12);
INSERT INTO ab_permission_view VALUES(21,4,12);
INSERT INTO ab_permission_view VALUES(22,5,12);
INSERT INTO ab_permission_view VALUES(23,6,12);
INSERT INTO ab_permission_view VALUES(24,8,12);
INSERT INTO ab_permission_view VALUES(25,9,12);
INSERT INTO ab_permission_view VALUES(26,15,12);
INSERT INTO ab_permission_view VALUES(27,14,13);
INSERT INTO ab_permission_view VALUES(28,16,14);
INSERT INTO ab_permission_view VALUES(29,14,15);
INSERT INTO ab_permission_view VALUES(30,8,16);
INSERT INTO ab_permission_view VALUES(31,14,17);
INSERT INTO ab_permission_view VALUES(32,8,18);
INSERT INTO ab_permission_view VALUES(33,14,19);
INSERT INTO ab_permission_view VALUES(34,8,20);
INSERT INTO ab_permission_view VALUES(35,14,21);
INSERT INTO ab_permission_view VALUES(36,17,22);
INSERT INTO ab_permission_view VALUES(37,8,23);
INSERT INTO ab_permission_view VALUES(38,9,23);
INSERT INTO ab_permission_view VALUES(39,3,23);
INSERT INTO ab_permission_view VALUES(40,5,23);
INSERT INTO ab_permission_view VALUES(41,18,23);
INSERT INTO ab_permission_view VALUES(42,8,24);
INSERT INTO ab_permission_view VALUES(43,9,24);
INSERT INTO ab_permission_view VALUES(44,3,24);
INSERT INTO ab_permission_view VALUES(45,5,24);
INSERT INTO ab_permission_view VALUES(46,3,25);
INSERT INTO ab_permission_view VALUES(47,4,25);
INSERT INTO ab_permission_view VALUES(48,5,25);
INSERT INTO ab_permission_view VALUES(49,6,25);
INSERT INTO ab_permission_view VALUES(50,8,25);
INSERT INTO ab_permission_view VALUES(51,9,25);
INSERT INTO ab_permission_view VALUES(52,3,26);
INSERT INTO ab_permission_view VALUES(53,4,26);
INSERT INTO ab_permission_view VALUES(54,5,26);
INSERT INTO ab_permission_view VALUES(55,6,26);
INSERT INTO ab_permission_view VALUES(56,8,26);
INSERT INTO ab_permission_view VALUES(57,9,26);
INSERT INTO ab_permission_view VALUES(58,8,27);
INSERT INTO ab_permission_view VALUES(59,9,27);
INSERT INTO ab_permission_view VALUES(60,3,27);
INSERT INTO ab_permission_view VALUES(61,5,27);
INSERT INTO ab_permission_view VALUES(62,14,28);
INSERT INTO ab_permission_view VALUES(63,14,29);
INSERT INTO ab_permission_view VALUES(64,8,30);
INSERT INTO ab_permission_view VALUES(65,9,30);
INSERT INTO ab_permission_view VALUES(66,3,30);
INSERT INTO ab_permission_view VALUES(67,5,30);
INSERT INTO ab_permission_view VALUES(68,14,31);
INSERT INTO ab_permission_view VALUES(69,8,32);
INSERT INTO ab_permission_view VALUES(70,9,32);
INSERT INTO ab_permission_view VALUES(71,3,32);
INSERT INTO ab_permission_view VALUES(72,5,32);
INSERT INTO ab_permission_view VALUES(73,14,33);
INSERT INTO ab_permission_view VALUES(74,14,34);
INSERT INTO ab_permission_view VALUES(75,14,36);
INSERT INTO ab_permission_view VALUES(76,3,37);
INSERT INTO ab_permission_view VALUES(77,4,37);
INSERT INTO ab_permission_view VALUES(78,5,37);
INSERT INTO ab_permission_view VALUES(79,6,37);
INSERT INTO ab_permission_view VALUES(80,8,37);
INSERT INTO ab_permission_view VALUES(81,9,37);
INSERT INTO ab_permission_view VALUES(82,14,38);
INSERT INTO ab_permission_view VALUES(83,14,39);
INSERT INTO ab_permission_view VALUES(84,19,23);
INSERT INTO ab_permission_view VALUES(85,19,27);
INSERT INTO ab_permission_view VALUES(86,4,27);
INSERT INTO ab_permission_view VALUES(87,20,23);
INSERT INTO ab_permission_view VALUES(88,6,40);
INSERT INTO ab_permission_view VALUES(89,5,40);
INSERT INTO ab_permission_view VALUES(90,4,40);
INSERT INTO ab_permission_view VALUES(91,8,40);
INSERT INTO ab_permission_view VALUES(92,3,40);
INSERT INTO ab_permission_view VALUES(93,9,40);
INSERT INTO ab_permission_view VALUES(94,8,41);
INSERT INTO ab_permission_view VALUES(95,9,41);
INSERT INTO ab_permission_view VALUES(96,3,41);
INSERT INTO ab_permission_view VALUES(97,5,41);
INSERT INTO ab_permission_view VALUES(98,14,42);
INSERT INTO ab_permission_view VALUES(99,14,43);
INSERT INTO ab_permission_view VALUES(100,8,44);
INSERT INTO ab_permission_view VALUES(101,9,44);
INSERT INTO ab_permission_view VALUES(102,3,44);
INSERT INTO ab_permission_view VALUES(103,5,44);
INSERT INTO ab_permission_view VALUES(104,14,45);
INSERT INTO ab_permission_view VALUES(105,21,32);
INSERT INTO ab_permission_view VALUES(106,22,32);
INSERT INTO ab_permission_view VALUES(107,14,47);
INSERT INTO ab_permission_view VALUES(108,14,48);
INSERT INTO ab_permission_view VALUES(109,19,32);
INSERT INTO ab_permission_view VALUES(110,23,35);
INSERT INTO ab_permission_view VALUES(111,24,32);
INSERT INTO ab_permission_view VALUES(112,14,49);
INSERT INTO ab_permission_view VALUES(113,14,50);
INSERT INTO ab_permission_view VALUES(114,8,51);
INSERT INTO ab_permission_view VALUES(115,9,51);
INSERT INTO ab_permission_view VALUES(116,3,51);
INSERT INTO ab_permission_view VALUES(117,5,51);
INSERT INTO ab_permission_view VALUES(118,25,23);
INSERT INTO ab_permission_view VALUES(119,25,24);
INSERT INTO ab_permission_view VALUES(120,25,40);
INSERT INTO ab_permission_view VALUES(121,25,26);
INSERT INTO ab_permission_view VALUES(122,25,32);
INSERT INTO ab_permission_view VALUES(123,25,41);
INSERT INTO ab_permission_view VALUES(124,25,44);
INSERT INTO ab_permission_view VALUES(125,25,37);
INSERT INTO ab_permission_view VALUES(126,25,51);
INSERT INTO ab_permission_view VALUES(127,1,46);
INSERT INTO ab_permission_view VALUES(128,2,46);
INSERT INTO ab_permission_view VALUES(129,26,9);
INSERT INTO ab_permission_view VALUES(130,27,9);
INSERT INTO ab_permission_view VALUES(131,26,12);
INSERT INTO ab_permission_view VALUES(132,27,12);
INSERT INTO ab_permission_view VALUES(133,27,32);
INSERT INTO ab_permission_view VALUES(134,27,23);
INSERT INTO ab_permission_view VALUES(135,28,23);
INSERT INTO ab_permission_view VALUES(136,27,24);
INSERT INTO ab_permission_view VALUES(137,19,24);
INSERT INTO ab_permission_view VALUES(138,24,40);
INSERT INTO ab_permission_view VALUES(139,27,40);
INSERT INTO ab_permission_view VALUES(140,27,26);
INSERT INTO ab_permission_view VALUES(141,24,26);
INSERT INTO ab_permission_view VALUES(142,14,52);
INSERT INTO ab_permission_view VALUES(143,27,37);
INSERT INTO ab_permission_view VALUES(144,8,53);
INSERT INTO ab_permission_view VALUES(145,9,53);
INSERT INTO ab_permission_view VALUES(146,3,53);
INSERT INTO ab_permission_view VALUES(147,27,53);
INSERT INTO ab_permission_view VALUES(148,28,53);
INSERT INTO ab_permission_view VALUES(149,20,53);
INSERT INTO ab_permission_view VALUES(150,18,53);
INSERT INTO ab_permission_view VALUES(151,8,54);
INSERT INTO ab_permission_view VALUES(152,9,54);
INSERT INTO ab_permission_view VALUES(153,3,54);
INSERT INTO ab_permission_view VALUES(154,27,54);
INSERT INTO ab_permission_view VALUES(155,20,54);
INSERT INTO ab_permission_view VALUES(156,29,54);
INSERT INTO ab_permission_view VALUES(157,18,54);
INSERT INTO ab_permission_view VALUES(158,8,55);
INSERT INTO ab_permission_view VALUES(159,9,55);
INSERT INTO ab_permission_view VALUES(160,3,55);
INSERT INTO ab_permission_view VALUES(161,27,55);
INSERT INTO ab_permission_view VALUES(162,14,56);
INSERT INTO ab_permission_view VALUES(163,14,57);
INSERT INTO ab_permission_view VALUES(164,8,58);
INSERT INTO ab_permission_view VALUES(165,26,58);
INSERT INTO ab_permission_view VALUES(166,3,58);
INSERT INTO ab_permission_view VALUES(167,4,58);
INSERT INTO ab_permission_view VALUES(168,6,58);
INSERT INTO ab_permission_view VALUES(169,27,58);
INSERT INTO ab_permission_view VALUES(170,9,58);
INSERT INTO ab_permission_view VALUES(171,5,58);
INSERT INTO ab_permission_view VALUES(172,24,55);
INSERT INTO ab_permission_view VALUES(173,5,55);
INSERT INTO ab_permission_view VALUES(174,24,23);
INSERT INTO ab_permission_view VALUES(175,8,59);
INSERT INTO ab_permission_view VALUES(176,9,59);
INSERT INTO ab_permission_view VALUES(177,3,59);
INSERT INTO ab_permission_view VALUES(178,27,59);
INSERT INTO ab_permission_view VALUES(179,5,59);
INSERT INTO ab_permission_view VALUES(180,24,59);
INSERT INTO ab_permission_view VALUES(181,20,59);
INSERT INTO ab_permission_view VALUES(182,18,59);
INSERT INTO ab_permission_view VALUES(183,8,60);
INSERT INTO ab_permission_view VALUES(184,9,60);
INSERT INTO ab_permission_view VALUES(185,3,60);
INSERT INTO ab_permission_view VALUES(186,27,60);
INSERT INTO ab_permission_view VALUES(187,5,60);
INSERT INTO ab_permission_view VALUES(188,20,60);
INSERT INTO ab_permission_view VALUES(189,18,60);
INSERT INTO ab_permission_view VALUES(190,8,61);
INSERT INTO ab_permission_view VALUES(191,9,61);
INSERT INTO ab_permission_view VALUES(192,3,61);
INSERT INTO ab_permission_view VALUES(193,27,61);
INSERT INTO ab_permission_view VALUES(194,5,61);
INSERT INTO ab_permission_view VALUES(195,20,61);
INSERT INTO ab_permission_view VALUES(196,18,61);
INSERT INTO ab_permission_view VALUES(197,8,62);
INSERT INTO ab_permission_view VALUES(198,9,62);
INSERT INTO ab_permission_view VALUES(199,3,62);
INSERT INTO ab_permission_view VALUES(200,27,62);
INSERT INTO ab_permission_view VALUES(201,5,62);
INSERT INTO ab_permission_view VALUES(202,20,62);
INSERT INTO ab_permission_view VALUES(203,18,62);
INSERT INTO ab_permission_view VALUES(204,30,41);
INSERT INTO ab_permission_view VALUES(205,30,44);
INSERT INTO ab_permission_view VALUES(206,30,59);
INSERT INTO ab_permission_view VALUES(207,30,62);
INSERT INTO ab_permission_view VALUES(208,8,63);
INSERT INTO ab_permission_view VALUES(209,9,63);
INSERT INTO ab_permission_view VALUES(210,3,63);
INSERT INTO ab_permission_view VALUES(211,27,63);
INSERT INTO ab_permission_view VALUES(212,8,64);
INSERT INTO ab_permission_view VALUES(213,9,64);
INSERT INTO ab_permission_view VALUES(214,3,64);
INSERT INTO ab_permission_view VALUES(215,27,64);
CREATE TABLE ab_user_role (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	role_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (user_id, role_id), 
	FOREIGN KEY(user_id) REFERENCES ab_user (id), 
	FOREIGN KEY(role_id) REFERENCES ab_role (id)
);
INSERT INTO ab_user_role VALUES(1,1,3);
INSERT INTO ab_user_role VALUES(2,2,2);
INSERT INTO ab_user_role VALUES(3,3,2);
INSERT INTO ab_user_role VALUES(4,4,2);
CREATE TABLE ab_permission_view_role (
	id INTEGER NOT NULL, 
	permission_view_id INTEGER, 
	role_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (permission_view_id, role_id), 
	FOREIGN KEY(permission_view_id) REFERENCES ab_permission_view (id), 
	FOREIGN KEY(role_id) REFERENCES ab_role (id)
);
INSERT INTO ab_permission_view_role VALUES(1,1,3);
INSERT INTO ab_permission_view_role VALUES(2,2,3);
INSERT INTO ab_permission_view_role VALUES(3,3,3);
INSERT INTO ab_permission_view_role VALUES(4,4,3);
INSERT INTO ab_permission_view_role VALUES(5,5,3);
INSERT INTO ab_permission_view_role VALUES(6,6,3);
INSERT INTO ab_permission_view_role VALUES(7,7,3);
INSERT INTO ab_permission_view_role VALUES(8,8,3);
INSERT INTO ab_permission_view_role VALUES(9,9,3);
INSERT INTO ab_permission_view_role VALUES(10,10,3);
INSERT INTO ab_permission_view_role VALUES(11,11,3);
INSERT INTO ab_permission_view_role VALUES(12,12,3);
INSERT INTO ab_permission_view_role VALUES(13,13,3);
INSERT INTO ab_permission_view_role VALUES(14,14,3);
INSERT INTO ab_permission_view_role VALUES(15,15,3);
INSERT INTO ab_permission_view_role VALUES(16,16,3);
INSERT INTO ab_permission_view_role VALUES(17,17,3);
INSERT INTO ab_permission_view_role VALUES(18,18,3);
INSERT INTO ab_permission_view_role VALUES(19,19,3);
INSERT INTO ab_permission_view_role VALUES(20,20,3);
INSERT INTO ab_permission_view_role VALUES(21,21,3);
INSERT INTO ab_permission_view_role VALUES(22,22,3);
INSERT INTO ab_permission_view_role VALUES(23,23,3);
INSERT INTO ab_permission_view_role VALUES(24,24,3);
INSERT INTO ab_permission_view_role VALUES(25,25,3);
INSERT INTO ab_permission_view_role VALUES(26,26,3);
INSERT INTO ab_permission_view_role VALUES(27,27,3);
INSERT INTO ab_permission_view_role VALUES(28,28,3);
INSERT INTO ab_permission_view_role VALUES(29,29,3);
INSERT INTO ab_permission_view_role VALUES(30,30,3);
INSERT INTO ab_permission_view_role VALUES(31,31,3);
INSERT INTO ab_permission_view_role VALUES(32,32,3);
INSERT INTO ab_permission_view_role VALUES(33,33,3);
INSERT INTO ab_permission_view_role VALUES(34,34,3);
INSERT INTO ab_permission_view_role VALUES(35,35,3);
INSERT INTO ab_permission_view_role VALUES(36,36,3);
INSERT INTO ab_permission_view_role VALUES(37,37,3);
INSERT INTO ab_permission_view_role VALUES(38,38,3);
INSERT INTO ab_permission_view_role VALUES(39,39,3);
INSERT INTO ab_permission_view_role VALUES(40,40,3);
INSERT INTO ab_permission_view_role VALUES(41,41,3);
INSERT INTO ab_permission_view_role VALUES(42,42,3);
INSERT INTO ab_permission_view_role VALUES(43,43,3);
INSERT INTO ab_permission_view_role VALUES(44,44,3);
INSERT INTO ab_permission_view_role VALUES(45,45,3);
INSERT INTO ab_permission_view_role VALUES(46,46,3);
INSERT INTO ab_permission_view_role VALUES(47,47,3);
INSERT INTO ab_permission_view_role VALUES(48,48,3);
INSERT INTO ab_permission_view_role VALUES(49,49,3);
INSERT INTO ab_permission_view_role VALUES(50,50,3);
INSERT INTO ab_permission_view_role VALUES(51,51,3);
INSERT INTO ab_permission_view_role VALUES(52,52,3);
INSERT INTO ab_permission_view_role VALUES(53,53,3);
INSERT INTO ab_permission_view_role VALUES(54,54,3);
INSERT INTO ab_permission_view_role VALUES(55,55,3);
INSERT INTO ab_permission_view_role VALUES(56,56,3);
INSERT INTO ab_permission_view_role VALUES(57,57,3);
INSERT INTO ab_permission_view_role VALUES(58,58,3);
INSERT INTO ab_permission_view_role VALUES(59,59,3);
INSERT INTO ab_permission_view_role VALUES(60,60,3);
INSERT INTO ab_permission_view_role VALUES(61,61,3);
INSERT INTO ab_permission_view_role VALUES(62,62,3);
INSERT INTO ab_permission_view_role VALUES(63,63,3);
INSERT INTO ab_permission_view_role VALUES(64,64,3);
INSERT INTO ab_permission_view_role VALUES(65,65,3);
INSERT INTO ab_permission_view_role VALUES(66,66,3);
INSERT INTO ab_permission_view_role VALUES(67,67,3);
INSERT INTO ab_permission_view_role VALUES(68,68,3);
INSERT INTO ab_permission_view_role VALUES(69,69,3);
INSERT INTO ab_permission_view_role VALUES(70,70,3);
INSERT INTO ab_permission_view_role VALUES(71,71,3);
INSERT INTO ab_permission_view_role VALUES(72,72,3);
INSERT INTO ab_permission_view_role VALUES(73,73,3);
INSERT INTO ab_permission_view_role VALUES(74,74,3);
INSERT INTO ab_permission_view_role VALUES(75,75,3);
INSERT INTO ab_permission_view_role VALUES(76,76,3);
INSERT INTO ab_permission_view_role VALUES(77,77,3);
INSERT INTO ab_permission_view_role VALUES(78,78,3);
INSERT INTO ab_permission_view_role VALUES(79,79,3);
INSERT INTO ab_permission_view_role VALUES(80,80,3);
INSERT INTO ab_permission_view_role VALUES(81,81,3);
INSERT INTO ab_permission_view_role VALUES(82,82,3);
INSERT INTO ab_permission_view_role VALUES(83,83,3);
INSERT INTO ab_permission_view_role VALUES(84,84,3);
INSERT INTO ab_permission_view_role VALUES(85,85,3);
INSERT INTO ab_permission_view_role VALUES(86,86,3);
INSERT INTO ab_permission_view_role VALUES(87,87,3);
INSERT INTO ab_permission_view_role VALUES(88,88,3);
INSERT INTO ab_permission_view_role VALUES(89,89,3);
INSERT INTO ab_permission_view_role VALUES(90,90,3);
INSERT INTO ab_permission_view_role VALUES(91,91,3);
INSERT INTO ab_permission_view_role VALUES(92,92,3);
INSERT INTO ab_permission_view_role VALUES(93,93,3);
INSERT INTO ab_permission_view_role VALUES(94,94,3);
INSERT INTO ab_permission_view_role VALUES(95,95,3);
INSERT INTO ab_permission_view_role VALUES(96,96,3);
INSERT INTO ab_permission_view_role VALUES(97,97,3);
INSERT INTO ab_permission_view_role VALUES(98,98,3);
INSERT INTO ab_permission_view_role VALUES(99,99,3);
INSERT INTO ab_permission_view_role VALUES(100,100,3);
INSERT INTO ab_permission_view_role VALUES(101,101,3);
INSERT INTO ab_permission_view_role VALUES(102,102,3);
INSERT INTO ab_permission_view_role VALUES(103,103,3);
INSERT INTO ab_permission_view_role VALUES(104,104,3);
INSERT INTO ab_permission_view_role VALUES(105,105,3);
INSERT INTO ab_permission_view_role VALUES(106,106,3);
INSERT INTO ab_permission_view_role VALUES(107,107,3);
INSERT INTO ab_permission_view_role VALUES(108,108,3);
INSERT INTO ab_permission_view_role VALUES(109,109,3);
INSERT INTO ab_permission_view_role VALUES(110,110,3);
INSERT INTO ab_permission_view_role VALUES(111,111,3);
INSERT INTO ab_permission_view_role VALUES(112,112,3);
INSERT INTO ab_permission_view_role VALUES(113,113,3);
INSERT INTO ab_permission_view_role VALUES(114,114,3);
INSERT INTO ab_permission_view_role VALUES(115,115,3);
INSERT INTO ab_permission_view_role VALUES(116,116,3);
INSERT INTO ab_permission_view_role VALUES(117,117,3);
INSERT INTO ab_permission_view_role VALUES(118,118,3);
INSERT INTO ab_permission_view_role VALUES(119,119,3);
INSERT INTO ab_permission_view_role VALUES(120,120,3);
INSERT INTO ab_permission_view_role VALUES(121,121,3);
INSERT INTO ab_permission_view_role VALUES(122,122,3);
INSERT INTO ab_permission_view_role VALUES(123,123,3);
INSERT INTO ab_permission_view_role VALUES(124,124,3);
INSERT INTO ab_permission_view_role VALUES(125,125,3);
INSERT INTO ab_permission_view_role VALUES(126,126,3);
INSERT INTO ab_permission_view_role VALUES(127,127,3);
INSERT INTO ab_permission_view_role VALUES(128,128,3);
INSERT INTO ab_permission_view_role VALUES(129,129,3);
INSERT INTO ab_permission_view_role VALUES(130,130,3);
INSERT INTO ab_permission_view_role VALUES(131,131,3);
INSERT INTO ab_permission_view_role VALUES(132,132,3);
INSERT INTO ab_permission_view_role VALUES(133,133,3);
INSERT INTO ab_permission_view_role VALUES(134,134,3);
INSERT INTO ab_permission_view_role VALUES(135,135,3);
INSERT INTO ab_permission_view_role VALUES(136,136,3);
INSERT INTO ab_permission_view_role VALUES(137,137,3);
INSERT INTO ab_permission_view_role VALUES(138,138,3);
INSERT INTO ab_permission_view_role VALUES(139,139,3);
INSERT INTO ab_permission_view_role VALUES(140,140,3);
INSERT INTO ab_permission_view_role VALUES(141,141,3);
INSERT INTO ab_permission_view_role VALUES(142,142,3);
INSERT INTO ab_permission_view_role VALUES(143,143,3);
INSERT INTO ab_permission_view_role VALUES(144,144,3);
INSERT INTO ab_permission_view_role VALUES(145,145,3);
INSERT INTO ab_permission_view_role VALUES(146,146,3);
INSERT INTO ab_permission_view_role VALUES(147,147,3);
INSERT INTO ab_permission_view_role VALUES(148,148,3);
INSERT INTO ab_permission_view_role VALUES(149,149,3);
INSERT INTO ab_permission_view_role VALUES(150,150,3);
INSERT INTO ab_permission_view_role VALUES(151,151,3);
INSERT INTO ab_permission_view_role VALUES(152,152,3);
INSERT INTO ab_permission_view_role VALUES(153,153,3);
INSERT INTO ab_permission_view_role VALUES(154,154,3);
INSERT INTO ab_permission_view_role VALUES(155,155,3);
INSERT INTO ab_permission_view_role VALUES(156,156,3);
INSERT INTO ab_permission_view_role VALUES(157,157,3);
INSERT INTO ab_permission_view_role VALUES(158,158,3);
INSERT INTO ab_permission_view_role VALUES(159,159,3);
INSERT INTO ab_permission_view_role VALUES(160,160,3);
INSERT INTO ab_permission_view_role VALUES(161,161,3);
INSERT INTO ab_permission_view_role VALUES(162,162,3);
INSERT INTO ab_permission_view_role VALUES(163,163,3);
INSERT INTO ab_permission_view_role VALUES(164,164,3);
INSERT INTO ab_permission_view_role VALUES(165,165,3);
INSERT INTO ab_permission_view_role VALUES(166,166,3);
INSERT INTO ab_permission_view_role VALUES(167,167,3);
INSERT INTO ab_permission_view_role VALUES(168,168,3);
INSERT INTO ab_permission_view_role VALUES(169,169,3);
INSERT INTO ab_permission_view_role VALUES(170,170,3);
INSERT INTO ab_permission_view_role VALUES(171,171,3);
INSERT INTO ab_permission_view_role VALUES(172,172,3);
INSERT INTO ab_permission_view_role VALUES(173,173,3);
INSERT INTO ab_permission_view_role VALUES(174,174,3);
INSERT INTO ab_permission_view_role VALUES(175,175,3);
INSERT INTO ab_permission_view_role VALUES(176,176,3);
INSERT INTO ab_permission_view_role VALUES(177,177,3);
INSERT INTO ab_permission_view_role VALUES(178,178,3);
INSERT INTO ab_permission_view_role VALUES(179,179,3);
INSERT INTO ab_permission_view_role VALUES(180,180,3);
INSERT INTO ab_permission_view_role VALUES(181,181,3);
INSERT INTO ab_permission_view_role VALUES(182,182,3);
INSERT INTO ab_permission_view_role VALUES(183,183,3);
INSERT INTO ab_permission_view_role VALUES(184,184,3);
INSERT INTO ab_permission_view_role VALUES(185,185,3);
INSERT INTO ab_permission_view_role VALUES(186,186,3);
INSERT INTO ab_permission_view_role VALUES(187,187,3);
INSERT INTO ab_permission_view_role VALUES(188,188,3);
INSERT INTO ab_permission_view_role VALUES(189,189,3);
INSERT INTO ab_permission_view_role VALUES(190,190,3);
INSERT INTO ab_permission_view_role VALUES(191,191,3);
INSERT INTO ab_permission_view_role VALUES(192,192,3);
INSERT INTO ab_permission_view_role VALUES(193,193,3);
INSERT INTO ab_permission_view_role VALUES(194,194,3);
INSERT INTO ab_permission_view_role VALUES(195,195,3);
INSERT INTO ab_permission_view_role VALUES(196,196,3);
INSERT INTO ab_permission_view_role VALUES(197,197,3);
INSERT INTO ab_permission_view_role VALUES(198,198,3);
INSERT INTO ab_permission_view_role VALUES(199,199,3);
INSERT INTO ab_permission_view_role VALUES(200,200,3);
INSERT INTO ab_permission_view_role VALUES(201,201,3);
INSERT INTO ab_permission_view_role VALUES(202,202,3);
INSERT INTO ab_permission_view_role VALUES(203,203,3);
INSERT INTO ab_permission_view_role VALUES(204,204,3);
INSERT INTO ab_permission_view_role VALUES(205,205,3);
INSERT INTO ab_permission_view_role VALUES(206,206,3);
INSERT INTO ab_permission_view_role VALUES(207,207,3);
INSERT INTO ab_permission_view_role VALUES(208,208,3);
INSERT INTO ab_permission_view_role VALUES(209,209,3);
INSERT INTO ab_permission_view_role VALUES(210,210,3);
INSERT INTO ab_permission_view_role VALUES(211,211,3);
INSERT INTO ab_permission_view_role VALUES(212,212,3);
INSERT INTO ab_permission_view_role VALUES(213,213,3);
INSERT INTO ab_permission_view_role VALUES(214,214,3);
INSERT INTO ab_permission_view_role VALUES(215,215,3);
CREATE TABLE coupon (
	created_on DATETIME NOT NULL, 
	changed_on DATETIME NOT NULL, 
	status VARCHAR(1) NOT NULL, 
	id INTEGER NOT NULL, 
	code VARCHAR(20) NOT NULL, 
	expiry_date DATE NOT NULL, 
	is_multiple VARCHAR(10) NOT NULL, 
	coupon_status VARCHAR(20) NOT NULL, 
	discount INTEGER NOT NULL, 
	created_by_fk INTEGER NOT NULL, 
	changed_by_fk INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(created_by_fk) REFERENCES ab_user (id), 
	FOREIGN KEY(changed_by_fk) REFERENCES ab_user (id)
);
INSERT INTO coupon VALUES('2019-09-11 14:28:24.659060','2019-09-11 17:28:34.573791','A',1,'PRO01','2020-01-01','Yes','Open',10,1,1);
INSERT INTO coupon VALUES('2019-09-12 14:26:30.154610','2019-09-16 11:24:01.039148','A',2,'AAA','2020-01-01','Yes','Open',15,2,2);
CREATE TABLE category (created_on DATETIME NOT NULL, changed_on DATETIME NOT NULL, status VARCHAR (1) NOT NULL, id INTEGER NOT NULL, category_type VARCHAR (20) NOT NULL, description VARCHAR (50) NOT NULL, price NUMERIC (8, 2) NOT NULL, expiry_date DATE NOT NULL, created_by_fk INTEGER NOT NULL, changed_by_fk INTEGER NOT NULL, quantity INTEGER DEFAULT (0) NOT NULL, PRIMARY KEY (id), FOREIGN KEY (created_by_fk) REFERENCES ab_user (id), FOREIGN KEY (changed_by_fk) REFERENCES ab_user (id));
INSERT INTO category VALUES('2019-09-11 15:01:00.136611','2019-09-11 15:01:00.136659','A',1,'Services','Physiotherapy',750,'2999-12-31',1,1,1);
INSERT INTO category VALUES('2019-09-11 15:01:55.066678','2019-09-11 15:01:55.066701','A',2,'Services','Sports Therapy (30mins)',400,'2999-12-31',1,1,1);
INSERT INTO category VALUES('2019-09-11 15:04:14.446067','2019-09-11 15:04:14.446089','A',3,'Services','Sports Therapy (45mins)',600,'2999-12-31',1,1,1);
INSERT INTO category VALUES('2019-09-11 15:05:10.084735','2019-09-11 15:05:10.084757','A',4,'Services','Stretching (30mins)',400,'2999-12-31',1,1,1);
INSERT INTO category VALUES('2019-09-16 01:04:26.180375','2019-09-16 01:04:26.180416','A',6,'Products','Miracle Prehab x Dr. Prehab 迷你拉力環帶特別版 (一套兩條)',88,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-16 01:10:47.172762','2019-09-16 01:10:47.172786','A',7,'Products','Dr. Prehab 迷你拉力環帶 (一套四條)',160,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-16 01:11:55.904437','2019-09-16 01:11:55.904545','A',8,'Products','Dr. Prehab 按摩球',120,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-16 01:13:35.872750','2019-09-16 01:13:35.872772','A',9,'Products','Curble 坐墊',480,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-16 01:14:30.911044','2019-09-16 01:14:30.911069','A',10,'Products','Curble 坐墊 (黑色加強版) ',580,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-16 01:15:03.162928','2019-09-16 01:15:03.162952','A',11,'Products','Posture medic 寒背帶',350,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-16 01:15:33.780848','2019-09-16 01:15:33.780870','A',12,'Products','T-max 肌內效貼布',120,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-16 01:16:42.369527','2019-09-16 01:16:42.369571','A',13,'Products','各款矯型鞋墊',0,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-16 01:17:19.840009','2019-09-16 01:17:19.840034','A',14,'Products','各款壓力襪',0,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-16 01:17:49.962143','2019-09-16 01:17:49.962193','A',15,'Products','Tazewa 按摩槍',0,'2999-12-31',2,2,1);
INSERT INTO category VALUES('2019-09-18 23:57:35.514323','2019-09-19 00:08:24.191977','A',16,'Packages','Sports Therapy (30mins)',3000,'2020-01-01',2,2,10);
INSERT INTO category VALUES('2019-09-19 00:01:12.484386','2019-09-22 23:51:39.477780','A',17,'Packages','Sports Therapy (45mins)',5000,'2019-12-31',2,2,10);
CREATE TABLE customer (
	created_on DATETIME NOT NULL, 
	changed_on DATETIME NOT NULL, 
	status VARCHAR(1) NOT NULL, 
	id INTEGER NOT NULL, 
	salvation VARCHAR(10) NOT NULL, 
	first_name VARCHAR(50) NOT NULL, 
	last_name VARCHAR(50) NOT NULL, 
	chinese_name VARCHAR(20), 
	date_of_birth VARCHAR(10) NOT NULL, 
	hkid VARCHAR(20) NOT NULL, 
	email VARCHAR(50), 
	contact_no VARCHAR(20) NOT NULL, 
	mobile_no VARCHAR(20), 
	emergency_contact VARCHAR(20), 
	referral_doctor VARCHAR(50), 
	source_of_referral VARCHAR(50), 
	physician1_id INTEGER NOT NULL, 
	physician2_id INTEGER, 
	physician3_id INTEGER, 
	physician4_id INTEGER, 
	physician5_id INTEGER, 
	created_by_fk INTEGER NOT NULL, 
	changed_by_fk INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(physician1_id) REFERENCES ab_user (id), 
	FOREIGN KEY(physician2_id) REFERENCES ab_user (id), 
	FOREIGN KEY(physician3_id) REFERENCES ab_user (id), 
	FOREIGN KEY(physician4_id) REFERENCES ab_user (id), 
	FOREIGN KEY(physician5_id) REFERENCES ab_user (id), 
	FOREIGN KEY(created_by_fk) REFERENCES ab_user (id), 
	FOREIGN KEY(changed_by_fk) REFERENCES ab_user (id)
);
INSERT INTO customer VALUES('2019-09-18 23:51:00.568485','2019-09-26 14:43:48.156305','A',1,'Mr','Peter','Chan','','1990-01-01','A123456(7)','','98765432','','','','',2,3,4,NULL,NULL,2,2);
INSERT INTO customer VALUES('2019-09-19 00:10:39.572383','2019-09-19 00:10:39.572407','A',2,'Miss','Mary','Jane','','1990-01-01','A23456(8)','','91234567','','','','',2,NULL,NULL,NULL,NULL,2,2);
INSERT INTO customer VALUES('2019-09-25 15:20:39.409208','2019-09-25 15:20:39.409251','A',3,'Mr','Chiu Hung','Yau','','9-3-1996','Y438402(2)','','90616157','','','','',2,NULL,NULL,NULL,NULL,2,2);
CREATE TABLE customer_document (
	created_on DATETIME NOT NULL, 
	changed_on DATETIME NOT NULL, 
	status VARCHAR(1) NOT NULL, 
	id INTEGER NOT NULL, 
	customer_id INTEGER, 
	file TEXT NOT NULL, 
	description VARCHAR(150), 
	created_by_fk INTEGER NOT NULL, 
	changed_by_fk INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_id) REFERENCES customer (id), 
	FOREIGN KEY(created_by_fk) REFERENCES ab_user (id), 
	FOREIGN KEY(changed_by_fk) REFERENCES ab_user (id)
);
CREATE TABLE medical_history (
	created_on DATETIME NOT NULL, 
	changed_on DATETIME NOT NULL, 
	status VARCHAR(1) NOT NULL, 
	id INTEGER NOT NULL, 
	customer_id INTEGER, 
	operation VARCHAR(100), 
	operation_date VARCHAR(50), 
	cancer VARCHAR(100), 
	certificated_date VARCHAR(50), 
	heart_diseases VARCHAR(10), 
	diabetes VARCHAR(10), 
	dizziness VARCHAR(10), 
	allergy VARCHAR(10), 
	medicine_currently_taking VARCHAR(100), 
	emergency_medicine VARCHAR(100), 
	notes TEXT, 
	created_by_fk INTEGER NOT NULL, 
	changed_by_fk INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_id) REFERENCES customer (id), 
	FOREIGN KEY(created_by_fk) REFERENCES ab_user (id), 
	FOREIGN KEY(changed_by_fk) REFERENCES ab_user (id)
);
CREATE TABLE ab_user (id INTEGER NOT NULL, first_name VARCHAR (64) NOT NULL, last_name VARCHAR (64) NOT NULL, username VARCHAR (64) NOT NULL, password VARCHAR (256), active BOOLEAN, email VARCHAR (64) NOT NULL, last_login DATETIME, login_count INTEGER, fail_login_count INTEGER, created_on DATETIME, changed_on DATETIME, speciality VARCHAR (20), created_by_fk INTEGER, changed_by_fk INTEGER, user_type VARCHAR (64), color_code VARCHAR (10), PRIMARY KEY (id), UNIQUE (username), CHECK (active IN (0, 1)), UNIQUE (email), FOREIGN KEY (created_by_fk) REFERENCES ab_user (id), FOREIGN KEY (changed_by_fk) REFERENCES ab_user (id));
INSERT INTO ab_user VALUES(1,'admin','user','admin','pbkdf2:sha256:50000$z34Sw1HS$562340253117ca1f4519e6cb8a52c186fff210db7475c447cf367c6d60181a75',1,'admin@fab.org','2019-09-11 14:21:37.998447',15,0,'2019-07-31 01:06:27.508446','2019-07-31 01:06:27.508454',NULL,NULL,NULL,'Admin','#337ab7');
INSERT INTO ab_user VALUES(2,'Derek','Yeung','derek','pbkdf2:sha256:50000$gUPH91Go$3b1dc38b6855ee5d46349a3434c92efa9933f5eae55b66b6f385503e45ddd620',1,'derek@miracleprehab.com.hk','2019-09-22 16:13:45.881274',17,0,'2019-07-31 01:07:20.354935','2019-09-11 12:13:16.792601','Physio',1,1,'Physician','#449d44');
INSERT INTO ab_user VALUES(3,'Chloe','Mo','chloe','pbkdf2:sha256:50000$QHlVKdyR$e5a6e7d433713e7860f313ffe5e4e9bbcdb14aa5364fccd1f08d056fc915ef7d',1,'chloe@miracleprehab.com.hk','2019-09-11 17:37:32.776060',3,0,'2019-07-31 04:52:19.408510','2019-09-11 12:14:44.855414','Physio',1,1,'Physician','#31b0d5');
INSERT INTO ab_user VALUES(4,'Aries','Cheng','aries','pbkdf2:sha256:50000$vECDboTQ$fda56f0bfbc8f6f02d801fe124aaf67ff431198794fe9624068e874a64ea4c4e',1,'aries@miracleprehab.com.hk','2019-09-02 03:09:27.063807',3,0,'2019-07-31 04:53:08.376499','2019-09-11 14:27:10.336679','Physio',1,1,'Physician','#ec971f');
CREATE TABLE appointment (created_on DATETIME NOT NULL, changed_on DATETIME NOT NULL, status VARCHAR (1) NOT NULL, id INTEGER NOT NULL, customer_id INTEGER NOT NULL, physician_id INTEGER NOT NULL, begin_datetime DATETIME NOT NULL, end_datetime DATETIME, referral_doctor VARCHAR (50), source_of_referral VARCHAR (50), sick_leave VARCHAR (50), insurance_cover VARCHAR (50), injury_due_to VARCHAR (100), facilities_booking VARCHAR (50), diagnosis TEXT, created_by_fk INTEGER NOT NULL, changed_by_fk INTEGER NOT NULL, receipt_no VARCHAR (10) NOT NULL DEFAULT ('-'), color_code VARCHAR (10), PRIMARY KEY (id), FOREIGN KEY (customer_id) REFERENCES customer (id), FOREIGN KEY (physician_id) REFERENCES ab_user (id), FOREIGN KEY (created_by_fk) REFERENCES ab_user (id), FOREIGN KEY (changed_by_fk) REFERENCES ab_user (id));
INSERT INTO appointment VALUES('2019-09-26 14:45:29.445375','2019-09-26 14:45:59.357357','A',1,1,2,'2019-09-27 13:00:00.000000','2019-09-27 14:00:00.000000','','','Yes','Yes','','No','',2,2,'00001','#337ab7');
CREATE TABLE receipt (created_on DATETIME NOT NULL, changed_on DATETIME NOT NULL, status VARCHAR (1) NOT NULL, id INTEGER NOT NULL, receipt_no VARCHAR (50) NOT NULL, receipt_type VARCHAR (10) NOT NULL, customer_id INTEGER, appointment_id INTEGER, package_id INTEGER, coupon_code VARCHAR (50), receipt_date DATE NOT NULL, payment_method VARCHAR (20) NOT NULL, payment_reference VARCHAR (50), created_by_fk INTEGER NOT NULL, changed_by_fk INTEGER NOT NULL, PRIMARY KEY (id), FOREIGN KEY (customer_id) REFERENCES customer (id), FOREIGN KEY (appointment_id) REFERENCES appointment (id), FOREIGN KEY (package_id) REFERENCES package (id), FOREIGN KEY (created_by_fk) REFERENCES ab_user (id), FOREIGN KEY (changed_by_fk) REFERENCES ab_user (id));
INSERT INTO receipt VALUES('2019-09-26 14:45:59.245273','2019-09-26 14:45:59.245332','A',1,'00001','Appointment',1,1,NULL,'PRO01','2019-09-26','CASH','',2,2);
INSERT INTO receipt VALUES('2019-09-26 14:48:43.358290','2019-09-26 14:48:43.358349','A',2,'00002','Package',1,NULL,1,'PRO01','2019-09-26','VISA','',2,2);
INSERT INTO receipt VALUES('2019-09-26 14:54:00.023592','2019-09-26 14:54:00.023673','A',3,'00003','General',NULL,NULL,NULL,'','2019-09-26','CASH','',2,2);
CREATE TABLE package_ticket (
	created_on DATETIME NOT NULL, 
	changed_on DATETIME NOT NULL, 
	status VARCHAR(1) NOT NULL, 
	id INTEGER NOT NULL, 
	package_id INTEGER NOT NULL, 
	mobile VARCHAR(20), 
	begin_datetime DATETIME NOT NULL, 
	end_datetime DATETIME, 
	customer_id INTEGER NOT NULL, 
	created_by_fk INTEGER NOT NULL, 
	changed_by_fk INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(package_id) REFERENCES package (id), 
	FOREIGN KEY(customer_id) REFERENCES customer (id), 
	FOREIGN KEY(created_by_fk) REFERENCES ab_user (id), 
	FOREIGN KEY(changed_by_fk) REFERENCES ab_user (id)
);
INSERT INTO package_ticket VALUES('2019-09-26 14:49:54.472666','2019-09-26 14:49:54.472748','A',1,1,'98765432','2019-09-27 13:00:00.000000','2019-09-27 14:00:00.000000',1,2,2);
CREATE TABLE package (created_on DATETIME NOT NULL, changed_on DATETIME NOT NULL, status VARCHAR (1) NOT NULL, id INTEGER NOT NULL, customer_id INTEGER NOT NULL, begin_date DATE NOT NULL, end_date DATE NOT NULL, category_id INTEGER NOT NULL, description VARCHAR (100) NOT NULL, sharing_mobile1 VARCHAR (20) NOT NULL, sharing_mobile2 VARCHAR (20), sharing_mobile3 VARCHAR (20), sharing_mobile4 VARCHAR (20), sharing_mobile5 VARCHAR (20), receipt_no VARCHAR (10) NOT NULL, created_by_fk INTEGER NOT NULL, changed_by_fk INTEGER NOT NULL, ticket_count INTEGER, ticket_remaining INTEGER, PRIMARY KEY (id), FOREIGN KEY (customer_id) REFERENCES customer (id), FOREIGN KEY (category_id) REFERENCES category (id), FOREIGN KEY (created_by_fk) REFERENCES ab_user (id), FOREIGN KEY (changed_by_fk) REFERENCES ab_user (id));
INSERT INTO package VALUES('2019-09-26 14:47:45.411000','2019-09-26 14:49:54.433762','A',1,1,'2019-10-01','2019-11-30',16,'Packages - Sports Therapy (30mins)','98765432','','','','','00002',2,2,10,9);
CREATE TABLE receipt_item (created_on DATETIME NOT NULL, changed_on DATETIME NOT NULL, status VARCHAR (1) NOT NULL, id INTEGER NOT NULL, receipt_id INTEGER NOT NULL, category_id INTEGER, description VARCHAR (100), price NUMERIC (8, 2), quantity INTEGER NOT NULL, apply_coupon VARCHAR (10) NOT NULL, discount NUMERIC (8, 2), amount NUMERIC (8, 2), created_by_fk INTEGER NOT NULL, changed_by_fk INTEGER NOT NULL, package_id INTEGER REFERENCES package (id), PRIMARY KEY (id), FOREIGN KEY (receipt_id) REFERENCES receipt (id), FOREIGN KEY (category_id) REFERENCES category (id), FOREIGN KEY (created_by_fk) REFERENCES ab_user (id), FOREIGN KEY (changed_by_fk) REFERENCES ab_user (id), FOREIGN KEY (package_id) REFERENCES package (id));
INSERT INTO receipt_item VALUES('2019-09-26 14:46:36.991993','2019-09-26 14:46:36.992061','A',1,1,1,'Services - Physiotherapy',750,1,'Yes',10,675,2,2,NULL);
INSERT INTO receipt_item VALUES('2019-09-26 14:48:43.524375','2019-09-26 14:48:43.524434','A',2,2,16,'Packages - Sports Therapy (30mins)',3000,1,'Yes',10,2700,2,2,NULL);
INSERT INTO receipt_item VALUES('2019-09-26 14:49:54.293393','2019-09-26 14:49:54.293472','A',3,1,NULL,'Packages - Sports Therapy (30mins) - $3000.00 (2019-10-01 - 2019-11-30)',3000,1,'No',100,0,2,2,1);
INSERT INTO receipt_item VALUES('2019-09-26 16:00:32.507210','2019-09-26 16:00:47.298237','A',4,3,7,'Products - Dr. Prehab 迷你拉力環帶 (一套四條)',160,1,'No',NULL,160,2,2,NULL);
CREATE VIEW view_appointment_calendar as
select a.id, a.customer_id, a.physician_id, a.begin_datetime, a.end_datetime, a.color_code,
       pa.first_name || ' ' || pa.last_name as customer_name,
       ph.first_name || ' ' || ph.last_name as physician_name
from 
    appointment a
left join customer pa on pa.id = a.customer_id
left join ab_user ph on ph.id = a.physician_id;
CREATE VIEW view_report_receipt as
select
    a.receipt_no, a.receipt_date,
    d.first_name || ' ' || d.last_name as customer_name, d.contact_no, d.hkid, d.date_of_birth,
    a.payment_method, a.payment_reference, b.total
from 
    receipt a
left join (
    select receipt_id, sum(amount) as total from (
        select receipt_id, amount from receipt_item where status = 'A'
    ) group by receipt_id
) b 
on a.id = b.receipt_id
left join customer d 
on a.customer_id = d.id
where a.status = 'A';
CREATE VIEW view_report_receipt_item as
select 
    c.receipt_no, c.receipt_date, 
    b.category_type, 
    a.description,
    a.apply_coupon,
    c.coupon_code,
    b.original_price,
    a.amount as actual_price
from receipt_item a
left join ( select id, category_type, description, price as original_price from category ) b 
on a.category_id = b.id
left join receipt c
on a.receipt_id = c.id
left join coupon e
on c.coupon_code = e.code
where
a.status = 'A' and
c.status = 'A';
COMMIT;
