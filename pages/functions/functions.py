##### `/pages/functions/functions.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading neded Python libraries
import streamlit as st
import pandas as pd
import io
import os
import xlsxwriter
import chronological
import deepl
import geocoder
from geopy.geocoders import Nominatim




#### All functions used in Car Fleet Management
### Function: check_password = Password / User checking
def check_password():
  # Returns `True` if the user had a correct password."""
  def password_entered():
    # Checks whether a password entered by the user is correct."""
    if (st.session_state["username"] in st.secrets["passwords"] and st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]):
      st.session_state["password_correct"] = True
      del st.session_state["password"]  # don't store username + password
      del st.session_state["username"]
    else:
      st.session_state["password_correct"] = False
    
  ## Sidebar
  # Sidebar Header Image
  st.sidebar.image('images/MoH.png')

  if "password_correct" not in st.session_state:
    # First run, show inputs for username + password
    # Show Header Text
    st.sidebar.subheader('Please enter username and password')
    st.sidebar.text_input(label = "Username", on_change = password_entered, key = "username")
    st.sidebar.text_input(label = "Password", type = "password", on_change = password_entered, key = "password")
    return False
  
  elif not st.session_state["password_correct"]:
    # Password not correct, show input + error
    st.sidebar.text_input(label = "Username", on_change=password_entered, key = "username")
    st.sidebar.text_input(label = "Password", type = "password", on_change = password_entered, key = "password")
    if (st.session_state['logout']):
      st.sidebar.success('Logout successful!', icon = "✅")
    else:
      st.sidebar.error(body = "User not known or password incorrect!", icon = "🚨")
    return False
  
  else:
    # Password correct
    st.sidebar.success(body = 'You are logged in.', icon = "✅")
    st.sidebar.info(body = 'You can close this menu')
    st.sidebar.button(label = 'Logout', on_click = logout)
    return True
 
 
      
### Funtion: logout = Logout Button
def logout():
  ## Set Logout to get Logout-message
  st.session_state['logout'] = True
  ## Logout
  st.session_state["password_correct"] = False



### Function: export_excel = Pandas Dataframe to Excel Makro File (xlsm)
def export_excel(sheet, column, columns, length, data, 
                sheet2 = 'N0thing', column2 = 'A', columns2 = '', length2 = '', data2 = '',
                sheet3 = 'N0thing', column3 = 'A', columns3 = '', length3 = '', data3 = '',
                sheet4 = 'N0thing', column4 = 'A', columns4 = '', length4 = '', data4 = '',
                sheet5 = 'N0thing', column5 = 'A', columns5 = '', length5 = '', data5 = '',
                sheet6 = 'N0thing', column6 = 'A', columns6 = '', length6 = '', data6 = '',
                sheet7 = 'N0thing', column7 = 'A', columns7 = '', length7 = '', data7 = '',
                image = 'NoImage', image_pos = 'D1', excel_file_name = 'Export.xlsm'):
  
  
  ## Store fuction arguments in array
  # Create empty array
  func_arr =[]
  
  # Add function arguments to array
  func_arr.append([sheet, column, columns, length, data])
  func_arr.append([sheet2, column2, columns2, length2, data2])
  func_arr.append([sheet3, column3, columns3, length3, data3])
  func_arr.append([sheet4, column4, columns4, length4, data4])
  func_arr.append([sheet5, column5, columns5, length5, data5])
  func_arr.append([sheet6, column6, columns6, length6, data6])
  func_arr.append([sheet7, column7, columns7, length7, data7])

  
  ## Create a Pandas Excel writer using XlsxWriter as the engine
  buffer = io.BytesIO()
  with pd.ExcelWriter(buffer, engine = 'xlsxwriter') as writer:
    for i in range(7):
      if (func_arr[i][0] != 'N0thing'):
        # Add dataframe data to worksheet
        func_arr[i][4].to_excel(writer, sheet_name = func_arr[i][0], index = False)

        # Add a table to the worksheet
        worksheet = writer.sheets[func_arr[i][0]]
        span = "A1:%s%s" %(func_arr[i][1], func_arr[i][3])
        worksheet.add_table(span, {'columns': func_arr[i][2]})
        range_table = "A:" + func_arr[i][1]
        worksheet.set_column(range_table, 30)
        
        # Add Image to worksheet
        if (image != 'NoImage'):
          # Write Image to a png file
          f = open('Image.png', 'wb')
          f.write(image)
          f.close()
          worksheet.insert_image(image_pos, 'Image.png')
      
      
    ## Add Excel VBA code
    workbook = writer.book
    workbook.add_vba_project('vbaProject.bin')
    

    ## Saving changes
    workbook.close()
    writer.save()
    if os.path.exists("Image.png"):
      os.remove("Image.png")
    
    
    ## Download Button
    st.download_button(label = 'Download Excel document', data = buffer, file_name = excel_file_name, mime = "application/vnd.ms-excel.sheet.macroEnabled.12")
 


### Function: loadFile = converts digital data to binary format
def loadFile(filename):
  with open(filename, 'rb') as file:
    binaryData = file.read()
  return binaryData



### Function: trans = DeepL translation
def trans(input, target_lang):
  translator = deepl.Translator(st.secrets["deepl"]["key"])
  result = translator.translate_text(input, target_lang = target_lang) 
  return result



### Function: landigPage = shows the landing page (not loged in state)
def landingPage(page):
  ## Title and information
  st.title('Kamuzu Central Hospital (KCH)')
  header = 'Welcome to ' + page
  st.header(header)
  st.subheader('User Login')
  st.write('Please login (sidebar on the left) to access the ', page, '.')
  
  
  ## Sub-pages menu
  st.subheader('Pages (without login)')
  st.write('You can access these pages without being logged in:')
  st.write("<a href='Statistics' target='_self'>Statistics</a>", unsafe_allow_html = True)
  st.write("<a href='Workshops' target='_self'>Workshops</a>", unsafe_allow_html = True)
  st.write("<a href='Network' target='_self'>Network</a>", unsafe_allow_html = True)
  st.write("<a href='About' target='_self'>About</a>", unsafe_allow_html = True)
  
  
  
### Function geo_check = Geo-Location checking
def geo_check(address_part):
  ## Geocoder gets coordinates related to the current IP address
  g = geocoder.ip('me')
  
  
  ## Geopy
  # Calling the Nominatim tool
  loc = Nominatim(user_agent = "GetLoc", timeout = 3)
  geolocator = Nominatim(user_agent = "geoapiExercises")
  
  # Entering the location name to get coordinates
  getLoc = loc.geocode("Lilongwe")
  
  # Get City name
  try:
    geolocator.reverse(g.latlng, language = lang)
    location = geolocator.geocode(g.latlng, addressdetails = True)
    loc = location.raw
    output = loc['address'][address_part]
    
  # Set to Lilongwe if not reachable
  except:
    print("An exception occurred in `Geocoder`")
    output = 'Lilongwe'
  
  # Return output 
  return output
  
