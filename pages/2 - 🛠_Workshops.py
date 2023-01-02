##### `pages/2 - 🛠_Workshops.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import openai
import geocoder
from geopy.geocoders import Nominatim
import mysql.connector
import sys
sys.path.insert(1, "pages/functions/")
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




#### Initialization of session states
## Answer / question states
if ('answer' not in st.session_state):
  st.session_state['answer'] = ''
  
  
## Feedback state
if ('feedback' not in st.session_state):
  st.session_state['feedback'] = False
  
  
## Write to `FAQ` table
if ('question_id' not in st.session_state):
  st.session_state['question_id'] = ''
if ('handbook_id' not in st.session_state):
  st.session_state['handbook_id'] = ''
  
  

  
#### Functions
### Function: run_query = Initial SQL Connection
def init_connection():
  ## Initialize connection
  try:
    return mysql.connector.connect(**st.secrets["mysql_benbox"])
  except:
    print("An exception occurred in function `init_connection`")
    st.error(body = 'Databank connection timeout!', icon = "🚨")
    st.stop()



### Function: run_query = SQL query
def run_query(query):
  with conn.cursor() as cur:
    # Perform query
    try:
      cur.execute(query)
      return cur.fetchall()
    
    except:
      print('An exception occurred in function `run_query` with query \"' + query + '\"')
      
      
      
### Function: lastID = checks for last ID number in Table (to add data after)
def lastID(url):
  query = "SELECT MAX(ID) FROM %s;" %(url)
  rows = run_query(query)
  
  # Check for ID
  for row in rows:
    if (row[0] != None):
      id = int(row[0]) + 1
    else:
      id = 1
      break
  
  # Return ID    
  return id



### Function geo_check = Geo-Location checking
def geo_check(address_part, fallback, language = 'en'):
  ## Geocoder gets coordinates related to the current IP address
  g = geocoder.ip('me')
  
  
  ## Geopy
  # Calling the Nominatim tool
  loc = Nominatim(user_agent = "GetLoc", timeout = 6)
  geolocator = Nominatim(user_agent = "geoapiExercises")
  
  # Get City name
  try:
    geolocator.reverse(g.latlng, language = language)
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



### Function: generateID = Generates an 5-digits ID
def generateID(id):
  if (id < 10):
    generated_id = '0000' + str(id)
  elif (id < 100):
    generated_id = '000' + str(id)
  elif (id < 1000):
    generated_id = '00' + str(id)
  elif (id < 10000):
    generated_id = '0' + str(id)
    
  # Return the 5-digit ID
  return(generated_id)
  



#### Sidebar
### Workshop Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')


