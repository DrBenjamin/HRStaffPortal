##### `pages/1 - 📈_Statistics.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import sys
import mysql.connector
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
sys.path.insert(1, "pages/functions/")
from functions import header
from functions import check_password
from functions import logout
from functions import landing_page




#### Streamlit initial setup
st.set_page_config(
  page_title = "KCH HR Staff Portal",
  page_icon = "images/thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the KCH HR Staff Portal. Version 0.1.1-b1"
        }
)




#### Initialization of session states
## Session states
if ('admin' not in st.session_state):
  st.session_state['admin'] = False
if ('header' not in st.session_state):
  st.session_state['header'] = True
  



#### Functions
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
  



#### Main program
### Logged in state (Statistics)
if check_password():
  ### Header
  header(title = 'Statistics page', data_desc = 'employee statistic data', expanded = st.session_state['header'])
  
  
  
  ### Statistics expander  
  with st.expander(label = 'Statistics', expanded = True):
    ## Open databank connection
    conn = init_connection()


    ## Getting employee data
    query = "SELECT ima.ID, emp.EMPLOYEE_GENDER, emp.EMPLOYEE_BIRTHDAY, ima.JOB_TITLE, emp.EMPLOYEE_NATIONALITY, emp.EMPLOYEE_MARRIAGE_STATUS FROM `idcard`.`IMAGEBASE` As ima LEFT JOIN `idcard`.`EMPLOYEE` AS emp ON emp.EMPLOYEE_NO = ima.EMPLOYEE_NO;"
    rows = run_query(query)
    databank_employee = pd.DataFrame(columns = ['ID', 'GENDER', 'BIRTHDAY', 'JOB', 'NATIONALITY', 'MARRIAGE'])
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5]]], columns = ['ID', 'GENDER', 'BIRTHDAY', 'JOB', 'NATIONALITY', 'MARRIAGE'])
      databank_employee = pd.concat([databank_employee, df])
    databank_employee = databank_employee.set_index('ID')
    
    
    ## Gender data
    st.subheader('Gender statistics')
    gender = []
    counter = []
    for sex in databank_employee['GENDER']:
      not_new = False
      i = 0
      for gen in gender:
        if sex == gen:
          not_new = True
          counter[i] += 1
        i += 1
      if not_new == False:
        if sex == None:
          gender.append('Unknown')
          counter.append(1)
        else:
          gender.append(sex)
          counter.append(1)
    gender_data = pd.DataFrame(columns = ['Gender', 'Number'])
    for i in range(len(gender)):
      df = pd.DataFrame([[gender[i], counter[i]]], columns = ['Gender', 'Number'])
      gender_data = pd.concat([gender_data, df])
    gender_data = gender_data.set_index('Gender')
    st.bar_chart(gender_data, x = gender)
    
  
    ## Job data
    st.subheader('Job statistics')
    jobs = []
    counter = []
    for job in databank_employee['JOB']:
      not_new = False
      i = 0
      for j in jobs:
        if j == job:
          not_new = True
          counter[i] += 1
        i += 1
      if not_new == False:
        if job == None:
          jobs.append('Unknown')
          counter.append(1)
        else:
          jobs.append(job)
          counter.append(1)
    job_data = pd.DataFrame(columns = ['Job', 'Number'])
    for i in range(len(jobs)):
      df = pd.DataFrame([[jobs[i], counter[i]]], columns = ['Job', 'Number'])
      job_data = pd.concat([job_data, df])
    job_data = job_data.set_index('Job')
    st.bar_chart(job_data, x = jobs)
    
    
    ## Nationality data
    st.subheader('Nationality statistics')
    nationality = []
    counter = []
    for nation in databank_employee['NATIONALITY']:
      not_new = False
      i = 0
      for n in nationality:
        if n == nation:
          not_new = True
          counter[i] += 1
        i += 1
      if not_new == False:
        if nation == None:
          nationality.append('Unknown')
          counter.append(1)
        else:
          nationality.append(nation)
          counter.append(1)
    nationality_data = pd.DataFrame(columns = ['Nationality', 'Number'])
    for i in range(len(nationality)):
      df = pd.DataFrame([[nationality[i], counter[i]]], columns = ['Nationality', 'Number'])
      nationality_data = pd.concat([nationality_data, df])
    nationality_data = nationality_data.set_index('Nationality')
    st.bar_chart(nationality_data, x = nationality)


    ## Marriage data
    st.subheader('Marriage data')
    marriage = []
    counter = []
    for married in databank_employee['MARRIAGE']:
      not_new = False
      i = 0
      for n in marriage:
        if n == married:
          not_new = True
          counter[i] += 1
        i += 1
      if not_new == False:
        if married == None:
          marriage.append('Unknown')
          counter.append(1)
        else:
          marriage.append(married)
          counter.append(1)
    marriage_data = pd.DataFrame(columns = ['Marriage', 'Number'])
    for i in range(len(marriage)):
      df = pd.DataFrame([[marriage[i], counter[i]]], columns = ['Marriage', 'Number'])
      marriage_data = pd.concat([marriage_data, df])
    marriage_data = marriage_data.set_index('Marriage')
    st.bar_chart(marriage_data, x = marriage)
 
    
    ## Age data
    st.subheader('Age data')
    age = []
    counter = []
    twenty_yrs_ago = date.today() - relativedelta(years = 20)
    thirty_yrs_ago = date.today() - relativedelta(years = 30)
    fourty_yrs_ago = date.today() - relativedelta(years = 40)
    fifty_yrs_ago = date.today() - relativedelta(years = 50)
    sisty_yrs_ago = date.today() - relativedelta(years = 60)
    for old in databank_employee['BIRTHDAY']:
      if old != None:
        if old < sisty_yrs_ago:
          old_cat = '+60y'
        elif old < fifty_yrs_ago:
          old_cat = '50-60y'
        elif old < fourty_yrs_ago:
          old_cat = '40-50y'
        elif old < thirty_yrs_ago:
          old_cat = '30-40y'
        elif old < twenty_yrs_ago:
          old_cat = '20-30y'
        else:
          old_cat = '<20y'
      else:
        old_cat = 'Unknown'
      not_new = False
      i = 0
      for a in age:
        if a == old_cat:
          not_new = True
          counter[i] += 1
        i += 1
      if not_new == False:
        if old == None:
          age.append('Unknown')
          counter.append(1)
        else:
          age.append(old_cat)
          counter.append(1)
    age_data = pd.DataFrame(columns = ['Age', 'Number'])
    for i in range(len(age)):
      df = pd.DataFrame([[age[i], counter[i]]], columns = ['Age', 'Number'])
      age_data = pd.concat([age_data, df])
    age_data = age_data.set_index('Age')
    st.bar_chart(age_data, x = age)


    
### Not Logged in state (Statistics)
else:
  landing_page('Statistics page.')
