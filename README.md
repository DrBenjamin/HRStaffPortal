# HRStaffPortal

[![GitHub][github_badge]][github_link]

## HR Staff Portal

This App handles *employee data* which is created through the process of printing *ID Cards* with the **EasyBadge ID Card Printer Software**. All data is stored in a MySQL databank.

For development choose your favorite **Text-Editor** or use an IDE as [RStudio](https://www.rstudio.com/products/rstudio/download/#download), [PyCharm](https://www.jetbrains.com/pycharm/) or **[VS Code](https://code.visualstudio.com)**. Install **[git](https://git-scm.com/download/win)** to use version control.

### Setup

Description of the installation and configuration to use the **HR Staff Portal**.

#### Installation and configuration of all needed Software

All Software which is used to run **HR Staff Portal** is **Open Source**. Please be aware of different licenses with varying policies.

##### Installation of Python and Streamlit

Install **[Streamlit & Python](https://docs.streamlit.io/library/get-started/installation)** to run the source code locally. A virtual Python environment like **Anaconda** / **Miniconda** is highly recommend.

#### Getting the HR Staff Portal source code and install dependencies

Clone the *repository* of **HRStaffPortal** with following command:

```cmd
git clone https://github.com/DrBenjamin/HRStaffPortal.git
```

After that you need to install some *Python libraries*. To do so use the `requirements.txt` file with:

```cmd
cd HRStaffPortal
python -m pip install -r requirements.txt
```

##### Configuration of Streamlit config files

First make a directory `.streamlit`. After that create the file `.streamlit/config.toml`. Here you define the *theming* and some *Streamlit server behaviour* flags:

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

##### Activating Secure Socket Layer (ssl)

If you want a secure connection (https), you need to generate the **[OpenSSL](https://slproweb.com/products/Win32OpenSSL.html)** certificate and the public key:

```cmd
openssl genrsa 2048 > host.key
chmod 400 host.key
openssl req -new -x509 -nodes -sha256 -days 365 -key host.key -out host.cert
```

Streamlit v1.20.0 brings secure connection, you just need to add these two lines to `.streamlit/config.toml`:

```python
# Server certificate file for connecting via HTTPS. Must be set at the same time as "server.sslKeyFile"
sslCertFile = "<path-to-file>/host.cert"

# Cryptographic key file for connecting via HTTPS. Must be set at the same time as "server.sslCertFile"
sslKeyFile = "<path-to-file>/host.key"
```

Now create the file `.streamlit/secrets.toml` where you define some customisations and the *user / password* combinations:

```python
### Customization
[custom]
images_url = "https://example.url/images/"
images_zip = "images.zip"
images_path = "images/"
facility = "XXXXXXXX"
facility_abbreviation = "XXX"
facility_image = "images/XXX.png"
facility_image_thumbnail = "images/XXX.png"
sidebar_image = "images/XXX.png"
placeholder = "images/placeholder.png"
placeholder_docu = "images/placeholder_documentation.png"
chat_bot = "images/Ben.png"
menu_items_help = "https://www.example.url/help"
menu_items_bug = "https://github.com/DrBenjamin/HRStaffPortal/issues"
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

## Administrators
[admins]
admin = "xxxxxxxx"
```

#### MySQL Server

**MySQL Server** is needed to run **HR Staff Portal**. Please install **MySQL Community Server** on your system (**[Windows](https://dev.mysql.com/downloads/mysql/)**, **[Ubuntu Linux](https://dev.mysql.com/doc/refman/8.0/en/binary-installation.html)**) or on Raspberry Pi use **MariaDB**:

```cmd
sudo apt-get install mariadb-server mariadb-client
```

Use **[MySQL Workbench](https://dev.mysql.com/downloads/workbench/)** to configure the databases and user rights.

##### MySQL server configuration in Streamlit

In the `.streamlit/secrets.toml` you define the MySQL server settings for the different modules (**HR Staff Portal** / **Car Fleet Management System** / **Handbook & Chat-Bot**):

```python
### MySQL configuration for HR Staff Portal
[mysql]
host = "127.0.0.1"
port = 3306
database = "idcard"
user = "xyz"
password = "xyz"

### MySQL configuration for handbook and ChatBot
[mysql_benbox]
host = "127.0.0.1"
port = 3306
database = "benbox"
user = "xyz"
password = "xyz"
```

Connect to your *MySQL database* and create the *user* you configured in `secrets.toml`. Create a *schema / database* with the name `idcard`. Give the user the rights to alter the *database tables*.

To configure the **HR Staff Portal** *database tables* run the following *SQL script*:

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

or use the database dump with sample data `files/idcard_dump.sql` and import them to a **MySQL** / **MariaDB** database using **MySQL Workbench**. To use the **Car Fleet Management System** module you also need to import the file `files/carfleet_dump.sql`. To use the **Chatbot** please import the `files/benbox_dump.sql` file.

#### Streamlit configuration for different services

To run services (e.g. mail sending) further configuration in `.streamlit/secrets.toml` is needed:

```python
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

#### Install and configure an IDE (Integrated Development Environment)

Developement of the **HR Staff Portal** mostly was done in **[VS Studio Code](https://code.visualstudio.com/download)**, but you are free to choose whatever *IDE* that supports the *Python* programming language and has a *Terminal* included (which makes lifee way easier).

##### Working with VS Studio Code on the project

In VS Studio Code choose *File* - *New Window* and choose *Existing Directory*. This will create a new Project. Add the *git* in the *Version Control* tab under the *Project Options* in the right upper corner of RStudio. Now you can open the source code as a RStudio project anytime you are working on the source files and easily use the *git* functionality within the RStudio IDE.

Alternatively you can directly download the sources of the project choosing *File* - *New Project* and choose *Clone Git Repository*. Insert the repository URL: [https://github.com/DrBenjamin/HRStaffPortal](https://github.com/DrBenjamin/HRStaffPortal)

You need to configure the Python environment (bottom), choose your **[Anaconda](https://anaconda.org/conda-forge/download)** or **[Miniconda Python](https://docs.conda.io/en/latest/miniconda.html)** installation.

### Use of the HR Staff Portal and updates

The **HR Staff Portal** software runs under the **[GNU General Public License v3.0](https://github.com/DrBenjamin/HRStaffPortal/blob/main/LICENSE)** which allows the commercial use, modification for your purposes, distribution, patent use as well as the private use.

#### Use of the web application

The **HR Staff Portal** is running as an *Web Service* through the *Python Streamlit framework*. It will use the *port* `8501` if you are not changing it in `.streamlit/config.toml` in the `browser` section:

```
[browser]
# Server port binding
serverPort = 8501
```

##### Clone a specific version of HR Staff Portal

To clone a specific version of HR Staff Portal use this command:

```cmd
git clone https://github.com/DrBenjamin/HRStaffPortal.git -b v0.1.1
```

##### Update HR Staff Portal

To update the source files to the newest version use the build-in *pull function* of git in RStudio (menu on the right upper side, choose git and press the green arrow which shows down). If you are using the app on a computer without a RStudio installation, just use this git command:

```cmd
git pull
```

##### Execute the Streamlit Web App

If you've installed all dependencies, configured the MySQL server and edited the Streamlit app config files (`config.toml` / `secrets.toml`) to your setup, you can run the app locally within the *Terminal* of your IDE or any other terminal with access to Python and the Python libraries (e.g. a virtual environment) with this command:

```cmd
python -m streamlit run 🏥_HR_Staff_Portal.py
```

This will open the **Web App** on the servers IP address(es) and the designated port. Open it in the browser with `http://xxx.xxx.xxx.xxx:8501` or `https://xxx.xxx.xxx.xxx:8501` if you are using SLL connections.

#### Update Streamlit & dependencies

The Software and its dependencies will be updated regularly, so make sure to always run the newest versions to avoid security risks.

##### Update of Streamlit

To update to the latest version of the **Streamlit web app framework**, run the following command:

```cmd
python -m pip install --upgrade streamlit
```

##### Update dependencies

To update all dependencies, use this command:

```cmd
python -m pip install --upgrade -r requirements.txt
```

### Demo

[![Open in Streamlit Cloud][share_badge]][share_link]

### Screencast

https://user-images.githubusercontent.com/40030246/215703347-6683efe5-f3b8-479f-8f5c-9346a8d61c3a.mp4

[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
[github_link]: https://github.com/DrBenjamin/HRStaffPortal

[share_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[share_link]: https://hr-staff-p0rtal.streamlit.app/
