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
  page_title = "KCH Car Fleet Management System",
  page_icon = "images/thumbnail_car_fleet.png",
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = { 
         'Get Help': 'http://www.health.gov.mw/index.php/contact-moh/head-office',
         'Report a bug': "http://www.health.gov.mw/index.php/contact-moh/head-office",
         'About': "This is the KCH Car Fleet Management System Version 0.2.0"
        }
)




#### Sidebar  (password check?)
### Sidebar Header 
## Sidebar Image
st.sidebar.image('images/MoH.png')




#### OS Check
### Check for 3 different platforms
## Check which OS
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
    return mysql.connector.connect(**st.secrets["mysql_car"])
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
 
    
    
### Function: pictureUploaderDrivers = uploads driver images
def pictureUploaderDrivers(image, index):
  # Initialize connection
  connection = mysql.connector.connect(**st.secrets["mysql_car"])
  cursor = connection.cursor()
  
  # SQL statement
  sql_insert_blob_query = """ UPDATE DRIVERS SET DRIVER_IMAGE = %s WHERE ID = %s;"""
  
  # Convert data into tuple format
  insert_blob_tuple = (image, index)
  result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
  connection.commit()
  


### Function: pictureUploaderVehicles = uploads vehicle images
def pictureUploaderVehicles(image, index):
  # Initialize connection
  connection = mysql.connector.connect(**st.secrets["mysql_car"])
  cursor = connection.cursor()
  
  # SQL statement
  sql_insert_blob_query = """ UPDATE VEHICLES SET VEHICLE_IMAGE = %s WHERE ID = %s;"""
  
  # Convert data into tuple format
  insert_blob_tuple = (image, index)
  result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
  connection.commit()
 
  
  
### Function: lastID = checks for last ID number in Table (to add data after)
def lastID(url):
  query = "SELECT MAX(ID) FROM %s;" %(url)
  rows = run_query(query)
  id = 0
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

# Current Image data
if ('image' not in st.session_state):
  st.session_state['image'] = loadFile('images/No_Image.png')




#### Main Program (password protection)
### Title Header
## Header information
with st.expander("Header", expanded = True):
  st.title('Car Fleet Management System')
  st.image('images/car_fleet.png')
  st.subheader('Kamuzu Central Hospital vehicle data')
  st.write('All data related to the KCH car fleet is stored in a local MySQL databank.')
  st.write('The Car Fleet Managmenet System is developed with Python and installed on WSL.')
  st.write('It uses the Streamlit framework for visualisation which turns Python scipts into web apps.')
    
    
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
query = "SELECT ID, VEHICLE_ID, DRIVER_ID, FUEL_AMOUNT, FUEL_COST, FUEL_TYPE, FUEL_DATE, FUEL_DISTANCE, FUEL_SHORTAGE, COST_CENTRE FROM `carfleet`.`FUEL`;"
rows = run_query(query)
   
# Create pandas dataframe 
databank_fuel = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'FUEL_AMOUNT', 'FUEL_COST', 'FUEL_TYPE', 'FUEL_DATE', 'FUEL_DISTANCE', 'FUEL_SHORTAGE', 'COST_CENTRE'])
  
# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]]], columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'FUEL_AMOUNT', 'FUEL_COST', 'FUEL_TYPE', 'FUEL_DATE', 'FUEL_DISTANCE', 'FUEL_SHORTAGE', 'COST_CENTRE'])
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
query = "SELECT ID, VEHICLE_ID, REPAIR_DETAILS, REPAIR_DATE, REPAIR_COSTS, REPAIR_SPARE_PARTS, REPAIR_DOWN_TIME, REPAIR_CENTRE_PERSON, COST_CENTRE FROM `carfleet`.`REPAIRS`;"
rows = run_query(query)
    
# Create pandas dataframe
databank_repairs = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'REPAIR_DETAILS', 'REPAIR_DATE', 'REPAIR_COSTS', 'REPAIR_SPARE_PARTS', 'REPAIR_DOWN_TIME', 'REPAIR_CENTRE_PERSON', 'COST_CENTRE'])
    
# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['ID', 'VEHICLE_ID', 'REPAIR_DETAILS', 'REPAIR_DATE', 'REPAIR_COSTS', 'REPAIR_SPARE_PARTS', 'REPAIR_DOWN_TIME', 'REPAIR_CENTRE_PERSON', 'COST_CENTRE'])
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
query = "SELECT ID, VEHICLE_ID, DRIVER_ID, TRIP_DATE, TRIP_DESCRIPTION, TRIP_COMMENTS, TRIP_TIME_OUT, TRIP_TIME_IN, TRIP_OPEN_MILEAGE, TRIP_CLOSE_MILEAGE, TRIP_DISTANCE FROM `carfleet`.`TRIPS`;"
rows = run_query(query)
   
# Create pandas dataframe 
databank_trips = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'TRIP_DATE', 'TRIP_DESCRIPTION', 'TRIP_COMMENTS', 'TRIP_TIME_OUT', 'TRIP_TIME_IN', 'TRIP_OPEN_MILEAGE', 'TRIP_CLOSE_MILEAGE', 'TRIP_DISTANCE'])
  
# Populate dataframe
for row in rows:
  df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]], columns = ['ID', 'VEHICLE_ID', 'DRIVER_ID', 'TRIP_DATE', 'TRIP_DESCRIPTION', 'TRIP_COMMENTS', 'TRIP_TIME_OUT', 'TRIP_TIME_IN', 'TRIP_OPEN_MILEAGE', 'TRIP_CLOSE_MILEAGE', 'TRIP_DISTANCE'])
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
    st.subheader('Enter drivers data')
    
    
    ## Input for new `DRIVERS` data
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
    #driver_image = ''
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
      pictureUploaderDrivers(driver_image, id)
      st.experimental_rerun()
      
      
  ## tab `Fuel Consumption`   
  elif (f"{chosen_id}" == '2'):
    st.title('Fuel Consumption')
    st.subheader('Enter fuel consumption data')

    
    ## Input for new `FUEL` data
    # Get latest ID from database
    id = lastID(url = "carfleet.FUEL")   
    id = st.text_input(label = 'ID', value = id, disabled = True)
    vehicle_id = st.text_input(label = 'Vehicle ID', placeholder = 'Vehicle ID?')
    driver_id = st.text_input(label = 'Driver ID', placeholder = 'Driver ID?')
    fuel_amount = st.text_input(label = 'Amount', placeholder = 'Amount?')
    fuel_cost = st.text_input(label = 'Cost', placeholder = 'Cost?')
    fuel_type = st.text_input(label = 'Type', placeholder = 'Type?')
    fuel_date = st.text_input(label = 'Date', placeholder = 'Date?')
    fuel_distance = st.text_input(label = 'Distance', placeholder = 'Distance?')
    fuel_shortage = st.text_input(label = 'Shortage', placeholder = 'Shortage?')
    cost_centre = st.text_input(label = 'Cost Centre', placeholder = 'Cost Centre?')

    
    ## Submit Button `Create new Refueling`
    submitted = st.form_submit_button("Create new Refueling")
    if submitted:
      # Get latest ID from database
      id = lastID(url = "carfleet.FUEL")
      query = "INSERT INTO `carfleet`.`FUEL`(ID, VEHICLE_ID, DRIVER_ID, FUEL_AMOUNT, FUEL_COST, FUEL_TYPE, FUEL_DATE, FUEL_DISTANCE, FUEL_SHORTAGE, COST_CENTRE) VALUES (%s, '%s', '%s', %s, %s, '%s', '%s', %s, '%s', '%s');" %(id, vehicle_id, driver_id, fuel_amount, fuel_cost, fuel_type, fuel_date, fuel_distance, fuel_shortage, cost_centre)
      run_query(query)
      conn.commit()
      st.experimental_rerun()
      
      
  ## tab `Insurances`   
  elif (f"{chosen_id}" == '3'):
    st.title('Insurances')
    st.subheader('Enter insurances data')

    
    ## Input for new `INSURANCES` data
    # Get latest ID from database
    id = lastID(url = "carfleet.INSURANCES")   
    id = st.text_input(label = 'ID', value = id, disabled = True)
    vehicle_id = st.text_input(label = 'Vehicle ID', placeholder = 'Vehicle ID?')
    insurance_details = st.text_input(label = 'Details', placeholder = 'Details?')
    insurance_type = st.text_input(label = 'Type', placeholder = 'Type?')
    insurance_start_date = st.text_input(label = 'Start date', placeholder = 'Start date?')
    insurance_expiry_date = st.text_input(label = 'Expiry date', placeholder = 'Expiry date?')
    

    ## Submit Button `Create new Insurance`
    submitted = st.form_submit_button("Create new Insurance")
    if submitted:
      # Get latest ID from database
      id = lastID(url = "carfleet.INSURANCES")
      query = "INSERT INTO `carfleet`.`INSURANCES`(ID, VEHICLE_ID, INSURANCE_DETAILS, INSURANCES_TYPE, INSURANCE_START_DATE, INSURANCE_EXPIRY_DATE) VALUES (%s, '%s', '%s', '%s', '%s', '%s');" %(id, vehicle_id, insurance_details, insurance_type, insurance_start_date, insurance_expiry_date)
      run_query(query)
      conn.commit()
      st.experimental_rerun()
  
  
  ## tab `Repairs` 
  elif (f"{chosen_id}" == '4'):
    st.title('Repairs')
    st.subheader('Enter repairs data')

  
    ## Input for new `REPAIRS` data
    # Get latest ID from database
    id = lastID(url = "carfleet.REPAIRS")   
    id = st.text_input(label = 'ID', value = id, disabled = True)
    vehicle_id = st.text_input(label = 'Vehicle ID', placeholder = 'Vehicle ID?')
    repair_details = st.text_input(label = 'Details', placeholder = 'Details?')
    repair_date = st.text_input(label = 'Date', placeholder = 'Date?')
    repair_costs = st.text_input(label = 'Costs', placeholder = 'Costs?')
    repair_spare_parts = st.text_input(label = 'Spare parts', placeholder = 'Spare parts?')
    repair_down_time = st.text_input(label = 'Down time', placeholder = 'Down time?')
    repair_centre_person = st.text_input(label = 'Centre / Person', placeholder = 'Centre / Person?')
    cost_centre = st.text_input(label = 'Cost Centre', placeholder = 'Cost Centre?')
    
    
    ## Submit Button `Create new Repair`
    submitted = st.form_submit_button("Create new Repair")
    if submitted:
      # Get latest ID from database
      id = lastID(url = "carfleet.REPAIRS")
      query = "INSERT INTO `carfleet`.`REPAIRS`(ID, VEHICLE_ID, REPAIR_DETAILS, REPAIR_DATE, REPAIR_COSTS, REPAIR_SPARE_PARTS, REPAIR_DOWN_TIME, REPAIR_CENTRE_PERSON, COST_CENTRE) VALUES (%s, '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s');" %(id, vehicle_id, repair_details, repair_date, repair_costs, repair_spare_parts, repair_down_time, repair_centre_person, cost_centre)
      run_query(query)
      conn.commit()
      st.experimental_rerun()
      
      
  ## tab `Services`   
  elif (f"{chosen_id}" == '5'):
    st.title('Services')
    st.subheader('Enter services data')

    
    ## Input for new `SERVICES` data
    # Get latest ID from database
    id = lastID(url = "carfleet.SERVICES")   
    id = st.text_input(label = 'ID', value = id, disabled = True)
    vehicle_id = st.text_input(label = 'Vehicle ID', placeholder = 'Vehicle ID?')
    driver_id = st.text_input(label = 'Driver ID', placeholder = 'Driver ID?')
    service_date = st.text_input(label = 'Date', placeholder = 'Date?')
    service_details = st.text_input(label = 'Details', placeholder = 'Details?')
    service_costs = st.text_input(label = 'Costs', placeholder = 'Costs?')
    service_mileage_on_service = st.text_input(label = 'Mileage', placeholder = 'Mileage?')
    service_mileage_nextservice = st.text_input(label = 'Next service mileage', placeholder = 'Next service mileage?')
    service_mileage_nextservice_max = st.text_input(label = 'Next service max. mileage', placeholder = 'Next service max. mileage?')
    
    
    ## Submit Button `Create new Service`
    submitted = st.form_submit_button("Create new Service")
    if submitted:
      # Get latest ID from database
      id = lastID(url = "carfleet.SERVICES")
      query = "INSERT INTO `carfleet`.`SERVICES`(ID, VEHICLE_ID, DRIVER_ID, SERVICE_DATE, SERVICE_DETAILS, SERVICE_COSTS, SERVICE_MILEAGE_ON_SERVICE, SERVICE_MILEAGE_NEXTSERVICE, SERVICE_MILEAGE_NEXTSERVICE_MAX) VALUES (%s, '%s', '%s', '%s', '%s', %s, %s, %s, %s);" %(id, vehicle_id, driver_id, service_date, service_details, service_costs, service_mileage_on_service, service_mileage_nextservice, service_mileage_nextservice_max)
      run_query(query)
      conn.commit()
      st.experimental_rerun()
      
      
  ## tab `Trips`   
  elif (f"{chosen_id}" == '6'):
    st.title('Trips')
    st.subheader('Enter trips data')

    
    ## Input for new `TRIPS` data
    # Get latest ID from database
    id = lastID(url = "carfleet.TRIPS")   
    id = st.text_input(label = 'ID', value = id, disabled = True)
    vehicle_id = st.text_input(label = 'Vehicle ID', placeholder = 'Vehicle ID?')
    driver_id = st.text_input(label = 'Driver ID', placeholder = 'Driver ID?')
    trip_date = st.text_input(label = 'Date', placeholder = 'Date?')
    trip_description = st.text_input(label = 'Description', placeholder = 'Description?')
    trip_comments = st.text_input(label = 'Comments', placeholder = 'Comments?')
    trip_time_out = st.text_input(label = 'Time out', placeholder = 'Time out?')
    trip_time_in = st.text_input(label = 'Time in', placeholder = 'Time in?')
    trip_open_mileage = st.text_input(label = 'Open mileage', placeholder = 'Open mileage?')
    trip_close_mileage = st.text_input(label = 'Close mileage', placeholder = 'Close mileage?')
    trip_distance = st.text_input(label = 'Distance', placeholder = 'Distance?')


    ## Submit Button `Create new Trip`
    submitted = st.form_submit_button("Create new Trip")
    if submitted:
      # Get latest ID from database
      id = lastID(url = "carfleet.TRIPS")
      query = "INSERT INTO `carfleet`.`TRIPS`(ID, VEHICLE_ID, DRIVER_ID, TRIP_DATE, TRIP_DESCRIPTION, TRIP_COMMENTS, TRIP_TIME_OUT, TRIP_TIME_IN, TRIP_OPEN_MILEAGE, TRIP_CLOSE_MILEAGE, TRIP_DISTANCE) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s);" %(id, vehicle_id, driver_id, trip_date, trip_description, trip_comments, trip_time_out, trip_time_in, trip_open_mileage, trip_close_mileage, trip_distance)
      run_query(query)
      conn.commit()
      st.experimental_rerun()
  
      
  ## tab `Vehicles`
  elif (f"{chosen_id}" == '7'):
    st.title('Vehicles')
    st.subheader('Enter vehicles data')
    
    
    ## Input for new `VEHICLES` data
    # Get latest ID from database
    id = lastID(url = "carfleet.VEHICLES")   
    id = st.text_input(label = 'ID', value = id, disabled = True)
    vehicle_id = st.text_input(label = 'Vehicle ID', placeholder = 'Vehicle ID?')
    vehicle_plate_number = st.text_input(label = 'Plate number', placeholder = 'Plate number?')
    vehicle_type = st.text_input(label = 'Type', placeholder = 'Type?')
    vehicle_brand = st.text_input(label = 'Brand', placeholder = 'Brand?')
    vehicle_model = st.text_input(label = 'Model', placeholder = 'Model?')
    vehicle_seats = st.text_input(label = 'Seats', placeholder = 'Seats?')
    vehicle_fuel_type = st.text_input(label = 'Fuel type', placeholder = 'Fuel type?')
    vehicle_colour = st.text_input(label = 'Colour', placeholder = 'Colour?')
    vehicle_chasis_number = st.text_input(label = 'Chasis number', placeholder = 'Chasis number?')
    vehicle_manufacture_year = st.text_input(label = 'Manufacture year', placeholder = 'Manufacture year?')
    vehicle_purchase_date = st.text_input(label = 'Purchase date', placeholder = 'Purchase date?')
    vehicle_purchase_price = st.text_input(label = 'Purchase price', placeholder = 'Purchase price?')
    vehicle_disposition_year = st.text_input(label = 'Disposition year', placeholder = 'Disposition year?')
    vehicle_vendor = st.text_input(label = 'Vendor', placeholder = 'Vendor?')
    vehicle_duty = st.text_input(label = 'Duty', placeholder = 'Duty?')
    vehicle_cost_km = st.text_input(label = 'Cost per km', placeholder = 'Cost per km?')
    uploaded_file = st.file_uploader(label = "Upload a picture (256×360)", type = 'png')
    
    if uploaded_file is not None:
      vehicle_image = uploaded_file.getvalue()
          
    else:
      vehicle_image = loadFile("images/placeholder.png")
        
    
    ## Submit Button `Create new Vehicles`
    submitted = st.form_submit_button("Create new Vehicle")
    if submitted:
      # Get latest ID from database
      id = lastID(url = "carfleet.VEHICLES")
      query = "INSERT INTO `carfleet`.`VEHICLES`(ID, VEHICLE_ID, VEHICLE_PLATE_NUMBER, VEHICLE_TYPE, VEHICLE_BRAND, VEHICLE_MODEL, VEHICLE_SEATS, VEHICLE_FUEL_TYPE, VEHICLE_COLOUR, VEHICLE_CHASIS_NUMBER, VEHICLE_MANUFACTURE_YEAR, VEHICLE_PURCHASE_DATE, VEHICLE_PURCHASE_PRICE, VEHICLE_DISPOSITION_YEAR, VEHICLE_VENDOR, VEHICLE_DUTY, VEHICLE_COST_KM) VALUES (%s, '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', %s, %s);" %(id, vehicle_id, vehicle_plate_number, vehicle_type, vehicle_brand, vehicle_model, vehicle_seats, vehicle_fuel_type, vehicle_colour, vehicle_chasis_number, vehicle_manufacture_year, vehicle_purchase_date, vehicle_purchase_price, vehicle_disposition_year, vehicle_vendor, vehicle_duty, vehicle_cost_km)
      run_query(query)
      conn.commit()
      
            
      ## Upload picture to database
      pictureUploaderVehicles(vehicle_image, id)
      st.experimental_rerun()



    
