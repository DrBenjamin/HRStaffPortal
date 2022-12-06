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
import tempfile
plt = platform.system()
if plt == "Windows":
  print("Your system is Windows")
  import win32api
  import win32print
elif plt == "Darwin":
  print("Your system is MacOS")
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
def check_vehicles(databank):
  vehicle = []
  i = 0
  while i < len(databank):
    if i > 0:
      x = 0
      double = False
      for x in range(len(vehicle)):
        if (vehicle[x] == databank['VEHICLE_ID'][i + 1]):
          double = True
      if (double != True):    
        vehicle.append(databank['VEHICLE_ID'][i + 1])
    else:
      vehicle.append(databank['VEHICLE_ID'][i + 1])
    i += 1
  return vehicle


### Function: printing = send text data to standard printer
def printing(print_data):
    filename = tempfile.mktemp(".txt")
    for i in range(len(print_data)):
      line = print_data.loc[i + 1].to_string()
      line = line + "\n" + "\n"
      open(filename, 'a+').write(line)
    if plt == "Windows":
      win32api.ShellExecute (0, "print", filename, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)
    elif plt == "Darwin":
      st.write("Open ", filename)
      
      
### Function: export_excel = Pandas Dataframe to Excel Makro File (xlsm)
def export_excel(sheet, column, columns, length, data):
  ## Create a Pandas Excel writer using XlsxWriter as the engine
  writer = pd.ExcelWriter('Export.xlsx', engine = 'xlsxwriter')
  workbook = writer.book

  # Add dataframe data
  data.to_excel(writer, sheet_name = sheet, index = False)
      
  # Add a table to the worksheet
  worksheet = writer.sheets[sheet]
  
  span = "A1:%s%s" %(column, length)
  worksheet.add_table(span, {'columns': columns})
  range_table = "A:" + column
  worksheet.set_column(range_table, 23)
      
  # Add Excel VBA code
  workbook.add_vba_project('vbaProject.bin')
  # Add a button tied to a macro in the VBA project
  worksheet.insert_button('G3', {'macro': 'Button', 'caption': 'Press Me', 'width': 80, 'height': 30})
  workbook.filename = 'Export.xlsm'
  writer.save()
      
  # Open Excel Workbook if OS is Windows
  if plt == "Windows":
    os.remove('Export.xlsx')
    os.startfile('Export.xlsm')
  elif plt == "Darwin":
    os.unlink('Export.xlsx')
    st.write("Open Export.xlsm")
    
    

#### Main Program
### Title
st.title("KCH Car Fleet")


## Open databank connection
conn = init_connection()


### Custom Tab with IDs
chosen_id = stx.tab_bar(data = [
  stx.TabBarItemData(id = 1, title = "Vehicles", description = "Vehicles at KCH"),
  stx.TabBarItemData(id = 2, title = "Repairs", description = "Repairs at KCH"),
  stx.TabBarItemData(id = 3, title = "Fuel", description = "Fuel consumption at KCH"),], default = 1)


