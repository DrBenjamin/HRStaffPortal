##### `pages/1 - 📈_Statistics.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
from azure.identity import InteractiveBrowserCredential
from msgraph.core import GraphClient
from pprint import pprint
from ms_graph.client import MicrosoftGraphClient
from configparser import ConfigParser




#### Streamlit initial setup
st.set_page_config(
  page_title = "KCH HR Staff Portal",
  page_icon = "images/thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "collapsed",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the KCH HR Staff Portal. Version 0.1.1-b1"
        }
)




#### Sidebar
# Sidebar Header Image
st.sidebar.image('images/MoH.png')




#### Main program
### Statistics expander
with st.expander(label = 'Statistics', expanded = True):
  ## Title
  st.title('Statistics')
  
  
  ## Download links
  # Data comes from Helmholtz-Zentrum Potsdam
  # https://www-app3.gfz-potsdam.de/kp_index/Kp_ap_nowcast.txt
  # https://www-app3.gfz-potsdam.de/kp_index/Kp_ap_since_1932.txt
  DATA_URL = 'files/Employees.txt'
  
  
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
  if st.checkbox(str('Show raw data?')):
    st.subheader('Raw data')
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
  
  
  ## Call function to do the calculation
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