#### Outside the form
### Data analysis
## Data analysis for `Drivers`
if (f"{chosen_id}" == '1'):
  ## Export `Drivers` dataframe to Excel Makro file
  if st.button('Export Drivers data to Excel document'):
    export_excel('Drivers', 'I', [{'header': 'DRIVER_ID'}, {'header': 'DRIVER_FORENAME'}, {'header': 'DRIVER_SURNAME'}, {'header': 'DRIVER_NATIONAL_ID'}, {'header': 'DRIVER_MOBILE_NO'}, {'header': 'DRIVER_LICENSE_NO'}, {'header': 'DRIVER_LICENSE_CLASS'}, {'header': 'DRIVER_PSV_BADGE'}, {'header': 'DRIVER_NOTES'},], int(len(databank_drivers_excel) + 1), databank_drivers_excel)


  ## Show driver profiles in an expander
  with st.expander('Driver profiles', expanded = False):
    st.subheader('Driver profiles')
    col1, col2, col3 = st.columns(3)
    drivers = lastID(url = "carfleet.DRIVERS")  
  
    # Column 1
    with col1:
      for i in range(1, drivers, 3):
        st.image(databank_drivers._get_value(i, 'DRIVER_IMAGE'))
        st.write(databank_drivers._get_value(i, 'DRIVER_FORENAME'))
        st.write(databank_drivers._get_value(i, 'DRIVER_SURNAME'))
        st.subheader("Driver ID")
        st.write(databank_drivers._get_value(i, 'DRIVER_ID'))

    # Coloumn 2
    with col2:
      for i in range(2, drivers, 3):
        st.image(databank_drivers._get_value(i, 'DRIVER_IMAGE'))
        st.write(databank_drivers._get_value(i, 'DRIVER_FORENAME'))
        st.write(databank_drivers._get_value(i, 'DRIVER_SURNAME'))
        st.subheader("Driver ID")
        st.write(databank_drivers._get_value(i, 'DRIVER_ID'))

    # Column 3
    with col3:
      for i in range(3, drivers, 3):
        st.image(databank_drivers._get_value(i, 'DRIVER_IMAGE'))
        st.write(databank_drivers._get_value(i, 'DRIVER_FORENAME'))
        st.write(databank_drivers._get_value(i, 'DRIVER_SURNAME'))
        st.subheader("Driver ID")
        st.write(databank_drivers._get_value(i, 'DRIVER_ID'))
  
