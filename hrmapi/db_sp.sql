CREATE TABLE `ItemListDb`.`tblUser` (
`UserId` INT NOT NULL AUTO_INCREMENT,
`UserName` VARCHAR(45) NULL,
`Password` VARCHAR(45) NULL,
PRIMARY KEY (`UserId`));

-- -----------------

USE `ItemListDb`;

DROP procedure IF EXISTS `spCreateUser`;

DELIMITER $$
USE `ItemListDb`$$
CREATE PROCEDURE `spCreateUser` (
IN p_Username varchar(50),
IN p_Password varchar(50)
)
BEGIN

if ( select exists (select 1 from tblUser where UserName = p_username) ) THEN

    select 'Username Exists !!';

ELSE

insert into tblUser
(
    UserName,
    Password
)
values
(
    p_Username,
    p_Password
);

END IF;

END$$

DELIMITER ;

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
Copy



USE `ItemListDb`;
DROP procedure IF EXISTS `sp_GetAllItems`;

DELIMITER $$
USE `ItemListDb`$$
CREATE PROCEDURE `sp_GetAllItems` (
in p_userId int
)
BEGIN
    select Id, ItemName from tblItem where UserId = p_userId;
END$$

DELIMITER ;

