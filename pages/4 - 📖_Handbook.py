##### `pages/4 - 📖_Handbook.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import mysql.connector
import openai
import geocoder
from geopy.geocoders import Nominatim
import sys
from datetime import date
sys.path.insert(1, "pages/functions/")
from functions import header
from functions import check_password
from functions import logout
from functions import load_file
from functions import export_docx
from functions import generateID
from network import trans
from network import send_mail




#### Streamlit initial setup
st.set_page_config(
  page_title = "Handbook",
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
## Session state
if ('admin' not in st.session_state):
  st.session_state['admin'] = False
if ('logout' not in st.session_state):
  st.session_state['logout'] = False
if ('header' not in st.session_state):
  st.session_state['header'] = True
  
  
## Answer states
if ('answer_done' not in st.session_state):
  st.session_state['answer_done'] = False
if ('answer' not in st.session_state):
  st.session_state['answer'] = ''
if ('answer_score' not in st.session_state):
  st.session_state['answer_score'] = 0.0
  
  
## Feedback state
if ('feedback' not in st.session_state):
  st.session_state['feedback'] = False
  
  
## Session state for writing to table `FAQ` and `ANSWERS`
if ('question_id' not in st.session_state):
  st.session_state['question_id'] = ''
if ('handbook_id' not in st.session_state):
  st.session_state['handbook_id'] = ''
if ('answer_id' not in st.session_state):
  st.session_state['answer_id'] = ''
if ('handbook_text' not in st.session_state):
  st.session_state['handbook_text'] = ''
  
  
## Chapter state for handbook
if ('chapter' not in st.session_state):
  st.session_state['chapter'] = 1




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
      
      

### Function: pictureUploader = uploads handbook images
def pictureUploader(image, index):
  # Initialize connection
  connection = mysql.connector.connect(**st.secrets["mysql_benbox"])
  cursor = connection.cursor()
  
  # SQL statement
  sql_insert_blob_query = """ UPDATE `HANDBOOK_USER` SET HANDBOOK_IMAGE = %s WHERE ID = %s;"""
  
  # Convert data into tuple format
  insert_blob_tuple = (image, index)
  result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
  connection.commit()
      
      
      
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



### Function faq = Shows FAQ 
def faq():
  with st.expander('FAQ', expanded = False):
    st.header('FAQ')
    st.write('Here you will find all frequently asked questions.')
    
    
    ## Get categories and sub-categories
    # Open databank connection
    conn = init_connection()
    
    # Run query
    query = "SELECT CATEGORY_ID, CATEGORY_DESCRIPTION, CATEGORY_SUB_ID, CATEGORY_SUB_DESCRIPTION FROM benbox.CATEGORIES;"
    rows = run_query(query)
    
    # Filling variables
    filter_cat = []
    filter_sub = []
    categories = []
    sub_categories = []
    categories_id = []
    sub_categories_id = []
    for row in rows:
      if (row[0] != None):
        categories.append(row[1])
        categories_id.append(row[0])
        filter_cat.append(True)
      else:
        sub_categories.append(row[3])
        sub_categories_id.append(row[2])
        filter_sub.append(True)
    
    
    ## Columns
    col1, col2 = st.columns(2)
    
    
    ## Column 1
    with col1:
      ## Checkboxen for filtering
      st.subheader('Filter')
      
      
      ## Categories
      st.write('**:orange[Categories:]** ')
      for i in range(len(categories)):
        filter_cat[i] = st.checkbox(label = categories[i], value = True)
      
      # Write category ids into array for checking
      filter_cat_ids = []  
      for i in range(len(filter_cat)):
        if filter_cat[i] == True:
          filter_cat_ids.append(categories_id[i])
    
    
      ## Sub-categories
      st.write('**Sub-categories:** ')
      for i in range(len(sub_categories)):
        filter_sub[i] = st.checkbox(label = sub_categories[i], value = True)
        
      # Write sub-category ids into array for checking
      filter_sub_ids = []  
      for i in range(len(filter_sub)):
        if filter_sub[i] == True:
          filter_sub_ids.append(sub_categories_id[i])
      
      
    ## Column 2
    with col2:
      st.subheader('Questions & answers')
        
      
      ## Get FAQ
      query = "SELECT que.QUESTION_TEXT, ans.ANSWER_ID, ans.ANSWER_TEXT, ans.ANSWER_SCORE, ans.ANSWER_APPROVED, cat.CATEGORY_DESCRIPTION, catsub.CATEGORY_SUB_DESCRIPTION, que.CATEGORY_ID, que.CATEGORY_SUB_ID, faq.FAQ_DATE FROM benbox.FAQ AS faq LEFT JOIN benbox.QUESTIONS AS que ON que.QUESTION_ID = faq.QUESTION_ID LEFT JOIN benbox.CATEGORIES AS cat ON cat.CATEGORY_ID = que.CATEGORY_ID LEFT JOIN benbox.CATEGORIES AS catsub ON catsub.CATEGORY_SUB_ID = que.CATEGORY_SUB_ID LEFT JOIN benbox.ANSWERS AS ans ON faq.ANSWER_ID = ans.ANSWER_ID;"
      faq = run_query(query)
     
      
      ## Showing expander
      # Check if data is existend
      if (faq != None):
        for i in range(len(faq)):
          for x in range(len(filter_cat_ids)):
            if faq[i][7] == filter_cat_ids[x]:
              for y in range(len(filter_sub_ids)):
                if faq[i][8] == filter_sub_ids[y]:
                  if faq[i][4] == 1:
                    st.write('**\"' + faq[i][0].upper() + '\"**')
                    st.write('**:orange[Category:]** ' + faq[i][5])
                    st.write('**Sub-category:** ' + faq[i][6])
                    st.write('**:blue[Ben`s answer:]** ' + faq[i][2])
                    if faq[i][3] >= 0.85:
                      st.write('**:green[Score ' + str(format(faq[i][3], '.0%')) + ']**')
                    elif faq[i][3] >= 0.7:
                      st.write('**:orange[Score ' + str(format(faq[i][3], '.0%')) + ']**')
                    else:
                      st.write('**:red[Score ' + str(format(faq[i][3], '.0%')) + ']**')
                    st.write('-------------')
                    
      # No data existend
      else:
        st.write('No questions & answer available')



### Function ben = Chat-Bot Ben
def ben():
  with st.expander(label = 'Chat-Bot Ben', expanded = True):
    st.header('Chat-Bot Ben')
    st.write('You can ask Ben questions here.')
    
    
    ## Global variables
    answer = ''
    question_id = '' #st.session_state['question_id']
    handbook_id = '' #st.session_state['handbook_id']
    
    
    ## Form
    with st.form('Chat-Bot', clear_on_submit = False):
      ## Ask for language in sidebar
      lang = st.sidebar.selectbox('In which language should Ben answer?', ('BG', 'CS', 'DA', 'DE', 'EL', 'EN-GB', 'ES', 'ET', 'FI', 'FR', 'HU', 'IT', 'JA', 'LT', 'LV', 'NL', 'PL', 'PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'ZH'), index = 5, key = 'lang')
  
      ## Columns
      col1, col2 = st.columns(2)
      
      
      if (st.session_state['feedback'] == False):
        ## Column 1
        with col1:
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
          category = st.selectbox(label = 'Please choose the category of the question', options = range(len(categories)), format_func = lambda x: categories[x])
          
          
          ## Sub-Category menu
          sub_category = st.selectbox(label = 'Please choose the sub-category of the question', options = range(len(sub_categories)), format_func = lambda x: sub_categories[x])
          
          
          ## User question
          user_question = st.text_input(label = 'What do you want to ask Ben?')
          
          
        ## Submit button
        submitted = st.form_submit_button("Ask Ben")
        if submitted:
          ## Using ChatGPT from OpenAI
          # Set API key
          openai.api_key = st.secrets['openai']['key']
          
          
          ## Call geo_check function with params
          city = geo_check(address_part = 'city', fallback = 'Lilongwe', language = lang[:2].lower())
          
          
          try:
            ## Doing the requests to OpenAI for summarizing / keyword extracting the question
            # Creating summary of user question
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
            # Create keywords array out of comma seperated string
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
            st.session_state['answer_done'] = False
            
            
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
              st.session_state['handbook_text'] = databank_handbook._get_value(databank_handbook.iloc[0][0], 'HANDBOOK_TEXT')
              st.session_state['handbook_id'] = databank_handbook._get_value(databank_handbook.iloc[0][0], 'HANDBOOK_ID')
              st.session_state['answer_score'] = databank_handbook._get_value(databank_handbook.iloc[0][0], 'HANDBOOK_HITS')
              
              # From abolute figures to percentages
              st.session_state['answer_score'] = round((st.session_state['answer_score'] / 100) * 3.333, 2)
              
              # Add handbook entries which scored with difference under 15%
              for i in range(len(databank_handbook) - 1):
                if (databank_handbook._get_value(databank_handbook.iloc[i + 1][0], 'HANDBOOK_HITS') / databank_handbook._get_value(databank_handbook.iloc[0][0], 'HANDBOOK_HITS') >= 0.85):
                  st.session_state['handbook_text'] = st.session_state['handbook_text'] + ' ' + databank_handbook._get_value(databank_handbook.iloc[i + 1][0], 'HANDBOOK_TEXT')
                  
                  # Adding 10% to score for each concatenation
                  st.session_state['answer_score'] += 0.1  
                  
              # Limiting score to 100%
              if st.session_state['answer_score'] > 1:
                st.session_state['answer_score'] = 1  
              
              
              ## Debugging output
              st.write(databank_handbook)
              st.write(st.session_state['handbook_text'])
              st.write(st.session_state['answer_score'])
              
              
              ## Doing the request to OpenAI for answering the question
              answer_question = 'The user handbook contains following information: \"' + st.session_state['handbook_text'] + '\". Right now you are in the city called \"' + city + '\". Please answer following user question: \"' + user_question + '\"'
              response_answer = openai.Completion.create(model = "text-davinci-003", prompt = answer_question, temperature = 0.5, max_tokens = 128, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
              answer = response_answer['choices'][0]['text'].lstrip()
          
              # Store the answer in session state
              st.session_state['answer'] = answer
            
            
            ## No handbook data found  
            else:
              answer = 'Unfortunately we have not found the answer to your question.'
              
              # Store the answer in session state
              st.session_state['answer'] = answer
          
          
          ## Error
          except:
            print('An exception occurred in `OpenAI`')
            answer = 'Unfortunately we have not found the answer to your question.'
            
            # Store the answer in session state
            st.session_state['answer'] = answer
          
      
      ## Feedback was given, show `empty form` button     
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
        
      
    ## Give the answer (Outside the form)
    if (st.session_state['feedback'] == False):
      if (len(st.session_state['answer']) > 0):
        st.write('**:blue[Ben:]** ' + st.session_state['answer'] + ' **(Score = ' + str(format(st.session_state['answer_score'], '.0%')) + ')**' )
      
        
        ## Write every answer to table `ANSWERS`
        if (st.session_state['answer_done'] == False):
          # Get latest ID from table
          id = lastID(url = '`benbox`.`ANSWERS`')
          
          # Populate `ANSWER_ID`
          st.session_state['answer_id'] = generateID(id = id)
          
          # Writing the answer
          query = "INSERT INTO `benbox`.`ANSWERS`(ID, ANSWER_ID, QUESTION_ID, HANDBOOK_ID, ANSWER_TEXT, ANSWER_HANDBOOK_TEXT, ANSWER_SCORE, ANSWER_APPROVED, ANSWER_DATE) VALUES (%s, '%s', '%s', '%s', '%s', '%s', %s, 0, '%s');" %(id, st.session_state['answer_id'], st.session_state['question_id'], st.session_state['handbook_id'], st.session_state['answer'], st.session_state['handbook_text'], st.session_state['answer_score'], date.today())
          run_query(query)
          conn.commit()
          
          # Set to true to prevent duplicate in table
          st.session_state['answer_done'] = True
              
              
        ## Write to database if it was useful
        if (st.session_state['answer'] != 'Unfortunately we have not found the answer to your question.'):
          # Ask if it was useful
          st.write(':orange[Was this answer useful?]')
          
          
          ## Writing to table `FAQ` if it was useful
          if (st.session_state['feedback'] == False):
            if st.button(label = 'Yes'):
              # Set session state `feedback`
              st.session_state['feedback'] = True
              
              # Get latest ID from table
              id = lastID(url = '`benbox`.`FAQ`')
                
              # Write question to table `FAQ`
              query = "INSERT INTO `benbox`.`FAQ`(ID, FAQ_ID, QUESTION_ID, HANDBOOK_ID, ANSWER_ID, FAQ_HITS, FAQ_DATE) VALUES (%s, '%s', '%s', '%s', '%s', %s, '%s');" %(id, generateID(id = id), st.session_state['question_id'], st.session_state['handbook_id'], st.session_state['answer_id'], 0, date.today())
              run_query(query)
              conn.commit()
              
              # Send mail to admin
              send_mail(subject = 'Please review new FAQ item!', body = 'Hello Admin,\n\nthis is a request to review an new item from ' + str(date.today()) + ' in the FAQ database table.\n\nBest regards\n\nStreamlit' , receiver = st.secrets['custom']['contact_admin'])
              
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



### Function book = Handbook
def book():
  with st.expander(label = 'Handbook', expanded = False):
    st.header('Handbook ')
    st.write('Here you can export the handbook as a Word document.')
    
    
    ## Docx export
    if st.button(label = 'Export handbook'):
      ## Get handbook data to export from table `HANDBOOK_USER`
      query = "SELECT han.ID, han.HANDBOOK_CHAPTER, str.HANDBOOK_CHAPTER_DESCRIPTION, str.HANDBOOK_CHAPTER_TEXT, han.HANDBOOK_PARAGRAPH, stp.HANDBOOK_PARAGRAPH_DESCRIPTION, stp.HANDBOOK_PARAGRAPH_TEXT, cat.CATEGORY_DESCRIPTION, sub.CATEGORY_SUB_DESCRIPTION, han.HANDBOOK_KEYWORD1, han.HANDBOOK_KEYWORD2, han.HANDBOOK_KEYWORD3, han.HANDBOOK_KEYWORD4, han.HANDBOOK_KEYWORD5, han.HANDBOOK_SUMMARY, han.HANDBOOK_TEXT, han.HANDBOOK_TEXT_HEADLINE, han.HANDBOOK_IMAGE_TEXT, han.HANDBOOK_IMAGE FROM benbox.HANDBOOK_USER AS han LEFT JOIN benbox.CATEGORIES AS cat ON cat.CATEGORY_ID = han.CATEGORY_ID LEFT JOIN benbox.CATEGORIES AS sub ON sub.CATEGORY_SUB_ID = han.CATEGORY_SUB_ID LEFT JOIN benbox.HANDBOOK_CHAPTER_STRUCTURE AS str ON str.HANDBOOK_CHAPTER = han.HANDBOOK_CHAPTER LEFT JOIN benbox.HANDBOOK_PARAGRAPH_STRUCTURE AS stp ON stp.HANDBOOK_PARAGRAPH = han.HANDBOOK_PARAGRAPH;"
      rows = run_query(query)
      databank_handbook = pd.DataFrame(columns = ['ID', 'HANDBOOK_CHAPTER', 'HANDBOOK_CHAPTER_DESCRIPTION', 'HANDBOOK_CHAPTER_TEXT', 'HANDBOOK_PARAGRAPH', 'HANDBOOK_PARAGRAPH_DESCRIPTION', 'HANDBOOK_PARAGRAPH_TEXT', 'CATEGORY', 'CATEGORY_SUB', 'HANDBOOK_KEYWORD1', 'HANDBOOK_KEYWORD2', 'HANDBOOK_KEYWORD3', 'HANDBOOK_KEYWORD4', 'HANDBOOK_KEYWORD5', 'HANDBOOK_SUMMARY', 'HANDBOOK_TEXT', 'HANDBOOK_TEXT_HEADLINE', 'HANDBOOK_IMAGE_TEXT', 'HANDBOOK_IMAGE'])
      for row in rows:
        df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]]], columns = ['ID', 'HANDBOOK_CHAPTER', 'HANDBOOK_CHAPTER_DESCRIPTION', 'HANDBOOK_CHAPTER_TEXT', 'HANDBOOK_PARAGRAPH', 'HANDBOOK_PARAGRAPH_DESCRIPTION', 'HANDBOOK_PARAGRAPH_TEXT', 'CATEGORY', 'CATEGORY_SUB', 'HANDBOOK_KEYWORD1', 'HANDBOOK_KEYWORD2', 'HANDBOOK_KEYWORD3', 'HANDBOOK_KEYWORD4', 'HANDBOOK_KEYWORD5', 'HANDBOOK_SUMMARY', 'HANDBOOK_TEXT', 'HANDBOOK_TEXT_HEADLINE', 'HANDBOOK_IMAGE_TEXT', 'HANDBOOK_IMAGE'])
        databank_handbook = pd.concat([databank_handbook, df])
      databank_handbook = databank_handbook.set_index('ID')
      
      
      ## Get FAQ
      query = "SELECT que.QUESTION_TEXT, faq.FAQ_ANSWER, cat.CATEGORY_DESCRIPTION, catsub.CATEGORY_SUB_DESCRIPTION, que.CATEGORY_ID, que.CATEGORY_SUB_ID FROM benbox.FAQ AS faq LEFT JOIN benbox.QUESTIONS AS que ON que.QUESTION_ID = faq.QUESTION_ID LEFT JOIN benbox.CATEGORIES AS cat ON cat.CATEGORY_ID = que.CATEGORY_ID LEFT JOIN benbox.CATEGORIES AS catsub ON catsub.CATEGORY_SUB_ID = que.CATEGORY_SUB_ID;"
      faq = run_query(query)
      
      
      ## Export docx file
      export_docx(data = databank_handbook, faq = faq, docx_file_name = 'Handbook.docx')



     