## Ask for language
lang = st.sidebar.selectbox('In which language should Ben answer?', ('BG', 'CS', 'DA', 'DE', 'EL', 'EN-GB', 'ES', 'ET', 'FI', 'FR', 'HU', 'IT', 'JA', 'LT', 'LV', 'NL', 'PL', 'PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'ZH'), index = 5, key = 'lang')




#### Main Program
### Chat Bot Ben
## Header
st.title('Workshop page')
st.subheader('Ben chatbot')


## Global variables
answer = ''
question_id = '' #st.session_state['question_id']
handbook_id = '' #st.session_state['handbook_id']



### Form
with st.form('Input', clear_on_submit = False):
  ## Columns
  col1, col2 = st.columns(2)
  
  
  if (st.session_state['feedback'] == False):
    ## Column 1
    with col1:
      ### Implementation of OpenAI
      ## Open databank connection
      conn = init_connection()
      
      ## Get categories and sub-categories
      query = "SELECT CATEGORY_ID, CATEGORY_DESCRIPTION, CATEGORY_SUB_ID, CATEGORY_SUB_DESCRIPTION FROM benbox.CATEGORIES;"
      rows = run_query(query)
      
      # Filling variables   
      categories = []
      sub_categories = []
      categories_id = []
      sub_categories_id = []
      for row in rows:
        if (row[0] != None):
          categories.append(row[1])
          categories_id.append(row[0])
        else:
          sub_categories.append(row[3])
          sub_categories_id.append(row[2])
        
        
      ## Category menu
      category = st.selectbox(label = 'Please choose the category of the question (if unknown, choose \"General\"', options = range(len(categories)), format_func = lambda x: categories[x])
      
      
      ## Sub-Category menu
      sub_category = st.selectbox(label = 'Please choose the sub-category of the question', options = range(len(sub_categories)), format_func = lambda x: sub_categories[x])
      
      
      ## User question
      user_question = st.text_input(label = 'What do you want to ask Ben?')
      
      
    ## Submit button
    submitted = st.form_submit_button("Ask Ben")
    if submitted:
      ## Get response from openai
      # Set API key
      openai.api_key = st.secrets['openai']['key']
      
      
      ## Call geo_check function with params
      city = geo_check(address_part = 'city', fallback = 'Lilongwe', language = lang[:2].lower())
      
      
      try:
        ## Doing the requests to OpenAI for summarizing / keyword extracting the question
        # Summary
        summary_question = 'A User asks in the category \"' + categories[category] + '\" and the sub-category"' + sub_categories[sub_category] + '" about this question: \"' + user_question + '" Please summarise it to a statement in no more than three words.'
        response_summary = openai.Completion.create(model = "text-davinci-003", prompt = summary_question, temperature = 0.3, max_tokens = 64, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
        summary = response_summary['choices'][0]['text'].lstrip()
        summary = summary.replace('.', '')
        
        # Find the keyword1
        keyword_question = 'Extract one one-word keyword of the beginning of the text which is a noun without the accompanying article and pronoun: \"' + user_question + '"'
        response_keyword = openai.Completion.create(model = "text-curie-001", prompt = keyword_question, temperature = 0.0, max_tokens = 64, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
        keyword1 = response_keyword['choices'][0]['text'].lstrip()
        keyword1 = keyword1.capitalize()
        
        # Find the 4 other keywords 
        keywords_question = 'Extract four one-word keywords which are not the same as \"' + keyword1 + '\"' + ' of this text: \"' + user_question + '" Please indicate your answer separated by commas.'
        response_keywords = openai.Completion.create(model = "text-davinci-003", prompt = keywords_question, temperature = 0.0, max_tokens = 64, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
        keywords = response_keywords['choices'][0]['text']
        
        
        ## Cleaning response
        # Create array out of comma seperated string
        keywords = keywords.split(',')
        for i in range(4):
          # Remove leading space
          keywords[i] = keywords[i].strip()
          keywords[i] = keywords[i].lstrip()
          
          # Delete '.' in strings
          keywords[i] = keywords[i].replace('.', '')
          
          # Just keep first word
          if (len(keywords[i]) >= 1):
            keywords[i] = keywords[i].split()[0]
            
          # Capitalize
          keywords[i] = keywords[i].capitalize()
          
          
        ## Writing responses to table `QUESTIONS` in database `benbox`
        # Get latest ID from database
        id = lastID(url = '`benbox`.`QUESTIONS`')
          
        # Pollute `QUESTION_ID`
        question_id = generateID(id)
        st.session_state['question_id'] = question_id
          
        # Write question to table `QUESTIONS`
        query = "INSERT INTO `benbox`.`QUESTIONS`(ID, QUESTION_ID, CATEGORY_ID, CATEGORY_SUB_ID, QUESTION_KEYWORD1, QUESTION_KEYWORD2, QUESTION_KEYWORD3, QUESTION_KEYWORD4, QUESTION_KEYWORD5, QUESTION_SUMMARY, QUESTION_TEXT, QUESTION_TEXT_LANGUAGE) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(id, question_id, categories_id[category], sub_categories_id[sub_category], keyword1, keywords[0], keywords[1], keywords[2], keywords[3], summary, user_question, lang[:2].lower())
        run_query(query)
        conn.commit()
        
        
        ## Get handbook data to answer from table `HANDBOOK_USER`
        query = "SELECT ID, ID, HANDBOOK_ID, CATEGORY_ID, CATEGORY_SUB_ID, HANDBOOK_KEYWORD1, HANDBOOK_KEYWORD2, HANDBOOK_KEYWORD3, HANDBOOK_KEYWORD4, HANDBOOK_KEYWORD5, HANDBOOK_SUMMARY, HANDBOOK_TEXT, HANDBOOK_TEXT_HEADLINE, HANDBOOK_HITS FROM benbox.HANDBOOK_USER WHERE HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s' OR CATEGORY_ID = '%s' OR CATEGORY_SUB_ID = '%s';" % (keyword1, keywords[0], keywords[1], keywords[2], keywords[3], keyword1, keywords[0], keywords[1], keywords[2], keywords[3], keyword1, keywords[0], keywords[1], keywords[2], keywords[3], keyword1, keywords[0], keywords[1], keywords[2], keywords[3], keyword1, keywords[0], keywords[1], keywords[2], keywords[3], categories_id[category], sub_categories_id[sub_category])
        rows = run_query(query)
        databank_handbook = pd.DataFrame(columns = ['ID_Index', 'ID', 'HANDBOOK_ID', 'CATEGORY_ID', 'CATEGORY_SUB_ID', 'HANDBOOK_KEYWORD1', 'HANDBOOK_KEYWORD2', 'HANDBOOK_KEYWORD3', 'HANDBOOK_KEYWORD4', 'HANDBOOK_KEYWORD5', 'HANDBOOK_SUMMARY', 'HANDBOOK_TEXT', 'HANDBOOK_TEXT_HEADLINE', 'HANDBOOK_HITS'])
        for row in rows:
          df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]]], columns = ['ID_Index', 'ID', 'HANDBOOK_ID', 'CATEGORY_ID', 'CATEGORY_SUB_ID', 'HANDBOOK_KEYWORD1', 'HANDBOOK_KEYWORD2', 'HANDBOOK_KEYWORD3', 'HANDBOOK_KEYWORD4', 'HANDBOOK_KEYWORD5', 'HANDBOOK_SUMMARY', 'HANDBOOK_TEXT', 'HANDBOOK_TEXT_HEADLINE', 'HANDBOOK_HITS'])
          databank_handbook = pd.concat([databank_handbook, df])
        databank_handbook = databank_handbook.set_index('ID_Index')
  
      
        ## Checking if handbook data was found
        if (len(databank_handbook) > 0):     
          # Adding keyword1 at first position
          keywords.insert(0, keyword1)
            
                
          ## Loop through all matches
          for x in range(len(databank_handbook)):
            handbook = databank_handbook.iloc[x]
                  
            # Add importance through `HANDBOOK_HITS` value
            counter = 0 + handbook[12]
              
                  
            ## Check for matching category and sub-category
            if (handbook[2] == categories_id[category]):
              counter += 3
              if (handbook[3] == sub_categories_id[sub_category]):
                counter += 5
              
                
            ## Counting matching words in summary (score 4 per hit)
            string1_words = set(handbook[9].split())
            string2_words = set(summary.split())
            
            # Remove unwanted characters
            unwanted_characters = ".,!?"
            string1_words = {word.strip(unwanted_characters) for word in string1_words}
            string2_words = {word.strip(unwanted_characters) for word in string2_words}
            
            # Check for matching words
            matches = string1_words & string2_words
            
            # Adding matching words to `counter`
            counter += 4 * len(matches)
            
            
            ## Counting matching words in headline (score 3 per hit)
            string1_words = set(handbook[11].split())
            string2_words = set(summary.split())
            
            # Remove unwanted characters
            unwanted_characters = ".,!?"
            string1_words = {word.strip(unwanted_characters) for word in string1_words}
            string2_words = {word.strip(unwanted_characters) for word in string2_words}
            
            # Check for matching words
            matches = string1_words & string2_words
            
            # Adding matching words to `counter`
            counter += 3 * len(matches)
            
            
            ## Counting matching words in text (score 1 per hit)
            string1_words = set(handbook[10].split())
            string2_words = set(user_question.split())
            
            # Remove unwanted characters
            unwanted_characters = ".,!?"
            string1_words = {word.strip(unwanted_characters) for word in string1_words}
            string2_words = {word.strip(unwanted_characters) for word in string2_words}
            
            # Check for matching words
            matches = string1_words & string2_words
            
            # Adding matching words to `counter`
            counter += len(matches)
              
                
            ## Do the keyword matching through all keywords
            for i in range(5):
              # First keyword gets highest score
              if handbook[4].capitalize() == keywords[i]:
                counter += 9
                    
              # Second and third get medium score
              if handbook[5].capitalize() == keywords[i]:
                counter += 8
              if handbook[6].capitalize() == keywords[i]:
                counter += 7
                      
              # Fourth and fith geth lowest score
              if handbook[7].capitalize() == keywords[i]:
                counter += 6
              if handbook[8].capitalize() == keywords[i]:
                counter += 5
              databank_handbook['HANDBOOK_HITS'][handbook[0]] = counter
                      
           
          ## Sorting highest score ('HANDBOOK_HITS') descending         
          databank_handbook = databank_handbook.sort_values('HANDBOOK_HITS', ascending = False)
          handbook = databank_handbook._get_value(databank_handbook.iloc[0][0], 'HANDBOOK_TEXT')
          handbook_id = databank_handbook._get_value(databank_handbook.iloc[0][0], 'HANDBOOK_ID')
          
          # Add handbook entries which scored with difference under 15%
          for i in range(len(databank_handbook) - 1):
            if (databank_handbook._get_value(databank_handbook.iloc[i + 1][0], 'HANDBOOK_HITS') / databank_handbook._get_value(databank_handbook.iloc[0][0], 'HANDBOOK_HITS') >= 0.85):
              handbook = handbook + ' ' + databank_handbook._get_value(databank_handbook.iloc[i + 1][0], 'HANDBOOK_TEXT')
          
            
          ## Debugging output
          st.write(databank_handbook)
          st.write(handbook)
          
          
          ## Doing the request to OpenAI for answering the question
          # Answer
          answer_question = 'The user handbook contains following information: \"' + handbook + '\". Right now you are in the city called \"' + city + '\". Please answer following user question: \"' + user_question + '\"'
          response_answer = openai.Completion.create(model = "text-davinci-003", prompt = answer_question, temperature = 0.5, max_tokens = 128, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
          answer = response_answer['choices'][0]['text'].lstrip()
          st.session_state['answer'] = answer
          
        else:
          answer = 'Unfortunately we have not found the answer to your question.' 
          st.session_state['answer'] = answer
        
      except:
        print('An exception occurred in `OpenAI`')
        answer = 'Unfortunately we have not found the answer to your question.'
        st.session_state['answer'] = answer
        
  else:
    submitted = st.form_submit_button('Press button to empty form for a new request')
    if submitted:
      # Set session states
      st.session_state['feedback'] = False
      st.session_state['answer'] = ''
      
      # Rerun
      st.experimental_rerun()

    
  ## Column 2
  with col2:
    st.image("images/Ben.png")
    
  
  
### Outside the form
## Give the answer
answer = st.session_state['answer']

if (st.session_state['feedback'] == False):
  if (len(answer) > 0):
    st.write(':blue[Ben:] ', answer)
  
  
    ## Writing to database if it was useful
    if (answer != 'Unfortunately we have not found the answer to your question.'):
      # Ask if it was useful
      st.write(':orange[Was this answer useful?]')
      
      
      ## Write to table `FAQ` if it was useful
      if (st.session_state['feedback'] == False):
        if st.button(label = 'Yes'):
          # Set session state `feedback`
          st.session_state['feedback'] = True
            
          # Get latest ID from table
          id = lastID(url = '`benbox`.`FAQ`')
          
          # Pollute `FAQ_ID`
          faq_id = generateID(id = id)
            
          # Pollute `QUESTION_ID`
          question_id = st.session_state['question_id']
            
          # Pollute `HANDBOOK_ID`
          handbook_id = st.session_state['handbook_id']
            
          # Pollute `FAQ_ANSWER`
          answer = st.session_state['answer']
            
          # Summarising the answer
          answer_summary_question = 'Please summarise this text in no more than seven words: \"' + answer + '\"'
          response_answer_summary = openai.Completion.create(model = "text-curie-001", prompt = answer_summary_question, temperature = 0.3, max_tokens = 128, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
          answer_summary = response_answer_summary['choices'][0]['text'].lstrip()
              
          # Write question to table `FAQ`
          query = "INSERT INTO `benbox`.`FAQ`(ID, QUESTION_ID, HANDBOOK_ID, FAQ_ID, FAQ_ANSWER, FAQ_ANSWER_SUMMARY, FAQ_ANSWER_LANGUAGE, FAQ_HITS) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', %s);" %(id, question_id, handbook_id, faq_id, answer, answer_summary, lang[:2].lower(), 0)
          run_query(query)
          conn.commit()
          
          # Rerun
          st.experimental_rerun()
      
        
      ## Clear form if negative feedback received
      if (st.session_state['feedback'] == False):
        if st.button(label = 'No'):
          # Set session state `feedback`
          st.session_state['feedback'] = True
          
          # Rerun
          st.experimental_rerun()
        
        else:
          if (st.session_state['feedback'] == False):
            st.write('(Your feedback will be recorded)')

      
## Response after feedback was given to user
if (st.session_state['feedback'] == True):
  st.info(body = 'Thanks for your feedback, it was recorded.', icon = 'ℹ️')
