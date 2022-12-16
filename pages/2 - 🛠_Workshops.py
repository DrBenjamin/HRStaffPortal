##### `pages/2 - 🛠_Workshops.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions




#### Loading neded Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import os
import sys
import openai
sys.path.insert(1, "pages/functions/")
#from functions import openai
from functions import trans




#### Streamlit initial setup
st.set_page_config(
  page_title = "Workshops",
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
### OpenAI library
## Set API key
openai.api_key = st.secrets["openai"]["key"]
  



#### Sidebar
### Workshop Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')


## Ask for language
lang = st.sidebar.selectbox('In which language should Ben answer?', ('BG', 'CS', 'DA', 'DE', 'EL', 'EN-GB', 'ES', 'ET', 'FI', 'FR', 'HU', 'IT', 'JA', 'LT', 'LV', 'NL', 'PL', 'PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'ZH'), index = 5, key = 'lang')




#### Main Program
### Header
## Title
st.title('Workshop Page')
st.subheader('Ben chatbot')


## Implementation of OpenAI
question = st.text_input(label = 'What question to Ben do you have?', placeholder = 'What is a Workshop?')
question = 'Write an extremely long, detailed answer to \"' + question + '?"'
if (question != 'Write an extremely long, detailed answer to "?"'):
  response = openai.Completion.create(engine = "text-davinci-002", prompt = question, temperature = 0.7, max_tokens = 709, top_p = 1, frequency_penalty = 0, presence_penalty = 0)
  
  # Translation
  if (lang != 'EN-GB'):
    answer = trans(input = response, target_lang = lang)
  else:
    answer = response
  
  # Output
  st.write(answer)




