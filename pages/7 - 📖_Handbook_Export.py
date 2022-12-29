##### `pages/7 - 📖_Handbook_Export.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import mysql.connector
import sys
sys.path.insert(1, "pages/functions/")
from functions import loadFile
from functions import export_docx




#### Streamlit initial setup
st.set_page_config(
  page_title = "HR Staff Portal",
  page_icon = "images/thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the HR Staff Portal Version 0.2.0"
        }
)




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


  

#### Sidebar
### Handbook Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')




#### Main Program
### Header
## Header
st.title('Handbook Export')
st.subheader('User Handbook Export')



### Handbook
## Open databank connection
conn = init_connection()


## Docx export
if st.button(label = 'Export docx'):
  ## Get handbook data to export from table `HANDBOOK_USER`
  query = "SELECT ID, HANDBOOK_ID, CATEGORY_ID, CATEGORY_SUB_ID, HANDBOOK_KEYWORD1, HANDBOOK_KEYWORD2, HANDBOOK_KEYWORD3, HANDBOOK_KEYWORD4, HANDBOOK_KEYWORD5, HANDBOOK_SUMMARY, HANDBOOK_TEXT, HANDBOOK_HITS FROM benbox.HANDBOOK_USER;"
  rows = run_query(query)
  databank_handbook = pd.DataFrame(columns = ['ID', 'HANDBOOK_ID', 'CATEGORY_ID', 'CATEGORY_SUB_ID', 'HANDBOOK_KEYWORD1', 'HANDBOOK_KEYWORD2', 'HANDBOOK_KEYWORD3', 'HANDBOOK_KEYWORD4', 'HANDBOOK_KEYWORD5', 'HANDBOOK_SUMMARY', 'HANDBOOK_TEXT', 'HANDBOOK_HITS'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]]], columns = ['ID', 'HANDBOOK_ID', 'CATEGORY_ID', 'CATEGORY_SUB_ID', 'HANDBOOK_KEYWORD1', 'HANDBOOK_KEYWORD2', 'HANDBOOK_KEYWORD3', 'HANDBOOK_KEYWORD4', 'HANDBOOK_KEYWORD5', 'HANDBOOK_SUMMARY', 'HANDBOOK_TEXT', 'HANDBOOK_HITS'])
    databank_handbook = pd.concat([databank_handbook, df])
  databank_handbook = databank_handbook.set_index('ID')
  
  
  ## Export docx file
  export_docx(data = databank_handbook, docx_file_name = 'Handbook.docx')
