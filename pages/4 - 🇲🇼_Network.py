##### `pages/4 - 🇲🇼_Network.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
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
      print("An exception occurred in function `run_query`")


  

#### Sidebar
### Workshop Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')






#### Main Program
### Header
## Header
st.title('Network')
st.subheader('FAQ')



### Chat Bot Ben
## Columns
col1, col2 = st.columns(2)


## Column 1
with col1:
  ## Get FAQ
  # Open databank connection
  conn = init_connection()
  query = "SELECT que.QUESTION_TEXT, faq.FAQ_ANSWER FROM benbox.FAQ AS faq LEFT JOIN benbox.QUESTIONS AS que ON que.QUESTION_ID = faq.QUESTION_ID;"
  faq = run_query(query)
 
  
  ## Showing expander
  for i in range(len(faq)):
    with st.expander(faq[i][0]):
      st.write(faq[i][1])
    
  
## Column 1
with col2:
  st.image("images/Ben.png")


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
