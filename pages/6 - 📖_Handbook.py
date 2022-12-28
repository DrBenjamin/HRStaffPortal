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
      
      
      
### Function: pictureUploader = uploads employee images
def pictureUploader(image, index):
  # Initialize connection
  connection = mysql.connector.connect(**st.secrets["mysql"])
  cursor = connection.cursor()
  
  # SQL statement
  sql_insert_blob_query = """ UPDATE IMAGEBASE SET IMAGE = %s WHERE ID = %s;"""
  
  # Convert data into tuple format
  insert_blob_tuple = (image, index)
  result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
  connection.commit()
      
      
      
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
## Open databank connection
conn = init_connection()


## Get categories and sub-categories
query = "SELECT CATEGORY_ID, CATEGORY_DESCRIPTION, CATEGORY_SUB_ID, CATEGORY_SUB_DESCRIPTION FROM benbox.CATEGORIES;"
rows = run_query(query)

# Filling variables
categories = []
sub_categories = []
categories_id = []
sub_categories_id = []
for row in rows:
  if (row[0] != None):
    categories.append(row[1])
    categories_id.append(row[0])
  else:
    sub_categories.append(row[3])
    sub_categories_id.append(row[2])
        
        
## Category menu
category = st.selectbox(label = 'Please choose the category of the handbook entry', options = range(len(categories)), format_func = lambda x: categories[x])
      
      
## Sub-Category menu
sub_category = st.selectbox(label = 'Please choose the sub-category of the handbook entry', options = range(len(sub_categories)), format_func = lambda x: sub_categories[x])
     
      
## Columns
col1, col2 = st.columns(2)


## Column 1
with col1:
  with st.form('Input', clear_on_submit = False):
    ## Handbook data entry
    # Open databank connection
    conn = init_connection()
    
    
    ## Input for new `HANDBOOK_USER` data
    # Get latest ID from table
    id = lastID(url = '`benbox`.`HANDBOOK_USER`')
    handbook_id = generateID(id)
    st.text_input(label = 'ID', value = id, disabled = True)
    st.text_input(label = 'Handbook ID', value = handbook_id, disabled = True)
    st.text_input(label = 'Category ID', value = categories_id[category], disabled = True)
    st.text_input(label = 'Sub-Category ID', value = sub_categories_id[sub_category], disabled = True)
    handbook_chapter = st.text_input(label = 'Chapter', placeholder = 1)
    handbook_paragraph = st.text_input(label = 'Paragraph', placeholder = 1)
    handbook_keyword1 = st.text_input(label = 'Keyword 1')
    handbook_keyword2 = st.text_input(label = 'Keyword 2')
    handbook_keyword3 = st.text_input(label = 'Keyword 3')
    handbook_keyword4 = st.text_input(label = 'Keyword 4')
    handbook_keyword5 = st.text_input(label = 'Keyword 5')
    handbook_summary = st.text_input(label = 'Summary')
    handbook_text = st.text_input(label = 'Text')
    handbook_text_language = st.text_input(label = 'Language', value = 'en')
    handbook_hits = st.text_input(label = 'Hits', value = 0)
    
    uploaded_file = st.file_uploader(label = "Upload a picture", type = 'png')
        
    if uploaded_file is not None:
      handbook_image = uploaded_file.getvalue()
              
    else:
      handbook_image = loadFile("images/placeholder_documentation.png")
      
    
    ## Submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
      # Write entry to table `HANDBOOK_USER`
      query = "INSERT INTO `benbox`.`HANDBOOK_USER`(ID, HANDBOOK_ID, CATEGORY_ID, CATEGORY_SUB_ID, HANDBOOK_CHAPTER, HANDBOOK_PARAGRAPH, HANDBOOK_KEYWORD1, HANDBOOK_KEYWORD2, HANDBOOK_KEYWORD3, HANDBOOK_KEYWORD4, HANDBOOK_KEYWORD5, HANDBOOK_SUMMARY, HANDBOOK_TEXT, HANDBOOK_TEXT_LANGUAGE, HANDBOOK_HITS) VALUES (%s, '%s', '%s', '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(id, handbook_id, categories_id[category], sub_categories_id[sub_category], handbook_chapter, handbook_paragraph, handbook_keyword1, handbook_keyword2, handbook_keyword3, handbook_keyword4, handbook_keyword5, handbook_summary, handbook_text, handbook_text_language, handbook_hits)
      st.write(query)
      run_query(query)
      conn.commit()
      
      # Upload picture to database
      pictureUploader(handbook_image, id)

  
## Column 1
with col2:
  st.image("images/Ben.png")
