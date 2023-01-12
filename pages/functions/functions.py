##### `/pages/functions/functions.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import pandas as pd
import io
import os
import sys
import xlsxwriter
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import qrcode




#### All shared general functions
### Function: check_password = Password / user checking
def check_password():
	# Returns `True` if the user had a correct password
	def password_entered():
		# Checks whether a password entered by the user is correct
		if st.session_state["username"] in st.secrets["passwords"] and st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]:
			st.session_state["password_correct"] = True
			st.session_state["admin"] = False
			
			# Delete username + password
			del st.session_state["password"]
			del st.session_state["username"]
			
		# Checks whether a password entered by the user is correct for admins	
		elif st.session_state["username"] in st.secrets["admins"] and st.session_state["password"] == st.secrets["admins"][st.session_state["username"]]:
			st.session_state["password_correct"] = True
			st.session_state["admin"] = True
			
			# Delete username + password
			del st.session_state["password"]
			del st.session_state["username"]
			
		# No combination fits
		else:
			st.session_state["password_correct"] = False


	## Sidebar
	# Sidebar Header Image
	st.sidebar.image('images/MoH.png')
	
	# Header switch
	if st.session_state['header'] == True:
	  index = 0
	elif st.session_state['header'] == False:
	  index = 1
	else:
	  index = 0
	header = st.sidebar.radio(label = 'Switch headers on or off', options = ('on', 'off'), index = index, horizontal = True)
	if header == 'on':
	  st.session_state['header'] = True
	elif header == 'off':
	  st.session_state['header'] = False
	else:
	  st.session_state['header'] = True
	  
	# First run, show inputs for username + password
	if "password_correct" not in st.session_state:
		st.sidebar.subheader('Please enter username and password')
		st.sidebar.text_input(label = "Username", on_change = password_entered, key = "username")
		st.sidebar.text_input(label = "Password", type = "password", on_change = password_entered, key = "password")
		return False
	
	# Password not correct, show input + error
	elif not st.session_state["password_correct"]:
		st.sidebar.text_input(label = "Username", on_change = password_entered, key = "username")
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
 
 
			
### Funtion: logout = Logout button
def logout():
	# Set `logout` to get logout-message
	st.session_state['logout'] = True
	
	# Set password to `false`
	st.session_state["password_correct"] = False



### Function: export_excel = Pandas dataframe to MS Excel Makro File (xlsm)
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

	
	## Create an Excel file filled with a pandas dataframe using XlsxWriter as engine
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
					# Saving image as png to a buffer
					byteIO = io.BytesIO()
					image.save(byteIO, format = 'PNG')
					pic = byteIO.getvalue()
					worksheet.insert_image(image_pos, pic)
			
			
		## Add Excel VBA code
		workbook = writer.book
		workbook.add_vba_project('vbaProject.bin')
		

		## Saving changes
		workbook.close()
		writer.save()
		
		
		## Download Button
		st.download_button(label = 'Download Excel document', data = buffer, file_name = excel_file_name, mime = "application/vnd.ms-excel.sheet.macroEnabled.12")
 


