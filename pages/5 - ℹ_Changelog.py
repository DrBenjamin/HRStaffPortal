##### `pages/5 - ℹ_Changelogt.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import sys
sys.path.insert(1, "pages/functions/")
from functions import header
from functions import check_password
from functions import logout
from network import get_ip




#### Streamlit initial setup
desc_file = open('DESCRIPTION', 'r')
lines = desc_file.readlines()
print(lines[3])
st.set_page_config(
  page_title = "Cangelog",
  page_icon = st.secrets['custom']['facility_image_thumbnail'],
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': st.secrets['custom']['menu_items_help'],
         'Report a bug': st.secrets['custom']['menu_items_bug'],
         'About': '**HR Staff Portal** (' + lines[3] + ')\n\n' + st.secrets['custom']['facility'] + ' (' + st.secrets['custom']['facility_abbreviation'] + ')' + ', ' + st.secrets['custom']['address_line1'] + '\n' +st.secrets['custom']['address_line2'] + '\n\n' + st.secrets['custom']['contact_tel1'] + '\n\n' + st.secrets['custom']['contact_tel2'] + '\n\n' + st.secrets['custom']['contact_tel3'] + '\n\n' + st.secrets['custom']['contact_mail1_desc'] + ': ' + st.secrets['custom']['contact_mail1'] + '\n\n' + st.secrets['custom']['contact_mail2_desc'] + ': ' + st.secrets['custom']['contact_mail2'] + '\n\nAdministrator: ' + st.secrets['custom']['contact_admin'] + '\n\n-----------'
        }
)




#### Initialization of session states
## Session state
if ('admin' not in st.session_state):
  st.session_state['admin'] = False
if ('header' not in st.session_state):
  st.session_state['header'] = True
  



#### Functions




#### Main program
### Header
header(title = 'Changelog', data_desc = 'Software information', expanded = st.session_state['header']) 



### Changelog
## Changelog iframe
with st.expander('Changelog', expanded = True):
  #st.subheader('Changelog')
    
    
  ## Iframe of remote site
  #stc.html("""<iframe src="https://techhub.social/@DrBenjamin/109397699095825866/embed" class = "mastodon-embed" style = "max-width: 100%; border: 0" width = "600"></iframe><script src="https://techhub.social/embed.js" async = "async"></script>""", height = 520,)
  #stc.html("""<blockquote class="trello-card"><a href="https:&#x2F;&#x2F;trello.com&#x2F;c&#x2F;wNdVZqVq&#x2F;21-release-v020">Release v0.2.0</a></blockquote><script src="https://p.trellocdn.com/embed.min.js"></script>""", height = 520)  
  #stc.html("""<iframe src="https://github.com/DrBenjamin/HRStaffPortal/blob/main/CHANGELOG.md"" style = "max-width: 100%; border: 0" width = "600"></iframe>""", height = 520)  
  
  
  ## Local site
  source = 'http://' + get_ip() + '/index.html'
  st.write(source)
  #source = "http://192.168.1.173/index.html"
  #st.write(source)
  stc.iframe(src = "http://localhost/index.html", height = 520, scrolling = True)
  stc.html("""<iframe src="http://localhost/index.html" style = "max-width: 100%; border: 0" width = "600"></iframe>""", height = 520) 


    
### Logged in state (About)
if check_password():
  print('Logged in')
  


### Logged out state (About)
else:
  print('Logged out')
