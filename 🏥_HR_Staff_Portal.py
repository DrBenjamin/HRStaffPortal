##### `🏥_HR_Staff_Portal.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions




#### Loading neded Python libraries
import streamlit as st
import extra_streamlit_components as stx
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import mysql.connector
import sys
import webbrowser
import os
import platform
import io
import xlsxwriter




#### Streamlit initial setup
st.set_page_config(
  page_title = "KCH HR Staff Portal",
  page_icon = "images/thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the KCH HR Staff Portal Version 0.2.0"
        }
)




#### OS Check
plt = platform.system()
if plt == "Windows":
  print("Your system is Windows")
elif plt == "Linux":
  print("Your system is Linux")
elif plt == "Darwin":
  print("Your system is MacOS")




#### Query parameters
## Get param `EMPLOYE_NO`
eno = st.experimental_get_query_params()


## Get params for trainings / workshops
# [code]




#### Initialization of session states
## First Run State
if ('success' not in st.session_state):
  st.session_state['run'] = True
  
## Database transmission success state1
if ('success1' not in st.session_state):
  st.session_state['success1'] = False
if ('success2' not in st.session_state):
  st.session_state['success2'] = False
if ('success3' not in st.session_state):
  st.session_state['success3'] = False
  
## Selected Employee session state
if ('index' not in st.session_state):
  st.session_state['index'] = 0
  
## Logout
if ('logout' not in st.session_state):
  st.session_state['logout'] = False
  



#### All Functions used in HRStaffPortal
### Function: check_password = Password / User checking
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
 
 
      
### Funtion: logout = Logout Button
def logout():
  ## Set Logout to get Logout-message
  st.session_state['logout'] = True
  ## Logout
  st.session_state["password_correct"] = False

  

### Function: database_connect = Threadend SQL Connection
def database_connect():
  t = Thread(target = init_connection())
  t.daemon = True
  t.start()
  t.join(5)
  if t.is_alive():
    print("An exception occurred in function `init_connection` 2")
    st.error(body = 'Databank connection timeout 2!', icon = "🚨")



### Function: run_query = Initial SQL Connection
def init_connection():
  ## Initialize connection
  try:
    return mysql.connector.connect(**st.secrets["mysql"])
  except:
    print("An exception occurred in function `init_connection`")
    st.error(body = 'Databank connection timeout!', icon = "🚨")
    st.stop()



### Function: run_query = SQL query
def run_query(query):
  with conn.cursor() as cur:
    try:
      ## Perform query
      cur.execute(query)
      return cur.fetchall()
    except:
      print("An exception occurred in function `run_query`")



### Function: pictureUploader = uploads employee images
def pictureUploader(image, index):
  ## Initialize connection
  connection = mysql.connector.connect(**st.secrets["mysql"])
  cursor = connection.cursor()
  ## SQL statement
  sql_insert_blob_query = """ UPDATE IMAGEBASE SET IMAGE = %s WHERE ID = %s;"""
  ## Convert data into tuple format
  insert_blob_tuple = (image, index)
  result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
  connection.commit()
  

  
### Function: lastID = checks for last ID number in Table (to add data after)
def lastID(url):
  query = "SELECT MAX(ID) FROM %s;" %(url)
  rows = run_query(query)
  id = 0
  for row in rows:
    id = int(row[0]) + 1

  # If first entry in database start with `ID` `1` 
  if (id == 0):
    id = 1
  return id
 

  
### Function: loadFile = converts digital data to binary format
def loadFile(filename):
  with open(filename, 'rb') as file:
    binaryData = file.read()
  return binaryData
## Current Image data
if ('image' not in st.session_state):
  st.session_state['image'] = loadFile('images/No_Image.png')



### Function: writeFile = writes binary data on Hard Disk
def writeFile(data, filename):
  with open(filename, mode = 'wb') as file:
    file.write(data)

    
    
### Function: onChange = If Selectbox is used
def onChange():
  st.session_state['run'] = True



