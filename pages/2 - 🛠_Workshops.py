##### `pages/2 - 🛠_Workshops.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import mysql.connector
import io 
import sys
from array import array
sys.path.insert(1, "pages/functions/")
from functions import generateID
from functions import generate_qrcode
from network import send_mail
from network import get_ip




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




#### Query parameters
## Get query params
html_query = st.experimental_get_query_params()




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


## Open databank connection
conn = init_connection()


## Get workshop data
# Run query 
query = "SELECT ID, WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES, WORKSHOP_ATTENDEES_CONFIRMED FROM idcard.WORKSHOP;"
rows = run_query(query)
    
# Creating pandas dataframe
databank_workshop = pd.DataFrame(columns = ['ID', 'WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_FACILITATOR', 'WORKSHOP_DATE', 'WORKSHOP_DURATION', 'WORKSHOP_ATTENDEES', 'WORKSHOP_ATTENDEES_CONFIRMED'])
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['ID', 'WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_FACILITATOR', 'WORKSHOP_DATE', 'WORKSHOP_DURATION', 'WORKSHOP_ATTENDEES', 'WORKSHOP_ATTENDEES_CONFIRMED'])
  databank_workshop = pd.concat([databank_workshop, df])
databank_workshop = databank_workshop.set_index('ID')



### Existing workshop
if len(html_query) > 0:
  ## Get specific workshop data
  # Run query 
  query = "SELECT ID, WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES, WORKSHOP_ATTENDEES_CONFIRMED FROM idcard.WORKSHOP WHERE workshop_id = '%s';" %(html_query['workshop'][0])
  workshop = run_query(query)

  # Disabled selectbox
  option = str(workshop[0][2] + ' (' + html_query['workshop'][0] + ')')
  st.selectbox(label = "Which workshop do you want to select?", options = [option], index = 0, disabled = True)
  
  ## Output
  st.header('Workshop')
  st.write('**Title:** ', workshop[0][2])
  st.write('**Description:** ', workshop[0][3])
  st.write('**Facilitator:** ', workshop[0][4])
  st.write('**Date:** ', str(workshop[0][5]))
  st.write('**Duration:** ', str(workshop[0][6]))
  st.write('**Not confirmed:** ', workshop[0][7])
  st.write('**Confirmed:** ', workshop[0][8])
  
  not_confirmed = workshop[0][7].split(' ')
  st.write(not_confirmed)

### New workshop form
else:
  ## Workshop selectbox
  workshop_title = [str(title) + ' (' for title in list(databank_workshop['WORKSHOP_TITLE'])]
  workshop_id = [str(id) + ')' for id in list(databank_workshop['WORKSHOP_ID'])]
  workshops = [i + j for i, j in zip(workshop_title, workshop_id)]
  workshops.insert(0, 'None')
  index = st.selectbox(label = "Which workshop do you want to select?", options = range(len(workshops)), format_func = lambda x: workshops[x])
  
  
  ## Show specific workshop
  if index > 0:
    ## Get workshop data
    # Run query 
    query = "SELECT ID, WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES, WORKSHOP_ATTENDEES_CONFIRMED FROM idcard.WORKSHOP WHERE workshop_id = '%s';" %(databank_workshop['WORKSHOP_ID'][index])
    workshop = run_query(query)

  
    ## Output
    st.header('Workshop')
    st.write('**Title:** ', workshop[0][2])
    st.write('**Description:** ', workshop[0][3])
    st.write('**Facilitator:** ', workshop[0][4])
    st.write('**Date:** ', str(workshop[0][5]))
    st.write('**Duration:** ', str(workshop[0][6]))
    st.write('**Not confirmed:** ', workshop[0][7])
    st.write('**Confirmed:** ', workshop[0][8])
  
  
  ## Show all workshops
  else:
    st.dataframe(databank_workshop)
  
  
    ## Input form expander
    with st.expander(label = 'Workshop entry', expanded = False):
      ## Input form
      with st.form('Workshop', clear_on_submit = True):
        st.header('New workshop entry')
        st.write('Here you can enter a new workshop.')
        
        
        ## Workshop data entry
        id = lastID(url = '`idcard`.`WORKSHOP`')
        workshop_id = generateID(id)
        st.text_input(label = 'ID', value = id, disabled = True)
        st.text_input(label = 'Workshop ID', value = workshop_id, disabled = True)
        workshop_title = st.text_input(label = 'Title', disabled = False)
        workshop_description = st.text_input(label = 'Description', disabled = False)
        workshop_facilitator = st.text_input(label = 'Facilitator', disabled = False)
        workshop_date = st.text_input(label = 'Date', disabled = False)
        workshop_duration = st.text_input(label = 'Duration', disabled = False)
        
        
        ## Get employee data for filling the employee multiselect
        query = "SELECT ima.ID, ima.FORENAME, ima.SURNAME, ima.EMPLOYEE_NO, ima.JOB_TITLE, emp.EMPLOYEE_EMAIL FROM `idcard`.`IMAGEBASE` As ima LEFT JOIN `idcard`.`EMPLOYEE` AS emp ON emp.EMPLOYEE_NO = ima.EMPLOYEE_NO;"
        rows = run_query(query)
        
        # Building employees for  multiselect
        row = []
        names = []
        for row in rows:
          # Concenate employee data 
          names.append(str(row[1] + ' ' + row[2] + ', ' + row[3] + ', ' + row[4] + ' (' + row[5] + ')'))
          
        # Multiselect to choose employees for workshop
        options = st.multiselect(label = 'Which Employee(s) do you want to select?', options = names)
        
        # Extract mail addresses
        mail_addresses = [option.split('(', 1)[1][:-1] for option in options]
        
        # Extract employee numbers
        employee_no = [option.split(', ', 1)[1] for option in options]
        employees = [employee_n.split(', ', 1)[0] for employee_n in employee_no]
        
        
        ## Submit button
        submitted = st.form_submit_button(label = 'Submit')
        if submitted:
          ## Write workshop data
          id = lastID(url = '`idcard`.`WORKSHOP`')
          workshop_id = generateID(id)
          query = "INSERT INTO `idcard`.`WORKSHOP`(ID, WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(id, workshop_id, workshop_title, workshop_description, workshop_facilitator, workshop_date, workshop_duration, ' '.join(employees))
          run_query(query)
          conn.commit()
      
      
          ## Send mail to attendees
          i = 0
          for mail in mail_addresses:
            send_mail(subject = 'Invitation to workshop ' + workshop_title, body = 'Hello colleagues,\n\nthis is an invitation to the workshop ' + workshop_title + ' on ' + workshop_date + ' (' + workshop_duration + ' days).\n\nDetails: ' + workshop_description + '\n\nBest regards\n\n' + workshop_facilitator + '\n\n', receiver = mail, attachment = generate_qrcode(data = str('http://' + get_ip() + ':8501/Workshops?workshop=' + workshop_id + '&eno=' + employees[i])))
            i += 1
        
        

    
#### Outside the form

