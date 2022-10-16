# HRStaffPortal
## HR Staff Portal

This App handles **employee data** which is created through the process of printing *ID Cards* with the **EasyBadge ID Card Printer Software**. All data is stored in a MySQL Databank.

Development with [RStudio](https://www.rstudio.com/products/rstudio/download/#download) is highly recommended. Install [git](https://git-scm.com/download/win) to use version control.

Clone the **repository** of `HRStaffPortal` with following command:

```
git clone https://github.com/DrBenjamin/HRStaffPortal.git
```


#### [Streamlit Setup]
##### Installation of Python, Streamlit and dependencies plus some configuration

Install [Streamlit & Python](https://docs.streamlit.io/library/get-started/installation) to run the source code locally. A virtual Python-Environment like Anaconda is highly recommend.

After that you need to install some **Python libraries*:

```
pip install mysql-connector-python-rf
pip install mysql-connector-python==8.0.29
```

##### Configuration

In the `./streamlit/config.toml` you define the **theming** and some **Streamlit-Server behaviour** flags:

```
[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
```

Create `./streamlit/secrets.toml` and define the user / password combinations:

```
[passwords]
# Follow the rule: username = "password"
xyz = "xyz"

```


#### [MySQL Server Configuration]
##### For proper usage a local MySQL Server is needed

In the `./streamlit/secrets.toml` you define the **user/password** combination for the MySQL Server:

```
[mysql]
host = "127.0.0.1"
port = 3306
database = "idcard"
user = "xyz"
password = "xyz"
```

Connect to your **MySQL Database** and create the *user* you configured in `secrets.toml`. Create a **Schema / Database** with the name `idcard`. 

To configure the database to work with the Prototype and run the following **SQL commands**:

```
  CREATE TABLE `idcard`.`IMAGEBASE` (
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
  
  CREATE TABLE `idcard`.`TRAININGDATA` (
  `ID` INT NOT NULL,
  `EMPLOYEE_NO` VARCHAR(45) NULL,
  `TRAINING` VARCHAR(45) NULL,
  `INSTITUTE` VARCHAR(45) NULL,
  `DATE` VARCHAR(45) NULL,
  `DAYS` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`));
```


#### [Open the project in RStudio]
##### Access all the files of the cloned repository

Open the `HRStaffPortal.Rproj` file (RStudio Project will open) and configure the *Project Options* to set the **Anaconda / Miniconda Python** environment, plus the *Version Control* with **git**.  Now you can access all the source files.


#### [Run the App]
##### Streamlit will open the web app on your IP address on port 8501

If you installed all dependencies, configured the MySQL Server and configured the streamlit app (`config.toml` / `secrets.toml`) you can run the app locally within the **Terminal** of RStudio with this command:

```
streamlit run streamlit_app.py
```
