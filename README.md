# HRStaffPortal

[![GitHub][github_badge]][github_link]

## HR Staff Portal

This App handles *employee data* which is created through the process of printing *ID Cards* with the **EasyBadge ID Card Printer Software**. All data is stored in a MySQL databank.

For development **[RStudio](https://www.rstudio.com/products/rstudio/download/#download)** is used. Install **[git](https://git-scm.com/download/win)** to use version control.

### Setup

#### Install and configure all needed software

##### Installation of Python, Streamlit and dependencies

Install **[Streamlit & Python](https://docs.streamlit.io/library/get-started/installation)** to run the source code locally. A virtual Python environment like Anaconda / Miniconda are highly recommend.

After that you need to install some *Python libraries*:

```cmd
pip install mysql-connector-python-rf
pip install mysql-connector-python==8.0.29
pip install extra_streamlit_components
pip install streamlit-scrollable-textbox
pip install streamlit_image_select
pip install opencv-python-headless
pip install XlsxWriter
pip install python-docx
pip install openai
pip install deepl
pip install geocoder
pip install geopy
pip install qrcode
pip install loguru
```

or do it at once using the `requirements.txt` file with:

```cmd
pip install -r requirements.txt
```

Install the **Changelog converter** (Markdown to html) with **[Node.js](https://nodejs.org/en/download/)**:

```cmd
npm install --save-dev changelog-to-html
```

##### Activating Secure Socket Layer (ssl)

If you want a secure connection (https), you need to generate the **[OpenSSL](https://slproweb.com/products/Win32OpenSSL.html)** certificate and the public key:

```cmd
openssl genrsa 2048 > host.key
chmod 400 host.key
openssl req -new -x509 -nodes -sha256 -days 365 -key host.key -out host.cert
```

Also you need to add the `ssl_options` to server.py in the *Python* / *Virtual environment* folder `Lib/site-packages/streamlit/web/server/server.py`. Connections will now be only possible using `https://` + URL. Be aware, after each update of **Streamlit** to redo these changes.

```Python
http_server = HTTPServer(
        app, max_buffer_size=config.get_option("server.maxUploadSize") * 1024 * 1024,
        ssl_options={
            "certfile": "/Path-to-ssl-files/host.cert",
            "keyfile": "/Path-to-ssl-files/host.key",
        }
```

#### Getting the HR Staff Portal source code

Clone the *repository* of **HRStaffPortal** with following command:

```cmd
git clone https://github.com/DrBenjamin/HRStaffPortal.git
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

Now create the file `.streamlit/secrets.toml` where you define some customisations and the *user / password* combinations:

```python
### Customization
[custom]
facility = "XXXXXXXX"
facility_abbreviation = "XXX"
facility_image = "images/XXX.png"
facility_image_thumbnail = "images/XXX.png"
carfleet_image = "images/XXX.png"
carfleet_image_thumbnail = "images/XXX.png"
menu_items_help = "http://www.example.url/help"
menu_items_bug = "https://github.com/DrBenjamin/HRStaffPortal/issues"
menu_items_about = "This is the HR Staff Portal (Version 0.2.0)"
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

#### MySQL server configuration

##### For proper usage a local MySQL server is needed

In the `.streamlit/secrets.toml` you define the MySQL server settings for the different modules (**HR Staff Portal** / **Car Fleet Management System** / **Handbook & Chat-Bot**):

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

Connect to your *MySQL database* and create the *user* you configured in `secrets.toml`. Create a *schema / database* with the name `idcard`.

To configure the **HR Staff Portal** *database tables* run the following *SQL commands*:

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

or use the database dump with sample data `files/idcard_dump.sql` and import them to a *MySQL* / *MariaDB* database. To use the **Car Fleet Management** module you also need to import the file `files/carfleet_dump.sql`. To use the **Chatbot** please import the `files/benbox_dump.sql` file.

#### Create new project in RStudio

Developement of the **HR Staff Portal** was done in RStudio, but you are free to choose whatever *IDE* which supports *Python* programming language and has a *Terminal* included.

##### Working with RStudio on the project

In RStudio choose *File* - *New Project* and choose *Existing Directory*. This will create a new Project. Add the *git* in the *Version Control* tab under the *Project Options* in the right upper corner of RStudio. Now you can open the source code as a RStudio project anytime you are working on the source files and easily use the *git* functionality within the RStudio IDE.

Alternatively you can directly download the sources of the project choosing *File* - *New Project* and *Version Control*. Select *Git* and enter the repository [URL](https://github.com/DrBenjamin/HRStaffPortal).

Now you need to configure the Python environment under *Project Options* to set the **[Anaconda](https://anaconda.org/conda-forge/download)** / **[Miniconda Python](https://docs.conda.io/en/latest/miniconda.html)** which should be used.

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

##### Update Changelog html files

To convert `CHANGELOG.md` to html files use this command:

```cmd
npm exec changelog-to-html CHANGELOG.md
```

Copy these files to a local httpd service folder like **[Apache2](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-20-04)** (e.g. `/var/www/html`) to show the *Github Changelog* in the app.

Add these two lines in `etc/apache2/conf-enabled/security.conf` to allow *embedding* of the *Changelog page*:

```conf
Header set Access-Control-Allow-Origin "*"
Header set X-Frame-Options "ALLOW-FROM *"
```

For enabling *ssl* in Apache (if you are using Streamlit in ssl mode) do enter these commands:

```cmd
sudo a2enmod ssl
sudo a2enmod headers
a2ensite default-ssl
```

You also need to change the virtual configuration of your local website (e.g. `/etc/apache2/sites-available/default-ssl.conf`) to your needs and add the created OpenSSL certificate and key.

```conf
SSLCertificateFile /Path-to-ssl-files/host.cert
SSLCertificateKeyFile /Path-to-ssl-files/host.key
```

##### Execute Streamlit

If you've installed all dependencies, configured the MySQL server and edited the Streamlit app config files (`config.toml` / `secrets.toml`) to your setup, you can run the app locally within the *Terminal* of RStudio or any other terminal with access to Python and the Python libraries (e.g. a virtual environment) with this command:

```cmd
streamlit run 🏥_HR_Staff_Portal.py
```

This will open the **Web App** on the servers IP address(es) and the designated port. Open it in the browser with `http://xxx.xxx.xxx.xxx:8501` or `https://xxx.xxx.xxx.xxx:8501` if you are using SLL connections.

#### Update Streamlit & dependencies

The Software and its dependencies will be updated regularly, so make sure to always run the newest versions to avoid security risks.

##### Update of Streamlit

To update to the latest version of the **Streamlit web app framework**, run the following command:

```cmd
pip install --upgrade streamlit
```

##### Update dependencies

To update all dependencies, use this command:

```cmd
pip install --upgrade -r requirements.txt
```

#### Demo

[![Open in Streamlit][share_badge]][share_link]

#### Screencast

https://user-images.githubusercontent.com/40030246/215703347-6683efe5-f3b8-479f-8f5c-9346a8d61c3a.mp4

[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
[github_link]: https://github.com/DrBenjamin/HRStaffPortal

[share_badge]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[share_link]: https://hr-staff-p0rtal.streamlit.app/
