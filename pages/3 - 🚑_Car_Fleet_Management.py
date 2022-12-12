##### `3 - 🚑_Car_Fleet_Management.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions



#### Loading neded Python libraries
import streamlit as st
import extra_streamlit_components as stx
import platform
import pandas as pd
import mysql.connector
import os
import io
import xlsxwriter



#### Streamlit initial setup
st.set_page_config(
  page_title = "KCH HR Staff Portal",
  page_icon = "images/thumbnail.png",
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the KCH HR Staff Portal. Version 0.0.1"
        }
)



#### OS Check
plt = platform.system()
if plt == "Windows":
  print("Your system is Windows")
elif plt == "Linux":
  print("Your system is Linux")
elif plt == "Darwin":
  print("Your system is MacOS")



#### All functions used in Car Fleet Management
### Function: init_connection = Initial SQL connection
def init_connection():
  try:
    ## Initialize connection
    return mysql.connector.connect(**st.secrets["mysql"])
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


### Function: check_vehicles = checking for unique Vehicles IDs
def check_vehicles(column, data):
  vehicle = []
  i = 0
  while i < len(data):
    if i > 0:
      x = 0
      double = False
      for x in range(len(vehicle)):
        if (vehicle[x] == data[column][i + 1]):
          double = True
      if (double != True):    
        vehicle.append(data[column][i + 1])
    else:
      vehicle.append(data[column][i + 1])
    i += 1
  return vehicle


### Function: export_excel = Pandas Dataframe to Excel Makro File (xlsm)
def export_excel(sheet, column, columns, length, data, 
                sheet2 = 'N0thing', column2 = 'A', columns2 = '', length2 = '', data2 = '',
                sheet3 = 'N0thing', column3 = 'A', columns3 = '', length3 = '', data3 = '',
                sheet4 = 'N0thing', column4 = 'A', columns4 = '', length4 = '', data4 = '',
                sheet5 = 'N0thing', column5 = 'A', columns5 = '', length5 = '', data5 = '',
                sheet6 = 'N0thing', column6 = 'A', columns6 = '', length6 = '', data6 = '',
                sheet7 = 'N0thing', column7 = 'A', columns7 = '', length7 = '', data7 = ''):
  
  
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
      
      
    ## Add Excel VBA code
    workbook = writer.book
    workbook.add_vba_project('vbaProject.bin')
    

    ## Saving changes
    workbook.close()
    writer.save()
    
    
    ## Download Button
    st.download_button(label = 'Download Excel document', data = buffer, file_name = 'Export.xlsm', mime = "application/vnd.ms-excel.sheet.macroEnabled.12")
    
    
### Function: pictureUploader = uploads employee images
def pictureUploader(image, index):
  ## Initialize connection
  connection = mysql.connector.connect(**st.secrets["mysql"])
  cursor = connection.cursor()
  ## SQL statement
  sql_insert_blob_query = """ UPDATE IMAGEBASE SET IMAGE = %s WHERE ID = %s;"""
  ## Convert data into tuple format
  insert_blob_tuple = (image, index)
  result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
  connection.commit()
  
  
### Function: lastID = checks for last ID number in Table (to add data after)
def lastID(url):
  id = 0
  query = "SELECT ID from %s;" %(url)
  rows = run_query(query)
  row = [0]
  for row in rows:
    id = int(row[0]) + 1
  # If first entry in database start with `ID` `1` 
  if (id == 0):
    id = 1
  return id


### Function: loadFile = converts digital data to binary format
def loadFile(filename):
  with open(filename, 'rb') as file:
    binaryData = file.read()
  return binaryData
## Current Image data
if ('image' not in st.session_state):
  st.session_state['image'] = loadFile('images/No_Image.png')



#### Main Program
### Title
st.title("KCH Car Fleet")


## Use local databank carfleet
# Open databank connection
conn = init_connection()


## Get `DRIVERS` table data
query = "SELECT ID, DRIVER_ID, DRIVER_FORENAME, DRIVER_SURNAME, DRIVER_NATIONAL_ID, DRIVER_MOBILE_NO, DRIVER_LICENSE_NO, DRIVER_LICENSE_CLASS, DRIVER_PSV_BADGE, DRIVER_NOTES, DRIVER_IMAGE FROM `carfleet`.`DRIVERS`;"
rows = run_query(query)
   
