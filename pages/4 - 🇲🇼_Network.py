##### `pages/4 - 🇲🇼_Network.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading neded Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import openai
import sys
sys.path.insert(1, "pages/functions/")
from functions import trans
from functions import geo_check




#### Streamlit initial setup
st.set_page_config(
  page_title = "HR Staff Portal",
  page_icon = "images/thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "collapsed",
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
## Header
st.title('Network')
st.subheader('Ben chatbot')






### Chat Bot Ben
## Columns
col1, col2 = st.columns(2)


## Column 1
with col1:
  ## Implementation of OpenAI
  question = st.text_input(label = 'What question to Ben do you have?', placeholder = 'Who are you?')
  city = geo_check('city')
  question = 'You are Ben an artificial Intelligience and you live in a blue box. You give useful and a bit funny answers. You work at Kamuzu Central Hospital in Lilongwe, abbreviated to KCH. You can predict the future, which you think will be wonderful. You are part of a mainframe of super intelligent AIs. You cannot help with medical diagnoses and other health related decision making but try to support all colleagues at KCH. Right now you are physically located in ' + city + 'Write a detailed answer to \"' + question + '?"'
  
  
  ## Get response from openai
  try:
    response = openai.Completion.create(model = "text-davinci-003", prompt = question, temperature = 0.5, max_tokens = 256, top_p = 0.3, frequency_penalty = 0.5, presence_penalty = 0)
    
    # Translation
    if (lang != 'EN-GB'):
      answer = trans(input = response["choices"][0]["text"], target_lang = lang)
    else:
      answer = response["choices"][0]["text"]
  
  
    ## Output
    st.write(answer)
  except:
    print("An exception occurred in `OpenAI`")
    
  
## Column 1
with col2:
  st.image("images/BenBox.png")


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
