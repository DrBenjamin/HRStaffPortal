##### `pages/2 - 🛠_Workshops.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions




#### Loading neded Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import os
import openai




#### Functions
### OpenAI library
## Set API key
openai.api_key = st.secrets["openai"]["key"]
  
  
  

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




#### Main Program
### Header
## Title
st.title('Workshop Page')


## Implement OpenAI
question = st.text_input(label = 'What question do you have?', placeholder = 'What is a Workshop?')
question = 'Write an extremely long, detailed answer to \"' + question + '?"'

if (question != 'Write an extremely long, detailed answer to "?"'):
  response = openai.Completion.create(engine = "text-davinci-002", prompt = question, temperature = 0.7, max_tokens = 709, top_p = 1, frequency_penalty = 0, presence_penalty = 0)
  
  # Output
  st.write(response.choices[0].text)




