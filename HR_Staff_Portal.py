##### `streamlit_app.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions



#### Loading neded Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import mysql.connector
import sys
import webbrowser
from shillelagh.adapters.registry import registry
from shillelagh.adapters.file.csvfile import CSVFile
from shillelagh.backends.apsw.db import connect



#### Streamlit initial setup
st.set_page_config(
  page_title = "KCH HR Staff Portal",
  page_icon = "images/thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the KCH HR Staff Portal. Version 0.0.1"
        }
)



#### Query parameters
## Get param `EMPLOYE_NO`
eno = st.experimental_get_query_params()

## Get params for trainings / workshops
# [code]

  

#### All Functions used in HRStaffPortal
### Function: Password / User checking
def check_password():
  # Returns `True` if the user had a correct password."""
  def password_entered():
    # Checks whether a password entered by the user is correct."""
    if (st.session_state["username"] in st.secrets["passwords"] and st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]):
      st.session_state["password_correct"] = True
      del st.session_state["password"]  # don't store username + password
      del st.session_state["username"]
    else:
      st.session_state["password_correct"] = False
    
  ## Sidebar
  # Sidebar Header Image
  st.sidebar.image('images/MoH.png')

  if "password_correct" not in st.session_state:
    # First run, show inputs for username + password
    # Show Header Text
    st.sidebar.subheader('Please enter username and password')
    st.sidebar.text_input(label = "Username", on_change = password_entered, key = "username")
    st.sidebar.text_input(label = "Password", type = "password", on_change = password_entered, key = "password")
    return False
  
  elif not st.session_state["password_correct"]:
    # Password not correct, show input + error
    st.sidebar.text_input(label = "Username", on_change=password_entered, key = "username")
    st.sidebar.text_input(label = "Password", type = "password", on_change = password_entered, key = "password")
    if (st.session_state['logout']):
      st.sidebar.success('Logout successful!', icon = "✅")
    else:
      st.sidebar.error(body = "User not known or password incorrect!", icon = "🚨")
    return False
  
  else:
    # Password correct
    st.sidebar.success(body = 'You are logged in.', icon = "✅")
    st.sidebar.info(body = 'You can close this menu')
    st.sidebar.button(label = 'Logout', on_click = logout)
    return True
 
      
### Logout Button
def logout():
  ## Set Logout to get Logout-message
  st.session_state['logout'] = True
  ## Logout
  st.session_state["password_correct"] = False
  

### Function: SQL Connection
## Perform query
def run_query(query):
  return cursor.execute(query)


### Function: Picture-uploader
def pictureUploader(image, index):
  ## SQL statement
  sql_insert_blob_query = """ UPDATE 'test.csv' SET IMAGE = '%s' WHERE ID = '%s';"""
  ## Convert data into tuple format
  insert_blob_tuple = (image, index)
  result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
  conn.commit()
 
  
### Function: Convert digital data to binary format
def loadFile(filename):
  with open(filename, 'rb') as file:
    binaryData = file.read()
  return binaryData


### Function: Write binary data on Hard Disk
def writeFile(data, filename):
  with open(filename, mode = 'wb') as file:
    file.write(data)
    
    
    
#### Initialization of Session States
## First Run State
if ('success' not in st.session_state):
  st.session_state['run'] = True
  
## Database Transmition Success State
if ('success' not in st.session_state):
  st.session_state['success'] = False
  
## Selected Employee Session State
if ('index' not in st.session_state):
  st.session_state['index'] = 0
  
## Logout
if ('logout' not in st.session_state):
  st.session_state['logout'] = False
  
## Current Image data
if ('image' not in st.session_state):
  st.session_state['image'] = loadFile('images/No_Image.png')



