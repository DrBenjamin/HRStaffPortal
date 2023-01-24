##### `pages/2 - 🛠_Workshops.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import mysql.connector
import io
import sys
sys.path.insert(1, "pages/functions/")
from functions import header
from functions import check_password
from functions import logout
from functions import landing_page
from functions import generateID
from functions import generate_qrcode
from network import send_mail
from network import get_ip




#### Streamlit initial setup
st.set_page_config(
  page_title = "Workshops",
  page_icon = st.secrets['custom']['facility_image_thumbnail'],
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': st.secrets['custom']['menu_items_help'],
         'Report a bug': st.secrets['custom']['menu_items_bug'],
         'About': st.secrets['custom']['menu_items_about']
        }
)




#### Query parameters
## Get query params
html_query = st.experimental_get_query_params()




#### Initialization of session states
## Session states
if ('admin' not in st.session_state):
  st.session_state['admin'] = False
if ('header' not in st.session_state):
  st.session_state['header'] = True
  

## QR Code
if ('qrcode' not in st.session_state):
  st.session_state['qrcode'] = False



  
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




#### Main Program
### Logged in state (Workshops page)
if check_password():
  ### Header
  header(title = 'Workshops page', data_desc = 'workshops data', expanded = st.session_state['header'])
  
  
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
  if len(html_query) > 1:
    ## Get specific workshop data
    # Run query 
    query = "SELECT ID, WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES, WORKSHOP_ATTENDEES_CONFIRMED FROM idcard.WORKSHOP WHERE workshop_id = '%s';" %(html_query['workshop'][0])
    workshop = run_query(query)
  
  
    ## Disabled selectbox
    option = str(workshop[0][2] + ' (' + html_query['workshop'][0] + ')')
    st.selectbox(label = "Which workshop do you want to select?", options = [option], index = 0, disabled = True)
    
    
    ## Form
    with st.form('Workshop', clear_on_submit = True):
      ## Output
      st.header('Workshop')
      st.write('**Title:** ', workshop[0][2])
      st.write('**Description:** ', workshop[0][3])
      st.write('**Facilitator:** ', workshop[0][4])
      st.write('**Date:** ', str(workshop[0][5]))
      st.write('**Duration:** ', str(workshop[0][6]))
    
      # Check for comfirmation status of not confirmed
      not_confirmed = workshop[0][7].split(' ')
      st.write('**Employees not confirmed:** ', ' '.join(not_confirmed))
      
      # Check for comfirmation status of confirmed
      if workshop[0][8] != None:
        confirmed = workshop[0][8]
        st.write('**Employees confirmed:** ', confirmed)
      else:
        st.write('**Employees confirmed:** ', None)
      
      # Check for not confirmed to move to confirmed 
      confirmed_bool = False
      i = 0
      for eno in not_confirmed:
        if eno == html_query['eno'][0]:
          if workshop[0][8] == None:
            confirmed = eno
          else:
            confirmed = workshop[0][8] + ' ' + eno
          
          # Delete list item
          del not_confirmed[i]
          confirmed_bool = True
          break
        i += 1
      not_confirmed = ' '.join(not_confirmed)
  
          
      ## Submit button
      submitted = st.form_submit_button(label = 'Confirm employee No \"' + html_query['eno'][0] + '\"')
      if submitted:
        ## Update workshop data
        if confirmed_bool == True:
          query = "UPDATE `idcard`.`WORKSHOP` SET WORKSHOP_ATTENDEES = '%s', WORKSHOP_ATTENDEES_CONFIRMED = '%s' WHERE WORKSHOP_ID = '%s';" %(not_confirmed, confirmed, html_query['workshop'][0])
          run_query(query)
          conn.commit()
          
          # Rerun
          st.experimental_rerun()
          
        
        ## Already confirmed or not existend
        else:
          st.error(body = 'Not possible (already confirmed or not existend)!', icon = "🚨")
    
  
  
  ### Workshop select form
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
      query = "SELECT ID, WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_FACILITATOR_EMAIL, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES, WORKSHOP_ATTENDEES_CONFIRMED FROM idcard.WORKSHOP WHERE workshop_id = '%s';" %(databank_workshop['WORKSHOP_ID'][index])
      workshop = run_query(query)
      
      
      ## Sidebar
      attendees = workshop[0][8].split(' ')
      option = st.sidebar.selectbox(label = 'Which attendee do you want to confirm?', options = attendees)
      if st.sidebar.button(label = 'Confirm \"' + option + '\"'):
        not_confirmed = ''
        for attendee in attendees:
          if attendee != option:
            not_confirmed += attendee + ' '
        if workshop[0][9] != None:
          confirmed = workshop[0][9] + ' ' + option
        else:
          confirmed = option
        
        
        ## Update workshop data
        query = "UPDATE `idcard`.`WORKSHOP` SET WORKSHOP_ATTENDEES = '%s', WORKSHOP_ATTENDEES_CONFIRMED = '%s' WHERE WORKSHOP_ID = '%s';" %(not_confirmed, confirmed, databank_workshop['WORKSHOP_ID'][index])
        run_query(query)
        conn.commit()
  
          
        # Rerun
        st.experimental_rerun()
      
      
      ## Output form
      with st.form('Workshop existend', clear_on_submit = True):
        st.header('Workshop')
        st.write('**Title:** ', workshop[0][2])
        st.write('**Description:** ', workshop[0][3])
        st.write('**Facilitator:** ', workshop[0][4])
        st.write('**Email address:** ', workshop[0][5])
        st.write('**Date:** ', str(workshop[0][6]))
        st.write('**Duration:** ', str(workshop[0][7]))
        st.write('**Employees not confirmed:** ', workshop[0][8])
        st.write('**Employees confirmed:** ', workshop[0][9])
        
        
        ## Multiselect to choose employees for workshop
        # Get employee data for filling the employee multiselect
        query = "SELECT ima.ID, ima.FORENAME, ima.SURNAME, ima.EMPLOYEE_NO, ima.JOB_TITLE, emp.EMPLOYEE_EMAIL FROM `idcard`.`IMAGEBASE` As ima LEFT JOIN `idcard`.`EMPLOYEE` AS emp ON emp.EMPLOYEE_NO = ima.EMPLOYEE_NO;"
        rows = run_query(query)
            
        # Building employees for multiselect which are not already in the list
        row = []
        names = []
        not_in_list = True
        already_in = workshop[0][8].split(' ')
        for row in rows:
          for eno in already_in:
            if row[3] == eno:
              not_in_list = False
          if not_in_list == True:
            if row[5] is None:
              names.append(str(row[1] + ' ' + row[2] + ', ' + row[3] + ', ' + row[4] + ' ('')'))
            else:
              names.append(str(row[1] + ' ' + row[2] + ', ' + row[3] + ', ' + row[4] + ' (' + row[5] + ')'))
          else:
            not_in_list = True
        options = st.multiselect(label = 'Which Employee(s) do you want to add?', options = names)
        mail_addresses = [option.split('(', 1)[1][:-1] for option in options]
        new_in = [option.split(', ', 1)[1][:6] for option in options]
        attendees = ' '.join(already_in) + ' ' + ' '.join(new_in)
    
    
        ## Submit button
        submitted = st.form_submit_button(label = 'Add attendees')
        if submitted:
          ## Update workshop data
          query = "UPDATE `idcard`.`WORKSHOP` SET WORKSHOP_ATTENDEES = '%s' WHERE WORKSHOP_ID = '%s';" %(attendees, databank_workshop['WORKSHOP_ID'][index])
          run_query(query)
          conn.commit()
        
        
          ## Send mail to new attendees
          i = 0
          for mail in mail_addresses:
            send_mail(subject = 'Invitation to workshop ' + workshop[0][2], body = 'Hello colleague,\n\nthis is an invitation to the workshop ' + workshop[0][2] + ' on ' + str(workshop[0][6]) + ' (' + str(workshop[0][7]) + ' days).\n\nDetails: ' + workshop[0][3] + '\n\nBest regards\n\n' + workshop[0][4] + '\n\n', receiver = mail)
            send_mail(subject = 'Registration to workshop ' + workshop[0][2], body = 'Hello facilitator,\n\nthis is the qrcode for the workshop ' + workshop[0][2] + ' on ' + str(workshop[0][6]) + ' (' + str(workshop[0][7]) + ' days) for the employee ' + names[i] + '.\n\nDetails: ' + workshop[0][3] + '\n\nBest regards\n\nStreamlit\n\n', receiver = workshop[0][5], attachment = generate_qrcode(data = str('https://' + get_ip() + ':8501/Workshops?workshop=' + databank_workshop['WORKSHOP_ID'][index] + '&eno=' + new_in[i])))
            i += 1
            
          # Rerun  
          st.experimental_rerun()
  
    
    
    ### Show all workshops and new workshop entry form
    else:
      ## Show existing workshops
      st.dataframe(databank_workshop)
    
    
      ## Input form
      with st.form('Workshop new', clear_on_submit = True):
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
        workshop_facilitator_email = st.text_input(label = 'Email address', disabled = False)
        workshop_date = st.text_input(label = 'Date', disabled = False)
        workshop_duration = st.text_input(label = 'Duration', disabled = False)
          
          
        ## Multiselect to choose employees for workshop
        # Get employee data for filling the employee multiselect
        query = "SELECT ima.ID, ima.FORENAME, ima.SURNAME, ima.EMPLOYEE_NO, ima.JOB_TITLE, emp.EMPLOYEE_EMAIL FROM `idcard`.`IMAGEBASE` As ima LEFT JOIN `idcard`.`EMPLOYEE` AS emp ON emp.EMPLOYEE_NO = ima.EMPLOYEE_NO;"
        rows = run_query(query)
          
        # Building employees for  multiselect
        row = []
        names = []
        
        # Concenate employee data 
        for row in rows:
          if row[5] is None:
            names.append(str(row[1] + ' ' + row[2] + ', ' + row[3] + ', ' + row[4] + ' ('')'))
          else:
            names.append(str(row[1] + ' ' + row[2] + ', ' + row[3] + ', ' + row[4] + ' (' + row[5] + ')'))
        
        # Populate options
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
          query = "INSERT INTO `idcard`.`WORKSHOP`(ID, WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_FACILITATOR_EMAIL, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(id, workshop_id, workshop_title, workshop_description, workshop_facilitator, workshop_facilitator_email, workshop_date, workshop_duration, ' '.join(employees))
          run_query(query)
          conn.commit()
        
        
          ## Send mail to attendees
          i = 0
          for mail in mail_addresses:
            send_mail(subject = 'Invitation to workshop ' + workshop_title, body = 'Hello colleague,\n\nthis is an invitation to the workshop ' + workshop_title + ' on ' + workshop_date + ' (' + workshop_duration + ' days).\n\nDetails: ' + workshop_description + '\n\nBest regards\n\n' + workshop_facilitator + '\n\n', receiver = mail)
            send_mail(subject = 'Registration to workshop ' + workshop_title, body = 'Hello facilitator,\n\nthis is the qrcode for the workshop ' + workshop_title + ' on ' + workshop_date + ' (' + workshop_duration + ' days) for the employee ' + options[i] + '.\n\nDetails: ' + workshop_description + '\n\nBest regards\n\nStreamlit\n\n', receiver = workshop_facilitator_email, attachment = generate_qrcode(data = str('https://' + get_ip() + ':8501/Workshops?workshop=' + workshop_id + '&eno=' + employees[i])))
            i += 1
        
  
        
### Logged out state (Workshops page)
else:
  ## Landing page
  landing_page('Workshops page.')