## Data analysis for `Fuel`
elif (f"{chosen_id}" == '2'):
  ## Export `Fuel` dataframe to Excel Makro file
  if st.button('Export Fuel data to Excel document'):
    export_excel('Fuel', 'I', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'FUEL_AMOUNT'}, {'header': 'FUEL_COST'}, {'header': 'FUEL_TYPE'}, {'header': 'FUEL_DATE'}, {'header': 'FUEL_DISTANCE'}, {'header': 'FUEL_SHORTAGE'}, {'header': 'COST_CENTRE'},], int(len(databank_fuel) + 1), databank_fuel)

  
  ## Show fuel consumtion statistics in an expander
  with st.expander('Fuel consumption statistics', expanded = False):
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
        query = "SELECT ID, VEHICLE_ID, FUEL_AMOUNT, FUEL_DISTANCE FROM `carfleet`.`FUEL` WHERE VEHICLE_ID = %s;" %(vehicles[i])
        rows = run_query(query)
        i = 0
        fuel = 0.0
        for row in rows:
          i += 1
          fuel += round((100 * float(row[2])) / float(row[3]), 2)
        df = pd.DataFrame([[row[1], round((fuel / i), 2)]], columns = ['Vehicle ID', 'Average Fuel Consumption'])
        data_fuel_rate_average = pd.concat([data_fuel_rate_average, df])
      data_fuel_rate_average = data_fuel_rate_average.set_index('Vehicle ID')
    
      # Plotting
      st.bar_chart(data_fuel_rate_average, x = vehicles)
  
  
    ## Show fuel consumption of one vehicle
    else:
      data_fuel_rate = pd.DataFrame(columns = ['Date', 'Fuel Consumption Rate'])
      query = "SELECT ID, VEHICLE_ID, FUEL_AMOUNT, FUEL_DISTANCE, FUEL_DATE FROM `carfleet`.`FUEL` WHERE VEHICLE_ID = %s;" %(vehicles)
      rows = run_query(query)
      fuel = 0.0
      for row in rows:
        distance = round(float(row[3]), 2)
        fuel = round(float(row[2]), 2)
        df = pd.DataFrame([[row[4], (fuel * 100) / distance]], columns = ['Date', 'Fuel Consumption Rate'])
        data_fuel_rate = pd.concat([data_fuel_rate, df])
      data_fuel_rate = data_fuel_rate.set_index('Date')
    
      # Plotting
      st.bar_chart(data_fuel_rate)

  
