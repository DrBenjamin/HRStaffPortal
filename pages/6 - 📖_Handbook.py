##### `pages/6 - 📖_Handbook.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import mysql.connector
import sys
sys.path.insert(1, "pages/functions/")
from functions import loadFile




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
      print("An exception occurred in function `run_query`")
      
      
      
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



### Function: generateID = Generates an 5-digits ID
def generateID(id):
  if (id < 10):
    generated_id = '0000' + str(id)
  elif (id < 100):
    generated_id = '000' + str(id)
  elif (id < 1000):
    generated_id = '00' + str(id)
  elif (id < 10000):
    generated_id = '0' + str(id)
    
  # Return the 5-digit ID
  return(generated_id)


  

#### Sidebar
### Handbook Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')




#### Main Program
### Header
## Header
st.title('Handbook')
st.subheader('User Handbook')



### Handbook
## Columns
col1, col2 = st.columns(2)


## Column 1
with col1:
  with st.form('Input', clear_on_submit = False):
    ## Handbook
    # Open databank connection
    conn = init_connection()
    
    
    ## Input for new `HANDBOOK_USER` data
    # Get latest ID from table
    id = lastID(url = '`benbox`.`HANDBOOK_USER`')
    handbook_id = generateID(id)
    st.text_input(label = 'ID', value = id, disabled = True)
    st.text_input(label = 'Handbook ID', value = handbook_id, disabled = True)
    category_id = st.text_input(label = 'Category ID', value = '00001', disabled = True)
    category_sub_id = st.text_input(label = 'Sub-Category ID', value = '00001', disabled = True)
    handbook_chapter = st.text_input(label = 'Chapter', placeholder = 1)
    handbook_paragraph = st.text_input(label = 'Paragraph', placeholder = 1)
    
    uploaded_file = st.file_uploader(label = "Upload a picture (256×360)", type = 'png')
        
    if uploaded_file is not None:
      handbook_image = uploaded_file.getvalue()
              
    else:
      handbook_image = loadFile("images/placeholder.png")
      
    
    ## Submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
      # Write entry to table `HANDBOOK_USER`
      query = "INSERT INTO `benbox`.`HANDBOOK_USER`(ID, HANDBOOK_ID, CATEGORY_ID, CATEGORY_SUB_ID, HANDBOOK_CHAPTER, HANDBOOK_PARAGRAPH, HANDBOOK_KEYWORD1, HANDBOOK_KEYWORD2, HANDBOOK_KEYWORD3, HANDBOOK_KEYWORD4, HANDBOOK_KEYWORD5, HANDBOOK_SUMMARY, HANDBOOK_TEXT, HANDBOOK_TEXT_LANGUAGE, HANDBOOK_HITS) VALUES (%s, '%s', '%s', '%s', );" %(id, handbook_id, )
      st.write(query)
      run_query(query)
      conn.commit()

  
## Column 1
with col2:
  st.image("images/Ben.png")