# Create pandas dataframe 
databank_drivers = pd.DataFrame(columns = ['ID', 'DRIVER_ID', 'DRIVER_FORENAME', 'DRIVER_SURNAME', 'DRIVER_NATIONAL_ID', 'DRIVER_MOBILE_NO', 'DRIVER_LICENSE_NO', 'DRIVER_LICENSE_CLASS', 'DRIVER_PSV_BADGE', 'DRIVER_NOTES', 'DRIVER_IMAGE'])
  
# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]], columns = ['ID', 'DRIVER_ID', 'DRIVER_FORENAME', 'DRIVER_SURNAME', 'DRIVER_NATIONAL_ID', 'DRIVER_MOBILE_NO', 'DRIVER_LICENSE_NO', 'DRIVER_LICENSE_CLASS', 'DRIVER_PSV_BADGE', 'DRIVER_NOTES', 'DRIVER_IMAGE'])
  databank_drivers = pd.concat([databank_drivers, df])
databank_drivers = databank_drivers.set_index('ID')
# Drop last columns (Images)
databank_drivers_excel = databank_drivers.iloc[: , :-1]


## Get `FUEL` table data
query = "SELECT ID, VEHICLE_ID, DRIVER_ID, VEHICLE_FUEL_AMOUNT, VEHICLE_FUEL_COST, VEHICLE_FUEL_TYPE, VEHICLE_FUEL_DATE, VEHICLE_DISTANCE, FUEL_SHORTAGE, COST_CENTRE FROM `carfleet`.`FUEL`;"
rows = run_query(query)
   
# Create pandas dataframe 
databank_fuel = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'VEHICLE_FUEL_AMOUNT', 'VEHICLE_FUEL_COST', 'VEHICLE_FUEL_TYPE', 'VEHICLE_FUEL_DATE', 'VEHICLE_DISTANCE', 'FUEL_SHORTAGE', 'COST_CENTRE'])
  
# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]]], columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'VEHICLE_FUEL_AMOUNT', 'VEHICLE_FUEL_COST', 'VEHICLE_FUEL_TYPE', 'VEHICLE_FUEL_DATE', 'VEHICLE_DISTANCE', 'FUEL_SHORTAGE', 'COST_CENTRE'])
  databank_fuel = pd.concat([databank_fuel, df])
databank_fuel = databank_fuel.set_index('ID')
  

## Get `INSURANCES` table data
query = "SELECT ID, VEHICLE_ID, INSURANCE_DETAILS, INSURANCES_TYPE, INSURANCE_START_DATE, INSURANCE_EXPIRY_DATE FROM `carfleet`.`INSURANCES`;"
rows = run_query(query)
   
# Create pandas dataframe 
databank_insurances = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'INSURANCE_DETAILS', 'INSURANCES_TYPE', 'INSURANCE_START_DATE', 'INSURANCE_EXPIRY_DATE'])
  
# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5]]], columns = ['ID', 'VEHICLE_ID', 'INSURANCE_DETAILS', 'INSURANCES_TYPE', 'INSURANCE_START_DATE', 'INSURANCE_EXPIRY_DATE'])
  databank_insurances = pd.concat([databank_insurances, df])
databank_insurances = databank_insurances.set_index('ID')
  

## Get `REPAIRS` table data
query = "SELECT ID, VEHICLE_ID, VEHICLE_REPAIR_DETAILS, VEHICLE_REPAIR_DATE, VEHICLE_REPAIR_COSTS, VEHICLE_SPARE_PARTS, VEHICLE_DOWN_TIME, SERVICE_CENTRE_PERSON, COST_CENTRE FROM `carfleet`.`REPAIRS`;"
rows = run_query(query)
    
# Create pandas dataframe
databank_repairs = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_REPAIR_DETAILS', 'VEHICLE_REPAIR_DATE', 'VEHICLE_REPAIR_COSTS', 'VEHICLE_SPARE_PARTS', 'VEHICLE_DOWN_TIME', 'SERVICE_CENTRE_PERSON', 'COST_CENTRE'])
    
# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_REPAIR_DETAILS', 'VEHICLE_REPAIR_DATE', 'VEHICLE_REPAIR_COSTS', 'VEHICLE_SPARE_PARTS', 'VEHICLE_DOWN_TIME', 'SERVICE_CENTRE_PERSON', 'COST_CENTRE'])
  databank_repairs = pd.concat([databank_repairs, df])
databank_repairs = databank_repairs.set_index('ID')
  

