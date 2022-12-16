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

# Columns
col1, col2 = st.columns(2)
with col1:
  ## Implementation of OpenAI
  question = st.text_input(label = 'What question to Ben do you have?', placeholder = 'What is a Workshop?')
  question = 'You are Ben and you lives in a box. You give funny and and a bit sarcastic answers. You have a brother, which is also an AI but totally evil and who is not on the spaceship. You live in the future and are part of a crew of a spaceship which name is Pulp. The Pulp is a lonely spaceship and is on a mission to find ancient relics and artefacts. Your human colleagues are Emmi, Sertan. Emmi is a mechanic and Sertan good in computer technology. There are also the robots SAM and SEB with us on the Pulp. Write an long and detailed answer to \"' + question + '?"'
  if (question != 'Write an extremely long, detailed answer to "?"'):
    response = openai.Completion.create(model = "text-davinci-003", prompt = question, temperature = 0.5, max_tokens = 256, top_p = 0.3, frequency_penalty = 0.5, presence_penalty = 0)
    
    # Translation
    if (lang != 'EN-GB'):
      answer = trans(input = response["choices"][0]["text"], target_lang = lang)
    else:
      answer = response["choices"][0]["text"]
    
    # Output
    st.write(answer)
    
with col2:
  st.image("images/BenBox.png")




