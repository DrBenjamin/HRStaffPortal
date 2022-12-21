##### `pages/2 - 🛠_Workshops.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import openai
import mysql.connector
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
    try:
      ## Perform query
      cur.execute(query)
      return cur.fetchall()
    except:
      print("An exception occurred in function `run_query`")
      
      
      
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
  
  


#### Sidebar
### Workshop Sidebar
## Sidebar Header Image
st.sidebar.image('images/MoH.png')




#### Main Program
### Chat Bot Ben
## Header
st.title('Workshop page')
st.subheader('Ben chatbot')


## Global variables
answer = ''
keyword1 = ''
keywords = []



### Form
with st.form('Input', clear_on_submit = True):
  ## Columns
  col1, col2 = st.columns(2)
  
  
  ## Column 1
  with col1:
    ## Implementation of OpenAI
    # Open databank connection
    conn = init_connection()
    query = "SELECT CATEGORY_ID, CATEGORY_DESCRIPTION, CATEGORY_SUB_ID, CATEGORY_SUB_DESCRIPTION FROM benbox.CATEGORIES;"
    rows = run_query(query)
    
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
      
    # Category menu
    category = st.selectbox(label = 'Please choose the category of the question (if unknown, choose \"General\"', options = range(len(categories)), format_func = lambda x: categories[x])
    
    # Sub-Category menu
    sub_category = st.selectbox(label = 'Please choose the sub-category of the question', options = range(len(sub_categories)), format_func = lambda x: sub_categories[x])
    
    # User question
    user_question = st.text_input(label = 'What text should be summarised to one keyword?', placeholder = 'Salary, is what an employee get paid at the end of the month')
    
    # Concacenate questions
    summary_question = 'A User asks in the category \"' + categories[category] + '\" and the sub-category"' + sub_categories[sub_category] + '" about this question: \"' + user_question + '" Please summarise it to a statement in no more than three words.'
    keyword_question = 'Extract one keyword of the beginning of the text which is a noun without the accompanying article and pronoun: \"' + user_question + '"'
    
    
  ## Submit button
  submitted = st.form_submit_button("Submit")
  if submitted:
    ## Get response from openai
    # Set API key
    openai.api_key = st.secrets['openai']['key']
    
    try:
      ## Doing the requests to OpenAI for summarizing / keyword extracting the question
      # Summary
      response_summary = openai.Completion.create(model = "text-davinci-003", prompt = summary_question, temperature = 0.3, max_tokens = 64, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
      summary = response_summary['choices'][0]['text'].lstrip()
      summary = summary.replace('.', '')
      
      # Find the keyword1
      response_keyword = openai.Completion.create(model = "text-curie-001", prompt = keyword_question, temperature = 0.0, max_tokens = 64, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
      keyword1 = response_keyword['choices'][0]['text'].lstrip()
      keyword1 = keyword1.capitalize()
      
      # Find the 4 other keywords 
      keywords_question = 'Extract four one-word keywords which are not the same as \"' + keyword1 + '\"' + ' of this text: \"' + user_question + '"'
      response_keywords = openai.Completion.create(model = "text-davinci-003", prompt = keywords_question, temperature = 0.0, max_tokens = 64, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
      keywords = response_keywords['choices'][0]['text']
      
      
      ## Cleaning response
      # Create array out of comma seperated string
      st.write(keyword1)
      st.write(keywords)
      st.write(summary)
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
      id = lastID(url = "benbox.QUESTIONS")
        
      # Pollute `QUESTION_ID`
      if (id < 10):
        question_id = '0000' + str(id)
      elif (id < 100):
        question_id = '000' + str(id)
      elif (id < 1000):
        question_id = '00' + str(id)
      elif (id < 10000):
        question_id = '0' + str(id)
        
      # Pollute `QUESTTION_TEXT_LANGUAGE
      language = 'en'
        
      # Write to table
      query = "INSERT INTO `benbox`.`QUESTIONS`(ID, QUESTION_ID, QUESTION_CATEGORY, QUESTION_CATEGORY_SUB, QUESTION_KEYWORD1, QUESTION_KEYWORD2, QUESTION_KEYWORD3, QUESTION_KEYWORD4, QUESTION_KEYWORD5, QUESTION_SUMMARY, QUESTION_TEXT, QUESTION_TEXT_LANGUAGE) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(id, question_id, categories_id[category], sub_categories_id[sub_category], keyword1, keywords[0], keywords[1], keywords[2], keywords[3], summary, user_question, language)
      run_query(query)
      conn.commit()
      
      
      ## Get handbook data to answer
      query = "SELECT ID, ID, HANDBOOK_ID, HANDBOOK_KEYWORD1, HANDBOOK_KEYWORD2, HANDBOOK_KEYWORD3, HANDBOOK_KEYWORD4, HANDBOOK_KEYWORD5, HANDBOOK_TEXT, HANDBOOK_HITS FROM benbox.HANDBOOK_USER WHERE HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD1 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD2 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD3 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD4 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s' OR HANDBOOK_KEYWORD5 LIKE '%s';" % (keyword1, keywords[0], keywords[1], keywords[2], keywords[3], keyword1, keywords[0], keywords[1], keywords[2], keywords[3], keyword1, keywords[0], keywords[1], keywords[2], keywords[3], keyword1, keywords[0], keywords[1], keywords[2], keywords[3], keyword1, keywords[0], keywords[1], keywords[2], keywords[3])
      rows = run_query(query)
      databank_handbook = pd.DataFrame(columns = ['ID_Index', 'ID', 'HANDBOOK_ID', 'HANDBOOK_KEYWORD1', 'HANDBOOK_KEYWORD2', 'HANDBOOK_KEYWORD3', 'HANDBOOK_KEYWORD4', 'HANDBOOK_KEYWORD5', 'HANDBOOK_TEXT', 'HANDBOOK_HITS'])
      for row in rows:
        df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]]], columns = ['ID_Index', 'ID', 'HANDBOOK_ID', 'HANDBOOK_KEYWORD1', 'HANDBOOK_KEYWORD2', 'HANDBOOK_KEYWORD3', 'HANDBOOK_KEYWORD4', 'HANDBOOK_KEYWORD5', 'HANDBOOK_TEXT', 'HANDBOOK_HITS'])
        databank_handbook = pd.concat([databank_handbook, df])
      databank_handbook = databank_handbook.set_index('ID_Index')
      
      
      ## Checking if he found handbook data
      if (len(databank_handbook) > 0):     
        # Adding keyword1 at first position
        keywords.insert(0, keyword1)
        for x in range(len(databank_handbook)):
          handbook = databank_handbook.iloc[x]
          counter = 0 + int(databank_handbook._get_value(handbook[0], 'HANDBOOK_HITS'))
          for i in range(5):
            if handbook[2].capitalize() == keywords[i]:
              counter += 1
            if handbook[3].capitalize() == keywords[i]:
              counter += 1
            if handbook[4].capitalize() == keywords[i]:
              counter += 1
            if handbook[5].capitalize() == keywords[i]:
              counter += 1
            if handbook[6].capitalize() == keywords[i]:
              counter += 1
            databank_handbook['HANDBOOK_HITS'][handbook[0]] = counter
              
              
        ## Checking for highest Score ('HANDBOOK_HITS')
        for x in range(len(databank_handbook)):
          if (x == 0):
            handbook = databank_handbook._get_value(databank_handbook.iloc[x][0], 'HANDBOOK_TEXT')
          else:
            for i in range(x):
              if (databank_handbook.iloc[x][8] <= databank_handbook.iloc[i][8]):
                break
              else:
                if (i == x - 1):
                  handbook = databank_handbook._get_value(databank_handbook.iloc[x][0], 'HANDBOOK_TEXT')
                  
                  
        ## Doing the request to OpenAI for answering the question
        # Answer
        answer_question = 'The user handbook contains following information: \"' + handbook + '\". Please answer following user question: \"' + user_question + '\"'
        response_answer = openai.Completion.create(model = "text-davinci-003", prompt = answer_question, temperature = 0.5, max_tokens = 128, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0)
        answer = response_answer['choices'][0]['text'].lstrip()
      else:
        answer = 'Unfortunately we have not found the answer to your question.' 
      
      
    except:
      print('An exception occurred in `OpenAI`')
      
    
  ## Column 1
  with col2:
    st.image("images/Ben.png")
    
  
  
### Outside the form
st.write(answer)