### Function: export_docx = Pandas dataframe to MS Word file (docx)
def export_docx(data, faq, docx_file_name = 'Handbook.docx'):
	document = Document()
	

	## Sorting dataframe by chapter and paragraph
	data = data.sort_values(['HANDBOOK_CHAPTER', 'HANDBOOK_PARAGRAPH'], ascending = [True, True])


	## Writing handbook
	# Adding handbook header
	document.add_heading('User Handbook', 0)

	# Adding table of contents
	document.add_heading('Table of contents', level = 1)
	paragraph = document.add_paragraph()
	chapter = 0
	paragraf = 0
	for i in range(len(data)):
	  if (data.iloc[i]['HANDBOOK_PARAGRAPH'] != paragraf):
	    if (chapter != data.iloc[i]['HANDBOOK_CHAPTER']):
	      paragraph.add_run('\n' + data.iloc[i]['HANDBOOK_CHAPTER_DESCRIPTION'] + '\n').bold = True
	      chapter += 1
	    if (str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[1] == '0'):
	      paragraph.add_run(str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[0] + ' - ' + data.iloc[i]['HANDBOOK_TEXT_HEADLINE'] + '\n')
	    else:
	      if len(str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[1]) == 1:
	        placer = '\t'
	      elif len(str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[1]) == 2:
	        placer = '\t\t'
	      elif len(str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[1]) == 3:
	        placer = '\t\t\t'
	      else:
	        placer = '\t\t\t\t'
	      paragraph.add_run(placer + str(data.iloc[i]['HANDBOOK_PARAGRAPH']) + ' - ' + data.iloc[i]['HANDBOOK_TEXT_HEADLINE'] + '\n')
	  paragraf = data.iloc[i]['HANDBOOK_PARAGRAPH']

  # Writing paragraphs
	chapter = 0
	paragraf = 0
	for i in range(len(data)):
		# Adding chapter headings
		if data.iloc[i]['HANDBOOK_CHAPTER'] > chapter:
		  document.add_page_break()
		  
		  # Adding handbook header
		  document.add_heading('User Handbook', 0)
		  document.add_heading(data.iloc[i]['HANDBOOK_CHAPTER_DESCRIPTION'], level = 1)
		  paragraph = document.add_paragraph()
		  paragraph.add_run(data.iloc[i]['HANDBOOK_CHAPTER_TEXT']).italic = True
		  chapter = data.iloc[i]['HANDBOOK_CHAPTER']
		  
		# Adding paragraph headings
		if (data.iloc[i]['HANDBOOK_PARAGRAPH'] != paragraf):
		  if len(str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[1]) == 1:
		    if str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[1] == '0':
		      document.add_heading(str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[0] + '\t' + data.iloc[i]['HANDBOOK_TEXT_HEADLINE'], level = 2)
		    else:
		      document.add_heading(str(data.iloc[i]['HANDBOOK_PARAGRAPH']) + '\t' + data.iloc[i]['HANDBOOK_TEXT_HEADLINE'], level = 2)
		  elif len(str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[1]) == 2:
		    document.add_heading(str(data.iloc[i]['HANDBOOK_PARAGRAPH']) + '\t' + data.iloc[i]['HANDBOOK_TEXT_HEADLINE'], level = 3)
		  elif len(str(data.iloc[i]['HANDBOOK_PARAGRAPH']).split('.')[1]) == 3:
		    document.add_heading(str(data.iloc[i]['HANDBOOK_PARAGRAPH']) + '\t' + data.iloc[i]['HANDBOOK_TEXT_HEADLINE'], level = 4)
		  else:
		    document.add_heading(str(data.iloc[i]['HANDBOOK_PARAGRAPH']) + '\t' + data.iloc[i]['HANDBOOK_TEXT_HEADLINE'], level = 5)
    
		# Adding paragraphs
		paragraph = document.add_paragraph()
		if (data.iloc[i]['HANDBOOK_PARAGRAPH'] != paragraf):
		  if (data.iloc[i]['HANDBOOK_PARAGRAPH_TEXT'] != None):
			  paragraph.add_run(data.iloc[i]['HANDBOOK_PARAGRAPH_TEXT'] + '\n\n').italic = True
		paragraph.add_run(data.iloc[i]['HANDBOOK_TEXT'])
		#paragraph.add_run('Category & Sub-Category: ').bold = True
		#paragraph.add_run(data.iloc[i]['CATEGORY'] + ' / ' + data.iloc[i]['CATEGORY_SUB'] + '\n')
		#paragraph.add_run('Keywords: ').bold = True
		#paragraph.add_run(data.iloc[i]['HANDBOOK_KEYWORD1'].capitalize() + ', ' + data.iloc[i]['HANDBOOK_KEYWORD2'].capitalize() + ', ' + data.iloc[i]['HANDBOOK_KEYWORD3'].capitalize() + ', ' + data.iloc[i]['HANDBOOK_KEYWORD4'].capitalize() + ', ' + data.iloc[i]['HANDBOOK_KEYWORD5'].capitalize())
		paragraf = data.iloc[i]['HANDBOOK_PARAGRAPH']
    
		# Adding image
		if (data.iloc[i]['HANDBOOK_IMAGE_TEXT'] != 'Placeholder image.'):
			save_file(data = data.iloc[i]['HANDBOOK_IMAGE'], filename = 'temp.png')
			paragraph = document.add_paragraph()
			paragraph_format = paragraph.paragraph_format
			paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
			run = paragraph.add_run()
			run.add_picture('temp.png')
			paragraph.add_run('\n' + data.iloc[i]['HANDBOOK_IMAGE_TEXT']).italic = True
			

	## Writing FAQ
	# Adding handbook header
	document.add_page_break()
	document.add_heading('User Handbook', 0)

	# Adding FAQ header
	document.add_heading('FAQ', level = 1)

	# Adding FAQ items
	for i in range(len(faq)):
		paragraph = document.add_paragraph()
		paragraph.add_run('Question: ').bold = True
		paragraph.add_run(faq[i][0].upper() + '\n')
		paragraph.add_run('Category & Sub-Category: ').bold = True
		paragraph.add_run(faq[i][2] + ' / ' + faq[i][3] + '\n')
		paragraph.add_run('Ben`s answer: ').bold = True
		paragraph.add_run(faq[i][1]+ '\n\n')

	
	## Create a Word file using python-docx as engine
	buffer = io.BytesIO()
	document.save(buffer)
	if os.path.exists("temp.png"):
		os.remove("temp.png")


	## Download Button
	st.download_button(label = 'Download Word document', data = buffer, file_name = docx_file_name, mime = "application/vnd.openxmlformats")



