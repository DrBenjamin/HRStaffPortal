##### `pages/5 - ℹ_Changelog.py`
##### HR Staff Portal
##### Open-Source, hosted on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import sys
sys.path.insert(1, "pages/functions/")
from functions import header
from functions import check_password




#### Streamlit initial setup
desc_file = open('DESCRIPTION', 'r')
lines = desc_file.readlines()
print(lines[3])
try:
    st.set_page_config(
        page_title = "Changelog",
        page_icon = st.secrets['custom']['facility_image_thumbnail'],
        layout = "centered",
        initial_sidebar_state = "expanded",
        menu_items = {
            'Get Help': st.secrets['custom']['menu_items_help'],
            'Report a bug': st.secrets['custom']['menu_items_bug'],
            'About': '**HR Staff Portal** (' + lines[3] + ')\n\n' + st.secrets['custom']['facility'] + ' (' +
                     st.secrets['custom']['facility_abbreviation'] + ')' + ', ' + st.secrets['custom'][
                         'address_line1'] + '\n' + st.secrets['custom']['address_line2'] + '\n\n' + st.secrets['custom'][
                         'contact_tel1'] + '\n\n' + st.secrets['custom']['contact_tel2'] + '\n\n' + st.secrets['custom'][
                         'contact_tel3'] + '\n\n' + st.secrets['custom']['contact_mail1_desc'] + ': ' +
                     st.secrets['custom']['contact_mail1'] + '\n\n' + st.secrets['custom']['contact_mail2_desc'] + ': ' +
                     st.secrets['custom']['contact_mail2'] + '\n\nAdministrator: ' + st.secrets['custom'][
                         'contact_admin'] + '\n\n-----------'
        }
    )
except Exception as e:
    print(e)




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
with st.expander('', expanded = True):
    ## Local site hosted on Apache
    source = 'https://192.168.1.173/index.html'
    stc.iframe(src = source, height = 620, scrolling = True)

    
    
    ## Hugging Face
    #st.write(st.experimental_user)
    #source = "https://drbenjamin-openai.hf.space"
    #stc.iframe(src = source, height = 620, scrolling = True)



### Logged in state (About)
if check_password():
    print('Logged in')



### Logged out state (About)
else:
    print('Logged out')