### Function: export_excel = Pandas Dataframe to Excel Makro File (xlsm)
def export_excel(sheet, column, columns, length, data, 
                sheet2 = 'N0thing', column2 = 'A', columns2 = '', length2 = '', data2 = '',
                sheet3 = 'N0thing', column3 = 'A', columns3 = '', length3 = '', data3 = '',
                sheet4 = 'N0thing', column4 = 'A', columns4 = '', length4 = '', data4 = '',
                sheet5 = 'N0thing', column5 = 'A', columns5 = '', length5 = '', data5 = '',
                sheet6 = 'N0thing', column6 = 'A', columns6 = '', length6 = '', data6 = '',
                sheet7 = 'N0thing', column7 = 'A', columns7 = '', length7 = '', data7 = '',
                image = 'NoImage', image_pos = 'D1', excel_file_name = 'Export.xlsm'):

  
  ## Store function arguments in array
  # Create empty array
  func_arr =[]
  # Add function arguments to array
  func_arr.append([sheet, column, columns, length, data])
  func_arr.append([sheet2, column2, columns2, length2, data2])
  func_arr.append([sheet3, column3, columns3, length3, data3])
  func_arr.append([sheet4, column4, columns4, length4, data4])
  func_arr.append([sheet5, column5, columns5, length5, data5])
  func_arr.append([sheet6, column6, columns6, length6, data6])
  func_arr.append([sheet7, column7, columns7, length7, data7])

  
  ## Create a Pandas Excel writer using XlsxWriter as the engine
  buffer = io.BytesIO()
  with pd.ExcelWriter(buffer, engine = 'xlsxwriter') as writer:
    for i in range(7):
      if (func_arr[i][0] != 'N0thing'):
        # Add dataframe data to worksheet
        func_arr[i][4].to_excel(writer, sheet_name = func_arr[i][0], index = False)

        # Add a table to worksheet
        worksheet = writer.sheets[func_arr[i][0]]
        span = "A1:%s%s" %(func_arr[i][1], func_arr[i][3])
        worksheet.add_table(span, {'columns': func_arr[i][2]})
        range_table = "A:" + func_arr[i][1]
        worksheet.set_column(range_table, 30)
        
        # Add Image to worksheet
        # Add Image to worksheet
        if (image != 'NoImage'):
          # Write Image to a png file
          f = open('Image.png', 'wb')
          f.write(image)
          f.close()
          worksheet.insert_image(image_pos, 'Image.png')
      
      
    ## Add Excel VBA code
    workbook = writer.book
    workbook.add_vba_project('vbaProject.bin')
    
    
    ## Saving changes
    workbook.close()
    writer.save()
    if os.path.exists("Image.png"):
      os.remove("Image.png")
    
    
    ## Download Button
    st.download_button(label = 'Download Excel document', data = buffer, file_name = excel_file_name, mime = "application/vnd.ms-excel.sheet.macroEnabled.12")




