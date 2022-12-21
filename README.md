# HRStaffPortal

## HR Staff Portal

This App handles **employee data** which is created through the process of printing *ID Cards* with the **EasyBadge ID Card Printer Software**. All data is stored in a MySQL Databank.

For development [RStudio](https://www.rstudio.com/products/rstudio/download/#download) is used. Install [git](https://git-scm.com/download/win) to use version control.

### Setup

#### Install and Configure all needed software

##### Installation of Python, Streamlit and dependencies plus some configuration

Install [Streamlit & Python](https://docs.streamlit.io/library/get-started/installation) to run the source code locally. A virtual Python-Environment like Anaconda is highly recommend.

After that you need to install some **Python libraries**:

    pip install mysql-connector-python-rf
    pip install mysql-connector-python==8.0.29
    pip install extra_streamlit_components
    pip install XlsxWriter
    pip install python-docx
    pip install openai
    pip install deepl

or do it at once using the `requirements.txt` file with:

    pip install -r requirements.txt

##### Getting the Source Code

Clone the **repository** of `HRStaffPortal` with following command:

    git clone https://github.com/DrBenjamin/HRStaffPortal.git

##### Configuration of Streamlit config files

First make a directory `.streamlit`. After that create the file `.streamlit/config.toml`. Here you define the **theming** and some **Streamlit-Server behaviour** flags:

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

Now create the file `.streamlit/secrets.toml` where you define the **user / password** combinations:

    [passwords]
    # Follow the rule: username = "password"
    xyz = "xyz"

#### MySQL Server Configuration

##### For proper usage a local MySQL Server is needed

In the `.streamlit/secrets.toml` you define the **user / password** combination for the HR Staff Portal MySQL Server `[mysql]`, and if using the Car Fleet Management System module also in the section `[mysql_car]`:

    [mysql]
    host = "127.0.0.1"
    port = 3306
    database = "idcard"
    user = "xyz"
    password = "xyz"

    [mysql_car]
    host = "127.0.0.1"
    port = 3306
    database = "carfleet"
    user = "xyz"
    password = "xyz"

    [mysql_benbox]
    host = "127.0.0.1"
    port = 3306
    database = "benbox
    user = "xyz"
    password = "xyz"

Connect to your **MySQL Database** and create the *user* you configured in `secrets.toml`. Create a **Schema / Database** with the name `idcard`.

To configure the HR Staff Portal tables run the following **SQL commands**:

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
      
      CREATE TABLE `idcard`.`TRAININGDATA` (
      `ID` INT NOT NULL,
      `EMPLOYEE_NO` VARCHAR(45) NULL,
      `TRAINING` VARCHAR(45) NULL,
      `INSTITUTE` VARCHAR(45) NULL,
      `DATE` DATE NULL,
      `DAYS` VARCHAR(45) NULL,
      PRIMARY KEY (`ID`));

or use the database dump with sample data `files/idcard_dump.sql` and import them to a **MySQL** / **MariaDB** database. To use the **Car Fleet Management** module you also need to import the file `files/carfleet_dump.sql`. For the **Chatbot** please import the `files/benbox_dump.sql` file.

#### Create new project in RStudio

##### Working with RStudio on the project

In RStudio choose **File** - **New Project** and choose **Existing Directory**. This will create a new Project. Configure the *Project Options* to set the **Anaconda / Miniconda Python** environment. Also add the *Version Control* with **git**. Now you can open the source code as a RStudio project everytime you are working on the source files and easily use the **git** functionality within the RStudio IDE.

### Software update & use

#### Use of the web application

##### Clone a specific version of HR Staff Portal

To clone a specific version of HR Staff Portal use this command:

    git clone https://github.com/DrBenjamin/HRStaffPortal.git -b v0.1.1

##### Update HR Staff Portal

To update the source files to the newest version use the build-in **pull function** of git (git menu on the right upper corner, choose the green arrow which shows down). If you are using the app on a computer without a RStudio installion, just use this git command:

    git pull

##### Execute Streamlit

If you've installed all dependencies, configured the MySQL Server and edited the Streamlit app config files (`config.toml` / `secrets.toml`) to your setup, you can run the app locally within the **Terminal** of RStudio or any other terminal with access to Python and the Python libraries (e.g. a virtual environment) with this command:

    streamlit run 🏥_HR_Staff_Portal.py

This will open the web app on your IP address on **port 8501**.

#### Update Streamlit & Dependencies

##### Update of Streamlit

To install the latest version of the **Streamlit web app framework**, run the following command:

    pip install --upgrade streamlit

##### Update dependencies

To update a specifig dependency, for instance **extra_streamlit_components**, use this command:

    pip install --upgrade extra_streamlit_components
