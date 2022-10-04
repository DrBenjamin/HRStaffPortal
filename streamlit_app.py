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
    st.title('KCH HR Staff Portal')
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
    if (index != 0):
      checkbox_val = st.checkbox(label = 'Edit Employee', value = False)
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
        id = st.text_input(label = 'ID', value = id, key = 'id_input', disabled = True)
        layout = st.text_input(label = 'Layout', value = 1, key = 'layout_input')  
        forename = st.text_input(label = 'Forename', placeholder = 'Forename?', key = 'forename_input')
        surname = st.text_input(label = 'Surname', placeholder = 'Surname?', key = 'surname_input')
        job = st.text_input(label = 'Job', placeholder = 'Job?', key = 'job_input')
        exp = '2023-12-31 00:00:00'
        eno = st.text_input(label = 'Employee Number', placeholder = 'Employee Number?', key = 'eno_input')
        capri = st.text_input(label = 'Cards Printed', value = 0, key = 'capri_input')
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
        id = st.text_input(label = 'ID', value = employee[0][0], key = 'id_input', disabled = True)
        layout = st.text_input(label = 'Layout', value = employee[0][1], key = 'layout_input', disabled = True)
        forename = st.text_input(label = 'Forename', value = employee[0][2], key = 'forename_input', disabled = not checkbox_val)
        surname = st.text_input(label = 'Surname', value = employee[0][3], key = 'surname_input', disabled = not checkbox_val)
        job = st.text_input('Job', value = employee[0][4], key = 'job_input', disabled = not checkbox_val)
        exp = st.text_input(label = 'Expirity Date', value = employee[0][5], key = 'expdate_input', disabled = not checkbox_val)
        eno = st.text_input(label = 'Employee Number', value = employee[0][6], key = 'eno_input', disabled = not checkbox_val)
        capri = st.text_input(label = 'Cards Printed', value = employee[0][7], key = 'capri_input', disabled = not checkbox_val)
        uploaded_file = st.file_uploader("Upload a picture (256×360)")
        image = 'DATA'
        if uploaded_file is not None:
          image = bytes_data = uploaded_file.getvalue()
          
        submitted = st.form_submit_button("Save Changes")
        if submitted:
          # Writing to databank
          query = "  UPDATE `idcard`.`IMAGEBASE` SET LAYOUT = %s, FORENAME = '%s', SURNAME = '%s', JOB_TITLE = '%s', EXPIRY_DATE = '%s', EMPLOYEE_NO = '%s', CARDS_PRINTED = %s, IMAGE = '%s' WHERE ID = '%s';" %(layout, forename, surname, job, exp, eno, capri, image, index)
          run_query(query)
          conn.commit()
          st.experimental_rerun()
      
    # Print databank in dataframe table
    if st.checkbox('Show full databank data?', value = False):
      databank = databank.set_index('ID')
      st.table(databank)
  
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
    for i in range(1, len(ap)) : 
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
