#### HRStaffPortal
### KCH HR Staff Portal Prototype

## This Software is based on Streamlit, a Python framework to build web apps.

# [MySQL Server Configuration]
For proper usage a local MySQL Server is needed. Config:

In the ./streamlit/secrets.toml you define the user/password combination of the MySQL Server.

Create Schema / Database with the name 'idcard'. To configure the database to work with the 
Prototype, run the following SQL commands:

CREATE TABLE `idcard`.`ImageBase` (
  `ID` INT NOT NULL,
  `LAYOUT` INT NOT NULL,
  `FORENAME` VARCHAR(45) NULL,
  `SURNAME` VARCHAR(45) NULL,
  `JOB_TITLE` VARCHAR(45) NULL,
  `EXPIRY_DATE` VARCHAR(45) NULL,
  `EMPLOYEE_NO` VARCHAR(45) NULL,
  `CARDS_PRINTED` INT NOT NULL,
  `IMAGE` BLOB NULL,
  PRIMARY KEY (`ID`));
  
  CREATE TABLE `idcard`.`TrainingData` (
  `ID` INT NOT NULL,
  `EMPLOYEE_NO` VARCHAR(45) NULL,
  `TRAINING` VARCHAR(45) NULL,
  `INSTITUTE` VARCHAR(45) NULL,
  `DATE` VARCHAR(45) NULL,
  `DAYS` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`));
