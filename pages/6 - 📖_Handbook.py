##### `pages/6 - 📖_Handbook.py`
##### HR Staff Portal
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




#### Initialization of session states
## First Run State
if ('chapter' not in st.session_state):
  st.session_state['chapter'] = 1
  
  


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
      
      
      
### Function: pictureUploader = uploads handbook images
def pictureUploader(image, index):
  # Initialize connection
  connection = mysql.connector.connect(**st.secrets["mysql_benbox"])
  cursor = connection.cursor()
  
  # SQL statement
  sql_insert_blob_query = """ UPDATE `HANDBOOK_USER` SET HANDBOOK_IMAGE = %s WHERE ID = %s;"""
  
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



### Chapter and paragraph structures
## Open databank connection
conn = init_connection()


## Get chapter structure
query = "SELECT ID, HANDBOOK_CHAPTER, HANDBOOK_CHAPTER_DESCRIPTION, HANDBOOK_CHAPTER_TEXT FROM benbox.HANDBOOK_CHAPTER_STRUCTURE;"
rows = run_query(query)
databank_chapter = pd.DataFrame(columns = ['ID', 'HANDBOOK_CHAPTER', 'HANDBOOK_CHAPTER_DESCRIPTION', 'HANDBOOK_CHAPTER_TEXT'])
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3]]], columns = ['ID', 'HANDBOOK_CHAPTER', 'HANDBOOK_CHAPTER_DESCRIPTION', 'HANDBOOK_CHAPTER_TEXT'])
  databank_chapter = pd.concat([databank_chapter, df])
databank_chapter = databank_chapter.set_index('ID')

# Sort chapters
databank_chapter = databank_chapter.sort_values('HANDBOOK_CHAPTER', ascending = True)
chapters = list(databank_chapter['HANDBOOK_CHAPTER'])
chapters_str = map(str, chapters)
chapters_desc = list(databank_chapter['HANDBOOK_CHAPTER_DESCRIPTION'])

# Concatenate the two strings
chapters_desc = [' ' + str(row) for row in chapters_desc]
chapters_combo = [i + j for i, j in zip(chapters_str, chapters_desc)]


## Show chapter structure in expander
with st.expander(label = 'Chapter structure', expanded = False):
  st.write(databank_chapter)
  
  
  ## Input for new handbook chapter structure data
  with st.form('Chapter', clear_on_submit = True):
    st.subheader('New chapter entry')
    
    # Get latest ID from table
    id = lastID(url = '`benbox`.`HANDBOOK_CHAPTER_STRUCTURE`')
    st.text_input(label = 'ID', value = id, disabled = True)
    
    # Inputs
    handbook_chapter_structure_chapter = st.text_input(label = 'Chapter')
    handbook_chapter_structure_chapter_desc = st.text_input(label = 'Description')
    handbook_chapter_structure_chapter_text = st.text_input(label = 'Text')
    
    
    ## Submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
      # Write entry to table `HANDBOOK_CHAPTER_STRUCTURE`
      query = "INSERT INTO `benbox`.`HANDBOOK_CHAPTER_STRUCTURE`(ID, HANDBOOK_CHAPTER, HANDBOOK_CHAPTER_DESCRIPTION, HANDBOOK_CHAPTER_TEXT) VALUES (%s, '%s', '%s', '%s');" %(id, handbook_chapter_structure_chapter, handbook_chapter_structure_chapter_desc, handbook_chapter_structure_chapter_text)
      run_query(query)
      conn.commit()
      
      # Rerun
      st.experimental_rerun()
      

