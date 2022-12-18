##### `pages/2 - 🛠_Workshops.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading neded Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import openai
import sys
sys.path.insert(1, "pages/functions/")




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
### Function geo_check = Geo-Location checking
def geo_check(address_part, fallback, language = 'en'):
  ## Geocoder gets coordinates related to the current IP address
  g = geocoder.ip('me')
  
  
  ## Geopy
  # Calling the Nominatim tool
  loc = Nominatim(user_agent = "GetLoc", timeout = 3)
  geolocator = Nominatim(user_agent = "geoapiExercises")
  
  # Get City name
  try:
    geolocator.reverse(g.latlng, language = lang)
    location = geolocator.geocode(g.latlng, addressdetails = True)
    loc = location.raw
    output = loc['address'][address_part]
    print("Detected location:", output)
    
  # Set `output` to `fallback` if not reachable
  except:
    print("An exception occurred in `Geocoder`")
    output = fallback
  
  # Return output 
  return output
  
  


#### Sidebar
### Workshop Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')




#### Main Program
### Header
## Header
st.title('Workshop page')
st.subheader('Ben chatbot')



### Chat Bot Ben
## Columns
col1, col2 = st.columns(2)


## Column 1
with col1:
  ## Implementation of OpenAI
  text_input = st.text_input(label = 'What text should be summarised to one keyword?', placeholder = 'Salary, is what an employee get paid at the end of the month')
  
  # Concacenate question
  text_prompt = 'Extract one keyword of the beginning of the text which is a noun without the accompanying article and pronoun: \"' + text_input + '"'
  
  
  ## Get response from openai
  # Set API key
  openai.api_key = st.secrets["openai"]["key"]
  
  try:
    response = openai.Completion.create(model = "text-curie-001", prompt = text_prompt, temperature = 0.0, max_tokens = 64, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)

    summarization = response["choices"][0]["text"]
  
    # Output
    st.write(summarization)
    
  except:
    print("An exception occurred in `OpenAI`")
    
  
## Column 1
with col2:
  st.image("images/Ben.png")
