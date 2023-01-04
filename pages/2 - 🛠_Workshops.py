##### `pages/2 - 🛠_Workshops.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import mysql.connector
import qrcode
import io 
import sys
sys.path.insert(1, "pages/functions/")
from functions import generateID




#### Streamlit initial setup
st.set_page_config(
  page_title = "Workshops",
  page_icon = "images/thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "collapsed",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the HR Staff Portal Version 0.2.0"
        }
)




#### Initialization of session states
  
  

  
#### Functions
### Function: run_query = Initial SQL Connection
def init_connection():
  ## Initialize connection
  try:
    return mysql.connector.connect(**st.secrets["mysql_benbox"])
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




#### Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')




#### Main Program
### Header
## Title
st.title('Workshops')


## Get workshop data
# Open databank connection
conn = init_connection()

# Run query 
query = "SELECT ID, WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES FROM idcard.WORKSHOP;"
rows = run_query(query)

# Creating pandas dataframe
databank_workshop = pd.DataFrame(columns = ['ID', 'WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_DATE', 'WORKSHOP_DURATION', 'WORKSHOP_ATTENDEES'])
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6]]], columns = ['ID', 'WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_DATE', 'WORKSHOP_DURATION', 'WORKSHOP_ATTENDEES'])
  databank_workshop = pd.concat([databank_workshop, df])
databank_workshop = databank_workshop.set_index('ID')


## Output
st.dataframe(databank_workshop)


## Input
with st.form('Workshop', clear_on_submit = True):
  id = lastID(url = '`benbox`.`HANDBOOK_USER`')
  workshop_id = generateID(id)
  st.text_input(label = 'ID', value = id, disabled = True)
  st.text_input(label = 'Workshop ID', value = workshop_id, disabled = True)
  workshop_title = st.text_input(label = 'Title', disabled = False)
  workshop_description = st.text_input(label = 'Description', disabled = False)
  workshop_date = st.text_input(label = 'Date', disabled = False)
  workshop_duration = st.text_input(label = 'Duration', disabled = False)
  workshop_attendees = st.text_input(label = 'Attendees', disabled = False)
  
  ## Submit button
  submitted = st.form_submit_button("Ask Ben")
  if submitted:
    # Write workshop data
    id = lastID(url = '`idcard`.`WORKSHOPDATA`')
    #query = "INSERT INTO `idcard`.`WORKSHOPDATA`(ID, EMPLOYEE_NO, TRAINING, INSTITUTE, DATE, DAYS) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" %(id)
    #run_query(query)
    #conn.commit()
    
    
#### Outside the form
## QR Code generator
# Data to be encoded
data = 'https://www.benbox.org'

# Saving as an image file
#image = io.BytesIO()
 
# Encoding data using make() function
image = qrcode.make(data)

# Saving image as png in a buffer
byteIO = io.BytesIO()
image.save(byteIO, format = 'PNG')
qrcode = byteIO.getvalue()

# Showing qrcode
st.image(qrcode)