### Function: loadFile = Converts digital data to binary format
def load_file(filename):
	with open(filename, 'rb') as file:
		binaryData = file.read()
	return binaryData



### Function: saveFile = converts binary image data to png file
def save_file(data, filename = 'temp.png'):
	file = open(filename, 'wb')
	file.write(data)
	file.close()



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



### Function: generate_qrcode = QR Code generator
def generate_qrcode(data):
  # Encoding data using make() function
  image = qrcode.make(data)
  
  # Saving image as png in a buffer
  byteIO = io.BytesIO()
  image.save(byteIO, format = 'PNG')

  # Return qrcode
  return byteIO.getvalue()



### Function header = Shows header information 
def header(title, data_desc, expanded = True):
  with st.expander("Header", expanded = expanded):
    ## Header information
    st.title(title)
    st.image('images/MoH.png')
    st.header(st.secrets['custom']['facility'] + ' (' + st.secrets['custom']['facility_abbreviation'] + ')')
    st.subheader(st.secrets['custom']['facility_abbreviation'] + ' ' + data_desc)
    st.write('All data is stored in a local MySQL databank on a dedicated Server hosted at ' + st.secrets['custom']['facility_abbreviation'] + '.')
    st.write('The ' + title + ' is developed with Python (v' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + ') and the web app framework Streamlit.')



### Function: landing_page = Shows the landing page (not loged in state)
def landing_page(page):
  ## Title and information
  header = 'Welcome to ' + page
  st.title(header)
  st.header(st.secrets['custom']['facility'] + ' (' + st.secrets['custom']['facility_abbreviation'] + ')')
  st.subheader('User Login')
  st.info(body = 'Please login (sidebar on the left) to access the ' + page, icon = "ℹ️")
  
  
  ## Sub-pages menu
  st.subheader('Pages without login)')
  st.write('You can access these pages without being logged in:')
  st.write("<a href='Statistics' target='_self'>Statistics</a>", unsafe_allow_html = True)
  st.write("<a href='Workshops' target='_self'>Workshops</a>", unsafe_allow_html = True)
  st.write("<a href='Handbook' target='_self'>Handbook</a>", unsafe_allow_html = True)
  st.write("<a href='About' target='_self'>About</a>", unsafe_allow_html = True)