## Get paragraph structure
query = "SELECT ID, HANDBOOK_PARAGRAPH, HANDBOOK_PARAGRAPH_DESCRIPTION, HANDBOOK_PARAGRAPH_TEXT FROM benbox.HANDBOOK_PARAGRAPH_STRUCTURE;"
rows = run_query(query)
databank_paragraph = pd.DataFrame(columns = ['ID', 'HANDBOOK_PARAGRAPH', 'HANDBOOK_PARAGRAPH_DESCRIPTION', 'HANDBOOK_PARAGRAPH_TEXT'])
for row in rows:
  df = pd.DataFrame([[row[0], str(row[1]).strip('0'), row[2], row[3]]], columns = ['ID', 'HANDBOOK_PARAGRAPH', 'HANDBOOK_PARAGRAPH_DESCRIPTION', 'HANDBOOK_PARAGRAPH_TEXT'])
  databank_paragraph = pd.concat([databank_paragraph, df])
databank_paragraph = databank_paragraph.set_index('ID')

# Sort paragraphs
databank_paragraph = databank_paragraph.sort_values('HANDBOOK_PARAGRAPH', ascending = True)
paragraphs = list(databank_paragraph['HANDBOOK_PARAGRAPH'])
paragraphs_desc = list(databank_paragraph['HANDBOOK_PARAGRAPH_DESCRIPTION'])
paragraphs_list = []
paragraphs_desc_list = []
for i in range(len(paragraphs)):
  if int(paragraphs[i][0]) == st.session_state['chapter']:
    paragraphs_list.append(paragraphs[i])
    paragraphs_desc_list.append(paragraphs_desc[i])
    
# Concatenate the two strings
paragraphs_desc_list = [' ' + row for row in paragraphs_desc_list]
paragraphs_combo = [i + j for i, j in zip(paragraphs_list, paragraphs_desc_list)]


## Show paragraph structure in expander
with st.expander(label = 'Paragraph structure', expanded = False):
  st.write(databank_paragraph)
  
  
  ## Input for new handbook paragraph structure data
  with st.form('Paragraph', clear_on_submit = True):
    st.subheader('New paragraph entry')
    
    # Get latest ID from table
    id = lastID(url = '`benbox`.`HANDBOOK_PARAGRAPH_STRUCTURE`')
    st.text_input(label = 'ID', value = id, disabled = True)
    
    # Inputs
    handbook_paragraph_structure_paragraph = st.text_input(label = 'Paragraph')
    handbook_paragraph_structure_paragraph_desc = st.text_input(label = 'Description')
    handbook_paragraph_structure_paragraph_text = st.text_input(label = 'Text')
    
    
    ## Submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
      # Write entry to table `HANDBOOK_PARAGRAPH_STRUCTURE`
      query = "INSERT INTO `benbox`.`HANDBOOK_PARAGRAPH_STRUCTURE`(ID, HANDBOOK_PARAGRAPH, HANDBOOK_PARAGRAPH_DESCRIPTION, HANDBOOK_PARAGRAPH_TEXT) VALUES (%s, '%s', '%s', '%s');" %(id, handbook_paragraph_structure_paragraph, handbook_paragraph_structure_paragraph_desc, handbook_paragraph_structure_paragraph_text)
      run_query(query)
      conn.commit()
      
      # Rerun
      st.experimental_rerun()


### Handbook
## Get categories and sub-categories
query = "SELECT CATEGORY_ID, CATEGORY_DESCRIPTION, CATEGORY_SUB_ID, CATEGORY_SUB_DESCRIPTION FROM benbox.CATEGORIES;"
rows = run_query(query)

# Filling category and sub-category variables
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


## Title for handbook data entry      
st.subheader('New handbook entry')


## Category menu
category = st.selectbox(label = 'Please choose the category of the handbook entry', options = range(len(categories)), format_func = lambda x: categories[x])
      
      
## Sub-Category menu
sub_category = st.selectbox(label = 'Please choose the sub-category of the handbook entry', options = range(len(sub_categories)), format_func = lambda x: sub_categories[x])


## Chapter menu
chapter = st.selectbox(label = 'Please choose the chapter of the handbook entry', options = range(len(chapters_combo)), format_func = lambda x: chapters_combo[x])
st.session_state['chapter'] = chapters[chapter]