#### Two versions of the page -> Landing page vs. HRStaffPortal
### Logged in state (HRStattPortal)
if check_password():
  ## Header information
  with st.expander("Header", expanded = True):
    st.title('HR Staff Portal')
    st.image('images/MoH.png')
    st.subheader('Kamuzu Central Hospital employee data')
    st.write('All employee data is stored in a local MySQL databank on a Windows Server hosted at KCH.')
    st.write('The HR Staff Portal is developed with Python and installed on Windows Subsystem for Linux.')
    st.write('It uses Streamlit framework for visualisation which is turns Python scipts into data web apps.')


  ## Use local databank idcard with Table ImageBase (EasyBadge polluted)
  # Open databank connection
  conn = init_connection()


  ## Getting databank data
  # Getting Employee data
  query = "SELECT ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED FROM `idcard`.`IMAGEBASE`;"
  rows = run_query(query)
  databank = pd.DataFrame(columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]], columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED'])
    databank = pd.concat([databank, df])
  databank = databank.set_index('ID')
  
  # Getting Training data
  query = "SELECT ID, EMPLOYEE_NO, TRAINING, INSTITUTE, DATE, DAYS FROM `idcard`.`TRAININGDATA`;"
  rows = run_query(query)
  databank_training = pd.DataFrame(columns = ['ID', 'EMPLOYEE_NO', 'TRAINING', 'INSTITUTE', 'DATE', 'DAYS'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5]]], columns = ['ID', 'EMPLOYEE_NO', 'TRAINING', 'INSTITUTE', 'DATE', 'DAYS'])
    databank_training = pd.concat([databank_training, df])
  databank_training = databank_training.set_index('ID')
 
      
  ## Get employee data for searching for building `ID` / `EMPLOYEE` pairs and filling the employee Selectbox
  query = "SELECT ID, FORENAME, SURNAME, EMPLOYEE_NO, JOB_TITLE FROM `idcard`.`IMAGEBASE`;"
  rows = run_query(query)
  # Building `ID` / `EMPLOYEE` pair and
  # combine Forename and Surname for employee selectbox
  row = [0]
  names = ['New Employee']
  for row in rows:
    # Find pair and set session state `index` to `ID` if not empty
    if eno:
      if (eno['eno'][0].strip()):
        if (eno['eno'][0] == row[3]):
          st.session_state['index'] = row[0]
    # Concenate Forename and Surname for Selectbox
    names.append(str(row[1] + ' ' + row[2] + ' ' + row[3] + ' ' + row[4]))


  ## Employee Selectbox (on change sets first start session state)
  index = st.selectbox(label = "Which Employee do you want to select?", options = range(len(names)), format_func = lambda x: names[x], on_change = onChange, index = st.session_state['index'])
 
    
  ## Checkboxes for editing and adding Training data
  if (index != 0):
    checkbox_val = st.checkbox(label = 'Edit Mode', value = False)
    checkbox_training = st.checkbox(label = 'Add Training', value = checkbox_val, disabled = not checkbox_val)

  
  ## Custom Tabs with IDs
  chosen_id = stx.tab_bar(data = [
    stx.TabBarItemData(id = 1, title = "Master data", description = "Employee data"),
    stx.TabBarItemData(id = 2, title = "Training data", description = "Employee trainings"),
    stx.TabBarItemData(id = 3, title = "More data", description = "More employee data"),], default = 1)


  ## Form for showing Employee input fields 
  with st.form("Employee", clear_on_submit = True):
    ## tab `Master data`
    if (f"{chosen_id}" == '1'):
      st.title('Employee Master data')
      st.subheader('Enter or view exmployee master data')
      
      
      ## If new Employee just show empty form
      if (index == 0):
        ## Set query parameter
        st.experimental_set_query_params(eno = "xxxxxx")
        
        
        ## Input for new employee data
        # Check for ID number count of Employee
        id = lastID(url = "idcard.IMAGEBASE")
        id = st.text_input(label = 'ID', value = id, disabled = True)
        layout = st.text_input(label = 'Layout', value = 1)
        forename = st.text_input(label = 'Forename', placeholder = 'Forename?')
        surname = st.text_input(label = 'Surname', placeholder = 'Surname?')
        job = st.text_input(label = 'Job', placeholder = 'Job?')
        exp = st.text_input(label = 'Expirity Date', value = '2023-12-31 00:00:00')
        emp_no = st.text_input(label = 'Employee Number', placeholder = 'Employee Number?')
        capri = st.text_input(label = 'Cards Printed', value = 0)
        
        # empty image
        image = ''
        uploaded_file = st.file_uploader(label = "Upload a picture (256×360)", type = 'png')
        if uploaded_file is not None:
          image = uploaded_file.getvalue()
          
        else:
          image = loadFile("images/placeholder.png")
        
    
        ## Submit Button `Create New Employee`
        submitted = st.form_submit_button("Create New Employee")
        if submitted:
          ## Writing to databank if data was entered
          if (layout is not None and forename and surname and job and exp and emp_no and capri):
            ## Get latest ID from database
            id = lastID(url = "idcard.IMAGEBASE")
            
            
            ## Maybe it needs a break???
            query = "INSERT INTO `idcard`.`IMAGEBASE`(ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED) VALUES (%s, %s, '%s', '%s', '%s', '%s', %s, %s);" %(id, layout, forename, surname, job, exp, emp_no, capri)
            run_query(query)
            conn.commit()
            st.session_state['success1'] = True
            
            
            ## Upload picture to database
            pictureUploader(image, id)
            
            
            ## Set query parameter
            st.experimental_set_query_params(eno = eno)
            
            
            ## Set `index` to refer to new `ID` position in database, so that reload opens new employee data
            st.session_state['index'] = int(id)
            
            
          else:
            st.session_state['success1'] = False
          
          st.experimental_rerun()
 
      
      ## If data is already existent, show filled form  
      else:
        ## Get information of selected Employee
        query = "SELECT ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED, IMAGE FROM `idcard`.`IMAGEBASE` WHERE ID = %s;" %(index)
        employee = run_query(query)
        
        
        ## Set query parameter
        st.experimental_set_query_params(eno = employee[0][6])
        
        
        ## Input for updating employee data
        updateMaster = False
        id = st.text_input(label = 'ID', value = employee[0][0], disabled = True)
        layout = st.text_input(label = 'Layout', value = employee[0][1], disabled = True)
        forename = st.text_input(label = 'Forename', value = employee[0][2], disabled = not checkbox_val)
        if (employee[0][2] != forename):
          updateMaster = True
        surname = st.text_input(label = 'Surname', value = employee[0][3], disabled = not checkbox_val)
        if (employee[0][3] != surname):
          updateMaster = True
        job = st.text_input(label = 'Job', value = employee[0][4], disabled = not checkbox_val)
        if (employee[0][4] != job):
          updateMaster = True
        exp = st.text_input(label = 'Expirity Date', value = employee[0][5], disabled = not checkbox_val)
        if (employee[0][5] != exp):
          updateMaster = True
        emp_no = st.text_input(label = 'Employee Number', value = employee[0][6], disabled = not checkbox_val)
        if (employee[0][6] != emp_no):
          updateMaster = True
        capri = st.text_input(label = 'Cards Printed', value = employee[0][7], disabled = not checkbox_val)
        if (employee[0][7] != capri):
          updateMaster = True
          
          
        ## Check if image is empty and show a placeholder
        if (len(employee[0][8]) < 10):
          # Show placeholder
          st.image('images/portrait-placeholder.png')
          # Set Image Session State to `No Image` placeholder
          st.session_state['image'] = loadFile('images/No_Image.png')
         
          
        ## Show existing Image
        else:          
          st.image(employee[0][8])
          # Save Image for downloading to Image Session State
          st.session_state['image'] = employee[0][8]
        
        
        ## Image Uploader
        uploaded_file = st.file_uploader(label = "Upload a picture (256×360)", type = 'png', disabled = not checkbox_val)
        if uploaded_file is not None:
          updateMaster = True
          image = uploaded_file.getvalue()
          # Upload picture to database
          pictureUploader(image, index)
        
        
        ## No image data  
        else:
          image = ''
        
          
        ## Submit Button for Changes on employee master data
        submitted = st.form_submit_button("Save changes on Master data")
        if submitted:
          # Set session state `index`
          st.session_state['index'] = index
          
          
          ## Writing to databank idcard Table IMAGEBASE
          if (updateMaster == True):
            query = "UPDATE `idcard`.`IMAGEBASE` SET LAYOUT = %s, FORENAME = '%s', SURNAME = '%s', JOB_TITLE = '%s', EXPIRY_DATE = '%s', EMPLOYEE_NO = '%s', CARDS_PRINTED = %s WHERE ID = %s;" %(layout, forename, surname, job, exp, eno, capri, index)
            run_query(query)
            conn.commit()
            st.session_state['success1'] = True
            
          else:
            st.session_state['success1'] = False

          
          ## Set Session State to 2nd run and reloading to get actual data
          st.session_state['run'] = False
          st.experimental_rerun()
          
            
        ## Warning or Success messages after reloading
        if (st.session_state['run'] != True and st.session_state['success1'] == True):
          st.success(body = 'Master data submitted to Databank.', icon = "✅")
        else:
          if (st.session_state['run'] != True):
            st.warning(body = 'Not sumitted, as no new Master data was entered!', icon = "⚠️")
          
        
    ## tab `Training data`
    elif (f"{chosen_id}" == '2'):
      ## Get information of selected Employee regarding Training
      st.title('Employee Training data')
      st.subheader('Enter or view exmployee training data')
       
          
      ## If new Employee just show empty form
      if (index == 0):
        st.info(body = 'Create Employee first!', icon = "ℹ️")
        
        
        ## Submit Button for Changes on employee `Training data` - New employee
        submitted = st.form_submit_button("Nothing to save.")
        if submitted:
          print("Nothing changed")
      
          
      ## Employee existend
      else:
        ## Check for last ID number in TrainingData (to add data after)
        idT = lastID(url = "idcard.TRAININGDATA")
        
          
        ## Get Training Data
        query = "SELECT tr.TRAINING, tr.INSTITUTE, tr.DATE, tr.DAYS, tr.ID, ima.EMPLOYEE_NO FROM `idcard`.`IMAGEBASE` AS ima LEFT JOIN `idcard`.`TRAININGDATA` AS tr ON ima.EMPLOYEE_NO = tr.EMPLOYEE_NO WHERE ima.ID = %s;" %(index)
        trainingData = run_query(query)
        
        
        ## Set query parameter
        st.experimental_set_query_params(eno = trainingData[0][5])
         
          
        ## Variables for Text Input
        training = []
        institute = []
        date = []
        days = []
          
          
        ## Boolean for flow control
        insert = False # Will be set to `True` if a new entry is entered
        update = False # Will be set to `True` if existing data is altered
        
          
        ## Check if Training Data is already there for an Employee and show it
        if (trainingData[0][0] != None):
          for i in range(len(trainingData)):
            # Show (Multiple) Input(s)
            x = st.text_input(label = 'Training #' + str(i + 1), value = trainingData[i][0], key = 'training' + str(i), disabled = not checkbox_val)
            if (trainingData[i][0] != x):
              update = True
            training.append(x)
            x = st.text_input(label = 'Institute', value = trainingData[i][1], key = 'institute' + str(i), disabled = not checkbox_val)
            if (trainingData[i][1] != x):
              update = True
            institute.append(x)
            x = st.text_input(label = 'Date', value = trainingData[i][2], key = 'date' + str(i), disabled = not checkbox_val)
            if (trainingData[i][2] != x):
              update = True
            date.append(x)
            x = st.text_input(label = 'Days', value = trainingData[i][3], key = 'days' + str(i), disabled = not checkbox_val)
            if (trainingData[i][3] != x):
              update = True
            days.append(x)
  
              
        ## Show new entry input fields if checkbox 'Add Training' is checked
        ## If not checked
        if not checkbox_training:
          if (trainingData[0][0] == None):
            st.info(body = 'No Training data available', icon = "ℹ️")


        ## If checked    
        else:
          # Calculating number of training
          if (trainingData[0][0] == None):
            counter = 'Training #1'
              
          else:
            counter = 'Training #' + str(len(trainingData) + 1)
          

          ## Inputs for new Training
          x = st.text_input(label = counter, placeholder = 'Training?', disabled = not checkbox_val)
          if x.strip():
            training.append(x)
            insert = True
          x = st.text_input(label = 'Institute', placeholder = 'Institute?', disabled = not checkbox_val)
          if x.strip():
            institute.append(x)
            insert = True
          x = st.text_input(label = 'Date', placeholder = 'Date?', disabled = not checkbox_val)
          if x.strip():
            date.append(x)
            insert = True
          x = st.text_input(label = 'Days', placeholder = 'Days?', disabled = not checkbox_val)
          if x.strip():
            days.append(x)
            insert = True
                
                
        ## Submit Button for Changes on employee `Training data` - existend employee
        submitted = st.form_submit_button("Save changes on Training data")
        if submitted:
          ## Writing to databank idcard Table TRAININGDATA - first entry
          if (insert == True and update == False):
            if (training[0].strip() and institute[0].strip() and date[0].strip() and days[0].strip()):
              if (trainingData[0][0] == None):
                query = "INSERT INTO `idcard`.`TRAININGDATA`(ID, EMPLOYEE_NO, TRAINING, INSTITUTE, DATE, DAYS) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" %(idT, eno['eno'][0], training[0], institute[0], date[0], days[0])
                run_query(query)
                conn.commit()
                st.session_state['success2'] = True
              
            else:
              st.session_state['success2'] = False
              
              
          ## Writing to databank idcard Table TRAININGDATA - new entry (not first)
          if (insert == True and trainingData[0][0] != None):
            if (training[len(trainingData)].strip() and institute[len(trainingData)].strip() and date[len(trainingData)].strip() and days[len(trainingData)].strip()):
              query = "INSERT INTO `idcard`.`TRAININGDATA`(ID, EMPLOYEE_NO, TRAINING, INSTITUTE, DATE, DAYS) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" %(idT, eno['eno'][0], training[len(trainingData)], institute[len(trainingData)], date[len(trainingData)], days[len(trainingData)])
              run_query(query)
              conn.commit()
              st.session_state['success2'] = True
              
            else:
              st.session_state['success2'] = False
              
              
          ## Writing to databank idcard Table TRAININGDATA - Updates to all existing entries
          if (update == True):
            for i in range(len(trainingData)):
              query = "UPDATE `idcard`.`TRAININGDATA` SET TRAINING = '%s', INSTITUTE = '%s', DATE = '%s', DAYS = '%s' WHERE ID = %s;" %(training[i], institute[i], date[i], days[i], trainingData[i][4])
              run_query(query)
              conn.commit()
            st.session_state['success2'] = True
                
                
          ## Set Session State to 2nd run and reloading to get actual data
          st.session_state['run'] = False
          st.experimental_rerun()
            
            
        ## Warning or Success messages after reloading
        if (st.session_state['run'] != True and st.session_state['success2'] == True):
          st.success(body = 'Training data submitted to Databank.', icon = "✅")
        else:
          if (st.session_state['run'] != True):
            st.warning(body = 'Not sumitted, as no new Training data was entered!', icon = "⚠️")
        
        
    ## tab `More data`
    elif (f"{chosen_id}" == '3'):
      st.title('More employee data')
      st.subheader('Enter or view exmployee data')
          
          
      ## If new Employee just show empty form
      if (index == 0):
        st.info(body = 'Create Employee first!', icon = "ℹ️")
        
        ## Submit Button for Changes on `More data` - New employee
        submitted = st.form_submit_button("Nothing to save.")
        if submitted:
          print("Nothing changed")
          
          
      ## Employee existend
      else:
        st.info(body = 'Coming soon...', icon = "ℹ️")
            
        ## Submit Button for Changes on `More data` - existend employee
        submitted = st.form_submit_button("Save changes on More data")
        if submitted:
          ## Let not succeed as there is nothing to submit!
          st.session_state['success3'] = False
            
          ## Set Session State to 2nd run and reloading to get actual data
          st.session_state['run'] = False
          st.experimental_rerun()
          
        ## Warning or Success messages after reloading
        if (st.session_state['run'] != True and st.session_state['success3'] == True):
          st.success(body = 'Data submitted to Databank.', icon = "✅")
        else:
          if (st.session_state['run'] != True):
            st.warning(body = 'Not submitted, as not yet implemented!', icon = "⚠️")
        
     
        
    ### Out of the Tabs
    ## Nothing yet to show
        
        


  #### Out of the Form
  ### More functionanlity
  ## Image Download Button
  st.download_button('Download Image', data = st.session_state['image'], mime="image/png")
  
  
  ## Print databank in dataframe table
  with st.expander("See all Databank entries", expanded = False):
    ## Show `IMAGEBASE` table data
    st.subheader('Employee data')
    st.dataframe(databank, use_container_width = True)
    
    
    # Show `TRAININGDATA` table data
    st.subheader('Training data')
    st.dataframe(databank_training, use_container_width = True)
    
    
    ## Export `Vehicles` dataframe to Excel Makro file
    if st.button('Export Excel'):
      export_excel('Employees', 'G', [{'header': 'LAYOUT'}, {'header': 'FORENAME'}, {'header': 'SURNAME'}, {'header': 'JOB_TITLE'}, {'header': 'EXPIRY_DATE'}, {'header': 'EMPLOYEE_NO'}, {'header': 'CARDS_PRINTED'},], int(len(databank) + 1), databank,
                  'Trainings', 'E', [{'header': 'EMPLOYEE_NO'}, {'header': 'TRAINING'}, {'header': 'INSTITUTE'}, {'header': 'DATE'}, {'header': 'DAYS'},], int(len(databank_training) + 1), databank_training)
  

       
          
#### Not Logged in state (Landing page)
else :
  ### Header of Landing Page
  ## Title and information
  st.title('Kamuzu Central Hospital (KCH)')
  st.header('Welcome to the KCH HR Staff Portal')
  st.subheader('User Login')
  st.write('Please login (sidebar on the left) to access the KCH HR Staff Portal.')
  
  
  
  ### Sub-pages menu
  ## Menu to open sub-pages  
  st.subheader('Pages (without login)')
  st.write('You can access these pages without user log in:')
  st.write("<a href='Statistics' target='_self'>Statistics</a>", unsafe_allow_html = True)
  st.write("<a href='Workshops' target='_self'>Workshops</a>", unsafe_allow_html = True)
  st.write("<a href='About' target='_self'>About</a>", unsafe_allow_html = True)