## Data analysis for `Insurances`
elif (f"{chosen_id}" == '3'):
  ## Export `Insurances` dataframe to Excel Makro file
  if st.button('Export Insurances data to Excel document'):
    export_excel('Insurances', 'E', [{'header': 'VEHICLE_ID'}, {'header': 'INSURANCE_DETAILS'}, {'header': 'INSURANCES_TYPE'}, {'header': 'INSURANCE_START_DATE'}, {'header': 'INSURANCE_EXPIRY_DATE'},], int(len(databank_insurances) + 1), databank_insurances)

  ## Show `Insurances` statistics in an expander
  with st.expander('Insurances statistics', expanded = False):
    st.write('Statistics')
    
    
## Data analysis for `Repairs`
elif (f"{chosen_id}" == '4'):
  ## Export `Repairs` dataframe to Excel Makro file
  if st.button('Export Repairs data to Excel document'):
    export_excel('Repairs', 'H', [{'header': 'VEHICLE_ID'}, {'header': 'REPAIR_DETAILS'}, {'header': 'REPAIR_DATE'}, {'header': 'REPAIR_COSTS'}, {'header': 'REPAIR_SPARE_PARTS'}, {'header': 'REPAIR_DOWN_TIME'}, {'header': 'REPAIR_CENTRE_PERSON'}, {'header': 'COST_CENTRE'},], int(len(databank_repairs) + 1), databank_repairs)
    
  
  ## Show `Repairs` statistics in an expander
  with st.expander('Repairs statistics', expanded = False):
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
        query = "SELECT ID, VEHICLE_ID, REPAIR_COSTS FROM `carfleet`.`REPAIRS` WHERE VEHICLE_ID = %s;" %(vehicles[i])
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
      query = "SELECT ID, VEHICLE_ID, REPAIR_DETAILS, REPAIR_COSTS FROM `carfleet`.`REPAIRS` WHERE VEHICLE_ID = %s;" %(vehicles)
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
  
  
  ## Show `Services` statistics in an expander
  with st.expander('Services statistics', expanded = False):
    st.write('Statistics')
    
    
