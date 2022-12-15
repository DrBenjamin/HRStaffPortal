##### `pages/4 - 🇲🇼_Network.py`
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
#stc.iframe(src = "https://techhub.social/@DrBenjamin", height = 692, scrolling = True)
stc.iframe(src = "http://192.168.1.173/index.html", height = 500, scrolling = True)

stc.html(
  """
  <iframe src="https://techhub.social/@DrBenjamin/109397699095825866/embed" class="mastodon-embed" style="max-width: 100%; border: 0" width="400"></iframe><script src="https://techhub.social/embed.js" async="async"></script>
  """,
  height=300,
)
