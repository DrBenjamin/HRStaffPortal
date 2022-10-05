import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import math
from datetime import datetime
import mysql.connector
import sys

### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
## Streamlit initial setup
st.set_page_config(
  page_title = "KCH HR Staff Portal",
  page_icon = "thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the KCH HR Staff Portal. Version 0.0.1"
        }
)

## Password / User checking
def check_password():
    """Returns `True` if the user had a correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
    
    ## Header
    # Header Image
    st.sidebar.image('MoH.png')

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        # Show Header Text
        st.sidebar.title('You are welcome to the KCH HR Staff Portal')
        st.sidebar.subheader('Please enter username and password')
        st.sidebar.text_input("Username", on_change=password_entered, key="username")
        st.sidebar.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        show_title = True
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.sidebar.text_input("Username", on_change=password_entered, key="username")
        st.sidebar.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.sidebar.error("User not known or password incorrect!")
        show_title = True
        return False
    else:
        # Password correct.
        st.sidebar.subheader('You are logged in.')
        st.sidebar.write('You can close this menu.')
        show_title = False
        return True

if check_password():
    ## SQL Connection
    # Initialize connection
    def init_connection():
      return mysql.connector.connect(**st.secrets["mysql"])
    # Perform query
    def run_query(query):
      with conn.cursor() as cur:  
        cur.execute(query)
        return cur.fetchall()
    
    # Show information
    with st.expander("Header", expanded = True):
      st.title('KCH HR Staff Portal')
      st.image('MoH.png')
      st.subheader('Kamuzu Central Hospital employee data.')
      st.write('All the employee data is stored in a local MySQL databank on a Raspberry Pi.')
      st.write('The HR Portal is running on Streamlit, an Open Source Python framework for visualisation.')

    ## Use local databank idcard with Table ImageBase (EasyBadge polluted)
    # open Databak Connection
    conn = init_connection()

    # Checkbox for option to see databank data
    st.subheader('Databank data')
    query = "SELECT ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED, IMAGE FROM `idcard`.`IMAGEBASE`;"
    rows = run_query(query)
    databank = pd.DataFrame(columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED', 'IMAGE'])
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['ID', 'LAYOUT', 'FORENAME', 'SURNAME', 'JOB_TITLE', 'EXPIRY_DATE', 'EMPLOYEE_NO', 'CARDS_PRINTED', 'IMAGE'])
      databank = databank.append(df)
    
    # Print databank in dataframe table
    with st.expander("See all Databank entries", expanded = False):
      databank = databank.set_index('ID')
      st.dataframe(databank, use_container_width = True)
      
    # Combine Forename and Surname for Sidebar Selectbox
    query = "SELECT ID, FORENAME, SURNAME, EMPLOYEE_NO, JOB_TITLE FROM `idcard`.`IMAGEBASE`;"
    rows = run_query(query)
    row = [0]
    names = ['New Employee']
    for row in rows:
      # Concenate Forename and Surname for Sidebar Selectbox
      names.append(str(row[1] + ' ' + row[2] + ' ' + row[3] + ' ' + row[4]))

    # Employee Selectbox
    index = st.selectbox(label = "Which Employee do you want to select?", options = range(len(names)), format_func = lambda x: names[x])
    
    # Checkboxes for Editing and Adding
    if (index != 0):
      checkbox_val = st.checkbox(label = 'Edit Mode', value = False)
      checkbox_training = st.checkbox(label = 'Add Training', value = False, disabled = not checkbox_val)
      
    # If new Employee just show empty form
    if (index == 0):
      with st.form("new", clear_on_submit = True):
        # Check for ID number
        id = 0
        query = "SELECT ID from `idcard`.`IMAGEBASE`;"
        rows = run_query(query)
        row = [0]
        for row in rows:
          # Checking for ID
          id = int(row[0]) + 1
        id = st.text_input(label = 'ID', value = id, disabled = True)
        layout = st.text_input(label = 'Layout', value = 1)  
        forename = st.text_input(label = 'Forename', placeholder = 'Forename?')
        surname = st.text_input(label = 'Surname', placeholder = 'Surname?')
        job = st.text_input(label = 'Job', placeholder = 'Job?')
        exp = st.text_input(label = 'Layout', value = '2023-12-31 00:00:00')
        eno = st.text_input(label = 'Employee Number', placeholder = 'Employee Number?')
        capri = st.text_input(label = 'Cards Printed', value = 0)
        st.image('portrait-placeholder.png')
        uploaded_file = st.file_uploader("Upload a picture (256×360)")
        image = 'DATA'
        if uploaded_file is not None:
          image = bytes_data = uploaded_file.getvalue()
        
        submitted = st.form_submit_button("Create New Employee")
        if submitted:
          # Writing to databank
          query = "INSERT INTO `idcard`.`IMAGEBASE`(ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED, IMAGE) VALUES (%s, %s, '%s', '%s', '%s', '%s', %s, %s, '%s');" %(id, layout, forename, surname, job, exp, eno, capri, image)
          run_query(query)
          conn.commit()
          st.experimental_rerun()
    else:
      with st.form("edit", clear_on_submit = True):
        # Get information of selected Employee
        query = "SELECT ID, LAYOUT, FORENAME, SURNAME, JOB_TITLE, EXPIRY_DATE, EMPLOYEE_NO, CARDS_PRINTED, IMAGE FROM `idcard`.`IMAGEBASE` WHERE ID = %s;" %(index)
        employee = run_query(query)
        id = st.text_input(label = 'ID', value = employee[0][0], disabled = True)
        layout = st.text_input(label = 'Layout', value = employee[0][1], disabled = True)
        forename = st.text_input(label = 'Forename', value = employee[0][2], disabled = not checkbox_val)
        surname = st.text_input(label = 'Surname', value = employee[0][3], disabled = not checkbox_val)
        job = st.text_input(label = 'Job', value = employee[0][4], disabled = not checkbox_val)
        exp = st.text_input(label = 'Expirity Date', value = employee[0][5], disabled = not checkbox_val)
        eno = st.text_input(label = 'Employee Number', value = employee[0][6], disabled = not checkbox_val)
        capri = st.text_input(label = 'Cards Printed', value = employee[0][7], disabled = not checkbox_val)
        st.image('portrait-placeholder.png')
        uploaded_file = st.file_uploader("Upload a picture (256×360)")
        image = 'DATA'
        if uploaded_file is not None:
          image = bytes_data = uploaded_file.getvalue()
        
        with st.expander("Training Data", expanded = False):
          ## Get information of selected Employee regarding Training
          # Check for last ID number in TrainingData (to add data after)
          idT = 0
          query = "SELECT ID from `idcard`.`TrainingData`;"
          rows = run_query(query)
          row = [0]
          for row in rows:
            idT = int(row[0]) + 1
          # Get Training Data
          query = "SELECT tr.TRAINING, tr.INSTITUTE, tr.DATE, tr.DAYS FROM `idcard`.`ImageBase` AS ima LEFT JOIN `idcard`.`TrainingData` AS tr ON ima.EMPLOYEE_NO = tr.EMPLOYEE_NO WHERE ima.ID = %s;" %(index)
          trainingData = run_query(query)
          
          # Variables for Text Input
          training = []
          institute = []
          date = []
          days = []
          
          # Boolean for flow control
          insert = False
          update = False
          insertnew = False
          
          # Check if Training Data is already there for an Employee
          if (trainingData[0][0] != None):
            update = True
            for i in range(len(trainingData)):
              x = st.text_input(label = 'Training #' + str(i + 1), value = trainingData[i][0], key = 'training' + str(i), disabled = not checkbox_val)
              training.append(x)
              x = st.text_input(label = 'Institute', value = trainingData[i][1], key = 'institute' + str(i), disabled = not checkbox_val)
              institute.append(x)
              x = st.text_input(label = 'Date', value = trainingData[i][2], key = 'date' + str(i), disabled = not checkbox_val)
              date.append(x)
              x = st.text_input(label = 'Days', value = trainingData[i][3], key = 'days' + str(i), disabled = not checkbox_val)
              days.append(x)
          else:
            if checkbox_training:
              insert = True
              x = st.text_input(label = 'Training #1', placeholder = 'Training?', disabled = not checkbox_val)
              training.append(x)
              x = st.text_input(label = 'Institute', placeholder = 'Institute?', disabled = not checkbox_val)
              institute.append(x)
              x = st.text_input(label = 'Date', placeholder = 'Date?', disabled = not checkbox_val)
              date.append(x)
              x = st.text_input(label = 'Days', placeholder = 'Days?', disabled = not checkbox_val)
              days.append(x)
            else:
              st.info('No Training Data available', icon="ℹ️")
          
        submitted = st.form_submit_button("Save Changes")
        if submitted:
          ## ImageBase
          # Writing to databank idcard Table ImageBase
          query = "UPDATE `idcard`.`ImageBase` SET LAYOUT = %s, FORENAME = '%s', SURNAME = '%s', JOB_TITLE = '%s', EXPIRY_DATE = '%s', EMPLOYEE_NO = '%s', CARDS_PRINTED = %s, IMAGE = '%s' WHERE ID = '%s';" %(layout, forename, surname, job, exp, eno, capri, image, index)
          run_query(query)
          conn.commit()
          
          ## TrainingData
          # Writing to databank idcard Table TrainingData - new first Entry
          if (insert == True):
            if (training[0].strip() and institute[0].strip() and date[0].strip() and days[0].strip()):
              query = "INSERT INTO `idcard`.`TrainingData`(ID, EMPLOYEE_NO, TRAINING, INSTITUTE, DATE, DAYS) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" %(idT, eno, training[0], institute[0], date[0], days[0])
              run_query(query)
              conn.commit()
            else:
              st.warning('Not sumitted as Data is missing', icon="⚠️")
          # Writing to databank idcard Table TrainingData - new Entries (not first)
          if (insertnew == True):
            if (training[len(trainingData)].strip() and institute[len(trainingData)].strip() and date[len(trainingData)].strip() and days[len(trainingData)].strip()):
              query = "INSERT INTO `idcard`.`TrainingData`(ID, EMPLOYEE_NO, TRAINING, INSTITUTE, DATE, DAYS) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" %(idT, eno, training[len(trainingData)], institute[len(trainingData)], date[len(trainingData)], days[len(trainingData)])
              run_query(query)
              conn.commit()
            else:
              st.warning('Not sumitted as Data is missing', icon="⚠️")
          # Writing to databank idcard Table TrainingData - Updates to all existing entries
          if (update == True):
            for i in range(len(trainingData)):
              query = "UPDATE `idcard`.`TrainingData` SET TRAINING = '%s', INSTITUTE = '%s', DATE = '%s', DAYS = '%s' WHERE ID = %s;" %(training[i], institute[i], date[i], days[i], i + 1)
              run_query(query)
              conn.commit()
          #st.experimental_rerun()
  
else :
  ## Landing Page
  st.title('Kamuzu Central Hospital (KCH) HR Staff Portal Landing Page')

  ## Download links
  # Data comes from Helmholtz-Zentrum Potsdam
  # https://www-app3.gfz-potsdam.de/kp_index/Kp_ap_nowcast.txt
  # https://www-app3.gfz-potsdam.de/kp_index/Kp_ap_since_1932.txt
  DATA_URL = './Employees.txt'

  ## Load data function
  # Function is cached
  @st.cache
  def load_data():
    colnames = ['Year', 'Month', 'Day', 'Hour', 'Hour_m', 'Days', 'Days_m', 'Kp', 'Employees', 'D']
    data = pd.read_table(DATA_URL, sep = " ", header = None, names = colnames, skiprows = 31, skipinitialspace = True)
    return data
  # Show loading message
  #data_load_state = st.text('Loading data...')
  data = load_data()
  #data_load_state.text(str('Download completed') + ' (' + str(round(sys.getsizeof(data)/1048576, 2)) + 'MB)!')

  ## Checkbox for option to see raw data
  #if st.checkbox(str('Show raw data?')):
  #  st.subheader('Raw data')
  #  st.write(data)
  
  ## Create data frames
  data_plot_today = pd.DataFrame({'Time': data.Hour.astype(int), 'Employees': data.Employees}).tail(8)
  data_cal = pd.DataFrame({'Date': pd.to_datetime(data.Year.map(str) + "-" + data.Month.map(str) + "-" + data.Day.map(str)), 'Employees': data.Employees})

  ## Calculation of avg ap per day and top 10 max values
  # Function is cached
  @st.cache(allow_output_mutation = True)
  def calc_top10(date, ap):
    avg_ap_d = []
    avg_ap_d_t = []
    max_ap = [ [0, ''], [0, ''], [0, ''], [0, ''], [0, ''], [0, ''], [0, ''], [0, ''], [0, ''], [0, ''] ]
    test_str = ""
    x = 0
    for i in range(1, len(ap)): 
      if date[i] == test_str or i == 1:
        x = x + ap[i]
        test_str = date[i]
      else :
        x = x / 8
        avg_ap_d_t.append(str(test_str))
        avg_ap_d.append(int(np.ceil(x)))
        for y in range(0, 10, 1) :
          # Creating top 10 list
          if x > max_ap[y][0] :
            max_ap[y][0] = int(np.ceil(x))
            max_ap[y][1] = str(test_str)[0:10]
            list.sort(max_ap, reverse = False)
            break
        x = ap[i]
        test_str = date[i]
    return avg_ap_d, avg_ap_d_t, max_ap
  # Call function to do the calculation
  avg_ap_d, avg_ap_d_t, max_ap = calc_top10(date = data_cal['Date'], ap = data_cal['Employees'])
  # Create dataframe with avg ap per day values
  data_plot = pd.DataFrame({'Date': pd.to_datetime(avg_ap_d_t),
                            'Employees': avg_ap_d})

  ## Plotting
  # Set indexes (x-axis) to 'Time' and 'Date' column
  data_plot_today = data_plot_today.set_index('Time')
  data_plot = data_plot.set_index('Date')
  # Daily activity
  st. subheader('Diagram of today`s employee activity')
  st.bar_chart(data_plot_today)
  # All data plot
  st.subheader('Diagram of employee activity last 30 days')
  st.line_chart(data_plot)

  ## Show 10 lowest employee days
  # Reverse 'False' -> order with lowest first
  list.sort(max_ap, reverse = False)
  # Create data frame
  max_ap_data = pd.DataFrame()
  max_ap_data['Date'] = [sublist[1] for sublist in max_ap]
  max_ap_data['Employees'] = [sublist[0] for sublist in max_ap]
  max_ap_data_index = pd.Index(range(1, 11, 1))
  max_ap_data = max_ap_data.set_index(max_ap_data_index)
  # Show Lowest 10
  st.write('The minimum of the daily employee activity was on ', str(max_ap[0][1]), ' at ', str(max_ap[0][0]), 'employees')
  if st.checkbox('Show minimum days?'):
    st.subheader('Days with the lowest number of staff')
    st.write(max_ap_data)  