## Get `SERVICES` table data
query = "SELECT ID, VEHICLE_ID, DRIVER_ID, SERVICE_DATE, SERVICE_DETAILS, SERVICE_COSTS, SERVICE_MILEAGE_ON_SERVICE, SERVICE_MILEAGE_NEXTSERVICE, SERVICE_MILEAGE_NEXTSERVICE_MAX FROM `carfleet`.`SERVICES`;"
rows = run_query(query)
   
# Create pandas dataframe 
databank_services = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'SERVICE_DATE', 'SERVICE_DETAILS', 'SERVICE_COSTS', 'SERVICE_MILEAGE_ON_SERVICE', 'SERVICE_MILEAGE_NEXTSERVICE', 'SERVICE_MILEAGE_NEXTSERVICE_MAX'])

# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'SERVICE_DATE', 'SERVICE_DETAILS', 'SERVICE_COSTS', 'SERVICE_MILEAGE_ON_SERVICE', 'SERVICE_MILEAGE_NEXTSERVICE', 'SERVICE_MILEAGE_NEXTSERVICE_MAX'])
  databank_services = pd.concat([databank_services, df])
databank_services = databank_services.set_index('ID')
  

## Get `TRIPS` table data
query = "SELECT ID, VEHICLE_ID, DRIVER_ID, TRIP_DATE, TRIP_DESCRIPTION, TRIP_COMMENTS, TRIP_TIME_OUT, TRIP_TIME_IN, TRIP_OPEN_MILEAGE, TRIP_CLOSE_MILEAGE, TRIP_TOTAL_MILEAGE FROM `carfleet`.`TRIPS`;"
rows = run_query(query)
   
# Create pandas dataframe 
databank_trips = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'TRIP_DATE', 'TRIP_DESCRIPTION', 'TRIP_COMMENTS', 'TRIP_TIME_OUT', 'TRIP_TIME_IN', 'TRIP_OPEN_MILEAGE', 'TRIP_CLOSE_MILEAGE', 'TRIP_TOTAL_MILEAGE'])
  
# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]], columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'TRIP_DATE', 'TRIP_DESCRIPTION', 'TRIP_COMMENTS', 'TRIP_TIME_OUT', 'TRIP_TIME_IN', 'TRIP_OPEN_MILEAGE', 'TRIP_CLOSE_MILEAGE', 'TRIP_TOTAL_MILEAGE'])
  databank_trips= pd.concat([databank_trips, df])
databank_trips = databank_trips.set_index('ID')
  

## Get `VEHICLES` table data
query = "SELECT ID, VEHICLE_ID, VEHICLE_PLATE_NUMBER, VEHICLE_TYPE, VEHICLE_BRAND, VEHICLE_MODEL, VEHICLE_SEATS, VEHICLE_FUEL_TYPE, VEHICLE_COLOUR, VEHICLE_CHASIS_NUMBER, VEHICLE_MANUFACTURE_YEAR, VEHICLE_PURCHASE_DATE, VEHICLE_PURCHASE_PRICE, VEHICLE_DISPOSITION_YEAR, VEHICLE_VENDOR, VEHICLE_DUTY, VEHICLE_COST_KM, VEHICLE_IMAGE FROM `carfleet`.`VEHICLES`;"
rows = run_query(query)
    
# Create pandas dataframes
databank_vehicles = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_PLATE_NUMBER', 'VEHICLE_TYPE', 'VEHICLE_BRAND', 'VEHICLE_MODEL', 'VEHICLE_SEATS', 'VEHICLE_FUEL_TYPE', 'VEHICLE_COLOUR', 'VEHICLE_CHASIS_NUMBER', 'VEHICLE_MANUFACTURE_YEAR', 'VEHICLE_PURCHASE_DATE', 'VEHICLE_PURCHASE_PRICE', 'VEHICLE_DISPOSITION_YEAR', 'VEHICLE_VENDOR', 'VEHICLE_DUTY', 'VEHICLE_COST_KM', 'VEHICLE_IMAGE'])
data_cars = pd.DataFrame(columns = ['VEHICLE_ID', 'VEHICLE_TYPE'])
  
# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_PLATE_NUMBER', 'VEHICLE_TYPE', 'VEHICLE_BRAND', 'VEHICLE_MODEL', 'VEHICLE_SEATS', 'VEHICLE_FUEL_TYPE', 'VEHICLE_COLOUR', 'VEHICLE_CHASIS_NUMBER', 'VEHICLE_MANUFACTURE_YEAR', 'VEHICLE_PURCHASE_DATE', 'VEHICLE_PURCHASE_PRICE', 'VEHICLE_DISPOSITION_YEAR', 'VEHICLE_VENDOR', 'VEHICLE_DUTY', 'VEHICLE_COST_KM', 'VEHICLE_IMAGE'])
  databank_vehicles = pd.concat([databank_vehicles, df])
databank_vehicles = databank_vehicles.set_index('ID')
# Drop last columns (Images)
databank_vehicles_excel = databank_vehicles.iloc[: , :-1]
    



### Database Excel Export Expander
with st.expander('Database Excel Export'):
  ## Show `DRIVERS` table dataframe
  st.subheader('Drivers data')
  st.dataframe(databank_drivers, use_container_width = True)
  
  
  ## Show `FUEL` table dataframe
  st.subheader('Fuel data')
  st.dataframe(databank_fuel, use_container_width = True)
  
  
  ## Show `INSURANCES` table dataframe
  st.subheader('Insurances data')
  st.dataframe(databank_insurances, use_container_width = True)
  
  
  ## Show `REPAIRS` table dataframe
  st.subheader('Repairs data')
  st.dataframe(databank_repairs, use_container_width = True)
  
  
  ## Show `SERVICES` table dataframe
  st.subheader('Services data')
  st.dataframe(databank_services, use_container_width = True)
  
  
  ## Show `TRIPS` table dataframe
  st.subheader('Trips data')
  st.dataframe(databank_trips, use_container_width = True)
  
  
  ## Show `VEHICLES` table dataframe
  st.subheader('Vehicles data')
  st.dataframe(databank_vehicles, use_container_width = True)
  
  
  ## Export tables to Excel workbook
  if st.button('Database Exel Export'):
    # Do the exporting
    export_excel('Drivers', 'I', [{'header': 'DRIVER_ID'}, {'header': 'DRIVER_FORENAME'}, {'header': 'DRIVER_SURNAME'}, {'header': 'DRIVER_NATIONAL_ID'}, {'header': 'DRIVER_MOBILE_NO'}, {'header': 'DRIVER_LICENSE_NO'}, {'header': 'DRIVER_LICENSE_CLASS'}, {'header': 'DRIVER_PSV_BADGE'}, {'header': 'DRIVER_NOTES'},], int(len(databank_drivers_excel) + 1), databank_drivers_excel,
                'Fuel', 'I', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'VEHICLE_FUEL_AMOUNT'}, {'header': 'VEHICLE_FUEL_COST'}, {'header': 'VEHICLE_FUEL_TYPE'}, {'header': 'VEHICLE_FUEL_DATE'}, {'header': 'VEHICLE_DISTANCE'}, {'header': 'FUEL_SHORTAGE'}, {'header': 'COST_CENTRE'},], int(len(databank_fuel) + 1), databank_fuel,
                'Insurances', 'E', [{'header': 'VEHICLE_ID'}, {'header': 'INSURANCE_DETAILS'}, {'header': 'INSURANCES_TYPE'}, {'header': 'INSURANCE_START_DATE'}, {'header': 'INSURANCE_EXPIRY_DATE'},], int(len(databank_insurances) + 1), databank_insurances,
                'Repairs', 'H', [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_REPAIR_DETAILS'}, {'header': 'VEHICLE_REPAIR_DATE'}, {'header': 'VEHICLE_REPAIR_COSTS'}, {'header': 'VEHICLE_SPARE_PARTS'}, {'header': 'VEHICLE_DOWN_TIME'}, {'header': 'SERVICE_CENTRE_PERSON'}, {'header': 'COST_CENTRE'},], int(len(databank_repairs) + 1), databank_repairs,
                'Services', 'H', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'SERVICE_DATE'}, {'header': 'SERVICE_DETAILS'}, {'header': 'SERVICE_COSTS'}, {'header': 'SERVICE_MILEAGE_ON_SERVICE'}, {'header': 'SERVICE_MILEAGE_NEXTSERVICE'}, {'header': 'SERVICE_MILEAGE_NEXTSERVICE_MAX'},], int(len(databank_services) + 1), databank_services,
                'Trips', 'J', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'TRIP_DATE'}, {'header': 'TRIP_DESCRIPTION'}, {'header': 'TRIP_COMMENTS'},{'header': 'TRIP_TIME_OUT'}, {'header': 'TRIP_TIME_IN'}, {'header': 'TRIP_OPEN_MILEAGE'}, {'header': 'TRIP_CLOSE_MILEAGE'}, {'header': '`TRIP_TOTAL_MILEAGE'},], int(len(databank_trips) + 1), databank_trips,
                'Vehicles', 'P', [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_PLATE_NUMBER'}, {'header': 'VEHICLE_TYPE'}, {'header': 'VEHICLE_BRAND'}, {'header': 'VEHICLE_MODEL'}, {'header': 'VEHICLE_SEATS'}, {'header': 'VEHICLE_FUEL_TYPE'}, {'header': 'VEHICLE_COLOUR'}, {'header': 'VEHICLE_CHASIS_NUMBER'}, {'header': 'VEHICLE_MANUFACTURE_YEAR'}, {'header': 'VEHICLE_PURCHASE_DATE'}, {'header': 'VEHICLE_PURCHASE_PRICE'}, {'header': 'VEHICLE_DISPOSITION_YEAR'}, {'header': 'VEHICLE_VENDOR'}, {'header': 'VEHICLE_DUTY'}, {'header': 'VEHICLE_COST_KM'},], int(len(databank_vehicles) + 1), databank_vehicles_excel)



### Custom Tab with IDs
chosen_id = stx.tab_bar(data = [
  stx.TabBarItemData(id = 1, title = "Drivers", description = "Drivers at KCH"),
  stx.TabBarItemData(id = 2, title = "Fuel", description = "Fuel consumption at KCH"),
  stx.TabBarItemData(id = 3, title = "Insurances", description = "Insurances at KCH"),
  stx.TabBarItemData(id = 4, title = "Repairs", description = "Repairs at KCH"),
  stx.TabBarItemData(id = 5, title = "Services", description = "Services at KCH"),
  stx.TabBarItemData(id = 6, title = "Trips", description = "Trips at KCH"),
  stx.TabBarItemData(id = 7, title = "Vehicles", description = "Vehicles at KCH"),
  ], default = 1)


with st.form("Car Fleet Management", clear_on_submit = True):
  ## tab `Fuel Consumption`   
  if (f"{chosen_id}" == '1'):
    st.title('Drivers')

    
    ## Input for new `Driver` data
    # Get latest ID from database
    id = lastID(url = "carfleet.DRIVERS")   
    id = st.text_input(label = 'ID', value = id, disabled = True)
    driver_id = st.text_input(label = 'Driver ID', placeholder = 'Driver ID?')
    driver_forename = st.text_input(label = 'Forename', placeholder = 'Forename?')
    driver_surname = st.text_input(label = 'Surname', placeholder = 'Surname?')
    driver_national_id = st.text_input(label = 'National ID', placeholder = 'National ID number?')
    driver_mobile_no = st.text_input(label = 'Mobile number', placeholder = 'Mobile number?')
    driver_license_no = st.text_input(label = 'License number', placeholder = 'License number?')
    driver_license_class = st.text_input(label = 'License Class', placeholder = 'License class?')
    driver_psv_badge = st.text_input(label = 'PSV Badge', placeholder = 'PSV Badge?')
    driver_notes = st.text_input(label = 'Notes', placeholder = 'Notes?')
    uploaded_file = st.file_uploader(label = "Upload a picture (256×360)", type = 'png')
    
    # empty image
    driver_image = ''
    if uploaded_file is not None:
      driver_image = uploaded_file.getvalue()
          
    else:
      driver_image = loadFile("images/placeholder.png")
        
    
    ## Submit Button `Create new Driver`
    submitted = st.form_submit_button("Create new Driver")
    if submitted:
      # Get latest ID from database
      id = lastID(url = "carfleet.DRIVERS")
      query = "INSERT INTO `carfleet`.`DRIVERS`(ID, DRIVER_ID, DRIVER_FORENAME, DRIVER_SURNAME, DRIVER_NATIONAL_ID, DRIVER_MOBILE_NO, DRIVER_LICENSE_NO, DRIVER_LICENSE_CLASS, DRIVER_PSV_BADGE, DRIVER_NOTES) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(id, driver_id, driver_forename, driver_surname, driver_national_id, driver_mobile_no, driver_license_no, driver_license_class, driver_psv_badge, driver_notes)
      run_query(query)
      conn.commit()
      
            
      ## Upload picture to database
      pictureUploader(driver_image, id)
      
      
  ## tab `Fuel Consumption`   
  elif (f"{chosen_id}" == '2'):
    st.title('Fuel Consumption')

    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export `Fuel` dataframe to Excel Makro file
      export = True
      
      
  ## tab `Insurances`   
  elif (f"{chosen_id}" == '3'):
    st.title('Insurances')

    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export `Insurances` dataframe to Excel Makro file
      export = True
  
  
  ## tab `Repairs` 
  elif (f"{chosen_id}" == '4'):
    st.title('Repairs')

  
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      export = True
      
      
  ## tab `Services`   
  elif (f"{chosen_id}" == '5'):
    st.title('Services')

    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export `Services` dataframe to Excel Makro file
      export = True
      
      
  ## tab `Trips`   
  elif (f"{chosen_id}" == '6'):
    st.title('Trips')

    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export `Trips` dataframe to Excel Makro file
      export = True
  
      
  ## tab `Vehicles`
  elif (f"{chosen_id}" == '7'):
    st.title('Vehicles')
    
    
    ## Columns
    col1, col2, col3 = st.columns(3)
    with col1:
      st.header("Vehicle ID")
      st.write(databank_vehicles._get_value(1, 'VEHICLE_ID'))
      st.subheader(databank_vehicles._get_value(1, 'VEHICLE_BRAND'))
      st.write(databank_vehicles._get_value(1, 'VEHICLE_MODEL'))
      st.image(databank_vehicles._get_value(1, 'VEHICLE_IMAGE'))

    # Coloumn 2
    with col2:
      st.header("Vehicle ID")
      st.write(databank_vehicles._get_value(2, 'VEHICLE_ID'))
      st.subheader(databank_vehicles._get_value(2, 'VEHICLE_BRAND'))
      st.write(databank_vehicles._get_value(2, 'VEHICLE_MODEL'))
      st.image(databank_vehicles._get_value(2, 'VEHICLE_IMAGE'))

    # Column 3
    with col3:
      st.header("Vehicle ID")
      st.write(databank_vehicles._get_value(3, 'VEHICLE_ID'))
      st.subheader(databank_vehicles._get_value(3, 'VEHICLE_BRAND'))
      st.write(databank_vehicles._get_value(3, 'VEHICLE_MODEL'))
      st.image(databank_vehicles._get_value(3, 'VEHICLE_IMAGE'))

    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export `Vehicles` dataframe to Excel Makro file
      export = True


    
#### Outside the form
### Data analysis
## Data analysis for `Drivers`
if (f"{chosen_id}" == '1'):
  ## Export `Drivers` dataframe to Excel Makro file
  if st.button('Export Drivers data to Excel document'):
    export_excel('Drivers', 'I', [{'header': 'DRIVER_ID'}, {'header': 'DRIVER_FORENAME'}, {'header': 'DRIVER_SURNAME'}, {'header': 'DRIVER_NATIONAL_ID'}, {'header': 'DRIVER_MOBILE_NO'}, {'header': 'DRIVER_LICENSE_NO'}, {'header': 'DRIVER_LICENSE_CLASS'}, {'header': 'DRIVER_PSV_BADGE'}, {'header': 'DRIVER_NOTES'},], int(len(databank_drivers_excel) + 1), databank_drivers_excel)

  
## Data analysis for `Fuel`
elif (f"{chosen_id}" == '2'):
  ## Export `Fuel` dataframe to Excel Makro file
  if st.button('Export Fuel data to Excel document'):
    export_excel('Fuel', 'I', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'VEHICLE_FUEL_AMOUNT'}, {'header': 'VEHICLE_FUEL_COST'}, {'header': 'VEHICLE_FUEL_TYPE'}, {'header': 'VEHICLE_FUEL_DATE'}, {'header': 'VEHICLE_DISTANCE'}, {'header': 'FUEL_SHORTAGE'}, {'header': 'COST_CENTRE'},], int(len(databank_fuel) + 1), databank_fuel)

  
  ## Average Fuel Consumption Chart
  # Checking for unique Vehicles IDs
  vehicles = check_vehicles(column = 'VEHICLE_ID', data = databank_fuel)
  # Prepare Selectbox list
  vehicles_list = list(vehicles)
  vehicles_list.insert(0, 'All vehicles')
  # Selectbox for choosing vehicle
  selected_vehicle = st.selectbox('All vehicles or a specific?', options = vehicles_list, index = 0)
  if (selected_vehicle != 'All vehicles'):
    vehicles = selected_vehicle


  ## Calculate average fuel consumption per Vehicle
  if (selected_vehicle == 'All vehicles'):
    data_fuel_rate_average = pd.DataFrame(columns = ['Vehicle ID', 'Average Fuel Consumption'])
    for i in range(len(vehicles)):
      query = "SELECT ID, VEHICLE_ID, VEHICLE_FUEL_AMOUNT, VEHICLE_DISTANCE FROM `carfleet`.`FUEL` WHERE VEHICLE_ID = %s;" %(vehicles[i])
      rows = run_query(query)
      i = 0
      fuel = 0.0
      for row in rows:
        i += 1
        fuel += round(float(row[3]) / float(row[2]), 2)
      df = pd.DataFrame([[row[1], round((fuel / i), 2)]], columns = ['Vehicle ID', 'Average Fuel Consumption'])
      data_fuel_rate_average = pd.concat([data_fuel_rate_average, df])
    data_fuel_rate_average = data_fuel_rate_average.set_index('Vehicle ID')
    
    # Plotting
    st.bar_chart(data_fuel_rate_average, x = vehicles)
  
  
  ## Show fuel consumption of one vehicle
  else:
    data_fuel_rate = pd.DataFrame(columns = ['Date', 'Fuel Consumption Rate'])
    query = "SELECT ID, VEHICLE_ID, VEHICLE_FUEL_AMOUNT, VEHICLE_DISTANCE, VEHICLE_FUEL_DATE FROM `carfleet`.`FUEL` WHERE VEHICLE_ID = %s;" %(vehicles)
    rows = run_query(query)
    fuel = 0.0
    for row in rows:
      distance = round(float(row[3]), 2)
      fuel = round(float(row[2]), 2)
      df = pd.DataFrame([[row[4], distance / fuel]], columns = ['Date', 'Fuel Consumption Rate'])
      data_fuel_rate = pd.concat([data_fuel_rate, df])
    data_fuel_rate = data_fuel_rate.set_index('Date')
    
    # Plotting
    st.bar_chart(data_fuel_rate)

  
