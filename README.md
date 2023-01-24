# HRStaffPortal

[![GitHub][github_badge]][github_link] [![Open in Streamlit][share_badge]][share_link]

## HR Staff Portal

This App handles **employee data** which is created through the process of printing *ID Cards* with the **EasyBadge ID Card Printer Software**. All data is stored in a MySQL databank.

For development [RStudio](https://www.rstudio.com/products/rstudio/download/#download) is used. Install [git](https://git-scm.com/download/win) to use version control.

### Setup

#### Install and configure all needed software

##### Installation of Python, Streamlit and dependencies plus some configuration

Install [Streamlit & Python](https://docs.streamlit.io/library/get-started/installation) to run the source code locally. A virtual Python environment like Anaconda / Miniconda are highly recommend.

After that you need to install some **Python libraries**:

```cmd
pip install mysql-connector-python-rf
pip install mysql-connector-python==8.0.29
pip install extra_streamlit_components
pip install streamlit-scrollable-textbox
pip install streamlit_image_select
pip install XlsxWriter
pip install python-docx
pip install openai
pip install deepl
pip install geocoder
pip install geopy
pip install qrcode
pip install streamlit_qrcode_scanner
pip install loguru
```

or do it at once using the `requirements.txt` file with:

```cmd
pip install -r requirements.txt
```

##### Getting the Source Code

Clone the **repository** of `HRStaffPortal` with following command:

```cmd
git clone https://github.com/DrBenjamin/HRStaffPortal.git
```

##### Configuration of Streamlit config files

First make a directory `.streamlit`. After that create the file `.streamlit/config.toml`. Here you define the **theming** and some **Streamlit server behaviour** flags:

```python
[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false

[server]
headless = true
```

Now create the file `.streamlit/secrets.toml` where you define some customizations and the **user / password** combinations:

```python
### Customization
[custom]
facility = "XXXXXXXX"
facility_abbreviation = "XXX"
header_image = "images/XYZ.png"
address_line1 = "XXXXXXXXXX,"
address_line2 = "XXXXX, XXXXX"
contact_tel1 = "+xxx x xxx xxx"
contact_tel2 = "+xxx x xxx xxx"
contact_tel3 = "+xxx x xxx xxx"
contact_mail1 = "xyz1@mail.com"
contact_mail1_desc = "XXX"
contact_mail2 = "xyz2@mail.com"
contact_mail2_desc = "XXX"
contact_admin = "xyz@mail.com"

### User management
[passwords]
# Follow the rule: username = "password"
user = "xxxxxxxx"
```

#### MySQL server configuration

##### For proper usage a local MySQL server is needed

In the `.streamlit/secrets.toml` you define the MySQL server settings for the different modules (HR Staff Portal / Car Fleet Management System / Handbook & Chat-Bot):

```python
### MySQL configuration for HR Staff Portal
[mysql]
host = "127.0.0.1"
port = 3306
database = "idcard"
user = "xyz"
password = "xyz"

### MySQL configuration for Car Fleet Management
[mysql_car]
host = "127.0.0.1"
port = 3306
database = "carfleet"
user = "xyz"
password = "xyz"

### MySQL configuration for handbook and ChatBot
[mysql_benbox]
host = "127.0.0.1"
port = 3306
database = "benbox"
user = "xyz"
password = "xyz"

### Mail configuration
[mail]
user = "xyz@mail.com"
password = "xxxxxxxx
smtp_server = "smtp.server.com"
smtp_server_port = 587

### OpenAI API key
[openai]
key = "xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              
### Deepl API key
[deepl]
key = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:xx"
```

Connect to your **MySQL database** and create the *user* you configured in `secrets.toml`. Create a **schema / database** with the name `idcard`.

To configure the HR Staff Portal tables run the following **SQL commands**:

```sql
CREATE TABLE `idcard`.`IMAGEBASE` (
      `ID` INT NOT NULL,
      `LAYOUT` INT NOT NULL,
      `FORENAME` VARCHAR(45) NULL,
      `SURNAME` VARCHAR(45) NULL,
      `JOB_TITLE` VARCHAR(45) NULL,
      `EXPIRY_DATE` DATE NULL,
      `EMPLOYEE_NO` VARCHAR(45) NULL,
      `CARDS_PRINTED` INT NOT NULL,
      `IMAGE` BLOB NULL,
      PRIMARY KEY (`ID`));
      
CREATE TABLE `idcard`.`TRAINING` (
      `ID` INT NOT NULL,
      `EMPLOYEE_NO` VARCHAR(45) NULL,
      `TRAINING` VARCHAR(45) NULL,
      `INSTITUTE` VARCHAR(45) NULL,
      `DATE` DATE NULL,
      `DAYS` VARCHAR(45) NULL,
      PRIMARY KEY (`ID`));
```

or use the database dump with sample data `files/idcard_dump.sql` and import them to a **MySQL** / **MariaDB** database. To use the **Car Fleet Management** module you also need to import the file `files/carfleet_dump.sql`. For the **Chatbot** please import the `files/benbox_dump.sql` file.

#### Create new project in RStudio

##### Working with RStudio on the project

In RStudio choose **File** - **New Project** and choose **Existing Directory**. This will create a new Project. Configure the *Project Options* to set the **Anaconda / Miniconda Python** environment. Also add the *Version Control* with **git**. Now you can open the source code as a RStudio project anytime you are working on the source files and easily use the **git** functionality within the RStudio IDE.

### Software update & use

#### Use of the web application

##### Clone a specific version of HR Staff Portal

To clone a specific version of HR Staff Portal use this command:

```cmd
git clone https://github.com/DrBenjamin/HRStaffPortal.git -b v0.1.1
```

##### Update HR Staff Portal

To update the source files to the newest version use the build-in **pull function** of git (git menu on the right upper corner, choose the green arrow which shows down). If you are using the app on a computer without a RStudio installation, just use this git command:

```cmd
git pull
```

##### Execute Streamlit

If you've installed all dependencies, configured the MySQL server and edited the Streamlit app config files (`config.toml` / `secrets.toml`) to your setup, you can run the app locally within the **Terminal** of RStudio or any other terminal with access to Python and the Python libraries (e.g. a virtual environment) with this command:

```cmd
streamlit run 🏥_HR_Staff_Portal.py
```

This will open the web app on your IP address on **port 8501**.

#### Update Streamlit & dependencies

##### Update of Streamlit

To update to the latest version of the **Streamlit web app framework**, run the following command:

```cmd
pip install --upgrade streamlit
```

##### Update dependencies

To update a specific dependency, for instance **extra_streamlit_components**, use this command:

```cmd
pip install --upgrade extra_streamlit_components
```

[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
[github_link]: https://github.com/DrBenjamin/HRStaffPortal

[share_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[share_link]: https://hr-staff-p0rtal.streamlit.app/
