import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import math
from datetime import datetime
import mysql.connector
import deepl
import sys

### KCH HR Staff Portal Prototype
## Streamlit initial setup
st.set_page_config(
  page_title = "KCH HR Staff Portal",
  page_icon = "thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "collapsed",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the KCH HR Staff Portal. Version 0.0.1a"
        }
)

## Password check
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

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("User not known or password incorrect!")
        return False
    else:
        # Password correct.
        return True

if check_password():
    ## DeepL Translating
    # Ask for language
    lang = st.sidebar.selectbox('In which language should this site appear?', ('BG', 'CS', 'DA', 'DE', 'EL', 'EN-GB', 'ES', 'ET', 'FI', 'FR', 'HU', 'IT', 'JA', 'LT', 'LV', 'NL', 'PL', 'PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'ZH'), index = 5, key = 'lang')
    # All text stuff
    title = 'KCH HR Staff Portal'
    subheader = 'Kamuzu Central Hospital employee data.'
    info1 = 'All the employee data is stored in a local MySQL databank on a Raspberry Pi.'
    info2 = 'The HR Portal is running on Streamlit, an Open Source Python framework for visualisation.'
    data_load_text = 'Loading data...'
    data_down_text = 'Download completed'
    check1 = 'Show raw data?'
    check1sub = 'Raw data'
    plot1_subheader = 'Diagram of today`s employee activity'
    plot2_subheader = 'Diagram of employee activity last 30 days'
    info_maxap = 'The maximum of the daily employee activity was on '
    info_maxapat = 'at'
    check_maxap = 'Show maximum days?'
    check_maxapsubheader = 'Top 10'
    use_databank = 'Use local databank?'
    day_event = 'On which day was the event?'
    text_input = 'What happened on this day?'
    text_output = 'You selected'
    text_placeholder = 'All kinds of events'
    stored_data = 'Store in databank?'
    stored_datasuccess = 'stored to databank!'
    show_data = 'Show databank data?'
    show_datasubheader = 'Databank data'
    # Just do the translation once (if language option was not changing) trough caching
    @st.cache(allow_output_mutation = True, suppress_st_warning = True, hash_funcs={'_thread.RLock': hash, 'builtins.weakref': hash})
    def translate(x, en_title, en_subheader, en_info1, en_info2, en_data_load_text, en_data_down_text, en_check1, en_check1sub, en_plot1_subheader, en_plot2_subheader, en_info_maxap, en_info_maxapat, en_check_maxap, en_check_maxapsubheader, en_use_databank, en_day_event, en_text_input, en_text_output, en_text_placeholder, en_stored_data, en_stored_datasuccess, en_show_data, en_show_datasubheader):
      if x != 'EN-GB' :
        en_title = trans(en_title, x)
        en_subheader = trans(en_subheader, x)
        en_info1 = trans(en_info1, x)
        en_info2 = trans(en_info2, x)
        en_data_load_text = trans(en_data_load_text, x)
        en_data_down_text = trans(en_data_down_text, x)
        en_check1 = trans(en_check1, x)
        en_check1sub = trans(en_check1sub, x)
        en_plot1_subheader = trans(en_plot1_subheader, x)
        en_plot2_subheader = trans(en_plot2_subheader, x)
        en_info_maxap = trans(en_info_maxap, x)
        en_info_maxapat = trans(en_info_maxapat, x)
        en_check_maxap = trans(en_check_maxap, x)
        en_check_maxapsubheader = trans(en_check_maxapsubheader, x)
        en_use_databank = trans(en_use_databank, x)
        en_day_event = trans(en_day_event, x)
        en_text_input = trans(en_text_input, x)
        en_text_output = trans(en_text_output, x)
        en_text_placeholder = trans(en_text_placeholder, x)
        en_stored_data = trans(en_stored_data, x)
        en_stored_datasuccess = trans(en_stored_datasuccess, x)
        en_show_data = trans(en_show_data, x)
        en_show_datasubheader = trans(en_show_datasubheader, x)
      return en_title, en_subheader, en_info1, en_info2, en_data_load_text, en_data_down_text, en_check1, en_check1sub, en_plot1_subheader, en_plot2_subheader, en_info_maxap, en_info_maxapat, en_check_maxap, en_check_maxapsubheader, en_use_databank, en_day_event, en_text_input, en_text_output, en_text_placeholder, en_stored_data, en_stored_datasuccess, en_show_data, en_show_datasubheader
    # DeepL function
    def trans(x, y):
      translator = deepl.Translator(st.secrets["deepl"]["key"])
      result = translator.translate_text(x, target_lang = y) 
      return result
    
    ## Sidebar configuration
    # 
    contact = st.sidebar.selectbox(
      "How would you like to be contacted?",
      ("Email", "Fixed Line", "Mobile Phone")
    )

    ## SQL Connection
    # Initialize connection
    def init_connection():
      return mysql.connector.connect(**st.secrets["mysql"])
    # Perform query
    def run_query(query):
      with conn.cursor() as cur:  
        cur.execute(query)
        return cur.fetchall()

    ## Title and some information
    # Do the translating
    if lang != 'EN-GB':
      title, subheader, info1, info2, data_load_text, data_down_text, check1, check1sub, plot1_subheader, plot2_subheader, info_maxap, info_maxapat, check_maxap, check_maxapsubheader, use_databank, day_event, text_input, text_output, text_placeholder, stored_data, stored_datasuccess, show_data, show_datasubheader = translate(lang, title, subheader, info1, info2, data_load_text, data_down_text, check1, check1sub, plot1_subheader, plot2_subheader, info_maxap, info_maxapat, check_maxap, check_maxapsubheader, use_databank, day_event, text_input, text_output, text_placeholder, stored_data, stored_datasuccess, show_data, show_datasubheader)
    # Show information
    st.title(title)
    st.subheader(subheader)
    st.write(str(info1))
    st.write(str(info2))

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
    data_load_state = st.text(data_load_text)
    data = load_data()
    data_load_state.text(str(data_down_text) + ' (' + str(round(sys.getsizeof(data)/1048576, 2)) + 'MB)!')

    ## Checkbox for option to see raw data
    if st.checkbox(str(check1)):
      st.subheader(check1sub)
      st.write(data)
  
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
    st. subheader(plot1_subheader)
    st.bar_chart(data_plot_today)
    # All data plot
    st.subheader(plot2_subheader)
    st.line_chart(data_plot)

    ## Show 10 maximum ap days
    # Reverse order (highest first)
    list.sort(max_ap, reverse = True)
    # Create data frame
    max_ap_data = pd.DataFrame()
    max_ap_data['Date'] = [sublist[1] for sublist in max_ap]
    max_ap_data['ap'] = [sublist[0] for sublist in max_ap]
    max_ap_data_index = pd.Index(range(1, 11, 1))
    max_ap_data = max_ap_data.set_index(max_ap_data_index)
    # Show Top 10
    st.write(str(info_maxap), str(max_ap[0][1]), ' ', str(info_maxapat), ' ', str(max_ap[0][0]), '.')
    if st.checkbox(str(check_maxap)):
      st.subheader(check_maxapsubheader)
      st.write(max_ap_data)
  
    ## Use local databank
    if st.checkbox(str(use_databank)):
      conn = init_connection()
      # Ask for events
      date = st.selectbox(str(day_event), max_ap_data, key = 'date')
      st.write(str(text_output), date)
      event = st.text_input(str(text_input), placeholder = text_placeholder, key = 'event')
      # Write data to databank
      if st.button(str(stored_data)):
      # Check for ID number
        id = 0
        query = "SELECT ID from `dbs5069306`.`topten`;"
        rows = run_query(query)
        row = [0]
        for row in rows:
          # Checking for ID
          print(row[0])
          id = int(row[0]) + 1
        # Writing to databank
        query = "INSERT INTO `dbs5069306`.`topten` VALUES ('%s', '%s', '%s');" %(id, date, event)
        run_query(query)
        conn.commit()
        st.write(date, event, ' ', stored_datasuccess)
      # Checkbox for option to see databank data
      if st.checkbox(str(show_data)):
        st.subheader(show_datasubheader)
        query = "SELECT * from `dbs5069306`.`topten`;"
        rows = run_query(query)
        databank = pd.DataFrame(columns = ['ID', 'Date', 'Event'])
        for row in rows:
          df = pd.DataFrame([[row[0], row[1], row[2]]], columns = ['ID', 'Date', 'Event'])
          databank = databank.append(df)
        # Print databank in dataframe table
        databank = databank.set_index('ID')
        st.table(databank)