#### Two Versions of the page -> Landing page vs. HRStaffPortal
### Logged in state (HRStattPortal)
if check_password():
    
    ## Header information
    with st.expander("Header", expanded = True):
      st.title('KCH HR Staff Portal')
      st.image('images/MoH.png')
      st.subheader('Kamuzu Central Hospital employee data.')
      st.write('All the employee data is stored in a local MySQL databank on a Raspberry Pi.')
      st.write('The HR Portal is running on Streamlit, an Open Source Python framework for visualisation.')


    ## Use local databank idcard with Table ImageBase (EasyBadge polluted)
    # open Databak Connection with Shillelagh
    conn = connect(":memory:", adapters = 'csvfile')
    cursor = conn.cursor()

    ## Checkbox for option to see databank data
    query = "SELECT ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED FROM 'test.csv';"
    rows = run_query(query)
    databank = pd.DataFrame(columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED'])
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]], columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED'])
      databank = databank.append(df)
 
    
    ## Print databank in dataframe table
    with st.expander("See all Databank entries", expanded = False):
      databank = databank.set_index('ID')
      st.dataframe(databank, use_container_width = True)

      
    ## Get employee data for searching for building `ID` / `EMPLOYEE` pairs and filling the employee Selectbox
    query = "SELECT ID, FORENAME, SURNAME, EMPLOYEE_NO, JOB_TITLE FROM 'test.csv';"
    rows = run_query(query)
    # Building `ID` / `EMPLOYEE` pair and
    # combine Forename and Surname for employee selectbox
    row = [0]
    names = ['New Employee']
    for row in rows:
      # Find pair and set sessoin state `index` to `ID` if not empty
      if eno:
        if (eno['eno'][0].strip()):
          if (eno['eno'][0] == row[3]):
            st.session_state.index = row[0]
      # Concenate Forename and Surname for Selectbox
      names.append(str(row[1] + ' ' + row[2] + ' ' + row[3] + ' ' + row[4]))


    ## Employee Selectbox (on change sets first start session state)
    def onChange():
      st.session_state.run = True
    index = st.selectbox(label = "Which Employee do you want to select?", options = range(len(names)), format_func = lambda x: names[x], on_change = onChange, index = int(st.session_state.index))
 
    
    ## Checkboxes for editing and adding Training data
    if (index != 0):
      checkbox_val = st.checkbox(label = 'Edit Mode', value = False)
      checkbox_training = st.checkbox(label = 'Add Training', value = checkbox_val, disabled = not checkbox_val)

    
    ## Form for showing Employee input fields 
    with st.form("Employee", clear_on_submit = True):
      st.title('Employee Master Data')
      
      # If new Employee just show empty form
      if (index == 0):
        # Set query parameter
        st.experimental_set_query_params(
        eno="xxxxxx")
        
        # empty image
        image = ''
        
        # Check for ID number count of Employee
        id = 0
        query = "SELECT ID from 'test.csv';"
        rows = run_query(query)
        row = [0]
        for row in rows:
          # Checking for ID
          id = int(row[0]) + 1
        # If first entry in database start with `ID` `1`
        if (id == 0):
          id = 1

        
        ## Input for new employee data
        id = st.text_input(label = 'ID', value = id, disabled = True)
        layout = st.text_input(label = 'Layout', value = 1)
        forename = st.text_input(label = 'Forename', placeholder = 'Forename?')
        surname = st.text_input(label = 'Surname', placeholder = 'Surname?')
        job = st.text_input(label = 'Job', placeholder = 'Job?')
        exp = st.text_input(label = 'Expirity Date', value = '2023-12-31 00:00:00')
        eno = st.text_input(label = 'Employee Number', placeholder = 'Employee Number?')
        capri = st.text_input(label = 'Cards Printed', value = 0)
        uploaded_file = st.file_uploader(label = "Upload a picture (256×360)", type = 'png')
        if uploaded_file is not None:
          image = uploaded_file.getvalue()
          
        else:
          image = loadFile("images/placeholder.png")
        
    
        ## Submit Button `Create New Employee`
        submitted = st.form_submit_button("Create New Employee")
        if submitted:
          ## Writing to databank if data was entered
          if (layout is not None and forename and surname and job and exp and eno and capri):
            query = "INSERT INTO 'test.csv'(ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(id, layout, forename, surname, job, exp, eno, capri)
            run_query(query)
            conn.commit()
            st.session_state.success = True
            
            # Upload picture to database
            #pictureUploader(image, id)
            
            # Set query parameter
            st.experimental_set_query_params(eno=eno)
            
            # Set `index` to refer to new `ID` position in database, so that reload opens new employee data
            st.session_state.index = int(id)
            
          else:
            st.session_state.success = False
          
          st.experimental_rerun()
 
      
      ## If data is already existent, show filled form  
      else:
        ## Get information of selected Employee
        query = "SELECT ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED, IMAGE FROM 'test.csv' WHERE ID = '%s';" %(str(index))
        for employee in run_query(query):
          print(employee)
          
        
        ## Input for updating employee data
        updataMaster = False
        id = st.text_input(label = 'ID', value = employee[0], disabled = True)
        layout = st.text_input(label = 'Layout', value = employee[1], disabled = True)
        forename = st.text_input(label = 'Forename', value = employee[2], disabled = not checkbox_val)
        if (employee[2] != forename):
          updateMaster = True
        surname = st.text_input(label = 'Surname', value = employee[3], disabled = not checkbox_val)
        if (employee[3] != surname):
          updateMaster = True
        job = st.text_input(label = 'Job', value = employee[4], disabled = not checkbox_val)
        if (employee[4] != job):
          updateMaster = True
        exp = st.text_input(label = 'Expirity Date', value = employee[5], disabled = not checkbox_val)
        if (employee[5] != exp):
          updateMaster = True
        eno = st.text_input(label = 'Employee Number', value = employee[6], disabled = not checkbox_val)
        if (employee[6] != eno):
          updateMaster = True
        capri = st.text_input(label = 'Cards Printed', value = employee[7], disabled = not checkbox_val)
        if (employee[7] != capri):
          updateMaster = True
          
        ## Check if image is empty and show a placeholder
        if (len(employee[8]) < 10):
          # Show placeholder
          st.image('images/portrait-placeholder.png')
          # Set Image Session State to `No Image` placeholder
          st.session_state['image'] = loadFile('images/No_Image.png')
          
        ## Show existing Image
        else:          
          st.image(employee[8])
          # Save Image for downloading to Image Session State
          st.session_state.image = employee[8]
        
        ## Image Uploader
        uploaded_file = st.file_uploader(label = "Upload a picture (256×360)", type = 'png', disabled = not checkbox_val)
        if uploaded_file is not None:
          updateMaster = True
          image = uploaded_file.getvalue()
          # Upload picture to database
          #pictureUploader(image, index)
        
        ## No image data  
        else:
          image = ''
        
        ## Set query parameter
        st.experimental_set_query_params(eno=eno)
          

        ## Get information of selected Employee regarding Training
        with st.expander("Training Data", expanded = checkbox_training):
          st.title('Employee Training Data')
          
          ## Check for last ID number in TrainingData (to add data after)
          idT = 0
          query = "SELECT ID from 'test2.csv';"
          rows = run_query(query)
          row = [0]
          for row in rows:
            idT = int(row[0]) + 1
          # If first entry in database start with `ID` `1` 
          if (idT == 0):
            idT = 1
          
          ## Get Training Data
          query = "SELECT tr.TRAINING, tr.INSTITUTE, tr.DATE, tr.DAYS, tr.ID FROM 'test.csv' AS ima LEFT JOIN 'test2.csv' AS tr ON ima.EMPLOYEE_NO = tr.EMPLOYEE_NO WHERE ima.ID = '%s';" %(str(index))
          row = [0]
          rows = run_query(query)
          #trainingData = pd.DataFrame(columns = ['TRAINING', 'INSTITUE', 'DATE', 'DAYS', 'ID'])

          trainingData = []
          trainingData = pd.DataFrame(columns = ['TRAINING', 'INSTITUE', 'DATE', 'DAYS', 'ID'])
          trainingData.set_index('TRAINING')
          for row in rows:
            df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4]]], columns = ['TRAINING', 'INSTITUE', 'DATE', 'DAYS', 'ID'])
            df.set_index('TRAINING')
            trainingData = trainingData.append(df)
            st.write('DF: ', df)
          trainingData..Index(range(1, 99, 1))

            
          # Debugging
          st.write(type(trainingData))
          st.write(trainingData)
          st.write(trainingData['TRAINING'][0])
          
          ## Variables for Text Input
          training = []
          institute = []
          date = []
          days = []
          
          ## Boolean for flow control
          insert = False # Will be set to `True` if a new entry is entered
          update = False # Will be set to `True` if existing data is altered
          
          ## Check if Training Data is already there for an Employee and show it
          #if (trainingData['TRAINING'][0] != None):
          #  update = False
          #  for i in range(len(trainingData)):
          #    # Show (Multiple) Input(s)
          #    x = st.text_input(label = 'Training #' + str(i + 1), value = trainingData[i][0], key = 'training' + str(i), disabled = not checkbox_val)
          #    if (trainingData[i][0] != x):
          #      update = True
          #    training.append(x)
          #    x = st.text_input(label = 'Institute', value = trainingData[i][1], key = 'institute' + str(i), disabled = not checkbox_val)
          #    if (trainingData[i][1] != x):
          #      update = True
          #    institute.append(x)
          #    x = st.text_input(label = 'Date', value = trainingData[i][2], key = 'date' + str(i), disabled = not checkbox_val)
          #    if (trainingData[i][2] != x):
          #      update = True
          #    date.append(x)
          #    x = st.text_input(label = 'Days', value = trainingData[i][3], key = 'days' + str(i), disabled = not checkbox_val)
          #    if (trainingData[i][3] != x):
          #      update = True
          #    days.append(x)
  
              
          ## Show new entry input fields if checkbox 'Add Training' is checked
          #if not checkbox_training:
          #  if (trainingData[0][0] == None):
          #    st.info(body = 'No Training Data available', icon = "ℹ️")
          #    
          #else:
            ## Calculating number of training
          #  if (trainingData[0][0] == None):
          #    counter = 'Training #1'
              
          #  else:
          #    counter = 'Training #' + str(len(trainingData) + 1)
              
            ## Inputs for new Training
          #  x = st.text_input(label = counter, placeholder = 'Training?', disabled = not checkbox_val)
          #  if x.strip():
          #    training.append(x)
          #    insert = True
          #  x = st.text_input(label = 'Institute', placeholder = 'Institute?', disabled = not checkbox_val)
          #  if x.strip():
          #    institute.append(x)
          #    insert = True
          #  x = st.text_input(label = 'Date', placeholder = 'Date?', disabled = not checkbox_val)
          #  if x.strip():
          #    date.append(x)
          #    insert = True
          #  x = st.text_input(label = 'Days', placeholder = 'Days?', disabled = not checkbox_val)
          #  if x.strip():
          #    days.append(x)
          #    insert = True
   
            
        ## Warning or Success messages after reloading
        if (st.session_state.run != True and st.session_state.success == True):
          st.success(body = 'Data submitted to Databank.', icon = "✅")
        else:
          if (st.session_state.run != True):
            st.warning(body = 'Not sumitted, as no new Data was entered!', icon = "⚠️")
        
        ## Submit Button for Changes
        submitted = st.form_submit_button("Save Changes")
        if submitted:
          # Set session state `index`
          st.session_state.index = index
          
          # Writing to databank idcard Table IMAGEBASE
          if (updateMaster == True):
            query = "UPDATE 'test.csv' SET LAYOUT = '%s', FORENAME = '%s', SURNAME = '%s', JOB_TITLE = '%s', EXPIRY_DATE = '%s', EMPLOYEE_NO = '%s', CARDS_PRINTED = '%s' WHERE ID = '%s';" %(layout, forename, surname, job, exp, eno, capri, str(index))
            run_query(query)
            conn.commit()
            
            st.session_state.success = True
            
          else:
            st.session_state.success = False
     
          
          ## Writing to databank idcard Table TRAININGDATA - new first Entry
          if (insert == True and update == False):
            st.write(training[0], institute[0], date[0], days[0])
            if (training[0].strip() and institute[0].strip() and date[0].strip() and days[0].strip()):
              query = "INSERT INTO 'test2.csv'(ID, EMPLOYEE_NO, TRAINING, INSTITUTE, DATE, DAYS) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" %(idT, eno, training[0], institute[0], date[0], days[0])
              run_query(query)
              conn.commit()
              st.session_state.success = True
              
            else:
              st.session_state.success = False
              
              
          ## Writing to databank idcard Table TRAININGDATA - new Entries (not first)
          if (insert == True and update == True):
            st.write(training[0], institute[0], date[0], days[0])
            st.write(len(trainingData))
            if (training[len(trainingData)].strip() and institute[len(trainingData)].strip() and date[len(trainingData)].strip() and days[len(trainingData)].strip()):
              query = "INSERT INTO 'test2.csv'(ID, EMPLOYEE_NO, TRAINING, INSTITUTE, DATE, DAYS) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" %(idT, eno, training[len(trainingData)], institute[len(trainingData)], date[len(trainingData)], days[len(trainingData)])
              run_query(query)
              conn.commit()
              st.session_state.success = True
            else:
              st.session_state.success = False
              
              
          ## Writing to databank idcard Table TRAININGDATA - Updates to all existing entries
          if (update == True):
            for i in range(len(trainingData)):
              st.write(training[i], institute[i], date[i], days[i])
              st.write(trainingData[i][4])
              query = "UPDATE 'test2.csv' SET TRAINING = '%s', INSTITUTE = '%s', DATE = '%s', DAYS = '%s' WHERE ID = '%s';" %(training[i], institute[i], date[i], days[i], trainingData[i][4])
              run_query(query)
              conn.commit()
            st.session_state.success = True

          
          ## Set Session State to 2nd run and reloading to get actual data
          st.session_state.run = False
          st.experimental_rerun()


          
    ### Out of the Form
    ## Image Download Button
    st.download_button('Download Image', data = st.session_state.image, mime="image/png")

 
          
          
#### Not Logged in state (Landing page)
else :
  ### Header of Landing Page
  ## Title and information
  st.title('Kamuzu Central Hospital (KCH)')
  st.header('Welcome to the HR Staff Portal')
  st.subheader('User Login')
  st.write('Please login (sidebar on the left) to access the KCH HR Staff Portal.')
  
  
  ## Sub-pages menu
  ## Menu to open sub-pages  
  #st.header('Menu')
  st.subheader('Pages (without login)')
  st.write('You can access these pages without user log in:')
  st.write("<a href='Statistics' target='_self'>Statistics</a>", unsafe_allow_html = True)
  st.write("<a href='Workshops' target='_self'>Workshops</a>", unsafe_allow_html = True)
  st.write("<a href='About' target='_self'>About</a>", unsafe_allow_html = True)
