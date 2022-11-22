##### `4 - 🇲🇼_Network.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions



#### Loading neded Python libraries
import streamlit as st
import streamlit.components.v1 as stc



#### Streamlit initial setup
st.set_page_config(
  page_title = "KCH HR Staff Portal",
  page_icon = "images/thumbnail.png",
  layout = "wide",
  initial_sidebar_state = "collapsed",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the KCH HR Staff Portal. Version 0.1.1-b1"
        }
)


## Header
#st.title('Network')
#st.header('Kamuzu Central Hospital (KCH)')
#st.subheader('Mastodon Server')


## Sidebar
# Sidebar Header Image
st.sidebar.image('images/MoH.png')

# Iframe
#stc.iframe(src = "http://localhost/hopecarrental/index.php", height = 600, scrolling = True)
stc.iframe(src = "https://joinmastodon.org", height = 692, scrolling = True)

stc.html(
  """
  <!DOCTYPE html>
  <html lang="en_UK">
  <head>
  <meta charset="UTF-8">
  <title>Titel of the Webpage</title>
  <meta name="robots" content="index,follow" />
  Text
  <br />
  Text 2
  </head>
  """,
  height=100,
)
