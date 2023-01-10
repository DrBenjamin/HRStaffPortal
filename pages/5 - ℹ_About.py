##### `pages/5 - ℹ_About.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import sys
sys.path.insert(1, "pages/functions/")
from functions import header
from network import get_ip




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
## Sidebar Header Image
st.sidebar.image('images/MoH.png')




#### Main program
### Logged out state (About)
## Header
header(title = 'About page', data_desc = 'contact information') 
 

## Contact information
with st.expander('Contact information', expanded = True):
  st.subheader('Address')
  st.write(st.secrets['custom']['address_line1'])
  st.write(st.secrets['custom']['address_line2'])
  st.subheader('Contact')
  st.write('**' + st.secrets['custom']['contact_tel1'] + '**')
  st.write('**' + st.secrets['custom']['contact_tel2'] + '**')
  st.write('**' + st.secrets['custom']['contact_tel3'] + '**')
  st.write('**' + '<a href=\"mailto:' + st.secrets['custom']['contact_mail1'].split('(mail:')[1][:-1] + '\">Mail: ' + st.secrets['custom']['contact_mail1'].split('(mail:')[1][:-1] + '</a>**', unsafe_allow_html = True)
  st.write('**' + '<a href=\"mailto:' + st.secrets['custom']['contact_mail2'].split('(mail:')[1][:-1] + '\">Mail: ' + st.secrets['custom']['contact_mail2'].split('(mail:')[1][:-1] + '</a>**', unsafe_allow_html = True)


## Network iframe
with st.expander('Changelog', expanded = True):
  ## Title
  st.subheader('Changelog')
  
  
  ## Remote site
  stc.html("""<iframe src="https://techhub.social/@DrBenjamin/109397699095825866/embed" class = "mastodon-embed" style = "max-width: 100%; border: 0" width = "600"></iframe><script src="https://techhub.social/embed.js" async = "async"></script>""", height = 520,)
  
  
  ## Local site
  #stc.iframe(src = 'http://' + get_ip() + '/index.html', height = 500, scrolling = True)