## Data analysis for `Trips`
elif (f"{chosen_id}" == '6'):
  ## Export `Trips` dataframe to Excel Makro file
  if st.button('Export Trips data to Excel document'):
    export_excel('Trips', 'J', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'TRIP_DATE'}, {'header': 'TRIP_DESCRIPTION'}, {'header': 'TRIP_COMMENTS'},{'header': 'TRIP_TIME_OUT'}, {'header': 'TRIP_TIME_IN'}, {'header': 'TRIP_OPEN_MILEAGE'}, {'header': 'TRIP_CLOSE_MILEAGE'}, {'header': 'TRIP_DISTANCE'},], int(len(databank_trips) + 1), databank_trips)
    
  
  ## Show `Trips` statistics in an expander
  with st.expander('Trips statistics', expanded = False):
    st.write('Statistics')
    
   
## Data analysis for `Vehicles`
elif (f"{chosen_id}" == '7'):
  ## Export `Vehicles` dataframe to Excel Makro file
  if st.button('Export Vehicles data to Excel document'):
    export_excel('Vehicles', 'P', [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_PLATE_NUMBER'}, {'header': 'VEHICLE_TYPE'}, {'header': 'VEHICLE_BRAND'}, {'header': 'VEHICLE_MODEL'}, {'header': 'VEHICLE_SEATS'}, {'header': 'VEHICLE_FUEL_TYPE'}, {'header': 'VEHICLE_COLOUR'}, {'header': 'VEHICLE_CHASIS_NUMBER'}, {'header': 'VEHICLE_MANUFACTURE_YEAR'}, {'header': 'VEHICLE_PURCHASE_DATE'}, {'header': 'VEHICLE_PURCHASE_PRICE'}, {'header': 'VEHICLE_DISPOSITION_YEAR'}, {'header': 'VEHICLE_VENDOR'}, {'header': 'VEHICLE_DUTY'}, {'header': 'VEHICLE_COST_KM'},], int(len(databank_vehicles) + 1), databank_vehicles_excel)
  
  
  ## Show `Vehicles` statistics in an expander
  with st.expander('Vehicles statistics', expanded = False):
    ## Columns for showing Vehicle profile
    col1, col2, col3 = st.columns(3)
    cars = lastID(url = "carfleet.VEHICLES")  
    
    # Column 1
    with col1:
      for i in range(1, cars, 3):
        st.image(databank_vehicles._get_value(i, 'VEHICLE_IMAGE'))
        st.subheader(databank_vehicles._get_value(i, 'VEHICLE_BRAND'))
        st.write(databank_vehicles._get_value(i, 'VEHICLE_MODEL'))
        st.subheader("Vehicle ID")
        st.write(databank_vehicles._get_value(i, 'VEHICLE_ID'))

    # Coloumn 2
    with col2:
      for i in range(2, cars, 3):
        st.image(databank_vehicles._get_value(i, 'VEHICLE_IMAGE'))
        st.subheader(databank_vehicles._get_value(i, 'VEHICLE_BRAND'))
        st.write(databank_vehicles._get_value(i, 'VEHICLE_MODEL'))
        st.subheader("Vehicle ID")
        st.write(databank_vehicles._get_value(i, 'VEHICLE_ID'))

    # Column 3
    with col3:
      for i in range(3, cars, 3):
        st.image(databank_vehicles._get_value(i, 'VEHICLE_IMAGE'))
        st.subheader(databank_vehicles._get_value(i, 'VEHICLE_BRAND'))
        st.write(databank_vehicles._get_value(i, 'VEHICLE_MODEL'))
        st.subheader("Vehicle ID")
        st.write(databank_vehicles._get_value(i, 'VEHICLE_ID'))
  
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
    
    # Plotting
    st.bar_chart(data_cars)



### Database Excel Export Expander
with st.expander('Database Excel Export', expanded = False):
  ## Show `DRIVERS` table dataframe
  st.subheader('Drivers data')
  st.dataframe(databank_drivers_excel, use_container_width = True)
  
  
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
  st.dataframe(databank_vehicles_excel, use_container_width = True)
  
  
  ## Export tables to Excel workbook
  if st.button('Database Exel Export'):
    # Do the exporting
    export_excel('Drivers', 'I', [{'header': 'DRIVER_ID'}, {'header': 'DRIVER_FORENAME'}, {'header': 'DRIVER_SURNAME'}, {'header': 'DRIVER_NATIONAL_ID'}, {'header': 'DRIVER_MOBILE_NO'}, {'header': 'DRIVER_LICENSE_NO'}, {'header': 'DRIVER_LICENSE_CLASS'}, {'header': 'DRIVER_PSV_BADGE'}, {'header': 'DRIVER_NOTES'},], int(len(databank_drivers_excel) + 1), databank_drivers_excel,
                'Fuel', 'I', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'FUEL_AMOUNT'}, {'header': 'FUEL_COST'}, {'header': 'FUEL_TYPE'}, {'header': 'FUEL_DATE'}, {'header': 'FUEL_DISTANCE'}, {'header': 'FUEL_SHORTAGE'}, {'header': 'COST_CENTRE'},], int(len(databank_fuel) + 1), databank_fuel,
                'Insurances', 'E', [{'header': 'VEHICLE_ID'}, {'header': 'INSURANCE_DETAILS'}, {'header': 'INSURANCES_TYPE'}, {'header': 'INSURANCE_START_DATE'}, {'header': 'INSURANCE_EXPIRY_DATE'},], int(len(databank_insurances) + 1), databank_insurances,
                'Repairs', 'H', [{'header': 'VEHICLE_ID'}, {'header': 'REPAIR_DETAILS'}, {'header': 'REPAIR_DATE'}, {'header': 'REPAIR_COSTS'}, {'header': 'REPAIR_SPARE_PARTS'}, {'header': 'REPAIR_DOWN_TIME'}, {'header': 'REPAIR_CENTRE_PERSON'}, {'header': 'COST_CENTRE'},], int(len(databank_repairs) + 1), databank_repairs,
                'Services', 'H', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'SERVICE_DATE'}, {'header': 'SERVICE_DETAILS'}, {'header': 'SERVICE_COSTS'}, {'header': 'SERVICE_MILEAGE_ON_SERVICE'}, {'header': 'SERVICE_MILEAGE_NEXTSERVICE'}, {'header': 'SERVICE_MILEAGE_NEXTSERVICE_MAX'},], int(len(databank_services) + 1), databank_services,
                'Trips', 'J', [{'header': 'VEHICLE_ID'}, {'header': 'DRIVER_ID'}, {'header': 'TRIP_DATE'}, {'header': 'TRIP_DESCRIPTION'}, {'header': 'TRIP_COMMENTS'},{'header': 'TRIP_TIME_OUT'}, {'header': 'TRIP_TIME_IN'}, {'header': 'TRIP_OPEN_MILEAGE'}, {'header': 'TRIP_CLOSE_MILEAGE'}, {'header': '`TRIP_DISTANCE'},], int(len(databank_trips) + 1), databank_trips,
                'Vehicles', 'P', [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_PLATE_NUMBER'}, {'header': 'VEHICLE_TYPE'}, {'header': 'VEHICLE_BRAND'}, {'header': 'VEHICLE_MODEL'}, {'header': 'VEHICLE_SEATS'}, {'header': 'VEHICLE_FUEL_TYPE'}, {'header': 'VEHICLE_COLOUR'}, {'header': 'VEHICLE_CHASIS_NUMBER'}, {'header': 'VEHICLE_MANUFACTURE_YEAR'}, {'header': 'VEHICLE_PURCHASE_DATE'}, {'header': 'VEHICLE_PURCHASE_PRICE'}, {'header': 'VEHICLE_DISPOSITION_YEAR'}, {'header': 'VEHICLE_VENDOR'}, {'header': 'VEHICLE_DUTY'}, {'header': 'VEHICLE_COST_KM'},], int(len(databank_vehicles) + 1), databank_vehicles_excel)
