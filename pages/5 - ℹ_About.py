##### `pages/5 - ℹ_About.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc




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
## Header
st.title('About')
st.header('Kamuzu Central Hospital (KCH)')
st.subheader('All KCH information')
st.write('Private Bag 149,')
st.write('Lilongwe, MALAWI')
st.write('[Tel: +265 1 753 400](tel:+2651753400)')
st.write('[Tel: +265 1 753 555](tel:+2651753555)')
st.write('[Tel: +265 1 753 744](tel:+2651753744)')
