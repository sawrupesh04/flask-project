CREATE TABLE `ItemListDb`.`tblUser` (
`UserId` INT NOT NULL AUTO_INCREMENT,
`UserName` VARCHAR(45) NULL,
`Password` VARCHAR(45) NULL,
PRIMARY KEY (`UserId`));

-- -----------------


-----------------------------------------------------------------

USE `ItemListDb`;
DROP procedure IF EXISTS `sp_AuthenticateUser`;

DELIMITER $$
USE `ItemListDb`$$
CREATE PROCEDURE `sp_AuthenticateUser` (
IN p_username VARCHAR(20)
)
BEGIN

     select * from tblUser where UserName = p_username;

END$$

DELIMITER ;

--------------------------------------------------------------------

CREATE TABLE `ItemListDb`.`tblItem` (
  `Id` INT NULL AUTO_INCREMENT,
  `UserId` VARCHAR(45) NULL,
  `ItemName` VARCHAR(45) NULL,
  PRIMARY KEY (`Id`));


-- SPS

DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_AddItems`(
in p_userId int,
in p_item varchar(25)
)
BEGIN
    insert into tblItem(
        UserId,
        ItemName
    )
    values(
        p_userId,
        p_item
    );
END

----------------------------WORKING EMPLOYEE Attendance--------------------------------------------------------

USE `hrmdb`;
DROP procedure IF EXISTS `sp_GetAllAttendance`;

DELIMITER $$
USE `hrmdb`$$
CREATE PROCEDURE `sp_GetAllAttendance` (
in p_empId int
)
BEGIN
    select (SELECT DATE_FORMAT(in_time, "%d/%m/%Y") AS in_date), (SELECT DATE_FORMAT(out_time, "%d/%m/%Y") AS out_date), note from Attendance where employee = p_empId;
END$$

DELIMITER ;
-----------------------------------------END--------------------------------------------------------------------

----------------------------WORKING EMPLOYEE CHECK IN-----------------------------------------------------------

USE `hrmdb`;

DROP procedure IF EXISTS `spAttendance`;

DELIMITER $$
USE `hrmdb`$$
CREATE PROCEDURE `spAttendance` (
IN p_EmployeeId varchar(50),
IN p_InTime varchar(50),
IN p_Note varchar(50)
)
BEGIN

if ( select exists (select 1 from Attendance where employee = p_EmployeeId and in_time = p_InTime) ) THEN

    select 'Already Punched !!';

ELSE

insert into Attendance
(
    employee,
    in_time,
    note
)
values
(
    p_EmployeeId,
    p_InTime,
    p_Note
);

END IF;

END$$

DELIMITER ;

-----------------------------------------END--------------------------------------------------------------------

----------------------------WORKING EMPLOYEE CHECK OUT-----------------------------------------------------------

USE `hrmdb`;

DROP procedure IF EXISTS `spAttendanceOut`;

DELIMITER $$
USE `hrmdb`$$
CREATE PROCEDURE `spAttendanceOut` (
IN p_EmployeeId varchar(50),
IN p_InTime varchar(50),
IN p_OutTime varchar(50),
IN p_Note varchar(50)
)

BEGIN
if ( select exists (select 1 from Attendance where employee = p_EmployeeId and out_time = p_OutTime) ) THEN

    select 'Already Punched Out for Day !!';

ELSE

update Attendance SET out_time = p_OutTime where in_time = p_InTime and employee = p_EmployeeId;

END IF;

END$$

DELIMITER ;

-----------------------------------------END---------------------------------------------------------------------

----------------------------WORKING EMPLOYEE CHECK AUTHORIZATION-----------------------------------------------------------

USE `hrmdb`;
DROP procedure IF EXISTS `sp_AuthenticateEmployee`;

DELIMITER $$
USE `hrmdb`$$
CREATE PROCEDURE `sp_AuthenticateEmployee` (
IN p_first_name VARCHAR(20),
IN p_last_name VARCHAR(20),
IN p_mobile_phone VARCHAR(20)
)
BEGIN

     select employee_id, mobile_phone, status from Employees where first_name = p_first_name and last_name = p_last_name and mobile_phone = p_mobile_phone;

END$$

DELIMITER ;

-----------------------------------------END---------------------------------------------------------------------

----------------------------WORKING EMPLOYEE CHECK AUTHORIZATION------[all parameters]---------------------------
USE `hrmdb`;
DROP procedure IF EXISTS `sp_EmployeeDetails`;

DELIMITER $$
USE `hrmdb`$$
CREATE PROCEDURE `sp_EmployeeDetails` (
IN p_employee_id VARCHAR(20)
)
BEGIN

     select * from Employees where employee_id = p_employee_id;

END$$

DELIMITER ;

-----------------------------------------END---------------------------------------------------------------------

-------------------WORKING EMPLOYEE CHECK AUTHORIZATION------[Selected Parameters]----[Running]------------------

USE `hrmdb`;
DROP procedure IF EXISTS `sp_EmployeeDetails`;

DELIMITER $$
USE `hrmdb`$$
CREATE PROCEDURE `sp_EmployeeDetails` (
IN p_employee_id VARCHAR(20)
)
BEGIN

     SELECT employee_id, first_name, middle_name, last_name, (SELECT name from Nationality where id = nationality),
     (SELECT DATE_FORMAT(birthday, "%d/%m/%Y") AS birthday), gender, city, marital_status, (SELECT name from JobTitles where id = job_title),
     mobile_phone, (SELECT DATE_FORMAT(joined_date, "%d/%m/%Y") AS joined_date), status from Employees where employee_id = p_employee_id;

END$$

DELIMITER ;

-----------------------------------------END---------------------------------------------------------------------