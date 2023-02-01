##### `🏥_HR_Staff_Portal.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import extra_streamlit_components as stx
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import cv2
import mysql.connector
import os
import platform
import io
import sys
from datetime import datetime, date
sys.path.insert(1, "pages/functions/")
from functions import header
from functions import check_password
from functions import logout
from functions import export_excel
from functions import load_file
from functions import landing_page




#### Streamlit initial setup
desc_file = open('DESCRIPTION', 'r')
lines = desc_file.readlines()
print(lines[3])
st.set_page_config(
  page_title = "HR Staff Portal",
  page_icon = st.secrets['custom']['facility_image_thumbnail'],
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': st.secrets['custom']['menu_items_help'],
         'Report a bug': st.secrets['custom']['menu_items_bug'],
         'About': '**HR Staff Portal** (' + lines[3] + ')\n\n' + st.secrets['custom']['facility'] + ' (' + st.secrets['custom']['facility_abbreviation'] + ')' + ', ' + st.secrets['custom']['address_line1'] + '\n' +st.secrets['custom']['address_line2'] + '\n\n' + st.secrets['custom']['contact_tel1'] + '\n\n' + st.secrets['custom']['contact_tel2'] + '\n\n' + st.secrets['custom']['contact_tel3'] + '\n\n' + st.secrets['custom']['contact_mail1_desc'] + ': ' + st.secrets['custom']['contact_mail1'] + '\n\n' + st.secrets['custom']['contact_mail2_desc'] + ': ' + st.secrets['custom']['contact_mail2'] + '\n\nAdministrator: ' + st.secrets['custom']['contact_admin'] + '\n\n-----------'
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
## Session states
if ('run' not in st.session_state):
  st.session_state['run'] = True
if ('admin' not in st.session_state):
  st.session_state['admin'] = False
if ('header' not in st.session_state):
  st.session_state['header'] = True
 
  
## Database transmission success state1
if ('success1' not in st.session_state):
  st.session_state['success1'] = False
if ('success2' not in st.session_state):
  st.session_state['success2'] = False
if ('success3' not in st.session_state):
  st.session_state['success3'] = False

  
## Selected employee session states
if ('index' not in st.session_state):
  st.session_state['index'] = 0
if ('chosen_id' not in st.session_state):
  st.session_state['chosen_id'] = 1
  
  
## Logout
if ('logout' not in st.session_state):
  st.session_state['logout'] = False
  

## Image
if ('image' not in st.session_state):
  st.session_state['image'] = 'images/placeholder.png'




#### All Functions used exclusively in HR Staff Portal
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
    # Perform query
    try:
      cur.execute(query)
      return cur.fetchall()
    
    except:
      print('An exception occurred in function `run_query` with query \"' + query + '\"')
      
      
      
### Function: lastID = checks for last ID number in Table (to add data after)
def lastID(url):
  query = "SELECT MAX(ID) FROM %s;" %(url)
  rows = run_query(query)
  
  # Check for ID
  for row in rows:
    if (row[0] != None):
      id = int(row[0]) + 1
    else:
      id = 1
      break
  
  # Return ID    
  return id



### Function: pictureUploader = uploads employee images
def pictureUploader(image, index):
  # Initialize connection
  connection = mysql.connector.connect(**st.secrets["mysql"])
  cursor = connection.cursor()
  
  # SQL statement
  sql_insert_blob_query = """ UPDATE IMAGEBASE SET IMAGE = %s WHERE ID = %s;"""
  
  # Convert data into tuple format
  insert_blob_tuple = (image, index)
  result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
  connection.commit()
 
    
    
### Function: onChange = If selectbox is used
def onChange():
  st.session_state['run'] = True
  #st.session_state['chosen_id'] = 1




#### Two versions of the page -> Landing page vs. HRStaffPortal
### Logged in state (HR Staff Portal)
if check_password():
  ## Header
  header(title = 'HR Staff Portal', data_desc = 'employee data', expanded = st.session_state['header'])


  ## Get data from the databank(s)
  # Open databank connection
  conn = init_connection()

  # Getting employee data
  query = "SELECT ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED FROM `idcard`.`IMAGEBASE`;"
  rows = run_query(query)
  databank = pd.DataFrame(columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]], columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED'])
    databank = pd.concat([databank, df])
  databank = databank.set_index('ID')
  
  # Getting extra employee data
  query = "SELECT ID, EMPLOYEE_NO, EMPLOYEE_GENDER, EMPLOYEE_BIRTHDAY, EMPLOYEE_ADDRESS_STREET, EMPLOYEE_ADDRESS_CITY, EMPLOYEE_ADDRESS_CITY_CODE, EMPLOYEE_EMAIL, EMPLOYEE_PHONE, EMPLOYEE_PHONE2, EMPLOYEE_NATIONALITY, EMPLOYEE_PLACE_OF_ORIGIN, EMPLOYEE_MARRIAGE_STATUS, EMPLOYEE_EMPLOYMENT_TYPE FROM `idcard`.`EMPLOYEE`;"
  rows = run_query(query)
  databank_employee = pd.DataFrame(columns = ['ID', 'EMPLOYEE_NO', 'EMPLOYEE_GENDER', 'EMPLOYEE_BIRTHDAY', 'EMPLOYEE_ADDRESS_STREET', 'EMPLOYEE_ADDRESS_CITY', 'EMPLOYEE_ADDRESS_CITY_CODE', 'EMPLOYEE_EMAIL', 'EMPLOYEE_PHONE', 'EMPLOYEE_PHONE2', 'EMPLOYEE_NATIONALITY', 'EMPLOYEE_PLACE_OF_ORIGIN', 'EMPLOYEE_MARRIAGE_STATUS', 'EMPLOYEE_EMPLOYMENT_TYPE'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]]], columns = ['ID', 'EMPLOYEE_NO', 'EMPLOYEE_GENDER', 'EMPLOYEE_BIRTHDAY', 'EMPLOYEE_ADDRESS_STREET', 'EMPLOYEE_ADDRESS_CITY', 'EMPLOYEE_ADDRESS_CITY_CODE', 'EMPLOYEE_EMAIL', 'EMPLOYEE_PHONE', 'EMPLOYEE_PHONE2', 'EMPLOYEE_NATIONALITY', 'EMPLOYEE_PLACE_OF_ORIGIN', 'EMPLOYEE_MARRIAGE_STATUS', 'EMPLOYEE_EMPLOYMENT_TYPE'])
    databank_employee = pd.concat([databank_employee, df])
  databank_employee = databank_employee.set_index('ID')
  
  # Getting Training data
  query = "SELECT ID, EMPLOYEE_NO, TRAINING_DESCRIPTION, TRAINING_INSTITUTE, TRAINING_DATE, TRAINING_DURATION FROM `idcard`.`TRAINING`;"
  rows = run_query(query)
  databank_training = pd.DataFrame(columns = ['ID', 'EMPLOYEE_NO', 'TRAINING_DESCRIPTION', 'TRAINING_INSTITUTE', 'TRAINING_DATE', 'TRAINING_DURATION'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5]]], columns = ['ID', 'EMPLOYEE_NO', 'TRAINING_DESCRIPTION', 'TRAINING_INSTITUTE', 'TRAINING_DATE', 'TRAINING_DURATION'])
    databank_training = pd.concat([databank_training, df])
  databank_training = databank_training.set_index('ID')
 
      
  ## Get employee data for searching for building `ID` / `EMPLOYEE` pairs and filling the employee selectbox
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


  ## Employee selectbox (on change sets first start session state)
  if (st.session_state['chosen_id'] != 1):
    selectbox_enabled = True
  else:
    selectbox_enabled = False
  index = st.selectbox(label = "Which employee do you want to select?", options = range(len(names)), format_func = lambda x: names[x], on_change = onChange, index = st.session_state['index'], disabled = selectbox_enabled)
 
    
  ## Checkboxes for editing and adding training data
  if (index != 0):
    checkbox_val = st.checkbox(label = 'Edit Mode', value = False)
    checkbox_training = st.checkbox(label = 'Add Training', value = checkbox_val, disabled = not checkbox_val)

  
  ## Custom Tabs with IDs
  chosen_id = stx.tab_bar(data = [
    stx.TabBarItemData(id = 1, title = "Master data", description = "Employee data"),
    stx.TabBarItemData(id = 2, title = "Training data", description = "Employee trainings"),
    stx.TabBarItemData(id = 3, title = "More data", description = "Extra employee data"),], default = 1)
  st.session_state['chosen_id'] = int(chosen_id)
  

  ## Form for showing employee input fields 
  with st.form("Employee", clear_on_submit = True):
    ## tab `Master data`
    if (st.session_state['chosen_id'] == 1):
      st.title('Employee Master data')
      st.subheader('Enter or view exmployee master data')
      
      
      ## If new employee just show empty form
      if (index == 0):
        ## Set query parameter
        st.experimental_set_query_params(eno = "xxxxxx")
        
        
        ## New employee data input
        # Check for ID number count of Employee
        id = lastID(url = '`idcard`.`IMAGEBASE`')
        st.text_input(label = 'ID', value = id, disabled = True)
        layout = st.text_input(label = 'Layout', value = 1)
        forename = st.text_input(label = 'Forename', placeholder = 'Forename?')
        surname = st.text_input(label = 'Surname', placeholder = 'Surname?')
        job = st.text_input(label = 'Job', placeholder = 'Job?')
        exp = st.text_input(label = 'Expirity date', value = '2023-12-31 00:00:00')
        emp_no = st.text_input(label = 'Employee number', placeholder = 'Employee number?')
        capri = st.text_input(label = 'Cards printed', value = 0)
        
        
        ## Image input
        # Upload image
        image = ''
        uploaded_file = st.file_uploader(label = "Upload a picture", type = 'png')
        
        # Capture image
        captured_file = st.camera_input("or take a picture")
        
        # Check for image data
        if uploaded_file is not None:
          image = cv2.imdecode(np.frombuffer(uploaded_file.getvalue(), np.uint8), cv2.IMREAD_COLOR)
        elif captured_file is not None:
          # Create OpenCV numpy array image
          image = cv2.imdecode(np.frombuffer(captured_file.getvalue(), np.uint8), cv2.IMREAD_COLOR)
          
        # Crop image if existend
        if image is not '':
          h, w, _ = image.shape
          ratio = h / w
          
          # Image is smaller in height than standard image of 478 x 331 pixels
          if ratio <= 1.4:
            new_width = h / 1.4
            crop_center_x = w / 2
            crop_left_x = int(crop_center_x - (new_width / 2))
            crop_right_x = int(crop_center_x + (new_width / 2))
            image = image[0:h, crop_left_x: crop_right_x]
            
          # Image is bigger in height than standard image of 478 x 331 pixels
          else:
            new_height = 1.4 * w
            print(new_height)
            crop_center_y = h / 2
            crop_upper_y = int(crop_center_y - (new_height / 2))
            crop_bottom_y = int(crop_center_y + (new_height / 2))
            image = image[crop_upper_y:crop_bottom_y, 0:w]
            
          # Resize cropped image to standard dimensions
          image = cv2.resize(image, (256, 360), interpolation = cv2.INTER_AREA)
          
          # Convert OpenCV numpy array image to byte string
          image = cv2.imencode('.png', image)[1].tobytes()
        
        # Set placeholder image, if no image data existend
        else:
          image = load_file("images/placeholder.png")
        
    
        ## Submit button `Create New Employee`
        submitted = st.form_submit_button("Create New Employee")
        if submitted:
          ## Writing to databank if data was entered
          if (layout is not None and forename and surname and job and exp and emp_no and capri):
            ## Get latest ID from database
            id = lastID(url = '`idcard`.`IMAGEBASE`')
            
            
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
        exp = st.text_input(label = 'Expirity date', value = employee[0][5], disabled = not checkbox_val)
        if (employee[0][5] != exp):
          updateMaster = True
        emp_no = st.text_input(label = 'Employee number', value = employee[0][6], disabled = not checkbox_val)
        if (employee[0][6] != emp_no):
          updateMaster = True
        capri = st.text_input(label = 'Cards printed', value = employee[0][7], disabled = not checkbox_val)
        if (employee[0][7] != capri):
          updateMaster = True
          
          
        ## Check if image is empty and show a placeholder
        if (len(employee[0][8]) < 10):
          # Show placeholder
          st.image('images/placeholder.png')
          
          # Set Image Session State to `No Image` placeholder
          st.session_state['image'] = load_file('images/placeholder.png')
         
          
        ## Show existing image
        else:          
          st.image(employee[0][8])
          
          # Save Image for downloading to Image Session State
          st.session_state['image'] = employee[0][8]
        
        
        ## Image input
        # Upload image
        image = ''
        uploaded_file = st.file_uploader(label = "Upload a picture", type = 'png', disabled = not checkbox_val)
        
        # Capture image
        captured_file = st.camera_input("or take a picture", disabled = not checkbox_val)
        
        # Check for image data
        if uploaded_file is not None:
          image = cv2.imdecode(np.frombuffer(uploaded_file.getvalue(), np.uint8), cv2.IMREAD_COLOR)
        elif captured_file is not None:
          # Create OpenCV numpy array image
          image = cv2.imdecode(np.frombuffer(captured_file.getvalue(), np.uint8), cv2.IMREAD_COLOR)
          
        # Crop image if existend
        if image is not '':
          h, w, _ = image.shape
          ratio = h / w
          
          # Image is smaller in height than standard image of 478 x 331 pixels
          if ratio <= 1.4:
            new_width = h / 1.4
            crop_center_x = w / 2
            crop_left_x = int(crop_center_x - (new_width / 2))
            crop_right_x = int(crop_center_x + (new_width / 2))
            image = image[0:h, crop_left_x: crop_right_x]
            
          # Image is bigger in height than standard image of 478 x 331 pixels
          else:
            new_height = 1.4 * w
            crop_center_y = h / 2
            crop_upper_y = int(crop_center_y - (new_height / 2))
            crop_bottom_y = int(crop_center_y + (new_height / 2))
            image = image[crop_upper_y:crop_bottom_y, 0:w]
            
          # Resize cropped image to standard dimensions
          image = cv2.resize(image, (256, 360), interpolation = cv2.INTER_AREA)
          
          # Convert OpenCV numpy array image to byte string
          image = cv2.imencode('.png', image)[1].tobytes()

          # Upload picture to database
          pictureUploader(image, index)
        
          
        ## Submit button for changes on employee master data
        submitted = st.form_submit_button("Save changes on Master data")
        if submitted:
          # Set session state `index`
          st.session_state['index'] = index
          
          ## Writing to databank idcard Table IMAGEBASE
          if (updateMaster == True):
            query = "UPDATE `idcard`.`IMAGEBASE` SET LAYOUT = %s, FORENAME = '%s', SURNAME = '%s', JOB_TITLE = '%s', EXPIRY_DATE = '%s', EMPLOYEE_NO = '%s', CARDS_PRINTED = %s WHERE ID = %s;" %(layout, forename, surname, job, exp, emp_no, capri, index)
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
    elif (st.session_state['chosen_id'] == 2):
      ## Get information of selected employee regarding training
      st.title('Employee Training data')
      st.subheader('Enter or view exmployee training data')
       
          
      ## If new Employee just show empty form
      if (index == 0):
        st.info(body = 'Create Employee first!', icon = "ℹ️")
        
        
        ## Submit Button for changes on employee `Training data` - New employee
        submitted = st.form_submit_button("Nothing to save.")
        if submitted:
          print("Nothing changed")
      
          
      ## Employee existend
      else:
        ## Check for last ID number in TRAINING (to add data after)
        idT = lastID(url = '`idcard`.`TRAINING`')
        
          
        ## Get training data
        query = "SELECT tr.TRAINING_DESCRIPTION, tr.TRAINING_INSTITUTE, tr.TRAINING_DATE, tr.TRAINING_DURATION, tr.ID, ima.EMPLOYEE_NO FROM `idcard`.`IMAGEBASE` AS ima LEFT JOIN `idcard`.`TRAINING` AS tr ON ima.EMPLOYEE_NO = tr.EMPLOYEE_NO WHERE ima.ID = %s;" %(index)
        TRAINING = run_query(query)
        
        
        ## Set query parameter
        st.experimental_set_query_params(eno = TRAINING[0][5])
         
          
        ## Variables for text input
        training = []
        institute = []
        date = []
        days = []
          
          
        ## Boolean for flow control
        insert = False # Will be set to `True` if a new entry is entered
        update = False # Will be set to `True` if existing data is altered
        
          
        ## Check if training data is already there for an Employee and show it
        if (TRAINING[0][0] != None):
          for i in range(len(TRAINING)):
            # Show (Multiple) Input(s)
            x = st.text_input(label = 'Training #' + str(i + 1), value = TRAINING[i][0], key = 'training' + str(i), disabled = not checkbox_val)
            if (TRAINING[i][0] != x):
              update = True
            training.append(x)
            x = st.text_input(label = 'Institute', value = TRAINING[i][1], key = 'institute' + str(i), disabled = not checkbox_val)
            if (TRAINING[i][1] != x):
              update = True
            institute.append(x)
            x = st.text_input(label = 'Date', value = TRAINING[i][2], key = 'date' + str(i), disabled = not checkbox_val)
            if (TRAINING[i][2] != x):
              update = True
            date.append(x)
            x = st.text_input(label = 'Duration', value = TRAINING[i][3], key = 'duration' + str(i), disabled = not checkbox_val)
            if (TRAINING[i][3] != x):
              update = True
            days.append(x)
  
              
        ## Show new entry input fields if checkbox 'Add Training' is checked
        # If not checked
        if not checkbox_training:
          if (TRAINING[0][0] == None):
            st.info(body = 'No Training data available', icon = "ℹ️")

        # If checked    
        else:
          # Calculating number of training
          if (TRAINING[0][0] == None):
            counter = 'Training #1'
              
          else:
            counter = 'Training #' + str(len(TRAINING) + 1)
          

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
                
                
        ## Submit button for changes on employee `Training data` - existend employee
        submitted = st.form_submit_button("Save changes on Training data")
        if submitted:
          ## Writing to databank idcard table TRAINING - first entry
          if (insert == True and update == False):
            if (training[0].strip() and institute[0].strip() and date[0].strip() and days[0].strip()):
              if (TRAINING[0][0] == None):
                query = "INSERT INTO `idcard`.`TRAINING`(ID, EMPLOYEE_NO, TRAINING_DESCRIPTION, TRAINING_INSTITUTE, TRAINING_DATE, TRAINING_Duration) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" %(idT, eno['eno'][0], training[0], institute[0], date[0], days[0])
                run_query(query)
                conn.commit()
                st.session_state['success2'] = True
            else:
              st.session_state['success2'] = False
              
              
          ## Writing to databank idcard table `TRAINING` - new entry (not first)
          if (insert == True and TRAINING[0][0] != None):
            if (training[len(TRAINING)].strip() and institute[len(TRAINING)].strip() and date[len(TRAINING)].strip() and days[len(TRAINING)].strip()):
              query = "INSERT INTO `idcard`.`TRAINING`(ID, EMPLOYEE_NO, TRAINING_DESCRIPTION, TRAINING_INSTITUTE, TRAINING_DATE, TRAINING_DURATION) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" %(idT, eno['eno'][0], training[len(TRAINING)], institute[len(TRAINING)], date[len(TRAINING)], days[len(TRAINING)])
              run_query(query)
              conn.commit()
              st.session_state['success2'] = True
            else:
              st.session_state['success2'] = False
              
              
          ## Writing to databank idcard table `TRAINING` - updates to all existing entries
          if (update == True):
            for i in range(len(TRAINING)):
              query = "UPDATE `idcard`.`TRAINING` SET TRAINING_DESCRIPTION = '%s', TRAINING_INSTITUTE = '%s', TRAINING_DATE = '%s', TRAINING_DURATION = '%s' WHERE ID = %s;" %(training[i], institute[i], date[i], days[i], TRAINING[i][4])
              run_query(query)
              conn.commit()
            st.session_state['success2'] = True
                
                
          ## Set Session State to 2nd run and reloading to get actual data
          st.session_state['run'] = False
          st.experimental_rerun()
            
            
        ## Warning or success messages after reloading
        if (st.session_state['run'] != True and st.session_state['success2'] == True):
          st.success(body = 'Training data submitted to Databank.', icon = "✅")
        else:
          if (st.session_state['run'] != True):
            st.warning(body = 'Not sumitted, as no new Training data was entered!', icon = "⚠️")
        
        
    ## tab `More data`
    elif (st.session_state['chosen_id'] == 3):
      st.title('More employee data')
      st.subheader('Enter or view extra employee data')
          
          
      ## If new Employee just show empty form
      if (index == 0):
        st.info(body = 'Create Employee first!', icon = "ℹ️")
        
        ## Submit Button for Changes on `More data` - New employee
        submitted = st.form_submit_button("Nothing to save.")
        if submitted:
          print("Nothing changed")
          
          
      ## Employee existend
      else:
        ## Get extra employee data
        query = "SELECT ID, EMPLOYEE_NO, EMPLOYEE_GENDER, EMPLOYEE_BIRTHDAY, EMPLOYEE_ADDRESS_STREET, EMPLOYEE_ADDRESS_CITY, EMPLOYEE_ADDRESS_CITY_CODE, EMPLOYEE_EMAIL, EMPLOYEE_PHONE, EMPLOYEE_PHONE2, EMPLOYEE_NATIONALITY, EMPLOYEE_PLACE_OF_ORIGIN, EMPLOYEE_MARRIAGE_STATUS, EMPLOYEE_EMPLOYMENT_TYPE FROM `idcard`.`EMPLOYEE` WHERE EMPLOYEE_NO = '%s';" %(eno['eno'][0])
        rows = run_query(query)
        
        # Create pandas dataframe 
        databank_employee1 = pd.DataFrame(columns = ['ID', 'EMPLOYEE_NO', 'EMPLOYEE_GENDER', 'EMPLOYEE_BIRTHDAY', 'EMPLOYEE_ADDRESS_STREET', 'EMPLOYEE_ADDRESS_CITY', 'EMPLOYEE_ADDRESS_CITY_CODE', 'EMPLOYEE_EMAIL', 'EMPLOYEE_PHONE', 'EMPLOYEE_PHONE2', 'EMPLOYEE_NATIONALITY', 'EMPLOYEE_PLACE_OF_ORIGIN', 'EMPLOYEE_MARRIAGE_STATUS', 'EMPLOYEE_EMPLOYMENT_TYPE'])
        
        # Populate dataframe
        for row in rows:
          df = pd.DataFrame([[1, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]]], columns = ['ID', 'EMPLOYEE_NO', 'EMPLOYEE_GENDER', 'EMPLOYEE_BIRTHDAY', 'EMPLOYEE_ADDRESS_STREET', 'EMPLOYEE_ADDRESS_CITY', 'EMPLOYEE_ADDRESS_CITY_CODE', 'EMPLOYEE_EMAIL', 'EMPLOYEE_PHONE', 'EMPLOYEE_PHONE2', 'EMPLOYEE_NATIONALITY', 'EMPLOYEE_PLACE_OF_ORIGIN', 'EMPLOYEE_MARRIAGE_STATUS', 'EMPLOYEE_EMPLOYMENT_TYPE'])
          databank_employee1 = pd.concat([databank_employee1, df])
        databank_employee1 = databank_employee1.set_index('ID')
        
        
        ## Boolean for flow control
        insertExtra = False # Will be set to `True` if a new entry is entered
        updateExtra = False # Will be set to `True` if existing data is altered


        ## Input for updating extra employee data if existend
        if (len(rows) > 0):
          options = ['Female', 'Male', 'Divers']
          if (databank_employee1._get_value(1, 'EMPLOYEE_GENDER') == 'Female'):
            index = 0
          elif (databank_employee1._get_value(1, 'EMPLOYEE_GENDER') == 'Male'):
            index = 1
          elif (databank_employee1._get_value(1, 'EMPLOYEE_GENDER') == 'Divers'):
            index = 2
          else:
            index = 0
          gender = st.selectbox('Gender', options = options, index = index)
          birthday = st.date_input(label = 'Birthday', value = databank_employee1._get_value(1, 'EMPLOYEE_BIRTHDAY'), min_value = date(1950, 1, 1), max_value = datetime.now())
          address_street = st.text_input(label = 'Street', value = databank_employee1._get_value(1, 'EMPLOYEE_ADDRESS_STREET'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_ADDRESS_STREET') != address_street):
            updateExtra = True
          address_city = st.text_input(label = 'City', value = databank_employee1._get_value(1, 'EMPLOYEE_ADDRESS_CITY'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_ADDRESS_CITY') != address_city):
            updateExtra = True
          address_city_code = st.text_input(label = 'City code', value = databank_employee1._get_value(1, 'EMPLOYEE_ADDRESS_CITY_CODE'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_ADDRESS_CITY_CODE') != address_city_code):
            updateExtra = True
          email = st.text_input(label = 'Email', value = databank_employee1._get_value(1, 'EMPLOYEE_EMAIL'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_EMAIL') != email):
            updateExtra = True
          phone = st.text_input(label = 'Phone', value = databank_employee1._get_value(1, 'EMPLOYEE_PHONE'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_PHONE') != phone):
            updateExtra = True
          phone2 = st.text_input(label = 'Phone 2', value = databank_employee1._get_value(1, 'EMPLOYEE_PHONE2'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_PHONE2') != phone2):
            updateExtra = True
          nationality = st.text_input(label = 'Nationality', value = databank_employee1._get_value(1, 'EMPLOYEE_NATIONALITY'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_NATIONALITY') != nationality):
            updateExtra = True
          origin = st.text_input(label = 'Place of origin', value = databank_employee1._get_value(1, 'EMPLOYEE_PLACE_OF_ORIGIN'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_PLACE_OF_ORIGIN') != origin):
            updateExtra = True
          marriage = st.text_input(label = 'Marriage status', value = databank_employee1._get_value(1, 'EMPLOYEE_MARRIAGE_STATUS'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_MARRIAGE_STATUS') != marriage):
            updateExtra = True
          employment_type = st.text_input(label = 'Employee type', value = databank_employee1._get_value(1, 'EMPLOYEE_EMPLOYMENT_TYPE'), disabled = False)
          if (databank_employee1._get_value(1, 'EMPLOYEE_EMPLOYMENT_TYPE') != employment_type):
            updateExtra = True
        
        
        ## Input extra employee data if not existend
        else:
          options = ['Female', 'Male', 'Divers']
          gender = st.selectbox('Gender', options = options, index = 0)
          birthday = st.date_input(label = 'Birthday', value = datetime.now(), min_value = date(1950, 1, 1), max_value = datetime.now())
          address_street = st.text_input(label = 'Street', placeholder = 'Street?', disabled = False)
          if (address_street != ''):
            insertExtra = True
          address_city = st.text_input(label = 'City', placeholder = 'City?', disabled = False)
          if (address_city != ''):
            insertExtra = True
          address_city_code = st.text_input(label = 'City code', placeholder = 'City code?', disabled = False)
          if (address_city_code != ''):
            insertExtra = True
          email = st.text_input(label = 'Email', placeholder = 'Email?', disabled = False)
          if (email != ''):
            insertExtra = True
          phone = st.text_input(label = 'Phone', placeholder = 'Phone?', disabled = False)
          if (phone != ''):
            insertExtra = True
          phone2 = st.text_input(label = 'Phone 2', placeholder = 'Phone 2?', disabled = False)
          if (phone2 != ''):
            insertExtra = True
          nationality = st.text_input(label = 'Nationality', placeholder = 'Nationality?', disabled = False)
          if (nationality != ''):
            insertExtra = True
          origin = st.text_input(label = 'Place of origin', placeholder = 'Place of origin?', disabled = False)
          if (origin != ''):
            insertExtra = True
          marriage = st.text_input(label = 'Marriage status', placeholder = 'Marriage status?', disabled = False)
          if (marriage != ''):
            insertExtra = True
          employment_type = st.text_input(label = 'Employee type', placeholder = 'Employee type?', disabled = False)
          if (employment_type != ''):
            insertExtra = True

          
        ## Get driver data if available
        query = "SELECT ID, DRIVER_ID, DRIVER_NATIONAL_ID, DRIVER_MOBILE_NO, DRIVER_LICENSE_NO, DRIVER_LICENSE_CLASS, DRIVER_LICENSE_EXPIRY_DATE, DRIVER_PSV_BADGE, DRIVER_NOTES FROM carfleet.DRIVERS WHERE EMPLOYEE_NO = '%s';" %(eno['eno'][0])
        rows = run_query(query)
        
        # Create pandas dataframe 
        databank_driver = pd.DataFrame(columns = ['ID', 'DRIVER_ID', 'DRIVER_NATIONAL_ID', 'DRIVER_MOBILE_NO', 'DRIVER_LICENSE_NO', 'DRIVER_LICENSE_CLASS', 'DRIVER_LICENSE_EXPIRY_DATE', 'DRIVER_PSV_BADGE', 'DRIVER_NOTES'])
        
        # Populate dataframe
        for row in rows:
          df = pd.DataFrame([[1, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['ID', 'DRIVER_ID', 'DRIVER_NATIONAL_ID', 'DRIVER_MOBILE_NO', 'DRIVER_LICENSE_NO', 'DRIVER_LICENSE_CLASS', 'DRIVER_LICENSE_EXPIRY_DATE', 'DRIVER_PSV_BADGE', 'DRIVER_NOTES'])
          databank_driver = pd.concat([databank_driver, df])
        databank_driver = databank_driver.set_index('ID')
        
        with st.expander(label = 'Driver data', expanded = False):
          st.subheader('View driver data')
          
          # Show driver data if existent
          if (len(databank_driver) == 1):
            
            st.text_input(label = 'Driver ID', value = databank_driver._get_value(1, 'DRIVER_ID'), disabled = True)
            st.text_input(label = 'Driver national ID', value = databank_driver._get_value(1, 'DRIVER_NATIONAL_ID'), disabled = True)
            st.text_input(label = 'Driver mobile number', value = databank_driver._get_value(1, 'DRIVER_MOBILE_NO'), disabled = True)
            st.text_input(label = 'Driver license number', value = databank_driver._get_value(1, 'DRIVER_LICENSE_NO'), disabled = True)
            st.text_input(label = 'Driver license class', value = databank_driver._get_value(1, 'DRIVER_LICENSE_CLASS'), disabled = True)
            st.text_input(label = 'Driver license expiry date', value = databank_driver._get_value(1, 'DRIVER_LICENSE_EXPIRY_DATE'), disabled = True)
            st.text_input(label = 'Driver PSV badge', value = databank_driver._get_value(1, 'DRIVER_PSV_BADGE'), disabled = True)
            st.text_input(label = 'Driver notes', value = databank_driver._get_value(1, 'DRIVER_NOTES'), disabled = True)
            
          # If no driver data existend
          else:
            st.info(body = 'No driver data available', icon = "ℹ️")
        
        
        ## Submit Button for Changes on `More data` - existend employee
        submitted = st.form_submit_button("Save changes")
        if submitted:
          ## Writing to databank idcard table `EMPLOYEE`
          if (updateExtra == True and insertExtra == False):
            query = "UPDATE `idcard`.`EMPLOYEE` SET EMPLOYEE_GENDER = '%s', EMPLOYEE_BIRTHDAY = '%s', EMPLOYEE_ADDRESS_STREET = '%s', EMPLOYEE_ADDRESS_CITY = '%s', EMPLOYEE_ADDRESS_CITY_CODE = '%s', EMPLOYEE_EMAIL = '%s', EMPLOYEE_PHONE = '%s', EMPLOYEE_PHONE2 = '%s', EMPLOYEE_NATIONALITY = '%s', EMPLOYEE_PLACE_OF_ORIGIN = '%s', EMPLOYEE_MARRIAGE_STATUS = '%s', EMPLOYEE_EMPLOYMENT_TYPE = '%s' WHERE EMPLOYEE_NO = '%s';" %(gender, birthday, address_street, address_city, address_city_code, email, phone, phone2, nationality, origin, marriage, employment_type, eno['eno'][0])
            run_query(query)
            conn.commit()
            st.session_state['success3'] = True
          elif (updateExtra == False and insertExtra == True):
            id = lastID('`idcard`.`EMPLOYEE`')
            query = "INSERT INTO `idcard`.`EMPLOYEE`(ID, EMPLOYEE_NO, EMPLOYEE_GENDER, EMPLOYEE_BIRTHDAY, EMPLOYEE_ADDRESS_STREET, EMPLOYEE_ADDRESS_CITY, EMPLOYEE_ADDRESS_CITY_CODE, EMPLOYEE_EMAIL, EMPLOYEE_PHONE, EMPLOYEE_PHONE2, EMPLOYEE_NATIONALITY, EMPLOYEE_PLACE_OF_ORIGIN, EMPLOYEE_MARRIAGE_STATUS, EMPLOYEE_EMPLOYMENT_TYPE) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(id, eno['eno'][0], gender, birthday, address_street, address_city, address_city_code, email, phone, phone2, nationality, origin, marriage, employment_type)
            run_query(query)
            conn.commit()
            st.session_state['success3'] = True
          else:
            st.session_state['success3'] = False
           
            
          ## Set Session State to 2nd run and reloading to get actual data
          st.session_state['run'] = False
          st.experimental_rerun()
          
          
        ## Warning or Success messages after reloading
        if (st.session_state['run'] != True and st.session_state['success3'] == True):
          st.success(body = 'Data submitted to Databank.', icon = "✅")
        else:
          if (st.session_state['run'] != True):
            st.warning(body = 'Not submitted, as no changes!', icon = "⚠️")
        
     
        
    ### Out of the Tabs
    ## Nothing yet to show
        
        


  #### Out of the Form
  ### More functionanlity
  ## Image Download Button
  st.download_button('Download Image', data = st.session_state['image'], mime="image/png")
  
  
  ## Show databank data in dataframe
  with st.expander("See all Databank entries", expanded = False):
    ## Show `IMAGEBASE` table data
    st.subheader('Employee data')
    st.dataframe(databank, use_container_width = True)
    
    
    ## Show `EMPLOYEE` table data
    st.subheader('Extra employee data')
    st.dataframe(databank_employee, use_container_width = True)
    
    
    ## Show `TRAINING` table data
    st.subheader('Training data')
    st.dataframe(databank_training, use_container_width = True)
    
    
    ## Export `Vehicles` dataframe to Excel Makro file
    if st.button('Export Excel'):
      export_excel('Employees', 'G', [{'header': 'LAYOUT'}, {'header': 'FORENAME'}, {'header': 'SURNAME'}, {'header': 'JOB_TITLE'}, {'header': 'EXPIRY_DATE'}, {'header': 'EMPLOYEE_NO'}, {'header': 'CARDS_PRINTED'},], int(len(databank) + 1), databank,
                  'Trainings', 'E', [{'header': 'EMPLOYEE_NO'}, {'header': 'TRAINING'}, {'header': 'INSTITUTE'}, {'header': 'DATE'}, {'header': 'DAYS'},], int(len(databank_training) + 1), databank_training)

       
          
### Not Logged in state (Landing page)
else :
  landing_page('HR Staff Portal')
