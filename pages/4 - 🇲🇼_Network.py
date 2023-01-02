##### `pages/4 - 🇲🇼_Network.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import mysql.connector
import sys
sys.path.insert(1, "pages/functions/")




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
### Network Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')




#### Main Program
### Header
## Header
st.title('FAQ')



### Chat Bot Ben
## Get categories and sub-categories
# Open databank connection
conn = init_connection()

# Run query
query = "SELECT CATEGORY_ID, CATEGORY_DESCRIPTION, CATEGORY_SUB_ID, CATEGORY_SUB_DESCRIPTION FROM benbox.CATEGORIES;"
rows = run_query(query)

# Filling variables
filter_cat = []
filter_sub = []
categories = []
sub_categories = []
categories_id = []
sub_categories_id = []
for row in rows:
  if (row[0] != None):
    categories.append(row[1])
    categories_id.append(row[0])
    filter_cat.append(True)
  else:
    sub_categories.append(row[3])
    sub_categories_id.append(row[2])
    filter_sub.append(True)


## Columns
col1, col2 = st.columns(2)


## Column 1
with col1:
  ## Checkboxen for filtering
  st.subheader('Filter')
  
  
  ## Categories
  st.write(':orange[Categories:] ')
  for i in range(len(categories)):
    filter_cat[i] = st.checkbox(label = categories[i], value = True)
  
  # Write category ids into array for checking
  filter_cat_ids = []  
  for i in range(len(filter_cat)):
    if filter_cat[i] == True:
      filter_cat_ids.append(categories_id[i])


  ## Sub-categories
  st.write(':green[Sub-categories:] ')
  for i in range(len(sub_categories)):
    filter_sub[i] = st.checkbox(label = sub_categories[i], value = True)
    
  # Write sub-category ids into array for checking
  filter_sub_ids = []  
  for i in range(len(filter_sub)):
    if filter_sub[i] == True:
      filter_sub_ids.append(sub_categories_id[i])
  
  
## Column 2
with col2:
  st.subheader('Questions & answers')
    
  ## Get FAQ
  query = "SELECT que.QUESTION_TEXT, faq.FAQ_ANSWER, cat.CATEGORY_DESCRIPTION, catsub.CATEGORY_SUB_DESCRIPTION, que.CATEGORY_ID, que.CATEGORY_SUB_ID FROM benbox.FAQ AS faq LEFT JOIN benbox.QUESTIONS AS que ON que.QUESTION_ID = faq.QUESTION_ID LEFT JOIN benbox.CATEGORIES AS cat ON cat.CATEGORY_ID = que.CATEGORY_ID LEFT JOIN benbox.CATEGORIES AS catsub ON catsub.CATEGORY_SUB_ID = que.CATEGORY_SUB_ID;"
  faq = run_query(query)
 
  
  ## Showing expander
  # Check if data is existend
  if (faq != None):
    for i in range(len(faq)):
      for x in range(len(filter_cat_ids)):
        if faq[i][4] == filter_cat_ids[x]:
          for y in range(len(filter_sub_ids)):
            if faq[i][5] == filter_sub_ids[y]:
              with st.expander(label = '\"' + faq[i][0].upper() + '\"', expanded = False):
                st.write(':orange[Category:] ', faq[i][2])
                st.write(':green[Sub-category:] ', faq[i][3])
                st.write(':blue[Ben`s answer:] ', faq[i][1])
                
  # No data existend
  else:
    st.write('No questions & answer available')
      

## Iframe
#stc.iframe(src = "http://localhost/hopecarrental/index.php", height = 600, scrolling = True)
#stc.iframe(src = "https://techhub.social/@DrBenjamin", height = 692, scrolling = True)
stc.iframe(src = "http://192.168.1.173/index.html", height = 500, scrolling = True)

stc.html(
  """
  <iframe src="https://techhub.social/@DrBenjamin/109397699095825866/embed" class="mastodon-embed" style="max-width: 100%; border: 0" width="400"></iframe><script src="https://techhub.social/embed.js" async="async"></script>
  """,
  height=300,
)