## Data analysis for `Insurances`
elif (f"{chosen_id}" == '3'):
  ## Export `Insurances` dataframe to Excel Makro file
  if st.button('Export Insurances data to Excel document'):
    export_excel('Insurances', 'E', [{'header': 'VEHICLE_ID'}, {'header': 'INSURANCE_DETAILS'}, {'header': 'INSURANCES_TYPE'}, {'header': 'INSURANCE_START_DATE'}, {'header': 'INSURANCE_EXPIRY_DATE'},], int(len(databank_insurances) + 1), databank_insurances)


## Data analysis for `Repairs`
elif (f"{chosen_id}" == '4'):
  ## Export `Repairs` dataframe to Excel Makro file
  if st.button('Export Repairs data to Excel document'):
    export_excel('Repairs', 'H', [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_REPAIR_DETAILS'}, {'header': 'VEHICLE_REPAIR_DATE'}, {'header': 'VEHICLE_REPAIR_COSTS'}, {'header': 'VEHICLE_SPARE_PARTS'}, {'header': 'VEHICLE_DOWN_TIME'}, {'header': 'SERVICE_CENTRE_PERSON'}, {'header': 'COST_CENTRE'},], int(len(databank_repairs) + 1), databank_repairs)
    
    
  ## Repair cost chart
  # Checking for unique vehicles IDs
  vehicles = check_vehicles(column = 'VEHICLE_ID', data = databank_repairs)
  # Prepare Selectbox list
  vehicles_list = list(vehicles)
  vehicles_list.insert(0, 'All vehicles')
  # Selectbox for choosing vehicle
  selected_vehicle = st.selectbox('All vehicles or a specific?', options = vehicles_list, index = 0)
  if (selected_vehicle != 'All vehicles'):
    vehicles = selected_vehicle
    
  # Calculate repair costs per vehicle
  if (selected_vehicle == 'All vehicles'): 
    data_repair_costs = pd.DataFrame(columns = ['Vehicle ID', 'Repair costs'])
    for i in range(len(vehicles)):
      query = "SELECT ID, VEHICLE_ID, VEHICLE_REPAIR_COSTS FROM `carfleet`.`REPAIRS` WHERE VEHICLE_ID = %s;" %(vehicles[i])
      rows = run_query(query)
      costs = 0.0
      for row in rows:
        costs += round(float(row[2]), 2)
      df = pd.DataFrame([[row[1], costs]], columns = ['Vehicle ID', 'Repair costs'])
      data_repair_costs = pd.concat([data_repair_costs, df])
    data_repair_costs = data_repair_costs.set_index('Vehicle ID')
    
    # Plotting
    st.bar_chart(data_repair_costs, x = vehicles)

  
  ## Show repair costs per incident
  else:
    data_repair_costs = pd.DataFrame(columns = ['Spare part', 'Repair cost'])
    query = "SELECT ID, VEHICLE_ID, VEHICLE_REPAIR_DETAILS, VEHICLE_REPAIR_COSTS FROM `carfleet`.`REPAIRS` WHERE VEHICLE_ID = %s;" %(vehicles)
    rows = run_query(query)
    for row in rows:
      df = pd.DataFrame([[row[2], round(float(row[3]), 1)]], columns = ['Repair Details', 'Repair cost'])
      data_repair_costs = pd.concat([data_repair_costs, df])
    data_repair_costs = data_repair_costs.set_index('Repair Details')
    
    # Plotting
    st.bar_chart(data_repair_costs)

  
## Data analysis for `Services`
elif (f"{chosen_id}" == '5'):
  ## Export `Services` dataframe to Excel Makro file
  if st.button('Export Services data to Excel document'):
    export_excel('Services', 'H', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'SERVICE_DATE'}, {'header': 'SERVICE_DETAILS'}, {'header': 'SERVICE_COSTS'}, {'header': 'SERVICE_MILEAGE_ON_SERVICE'}, {'header': 'SERVICE_MILEAGE_NEXTSERVICE'}, {'header': 'SERVICE_MILEAGE_NEXTSERVICE_MAX'},], int(len(databank_services) + 1), databank_services)
  
  
