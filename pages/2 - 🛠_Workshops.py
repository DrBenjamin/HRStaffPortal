##### `2 - 🛠_Workshops.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions



#### Loading neded Python libraries
import streamlit as st
import streamlit.components.v1 as stc
from shillelagh.adapters.registry import registry
from shillelagh.adapters.file.csvfile import CSVFile
from shillelagh.backends.apsw.db import connect


#### Functions
## Perform query
def run_query(query):
  sql = cursor.execute(query)
  return sql
  
  

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


### Header
## Title
st.title('Workshop Page')

## Shillelagh
connection = connect(":memory:", adapters = 'csvfile')
cursor = connection.cursor()

# Execute query
query = "SELECT * FROM 'test.csv';"
#csvData = cursor.execute(query)
csvData = run_query(query)
st.dataframe(csvData, use_container_width = True)


### Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')