## Paragraphs menu
paragraph = st.selectbox(label = 'Please choose the paragraph of the handbook entry', options = range(len(paragraphs_combo)), format_func = lambda x: paragraphs_combo[x])


## Handbook data entry
with st.form('Input', clear_on_submit = True):
  # Open databank connection
  conn = init_connection()
    
    
  ## Input for new `HANDBOOK_USER` data
  # Get latest ID from table
  id = lastID(url = '`benbox`.`HANDBOOK_USER`')
  handbook_id = generateID(id)
  st.text_input(label = 'ID', value = id, disabled = True)
  st.text_input(label = 'Handbook ID', value = handbook_id, disabled = True)
  st.text_input(label = 'Category', value = categories[category], disabled = True)
  st.text_input(label = 'Sub-Category', value = sub_categories[sub_category], disabled = True)
  st.text_input(label = 'Chapter', value = chapters_combo[chapter], disabled = True)
  handbook_chapter = chapters[chapter]
  if paragraphs_combo is None or len(paragraphs_combo) == 0:
    st.text_input(label = 'Paragraph', placeholder = 'Please add paragraph first!', disabled = True)
    handbook_paragraph = 0
  else:
    st.text_input(label = 'Paragraph', value = paragraphs_combo[paragraph], disabled = True)
    handbook_paragraph = paragraphs[paragraph]
  handbook_keyword1 = st.text_input(label = 'Keyword 1')
  handbook_keyword2 = st.text_input(label = 'Keyword 2')
  handbook_keyword3 = st.text_input(label = 'Keyword 3')
  handbook_keyword4 = st.text_input(label = 'Keyword 4')
  handbook_keyword5 = st.text_input(label = 'Keyword 5')
  handbook_summary = st.text_input(label = 'Summary')
  handbook_text = st.text_input(label = 'Text')
  handbook_text_headline = st.text_input(label = 'Headline')
  handbook_text_language = st.text_input(label = 'Language', value = 'en')
  handbook_hits = st.text_input(label = 'Hits', value = 0)
   
  # Handbook image upload 
  uploaded_file = st.file_uploader(label = "Upload a picture", type = 'png')
  if uploaded_file is not None:
    handbook_image = uploaded_file.getvalue()
  else:
    handbook_image = loadFile("images/placeholder_documentation.png")
    handbook_image_text = 'Placeholder image.'
  
  # Image description text input
  handbook_image_text = st.text_input(label = 'Image description')
  
  
  ## Submit button
  submitted = st.form_submit_button("Submit")
  if submitted:
    # Check if image description is not changed
    if (len(handbook_image_text) < 1):     
      handbook_image_text = 'Placeholder image.'
      
    # Write entry to table `HANDBOOK_USER`
    query = "INSERT INTO `benbox`.`HANDBOOK_USER`(ID, HANDBOOK_ID, CATEGORY_ID, CATEGORY_SUB_ID, HANDBOOK_CHAPTER, HANDBOOK_PARAGRAPH, HANDBOOK_KEYWORD1, HANDBOOK_KEYWORD2, HANDBOOK_KEYWORD3, HANDBOOK_KEYWORD4, HANDBOOK_KEYWORD5, HANDBOOK_SUMMARY, HANDBOOK_TEXT, HANDBOOK_TEXT_HEADLINE, HANDBOOK_TEXT_LANGUAGE, HANDBOOK_HITS, HANDBOOK_IMAGE_TEXT) VALUES (%s, '%s', '%s', '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s');" %(id, handbook_id, categories_id[category], sub_categories_id[sub_category], handbook_chapter, handbook_paragraph, handbook_keyword1, handbook_keyword2, handbook_keyword3, handbook_keyword4, handbook_keyword5, handbook_summary, handbook_text, handbook_text_headline, handbook_text_language, handbook_hits, handbook_image_text)
    run_query(query)
    conn.commit()
      
    # Upload picture to database
    pictureUploader(image = handbook_image, index = id)
    
    # Rerun
    st.experimental_rerun()
