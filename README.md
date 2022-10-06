# HRStaffPortal
## KCH HR Staff Portal Prototype

### This Software is based on Streamlit, a Python framework to build web apps.

#### [Streamlit Configuration]
##### Some extra configuration.

In the `./streamlit/config.toml` you define the theming and some Server behaviour flags.

````
[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
```
#### [MySQL Server Configuration]
##### For proper usage a local MySQL Server is needed.

In the `./streamlit/secrets.toml` you define the user/password combination of the MySQL Server.
```
[mysql]
host = "127.0.0.1"
port = 3306
database = "idcard"
user = "xyz"
password = "xyz"
```

Create Schema / Database with the name 'idcard'. To configure the database to work with the Prototype, run the following SQL commands:

```
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
```