## Data analysis for `Trips`
elif (f"{chosen_id}" == '6'):
  ## Export `Trips` dataframe to Excel Makro file
  if st.button('Export Trips data to Excel document'):
    export_excel('Trips', 'J', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'TRIP_DATE'}, {'header': 'TRIP_DESCRIPTION'}, {'header': 'TRIP_COMMENTS'},{'header': 'TRIP_TIME_OUT'}, {'header': 'TRIP_TIME_IN'}, {'header': 'TRIP_OPEN_MILEAGE'}, {'header': 'TRIP_CLOSE_MILEAGE'}, {'header': '`TRIP_TOTAL_MILEAGE'},], int(len(databank_trips) + 1), databank_trips)
    
   
## Data analysis for `Vehicles`
elif (f"{chosen_id}" == '7'):
  ## Export `Vehicles` dataframe to Excel Makro file
  if st.button('Export Vehicles data to Excel document'):
    export_excel('Vehicles', 'P', [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_PLATE_NUMBER'}, {'header': 'VEHICLE_TYPE'}, {'header': 'VEHICLE_BRAND'}, {'header': 'VEHICLE_MODEL'}, {'header': 'VEHICLE_SEATS'}, {'header': 'VEHICLE_FUEL_TYPE'}, {'header': 'VEHICLE_COLOUR'}, {'header': 'VEHICLE_CHASIS_NUMBER'}, {'header': 'VEHICLE_MANUFACTURE_YEAR'}, {'header': 'VEHICLE_PURCHASE_DATE'}, {'header': 'VEHICLE_PURCHASE_PRICE'}, {'header': 'VEHICLE_DISPOSITION_YEAR'}, {'header': 'VEHICLE_VENDOR'}, {'header': 'VEHICLE_DUTY'}, {'header': 'VEHICLE_COST_KM'},], int(len(databank_vehicles) + 1), databank_vehicles_excel)
  
  
  ## Plotting
  # Checking for unique vehicles types
  vehicles = check_vehicles(column = 'VEHICLE_TYPE', data = databank_vehicles)
  # Calculate total amount of vehicles per type / category
  data_cars= pd.DataFrame(columns = ['Vehicle Type', 'Amount'])
  for i in range(len(vehicles)):
    query = "SELECT VEHICLE_TYPE FROM `carfleet`.`VEHICLES` WHERE VEHICLE_TYPE = '%s';" %(vehicles[i])
    rows = run_query(query)
    amount = 0
    for row in rows:
      amount += 1
    df = pd.DataFrame([[row[0], amount]], columns = ['Vehicle Type', 'Amount'])
    data_cars = pd.concat([data_cars, df])
  data_cars = data_cars.set_index('Vehicle Type')
  st.bar_chart(data_cars)

  