#### Main Program
### Open databank connection
conn = init_connection()



### Logged in state (Handbook)
if check_password():
  ### Header
  header(title = 'Handbook page', data_desc = 'handbooks', expanded = st.session_state['header']) 
  
  
  
    ### FAQ
  faq()
  
  
  
  ### Chat-Bot Ben
  ben()
      
  
  
  ### Handbook
  book()
  
  
  
  ### Chapter and paragraph structures
  ## Get chapter structure
  # Run query
  query = "SELECT ID, HANDBOOK_CHAPTER, HANDBOOK_CHAPTER_DESCRIPTION, HANDBOOK_CHAPTER_TEXT FROM benbox.HANDBOOK_CHAPTER_STRUCTURE;"
  rows = run_query(query)
  databank_chapter = pd.DataFrame(columns = ['ID', 'HANDBOOK_CHAPTER', 'HANDBOOK_CHAPTER_DESCRIPTION', 'HANDBOOK_CHAPTER_TEXT'])
  for row in rows:
    df = pd.DataFrame([[row[0], row[1], row[2], row[3]]], columns = ['ID', 'HANDBOOK_CHAPTER', 'HANDBOOK_CHAPTER_DESCRIPTION', 'HANDBOOK_CHAPTER_TEXT'])
    databank_chapter = pd.concat([databank_chapter, df])
  databank_chapter = databank_chapter.set_index('ID')
  
  # Sort chapters
  databank_chapter = databank_chapter.sort_values('HANDBOOK_CHAPTER', ascending = True)
  chapters = list(databank_chapter['HANDBOOK_CHAPTER'])
  chapters_str = map(str, chapters)
  chapters_desc = list(databank_chapter['HANDBOOK_CHAPTER_DESCRIPTION'])
  
  # Concatenate the two strings
  chapters_desc = [' ' + str(row) for row in chapters_desc]
  chapters_combo = [i + j for i, j in zip(chapters_str, chapters_desc)]
  
  
  ## Show chapter structure in expander
  with st.expander(label = 'Handbook chapters', expanded = False):
    st.header('Handbook chapters')
    st.write('Here you will find all chapters of the handbook.')
    st.write(databank_chapter)
    
    
    ## Input for new handbook chapter structure data
    with st.form('Chapter', clear_on_submit = True):
      st.subheader('New chapter entry')
      
      # Get latest ID from table
      id = lastID(url = '`benbox`.`HANDBOOK_CHAPTER_STRUCTURE`')
      st.text_input(label = 'ID', value = id, disabled = True)
      
      # Inputs
      handbook_chapter_structure_chapter = st.text_input(label = 'Chapter')
      handbook_chapter_structure_chapter_desc = st.text_input(label = 'Description')
      handbook_chapter_structure_chapter_text = st.text_input(label = 'Text')
      
      
      ## Submit button
      submitted = st.form_submit_button("Submit")
      if submitted:
        # Write entry to table `HANDBOOK_CHAPTER_STRUCTURE`
        query = "INSERT INTO `benbox`.`HANDBOOK_CHAPTER_STRUCTURE`(ID, HANDBOOK_CHAPTER, HANDBOOK_CHAPTER_DESCRIPTION, HANDBOOK_CHAPTER_TEXT) VALUES (%s, '%s', '%s', '%s');" %(id, handbook_chapter_structure_chapter, handbook_chapter_structure_chapter_desc, handbook_chapter_structure_chapter_text)
        run_query(query)
        conn.commit()
        
        # Rerun
        st.experimental_rerun()
        
  
  ## Get paragraph structure
  query = "SELECT ID, HANDBOOK_PARAGRAPH, HANDBOOK_PARAGRAPH_DESCRIPTION, HANDBOOK_PARAGRAPH_TEXT FROM benbox.HANDBOOK_PARAGRAPH_STRUCTURE;"
  rows = run_query(query)
  databank_paragraph = pd.DataFrame(columns = ['ID', 'HANDBOOK_PARAGRAPH', 'HANDBOOK_PARAGRAPH_DESCRIPTION', 'HANDBOOK_PARAGRAPH_TEXT'])
  for row in rows:
    df = pd.DataFrame([[row[0], str(row[1]).strip('0'), row[2], row[3]]], columns = ['ID', 'HANDBOOK_PARAGRAPH', 'HANDBOOK_PARAGRAPH_DESCRIPTION', 'HANDBOOK_PARAGRAPH_TEXT'])
    databank_paragraph = pd.concat([databank_paragraph, df])
  databank_paragraph = databank_paragraph.set_index('ID')
  
  # Sort paragraphs
  databank_paragraph = databank_paragraph.sort_values('HANDBOOK_PARAGRAPH', ascending = True)
  paragraphs = list(databank_paragraph['HANDBOOK_PARAGRAPH'])
  paragraphs_desc = list(databank_paragraph['HANDBOOK_PARAGRAPH_DESCRIPTION'])
  paragraphs_list = []
  paragraphs_desc_list = []
  for i in range(len(paragraphs)):
    if int(paragraphs[i][0]) == st.session_state['chapter']:
      paragraphs_list.append(paragraphs[i])
      paragraphs_desc_list.append(paragraphs_desc[i])
      
  # Concatenate the two strings
  paragraphs_desc_list = [' ' + row for row in paragraphs_desc_list]
  paragraphs_combo = [i + j for i, j in zip(paragraphs_list, paragraphs_desc_list)]
  
  
  ## Show paragraph structure in expander
  with st.expander(label = 'Handbook paragraphs', expanded = False):
    st.header('Handbook paragraphs')
    st.write('Here you will find all paragraphs of the handbook.')
    st.write(databank_paragraph)
    
    
    ## Input for new handbook paragraph structure data
    with st.form('Paragraph', clear_on_submit = True):
      st.subheader('New paragraph entry')
      
      # Get latest ID from table
      id = lastID(url = '`benbox`.`HANDBOOK_PARAGRAPH_STRUCTURE`')
      st.text_input(label = 'ID', value = id, disabled = True)
      
      # Inputs
      handbook_paragraph_structure_paragraph = st.text_input(label = 'Paragraph')
      handbook_paragraph_structure_paragraph_desc = st.text_input(label = 'Description')
      handbook_paragraph_structure_paragraph_text = st.text_input(label = 'Text')
      
      
      ## Submit button
      submitted = st.form_submit_button("Submit")
      if submitted:
        # Write entry to table `HANDBOOK_PARAGRAPH_STRUCTURE`
        query = "INSERT INTO `benbox`.`HANDBOOK_PARAGRAPH_STRUCTURE`(ID, HANDBOOK_PARAGRAPH, HANDBOOK_PARAGRAPH_DESCRIPTION, HANDBOOK_PARAGRAPH_TEXT) VALUES (%s, '%s', '%s', '%s');" %(id, handbook_paragraph_structure_paragraph, handbook_paragraph_structure_paragraph_desc, handbook_paragraph_structure_paragraph_text)
        run_query(query)
        conn.commit()
        
        # Rerun
        st.experimental_rerun()
  
  
  ## Get categories and sub-categories
  query = "SELECT CATEGORY_ID, CATEGORY_DESCRIPTION, CATEGORY_SUB_ID, CATEGORY_SUB_DESCRIPTION FROM benbox.CATEGORIES;"
  rows = run_query(query)
  
  # Filling category and sub-category variables
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
  
  
  
  ### Handbook data entry      
  ## Show handbook paragraph entry in expander
  with st.expander(label = 'Handbook paragraph entry', expanded = False):
    st.header('New handbook paragraph entry')
    st.write('Here you can enter a new handbook paragraph.')
    
    
    ## Category menu
    category = st.selectbox(label = 'Please choose the category of the handbook entry', options = range(len(categories)), format_func = lambda x: categories[x])
          
          
    ## Sub-Category menu
    sub_category = st.selectbox(label = 'Please choose the sub-category of the handbook entry', options = range(len(sub_categories)), format_func = lambda x: sub_categories[x])
    
    
    ## Chapter menu
    chapter = st.selectbox(label = 'Please choose the chapter of the handbook entry', options = range(len(chapters_combo)), format_func = lambda x: chapters_combo[x])
    st.session_state['chapter'] = chapters[chapter]
    
    
    ## Paragraphs menu
    paragraph = st.selectbox(label = 'Please choose the paragraph of the handbook entry', options = range(len(paragraphs_combo)), format_func = lambda x: paragraphs_combo[x])
    
    
    ## Handbook data entry
    with st.form('Input', clear_on_submit = True):
      ## Input for new `HANDBOOK_USER` data
      # Get latest ID from table
      id = lastID(url = '`benbox`.`HANDBOOK_USER`')
      handbook_id = generateID(id)
      st.text_input(label = 'ID', value = id, disabled = True)
      st.text_input(label = 'Handbook ID', value = handbook_id, disabled = True)
      st.text_input(label = 'Category', value = categories[category], disabled = True)
      st.text_input(label = 'Sub-Category', value = sub_categories[sub_category], disabled = True)
      st.text_input(label = 'Chapter', value = chapters_combo[chapter], disabled = True)
      handbook_chapter = chapters[chapter]
      if paragraphs_combo is None or len(paragraphs_combo) == 0:
        st.text_input(label = 'Paragraph', placeholder = 'Please add paragraph first!', disabled = True)
        handbook_paragraph = 0
      else:
        st.text_input(label = 'Paragraph', value = paragraphs_combo[paragraph], disabled = True)
        handbook_paragraph = paragraphs[paragraph]
      handbook_keyword1 = st.text_input(label = 'Keyword 1')
      handbook_keyword2 = st.text_input(label = 'Keyword 2')
      handbook_keyword3 = st.text_input(label = 'Keyword 3')
      handbook_keyword4 = st.text_input(label = 'Keyword 4')
      handbook_keyword5 = st.text_input(label = 'Keyword 5')
      handbook_summary = st.text_input(label = 'Summary')
      handbook_text = st.text_input(label = 'Text')
      handbook_text_headline = st.text_input(label = 'Headline')
      handbook_text_language = st.text_input(label = 'Language', value = 'en')
      handbook_hits = st.text_input(label = 'Hits', value = 0)
       
      # Handbook image upload 
      uploaded_file = st.file_uploader(label = "Upload a picture", type = 'png')
      if uploaded_file is not None:
        handbook_image = uploaded_file.getvalue()
      else:
        handbook_image = load_file("images/placeholder_documentation.png")
        handbook_image_text = 'Placeholder image.'
      
      # Image description text input
      handbook_image_text = st.text_input(label = 'Image description')
      
      
      ## Submit button
      submitted = st.form_submit_button("Submit")
      if submitted:
        # Check if image description is not changed
        if (len(handbook_image_text) < 1):     
          handbook_image_text = 'Placeholder image.'
          
        # Write entry to table `HANDBOOK_USER`
        query = "INSERT INTO `benbox`.`HANDBOOK_USER`(ID, HANDBOOK_ID, CATEGORY_ID, CATEGORY_SUB_ID, HANDBOOK_CHAPTER, HANDBOOK_PARAGRAPH, HANDBOOK_KEYWORD1, HANDBOOK_KEYWORD2, HANDBOOK_KEYWORD3, HANDBOOK_KEYWORD4, HANDBOOK_KEYWORD5, HANDBOOK_SUMMARY, HANDBOOK_TEXT, HANDBOOK_TEXT_HEADLINE, HANDBOOK_TEXT_LANGUAGE, HANDBOOK_HITS, HANDBOOK_IMAGE_TEXT) VALUES (%s, '%s', '%s', '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s');" %(id, handbook_id, categories_id[category], sub_categories_id[sub_category], handbook_chapter, handbook_paragraph, handbook_keyword1, handbook_keyword2, handbook_keyword3, handbook_keyword4, handbook_keyword5, handbook_summary, handbook_text, handbook_text_headline, handbook_text_language, handbook_hits, handbook_image_text)
        run_query(query)
        conn.commit()
          
        # Upload picture to database
        pictureUploader(image = handbook_image, index = id)
        
        # Rerun
        st.experimental_rerun()
  


  ### Admin console    
  if st.session_state['admin'] ==  True:
    with st.expander(label = 'Admin console', expanded = False):
      st.header('Admin console')
      st.write('Here you can work as an admin.')
      
      
      ## Radio for chosing admin functions
      admin = st.radio("What do you want to access", ('Answer approval', 'Testing'), index = 1, horizontal = True)
      

      ## Answer approval      
      if admin == 'Answer approval':
        st.subheader('Approve answers from Ben')

        # Select score ranges
        values = st.slider(label = 'Select range of percentages', min_value = 0, max_value = 100, value = (0, 100))
  
        
        ## Get answers from table `benbox`.`ANSWERS`
        query = "SELECT ans.ANSWER_ID, que.QUESTION_ID, ans.HANDBOOK_ID, que.QUESTION_TEXT, ans.ANSWER_TEXT, ans.ANSWER_HANDBOOK_TEXT, ans.ANSWER_SCORE, ans.ANSWER_APPROVED, ans.ANSWER_DATE FROM `benbox`.`ANSWERS` AS ans LEFT JOIN `benbox`.`QUESTIONS` AS que ON ans.QUESTION_ID = que.QUESTION_ID;"
        rows = run_query(query)
        counter = 0
        databank_ben = pd.DataFrame(columns = ['ID', 'ANSWER_ID', 'QUESTION_ID', 'HANDBOOK_ID', 'QUESTION_TEXT', 'ANSWER_TEXT', 'ANSWER_HANDBOOK_TEXT', 'ANSWER_SCORE', 'ANSWER_APPROVED', 'ANSWER_DATE'])
        slider_bool = False
        for row in rows:
          if (row[6] >= values[0] / 100 and row[6] <= values[1] / 100) and row[7] == 0:
            # Select date ranges if more then one existend
            if slider_bool == False:
              time = st.slider('Select range of date', min_value = date(2023, 1, 1), max_value = date.today(), value = [date(2023, 1, 1), date.today()], format = "DD/MM/YY")
            slider_bool = True
            
            # Add percentage and time matching answers
            if row[8] >= time[0] and row[8] <= time[1]:
              counter += 1
              df = pd.DataFrame([[counter, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['ID', 'ANSWER_ID', 'QUESTION_ID', 'HANDBOOK_ID', 'QUESTION_TEXT', 'ANSWER_TEXT', 'ANSWER_HANDBOOK_TEXT', 'ANSWER_SCORE', 'ANSWER_APPROVED', 'ANSWER_DATE'])
              databank_ben = pd.concat([databank_ben, df])
        databank_ben = databank_ben.set_index('ID')
    
        # Sort by score
        databank_ben = databank_ben.sort_values('ANSWER_SCORE', ascending = True)
        
        # Show each item
        options = []
        for i in range(counter):
          options.append(i + 1)
        if len(options) > 0:
          if len(options) > 1:
            item = st.select_slider(label = 'Select an item from **' + str(counter) + '** options', options = options)
          else:
            item = 0
          st.write('**Question:** ' + databank_ben.iloc[item - 1][3])
          st.write('**Answer:** ' + databank_ben.iloc[item - 1][4])
          st.write('**Handbook:** ' + databank_ben.iloc[item - 1][5])
          st.write('**Score:** ' + str(format(databank_ben.iloc[item - 1][6], '.0%')))
          st.write('**Date:** ' + str(databank_ben.iloc[item - 1][8]))
          faq_bool = False
          for i in range(len(faq)):
            if (databank_ben.iloc[item - 1][0] == faq[i][1]):
              faq_bool = True
              faq_date = faq[i][9]
              
          # Already approved as useful by user (in FAQ)
          if faq_bool == True:
            st.write('**:green[In FAQ existend]** (' + str(faq_date) + ')')
            
            # Option to approve
            if databank_ben.iloc[item - 1][7] == 0:
              if st.button(label = 'Approve answer?'):
                query = "UPDATE `benbox`.`ANSWERS` SET ANSWER_APPROVED = 1 WHERE ANSWER_ID = '%s';" %(databank_ben.iloc[item - 1][0])
                rows = run_query(query)
                conn.commit()
                st.experimental_rerun()
                
          # Not approved by user (not in FAQ)
          else:
            st.write('**:red[Not in FAQ existend]**')
            
            # Option to approve
            if databank_ben.iloc[item - 1][7] == 0:
              if st.button(label = 'Approve answer?'):
                query = "UPDATE `benbox`.`ANSWERS` SET ANSWER_APPROVED = 1 WHERE ANSWER_ID = '%s';" %(databank_ben.iloc[item - 1][0])
                rows = run_query(query)
                conn.commit()
  
                # Get latest ID from table
                id = lastID(url = '`benbox`.`FAQ`')
                
                # Write question to table `FAQ`
                query = "INSERT INTO `benbox`.`FAQ`(ID, FAQ_ID, QUESTION_ID, HANDBOOK_ID, ANSWER_ID, FAQ_HITS, FAQ_DATE) VALUES (%s, '%s', '%s', '%s', '%s', %s, '%s');" %(id, generateID(id = id), databank_ben.iloc[item - 1][1], databank_ben.iloc[item - 1][2], databank_ben.iloc[item - 1][0], 0, date.today())
                run_query(query)
                conn.commit()
                st.experimental_rerun()
      
      
      ## Tesing
      elif admin == 'Testing':
        st.write('You did select Testing')
  
  
  ## Not admin user
  else:      
    # Show info box
  	st.info(body = 'Please login as admin (sidebar on the left) to access the \"Admin console\"', icon = "ℹ️")

  
            
  
  
#### Not Logged in state (Landing page)
else :
  ## Header
  header(title = 'Handbook page', data_desc = 'handbooks', expanded = st.session_state['header']) 



  ### FAQ
  faq()
  
  
  
  ### Chat-Bot Ben
  ben()
      
  
  
  ### Handbook
  book()
  
  
  
  ### Show `login` info box
  st.info(body = 'Please login (sidebar on the left) to enter handbook data (strutures and paragragphs).', icon = "ℹ️")
