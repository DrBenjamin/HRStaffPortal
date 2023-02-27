##### `🏥_HR_Staff_Portal.py`
##### HR Staff Portal
##### Open-Source, hosted on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import extra_streamlit_components as stx
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import pygsheets
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
from functions import rebuild_confirmation
from functions import qrcode_reader
from functions import parse_national_id
from network import google_sheet_credentials




#### Streamlit initial setup
desc_file = open('DESCRIPTION', 'r')
lines = desc_file.readlines()
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
  

## National ID
if ('national_id_data' not in st.session_state):
  st.session_state['national_id_data'] = None




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
  #st.session_state['national_id_data'] = None
  
  


#### Two versions of the page -> Landing page vs. HRStaffPortal
### Logged in state (HR Staff Portal)
if check_password():
  ### Header
  header(title = 'HR Staff Portal', data_desc = 'employee data', expanded = st.session_state['header'])



  ### Get data from the databank(s)
  # Open databank connection
  conn = init_connection()

  # Get employee data
  query = "SELECT ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED FROM `idcard`.`IMAGEBASE`;"
  rows = run_query(query)
  databank = pd.DataFrame(columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]], columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED'])
    databank = pd.concat([databank, df])
  databank = databank.set_index('ID')
  
  # Get extra employee data
  query = "SELECT ID, EMPLOYEE_NO, EMPLOYEE_GENDER, EMPLOYEE_BIRTHDAY, EMPLOYEE_ADDRESS_STREET, EMPLOYEE_ADDRESS_CITY, EMPLOYEE_ADDRESS_CITY_CODE, EMPLOYEE_EMAIL, EMPLOYEE_PHONE, EMPLOYEE_PHONE2, EMPLOYEE_NATIONALITY, EMPLOYEE_PLACE_OF_ORIGIN, EMPLOYEE_MARRIAGE_STATUS, EMPLOYEE_EMPLOYMENT_TYPE FROM `idcard`.`EMPLOYEE`;"
  rows = run_query(query)
  databank_employee = pd.DataFrame(columns = ['ID', 'EMPLOYEE_NO', 'EMPLOYEE_GENDER', 'EMPLOYEE_BIRTHDAY', 'EMPLOYEE_ADDRESS_STREET', 'EMPLOYEE_ADDRESS_CITY', 'EMPLOYEE_ADDRESS_CITY_CODE', 'EMPLOYEE_EMAIL', 'EMPLOYEE_PHONE', 'EMPLOYEE_PHONE2', 'EMPLOYEE_NATIONALITY', 'EMPLOYEE_PLACE_OF_ORIGIN', 'EMPLOYEE_MARRIAGE_STATUS', 'EMPLOYEE_EMPLOYMENT_TYPE'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]]], columns = ['ID', 'EMPLOYEE_NO', 'EMPLOYEE_GENDER', 'EMPLOYEE_BIRTHDAY', 'EMPLOYEE_ADDRESS_STREET', 'EMPLOYEE_ADDRESS_CITY', 'EMPLOYEE_ADDRESS_CITY_CODE', 'EMPLOYEE_EMAIL', 'EMPLOYEE_PHONE', 'EMPLOYEE_PHONE2', 'EMPLOYEE_NATIONALITY', 'EMPLOYEE_PLACE_OF_ORIGIN', 'EMPLOYEE_MARRIAGE_STATUS', 'EMPLOYEE_EMPLOYMENT_TYPE'])
    databank_employee = pd.concat([databank_employee, df])
  databank_employee = databank_employee.set_index('ID')
  
  # Get Training data
  query = "SELECT img.ID, img.EMPLOYEE_NO, img.WORKSHOP_ID, wor.WORKSHOP_TITLE, wor.WORKSHOP_DESCRIPTION, wor.WORKSHOP_FACILITATOR, wor.WORKSHOP_DATE, wor.WORKSHOP_DURATION FROM `idcard`.`TRAINING` AS img LEFT JOIN `idcard`.`WORKSHOP` AS wor ON img.WORKSHOP_ID = wor.WORKSHOP_ID;"
  rows = run_query(query)
  databank_training = pd.DataFrame(columns = ['ID', 'EMPLOYEE_NO', 'WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_FACILITATOR', 'WORKSHOP_DATE', 'WORKSHOP_DURATION'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]], columns = ['ID', 'EMPLOYEE_NO', 'WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_FACILITATOR', 'WORKSHOP_DATE', 'WORKSHOP_DURATION'])
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



  ### Google Sheet support
  ## Getting employee PIN data
  query = "SELECT ID, ID, EMPLOYEE_NO, PIN FROM `idcard`.`IMAGEBASE`;"
  rows = run_query(query)
  databank_pin = pd.DataFrame(columns = ['ID_INDEX', 'ID', 'EMPLOYEE_NO', 'PIN'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3]]], columns = ['ID_INDEX', 'ID', 'EMPLOYEE_NO', 'PIN'])
    databank_pin = pd.concat([databank_pin, df])
  databank_pin = databank_pin.set_index('ID_INDEX')
    
    
  ## Open the spreadsheet and the first sheet
  # Getting credentials
  client = google_sheet_credentials()
  
  # Opening sheet
  sh = client.open_by_key(st.secrets['google']['pin_spreadsheet_id'])
  wks = sh.sheet1
    
    
  ## Update the worksheet with the numpy array values, beginning at cell 'A2'
  # Creating numpy array
  numb = np.array(databank_pin)
    
  # Converting numby array to list
  numb = numb.tolist()
    
  # Writing to worksheet
  wks.update_values(crange = 'A2', values = numb)
  


  ### Employee selectbox (on change sets first start session state)
  st.title('Employee data')
  if (st.session_state['chosen_id'] != 1):
    selectbox_enabled = True
  else:
    selectbox_enabled = False
  index = st.selectbox(label = "Which employee do you want to select?", options = range(len(names)), format_func = lambda x: names[x], on_change = onChange, index = st.session_state['index'], disabled = selectbox_enabled)
 
    
  ## Checkboxes for editing and adding training data
  if (index != 0):
    checkbox_val = st.checkbox(label = 'Edit Mode', value = False)
    checkbox_training = st.checkbox(label = 'Confirm Training', value = checkbox_val, disabled = not checkbox_val)
  
  
  ## QR Code reader for `National ID` to prefil `New Employee` form
  else:
    column1, column2 = st.columns(2)
    with column1:
      national_id = st.radio(label = 'Type of Input', options = ('Input data manually', 'Scan National ID'), index = 0)
      if national_id == 'Scan National ID':
        qrcode = qrcode_reader()
        if qrcode != None:
          st.session_state['national_id_data'] = parse_national_id(qrcode)
    with column2:
      if national_id == 'Input data manually':
        st.write('Proceed below to type in employee data')
        st.image('images/Keyboard.png')
      else:
        st.write('Scan the National ID QR Code on the backside')
        st.image('images/ID.png')


  
  ### Custom Tabs with IDs
  chosen_id = stx.tab_bar(data = [
    stx.TabBarItemData(id = 1, title = "Master data", description = "Employee data"),
    stx.TabBarItemData(id = 2, title = "Training data", description = "Employee trainings"),
    stx.TabBarItemData(id = 3, title = "More data", description = "Extra Employee data"),], default = 1)
  st.session_state['chosen_id'] = int(chosen_id)
  
  

  ### tab `Master data`
  if (st.session_state['chosen_id'] == 1):

        
        
    ## Form for showing employee input fields 
    with st.form("Employee data"):
      st.write('')
      st.title('Employee Master data')
      st.subheader('Enter or view Employee Master data')
      
      
      ## If new employee just show empty form
      if (index == 0):
        ## Set query parameter
        st.experimental_set_query_params(eno = "xxxxxx")
        
        
        ## New employee data input
        # Check for ID number count of Employee
        id = lastID(url = '`idcard`.`IMAGEBASE`')
        
        # Input fields
        st.text_input(label = 'ID', value = id, disabled = True)
        layout = st.text_input(label = 'Layout', value = 1)
        if st.session_state['national_id_data'] == None:
          forename = st.text_input(label = 'Forename', placeholder = 'Forename?')
          surname = st.text_input(label = 'Surname', placeholder = 'Surname?')
        else:
          forename = st.text_input(label = 'Forename', value = st.session_state['national_id_data']['first_name'].lower().capitalize())
          surname = st.text_input(label = 'Surname', value = st.session_state['national_id_data']['last_name'].lower().capitalize())
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
        if image != '':
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
        if image != '':
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
          
   
        
  ### tab `Training data`
  elif (st.session_state['chosen_id'] == 2):
    ## Expander for showing Employee Training data 
    with st.expander(label = "", expanded = True):
      ## Get information of selected employee regarding training
      st.title('Employee Training data')
      st.subheader('View employee training data')
       
          
      ## If new Employee just show empty form
      if (index == 0):
        st.info(body = 'Create Employee first!', icon = "ℹ️")
        
        
      ## Employee existend
      else:
        ## Check for last ID number in TRAINING (to add data after)
        idT = lastID(url = '`idcard`.`TRAINING`')
        
          
        ## Get training data
        query = "SELECT wor.WORKSHOP_TITLE, wor.WORKSHOP_DESCRIPTION, wor.WORKSHOP_FACILITATOR, wor.WORKSHOP_FACILITATOR_EMAIL, wor.WORKSHOP_DATE, wor.WORKSHOP_DURATION, tr.ID, img.EMPLOYEE_NO FROM `idcard`.`IMAGEBASE` AS img LEFT JOIN `idcard`.`TRAINING` AS tr ON img.EMPLOYEE_NO = tr.EMPLOYEE_NO LEFT  JOIN  `idcard`.`WORKSHOP`  AS wor ON tr.WORKSHOP_ID = wor.WORKSHOP_ID WHERE img.ID = %s;" %(index)
        TRAINING = run_query(query)
        
        
        ## Set query parameter
        st.experimental_set_query_params(eno = TRAINING[0][7])
        
          
        ## Check if training data is already there for an Employee and show it
        if (TRAINING[0][0] != None):
          for i in range(len(TRAINING)):
            # Show (Multiple) Input(s)
            st.write('**Workshop #' + str(i + 1) + '**')
            st.text_input(label = 'Title', value = TRAINING[i][0], key = 'Workshop' + str(i), disabled = True)
            st.text_input(label = 'Description', value = TRAINING[i][1], key = 'Description' + str(i), disabled = True)
            st.text_input(label = 'Facilitator', value = TRAINING[i][2], key = 'Facilitator' + str(i), disabled = True)
            st.text_input(label = 'Facilitator Email', value = TRAINING[i][3], key = 'Email' + str(i), disabled = True)
            st.text_input(label = 'Date', value = TRAINING[i][4], key = 'Date' + str(i), disabled = True)
            st.text_input(label = 'Duration', value = TRAINING[i][5], key = 'Duration' + str(i), disabled = True)
        else:
          st.info(body = 'No Training data available', icon = "ℹ️")
          

        ## Show selectbox 'Add Training' is checked
        # If not checked
        if checkbox_training:
          # Calculating number of training
          if (TRAINING[0][0] == None):
            counter = 'Workshop #1'
          else:
            counter = 'Workshop #' + str(len(TRAINING) + 1)
          

          ## Get Workshop data
          query = "SELECT WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_FACILITATOR_EMAIL, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES, WORKSHOP_ATTENDEES_CONFIRMED FROM `idcard`.`WORKSHOP`;"
          rows = run_query(query)
          databank_workshop = pd.DataFrame(columns = ['WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_FACILITATOR', 'WORKSHOP_FACILITATOR_EMAIL', 'WORKSHOP_DATE', 'WORKSHOP_DURATION', 'WORKSHOP_ATTENDEES', 'WORKSHOP_ATTENDEES_CONFIRMED'])
          for row in rows:
            df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_FACILITATOR', 'WORKSHOP_FACILITATOR_EMAIL', 'WORKSHOP_DATE', 'WORKSHOP_DURATION', 'WORKSHOP_ATTENDEES', 'WORKSHOP_ATTENDEES_CONFIRMED'])
            databank_workshop = pd.concat([databank_workshop, df])
          databank_workshop = databank_workshop.sort_values('WORKSHOP_DATE', ascending = False)
          
          # Set index (starting with 1)
          id_list = []
          for i in range(len(databank_workshop)):
            id_list.append(i + 1)
          databank_workshop.insert(0, "ID", id_list, True)
          databank_workshop = databank_workshop.set_index('ID')
          
          # Drop not needed rows (employee not invided or already confirmed) for option Selectbox
          dropping = []
          for i in range(len(databank_workshop)):
            invited = False
            if databank_workshop._get_value(i + 1, 'WORKSHOP_ATTENDEES') != None:
              for row in databank_workshop._get_value(i + 1, 'WORKSHOP_ATTENDEES').split(' '):
                if row == eno['eno'][0]:
                  invited = True
              if invited == False:
                dropping.append(i)
          databank_workshop = databank_workshop.drop(databank_workshop.index[dropping])
                 
          # Set new index (starting with 1)
          id_list = []
          for i in range(len(databank_workshop)):
            id_list.append(i + 1)
          databank_workshop.insert(0, "ID", id_list, True)
          databank_workshop = databank_workshop.set_index('ID')
          
          
          ## Selectbox to choose from existing Workshop
          st.subheader('Confirm training')
          st.write("Workshop not available in Selectbox? Go to <a href='Workshops' target='_self'>Workhop page</a> to invite employee to it or to add the Workshop.", unsafe_allow_html = True)
          
          # Concacenating lists as option for Selectbox
          workshop_title = [str(title) + ' (' for title in list(databank_workshop['WORKSHOP_TITLE'])]
          workshop_date = [str(date) + ')' for date in list(databank_workshop['WORKSHOP_DATE'])]
          workshops = [a + b for a, b in zip(workshop_title, workshop_date)]
          
          # Show Selectbox and Workshop information
          st.write('**' +counter + '**')
          if len(workshops) > 0:
            index_workshop = st.selectbox(label = 'Title', options = range(len(workshops)), format_func = lambda x: workshops[x], index = 0)
            st.text_input(label = 'Description', value = databank_workshop._get_value(index_workshop + 1, 'WORKSHOP_DESCRIPTION'), disabled = True)
            st.text_input(label = 'Facilitator', value = databank_workshop._get_value(index_workshop + 1, 'WORKSHOP_FACILITATOR'), disabled = True)
            st.text_input(label = 'Facilitator Email', value = databank_workshop._get_value(index_workshop + 1, 'WORKSHOP_FACILITATOR_EMAIL'), disabled = True)
            st.text_input(label = 'Date', value = databank_workshop._get_value(index_workshop + 1, 'WORKSHOP_DATE'), disabled = True)
            st.text_input(label = 'Duration', value = databank_workshop._get_value(index_workshop + 1, 'WORKSHOP_DURATION'), disabled = True)
          else:
            st.info(body = 'Employee needs to be invited a Workshop!', icon = "ℹ")
                
          ## Submit button for changes on employee `Training data` - existend employee
          submitted = st.button("Confirm training for employee")
          if submitted:
            ## Rewriting changes to database 
            # Writing changes to databank idcard table TRAINING
            query = "INSERT INTO `idcard`.`TRAINING`(ID, EMPLOYEE_NO, WORKSHOP_ID) VALUES (%s, '%s', '%s');" %(idT, eno['eno'][0], databank_workshop._get_value(index_workshop + 1, 'WORKSHOP_ID'))
            run_query(query)
            conn.commit()
            
            # Rebuild confirmation status
            confirmed, not_confirmed = rebuild_confirmation(option_attendee = 1, confirmed = databank_workshop._get_value(index_workshop + 1, 'WORKSHOP_ATTENDEES_CONFIRMED'), not_confirmed = databank_workshop._get_value(index_workshop + 1, 'WORKSHOP_ATTENDEES'), employee = eno['eno'][0])
            
            # Update workshop data
            query = "UPDATE `idcard`.`WORKSHOP` SET WORKSHOP_ATTENDEES = '%s', WORKSHOP_ATTENDEES_CONFIRMED = '%s' WHERE WORKSHOP_ID = '%s';" %(not_confirmed, confirmed, databank_workshop._get_value(index_workshop + 1, 'WORKSHOP_ID'))        
            run_query(query)
            conn.commit()
            
            # Reload to refresh values
            st.experimental_rerun()


        
  ### tab `More data`
  elif (st.session_state['chosen_id'] == 3):
    ## Expander for extra data
    with st.expander(label = "", expanded = True):
      st.title('More Employee data')
      st.subheader('Enter or view extra Employee data')
          
          
      ## If new Employee just show empty form
      if (index == 0):
        st.info(body = 'Create Employee first!', icon = "ℹ️")
          
          
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
          if (databank_employee1._get_value(1, 'EMPLOYEE_GENDER') != gender):
            updateExtra = True
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
          options = ['Married', 'Unmarried', 'Widow(er)']
          if (databank_employee1._get_value(1, 'EMPLOYEE_MARRIAGE_STATUS') == 'Married'):
            index = 0
          elif (databank_employee1._get_value(1, 'EMPLOYEE_MARRIAGE_STATUS') == 'Unmarried'):
            index = 1
          elif (databank_employee1._get_value(1, 'EMPLOYEE_MARRIAGE_STATUS') == 'Widow(er)'):
            index = 2
          else:
            index = 0
          marriage = st.selectbox('Marriage status', options = options, index = index)
          if (databank_employee1._get_value(1, 'EMPLOYEE_MARRIAGE_STATUS') != marriage):
            updateExtra = True
          options = ['Employed', 'T.A.', 'Intern']
          if (databank_employee1._get_value(1, 'EMPLOYEE_EMPLOYMENT_TYPE') == 'Employed'):
            index = 0
          elif (databank_employee1._get_value(1, 'EMPLOYEE_EMPLOYMENT_TYPE') == 'T.A.'):
            index = 1
          elif (databank_employee1._get_value(1, 'EMPLOYEE_EMPLOYMENT_TYPE') == 'Intern'):
            index = 2
          else:
            index = 0
          employment_type = st.selectbox('Marriage status', options = options, index = index)
          if (databank_employee1._get_value(1, 'EMPLOYEE_EMPLOYMENT_TYPE') != employment_type):
            updateExtra = True
        
        
        ## Input extra employee data if not existend
        else:
          options = ['Female', 'Male', 'Divers']
          if st.session_state['national_id_data'] == None:
            gender = st.selectbox('Gender', options = options, index = 0)
          else:
            if (st.session_state['national_id_data']['gender'] == 'Female'):
              index = 0
            elif (st.session_state['national_id_data']['gender'] == 'Male'):
              index = 1
            elif (st.session_state['national_id_data']['gender'] == 'Divers'):
              index = 2
            else:
              index = 0
            gender = st.selectbox('Gender', options = options, index = index)
          if st.session_state['national_id_data'] == None:
            birthday = st.date_input(label = 'Birthday', value = datetime.now(), min_value = date(1950, 1, 1), max_value = datetime.now())
          else:
            birthday = st.date_input(label = 'Birthday', value = st.session_state['national_id_data']['dob'], min_value = date(1950, 1, 1), max_value = datetime.now())
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
          if st.session_state['national_id_data'] == None:
            nationality = st.text_input(label = 'Nationality', placeholder = 'Nationality?', disabled = False)
          else:
            nationality = st.text_input(label = 'Nationality', value = 'Malawian', disabled = False)
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
        
        
        ## Submit Button for Changes on `More data` - existend employee
        submitted = st.button("Save changes on more data")
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
          
          
        ## Show Driver data
        st.subheader('View Driver data')
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
          
          
        ## Warning or Success messages after reloading
        if (st.session_state['run'] != True and st.session_state['success3'] == True):
          st.success(body = 'Data submitted to Databank.', icon = "✅")
        else:
          if (st.session_state['run'] != True):
            st.warning(body = 'Not submitted, as no changes!', icon = "⚠️")
        
     
        
  ### Out of the Tabs
  ## Image Download Button
  st.download_button('Download Image', data = st.session_state['image'], mime="image/png")
  
  
  ## Show databank data in editable dataframe
  with st.expander("See all Databank entries", expanded = False):
    st.info('You may want to alter the data before exporting to Excel (e.g. delete specific column data cause of Data Privacy reasons - this will not change the database data!)', icon = 'ℹ️')


    ## Show `IMAGEBASE` table data
    st.subheader('Employee data')
    databank = st.experimental_data_editor(databank, use_container_width = True)
    
    
    ## Show `EMPLOYEE` table data
    st.subheader('Extra employee data')
    databank_employee = st.experimental_data_editor(databank_employee, use_container_width = True)
    
    
    ## Show `TRAINING` table data
    st.subheader('Training data')
    databank_training = st.experimental_data_editor(databank_training, use_container_width = True)
    
    
    ## Export `Vehicles` dataframe to Excel Makro file
    if st.button('Export Excel'):
      export_excel('Employees', 'G', [{'header': 'LAYOUT'}, {'header': 'FORENAME'}, {'header': 'SURNAME'}, {'header': 'JOB_TITLE'}, {'header': 'EXPIRY_DATE'}, {'header': 'EMPLOYEE_NO'}, {'header': 'CARDS_PRINTED'},], int(len(databank) + 1), databank,
                   'Extra data', 'M', [{'header': 'EMPLOYEE_NO'}, {'header': 'GENDER'}, {'header': 'BIRTHDAY'}, {'header': 'STREET'}, {'header': 'CITY'}, {'header': 'CITY_CODE'}, {'header': 'EMAIL'}, {'header': 'PHONE'}, {'header': 'PHONE2'}, {'header': 'NATIONALITY'}, {'header': 'ORIGIN'}, {'header': 'MARRIAGE'}, {'header': 'EMPLOYEMENT'},], int(len(databank_employee) + 1), databank_employee,
                   'Trainings', 'E', [{'header': 'EMPLOYEE_NO'}, {'header': 'TRAINING'}, {'header': 'INSTITUTE'}, {'header': 'DATE'}, {'header': 'DAYS'},], int(len(databank_training) + 1), databank_training)

       
          
### Not Logged in state (Landing page)
else :
  landing_page('HR Staff Portal')