with st.form("Car Fleet Management", clear_on_submit = True):
  ## tab `Vehicles`
  if (f"{chosen_id}" == '1'):
    st.title('Vehicles')
    
    ## Columns
    col1, col2, col3 = st.columns(3)
    with col1:
      st.header("Audi")
      st.image("./pages/images/audi-a4.jpg", caption = "Audi A4")
      st.write("Vehicle ID: 00001")

    with col2:
      st.header("BMW")
      st.image("./pages/images/bmw6.jpg", caption = "BMW 6")
      st.write("Vehicle ID: 00002")

    with col3:
      st.header("Hyundai")
      st.image("./pages/images/creta.jpg", caption = "Hyundai Creta")
      st.write("Vehicle ID: 00003")
    
    ## Get vehicle data and print out as a dataframe
    query = "SELECT ID, VEHICLE_ID, VEHICLE_TYPE, VEHICLE_BRAND, VEHICLE_MODEL, VEHICLE_SEATS, VEHICLE_FUEL_TYPE FROM `carfleet`.`VEHICLES`;"
    rows = run_query(query)
    
    databank_vehicles = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_TYPE', 'VEHICLE_BRAND', 'VEHICLE_MODEL', 'VEHICLE_SEATS', 'VEHICLE_FUEL_TYPE'])
    data_cars = pd.DataFrame(columns = ['VEHICLE_ID', 'VEHICLE_TYPE'])
    
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_TYPE', 'VEHICLE_BRAND', 'VEHICLE_MODEL', 'VEHICLE_SEATS', 'VEHICLE_FUEL_TYPE'])
      databank_vehicles = pd.concat([databank_vehicles, df])
      df = pd.DataFrame([[row[1], row[2]]], columns = ['VEHICLE_ID', 'VEHICLE_TYPE'])
      data_cars = pd.concat([data_cars, df])
    databank_vehicles = databank_vehicles.set_index('ID')
    st.dataframe(databank_vehicles, use_container_width = True)
    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export dataframe to Excel Makro file
      export_excel(sheet = 'Fuel', column = 'F', columns = [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_TYPE'}, {'header': 'VEHICLE_BRAND'}, {'header': 'VEHICLE_MODEL'}, {'header': 'VEHICLE_SEATS'}, {'header': 'VEHICLE_FUEL_TYPE'},], length = int(len(databank_vehicles) + 1), data = databank_vehicles)

  
  
  ## tab `Repairs` 
  elif (f"{chosen_id}" == '2'):
    st.title('Repairs')
    
      
    ## Get repair data and print out as a dataframe
    query = "SELECT ID, VEHICLE_ID, VEHICLE_REPAIR, VEHICLE_SPARE_PARTS, VEHICLE_SPARE_PART_COSTS, VEHICLE_DOWN_TIME FROM `carfleet`.`REPAIRS`;"
    rows = run_query(query)
    
    databank_repairs = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_REPAIR', 'VEHICLE_SPARE_PARTS', 'VEHICLE_SPARE_PART_COSTS', 'VEHICLE_DOWN_TIME'])
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_REPAIR', 'VEHICLE_SPARE_PARTS', 'VEHICLE_SPARE_PART_COSTS', 'VEHICLE_DOWN_TIME'])
      databank_repairs = pd.concat([databank_repairs, df])
    databank_repairs = databank_repairs.set_index('ID')
    st.dataframe(databank_repairs, use_container_width = True)
    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export dataframe to Excel Makro file
      export_excel(sheet = 'Fuel', column = 'E', columns = [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_REPAIR'}, {'header': 'VEHICLE_SPARE_PARTS'}, {'header': 'VEHICLE_SPARE_PART_COSTS'}, {'header': 'VEHICLE_DOWN_TIME'},], length = int(len(databank_repairs) + 1), data = databank_repairs)

  
  
  ## tab `Fuel Consumption`   
  elif (f"{chosen_id}" == '3'):
    st.title('Fuel Consumption')
    
    ## Get fuel consumption data and print out as a dataframe
    query = "SELECT ID, VEHICLE_ID, VEHICLE_FUEL, VEHICLE_DISTANCE, VEHICLE_FUEL_DATE, VEHICLE_FUEL_SHORTAGE FROM `carfleet`.`FUEL`;"
    rows = run_query(query)
    
    databank_fuel = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_FUEL', 'VEHICLE_DISTANCE', 'VEHICLE_FUEL_DATE', 'VEHICLE_FUEL_SHORTAGE'])
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_FUEL', 'VEHICLE_DISTANCE', 'VEHICLE_FUEL_DATE', 'VEHICLE_FUEL_SHORTAGE'])
      databank_fuel = pd.concat([databank_fuel, df])
    databank_fuel = databank_fuel.set_index('ID')
    st.dataframe(databank_fuel, use_container_width = True)
    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export dataframe to Excel Makro file
      export_excel(sheet = 'Fuel', column = 'E', columns = [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_FUEL'}, {'header': 'VEHICLE_DISTANCE'}, {'header': 'VEHICLE_FUEL_DATE'}, {'header': 'VEHICLE_FUEL_SHORTAGE'},], length = int(len(databank_fuel) + 1), data = databank_fuel)


    
#### Outside the form
### Data analysis
## Data analysis for `Vehicles`
if (f"{chosen_id}" == '1'):
  if st.button('Print vehicle data'):
      ## Print text data
      printing(databank_vehicles)

  # Plotting
  data_cars = data_cars.set_index('VEHICLE_TYPE')
  st.bar_chart(data_cars)


## Data analysis for `Repairs`
elif (f"{chosen_id}" == '2'):
  ## Repair cost chart
  # Checking for unique vehicles IDs
  vehicles = check_vehicles(databank_repairs)
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
      query = "SELECT ID, VEHICLE_ID, VEHICLE_SPARE_PART_COSTS FROM `carfleet`.`REPAIRS` WHERE VEHICLE_ID = %s;" %(vehicles[i])
      rows = run_query(query)
      i = 0
      costs = 0.0
      for row in rows:
        i += 1
        costs += round(float(row[2][:-1]), 2)
      df = pd.DataFrame([[row[1], costs]], columns = ['Vehicle ID', 'Repair costs'])
      data_repair_costs = pd.concat([data_repair_costs, df])
    data_repair_costs = data_repair_costs.set_index('Vehicle ID')
    
    # Plotting
    st.bar_chart(data_repair_costs, x = vehicles)

  
  ## Show repair costs per incident
  else:
    data_repair_costs = pd.DataFrame(columns = ['Spare part', 'Repair cost'])
    query = "SELECT ID, VEHICLE_ID, VEHICLE_SPARE_PARTS, VEHICLE_SPARE_PART_COSTS FROM `carfleet`.`REPAIRS` WHERE VEHICLE_ID = %s;" %(vehicles)
    rows = run_query(query)
    for row in rows:
      df = pd.DataFrame([[row[2], round(float(row[3][:-1]), 1)]], columns = ['Spare part', 'Repair cost'])
      data_repair_costs = pd.concat([data_repair_costs, df])
    data_repair_costs = data_repair_costs.set_index('Spare part')
    
    # Plotting
    st.bar_chart(data_repair_costs)

  
## Data analysis for `Fuel`
elif (f"{chosen_id}" == '3'):
  ## Average Fuel Consumption Chart
  # Checking for unique Vehicles IDs
  vehicles = check_vehicles(databank_fuel)
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
      query = "SELECT ID, VEHICLE_ID, VEHICLE_FUEL, VEHICLE_DISTANCE FROM `carfleet`.`FUEL` WHERE VEHICLE_ID = %s;" %(vehicles[i])
      rows = run_query(query)
      i = 0
      fuel = 0.0
      for row in rows:
        i += 1
        fuel += round(float(row[3][:-2]) / float(row[2][:-1]), 2)
      df = pd.DataFrame([[row[1], round((fuel / i), 2)]], columns = ['Vehicle ID', 'Average Fuel Consumption'])
      data_fuel_rate_average = pd.concat([data_fuel_rate_average, df])
    data_fuel_rate_average = data_fuel_rate_average.set_index('Vehicle ID')
    
    # Plotting
    st.bar_chart(data_fuel_rate_average, x = vehicles)
  
  
  ## Show fuel consumption of one vehicle
  else:
    data_fuel_rate = pd.DataFrame(columns = ['Date', 'Fuel Consumption Rate'])
    query = "SELECT ID, VEHICLE_ID, VEHICLE_FUEL, VEHICLE_DISTANCE, VEHICLE_FUEL_DATE FROM `carfleet`.`FUEL` WHERE VEHICLE_ID = %s;" %(vehicles)
    rows = run_query(query)
    fuel = 0.0
    for row in rows:
      distance = round(float(row[3][:-2]), 2)
      fuel = round(float(row[2][:-1]), 2)
      df = pd.DataFrame([[row[4], distance / fuel]], columns = ['Date', 'Fuel Consumption Rate'])
      data_fuel_rate = pd.concat([data_fuel_rate, df])
    data_fuel_rate = data_fuel_rate.set_index('Date')
    
    # Plotting
    st.bar_chart(data_fuel_rate)

  
