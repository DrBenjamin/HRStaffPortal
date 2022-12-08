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
def export_excel(sheet, column, columns, length, data):
  ## Create a Pandas Excel writer using XlsxWriter as the engine
  buffer = io.BytesIO()
  with pd.ExcelWriter(buffer, engine = 'xlsxwriter') as writer:
    # Add dataframe data
    data.to_excel(writer, sheet_name = sheet, index = False)

    # Add a table to the worksheet
    worksheet = writer.sheets[sheet]
    span = "A1:%s%s" %(column, length)
    worksheet.add_table(span, {'columns': columns})
    range_table = "A:" + column
    worksheet.set_column(range_table, 30)
      
    # Add Excel VBA code
    workbook = writer.book
    workbook.add_vba_project('vbaProject.bin')
    # Add a button tied to a macro in the VBA project
    #worksheet.insert_button('G3', {'macro': 'Button', 'caption': 'Press Me', 'width': 80, 'height': 30})

    # Saving changes
    workbook.close()
    writer.save()
    
    # Download Button
    st.download_button(label = 'Download Excel document', data = buffer, file_name = 'Export.xlsm', mime = "application/vnd.ms-excel.sheet.macroEnabled.12")
    
    

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
  export = False
  if (f"{chosen_id}" == '1'):
    st.title('Vehicles')
  
    
    ## Get vehicle data and print out as a dataframe
    query = "SELECT ID, VEHICLE_ID, VEHICLE_TYPE, VEHICLE_BRAND, VEHICLE_MODEL, VEHICLE_SEATS, VEHICLE_FUEL_TYPE, VEHICLE_COLOUR, VEHICLE_CHASIS_NUMBER, VEHICLE_MANUFACTURE_YEAR, VEHICLE_PURCHASE_DATE, VEHICLE_PURCHASE_PRICE, VEHICLE_DISPOSITION_YEAR, VEHICLE_VENDOR, VEHICLE_DUTY, VEHICLE_IMAGE FROM `carfleet`.`VEHICLES`;"
    rows = run_query(query)
    
    databank_vehicles = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_TYPE', 'VEHICLE_BRAND', 'VEHICLE_MODEL', 'VEHICLE_SEATS', 'VEHICLE_FUEL_TYPE', 'VEHICLE_COLOUR', 'VEHICLE_CHASIS_NUMBER', 'VEHICLE_MANUFACTURE_YEAR', 'VEHICLE_PURCHASE_DATE', 'VEHICLE_PURCHASE_PRICE', 'VEHICLE_DISPOSITION_YEAR', 'VEHICLE_VENDOR', 'VEHICLE_DUTY', 'VEHICLE_IMAGE'])
    data_cars = pd.DataFrame(columns = ['VEHICLE_ID', 'VEHICLE_TYPE'])
    
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_TYPE', 'VEHICLE_BRAND', 'VEHICLE_MODEL', 'VEHICLE_SEATS', 'VEHICLE_FUEL_TYPE', 'VEHICLE_COLOUR', 'VEHICLE_CHASIS_NUMBER', 'VEHICLE_MANUFACTURE_YEAR', 'VEHICLE_PURCHASE_DATE', 'VEHICLE_PURCHASE_PRICE', 'VEHICLE_DISPOSITION_YEAR', 'VEHICLE_VENDOR', 'VEHICLE_DUTY', 'VEHICLE_IMAGE'])
      databank_vehicles = pd.concat([databank_vehicles, df])
    databank_vehicles = databank_vehicles.set_index('ID')
    
    
    ## Columns
    col1, col2, col3 = st.columns(3)
    with col1:
      st.header("Vehicle ID")
      st.write(rows[0][1])
      st.subheader(rows[0][3])
      st.write(rows[0][4])
      st.image(rows[0][15])


    with col2:
      st.header("Vehicle ID")
      st.write(rows[1][1])
      st.subheader(rows[1][3])
      st.write(rows[1][4])
      st.image(rows[1][15])


    with col3:
      st.header("Vehicle ID")
      st.write(rows[2][1])
      st.subheader(rows[0][3])
      st.write(rows[2][4])
      st.image(rows[2][15])
      
    ## Show dataframe 
    st.dataframe(databank_vehicles, use_container_width = True)

    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export `Vehicles` dataframe to Excel Makro file
      export = True
  
  
  ## tab `Repairs` 
  elif (f"{chosen_id}" == '2'):
    st.title('Repairs')
    
      
    ## Get repair data and print out as a dataframe
    query = "SELECT ID, VEHICLE_ID, VEHICLE_REPAIR_DETAILS, VEHICLE_REPAIR_DATE, VEHICLE_REPAIR_COSTS, VEHICLE_SPARE_PARTS, VEHICLE_DOWN_TIME, SERVICE_CENTRE_PERSON, COST_CENTRE FROM `carfleet`.`REPAIRS`;"
    rows = run_query(query)
    
    databank_repairs = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_REPAIR_DETAILS', 'VEHICLE_REPAIR_DATE', 'VEHICLE_REPAIR_COSTS', 'VEHICLE_SPARE_PARTS', 'VEHICLE_DOWN_TIME', 'SERVICE_CENTRE_PERSON', 'COST_CENTRE'])
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_REPAIR_DETAILS', 'VEHICLE_REPAIR_DATE', 'VEHICLE_REPAIR_COSTS', 'VEHICLE_SPARE_PARTS', 'VEHICLE_DOWN_TIME', 'SERVICE_CENTRE_PERSON', 'COST_CENTRE'])
      databank_repairs = pd.concat([databank_repairs, df])
    databank_repairs = databank_repairs.set_index('ID')
    st.dataframe(databank_repairs, use_container_width = True)


    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      export = True

  
  
  ## tab `Fuel Consumption`   
  elif (f"{chosen_id}" == '3'):
    st.title('Fuel Consumption')
    
    
    ## Get fuel consumption data and print out as a dataframe
    query = "SELECT ID, VEHICLE_ID, VEHICLE_FUEL_AMOUNT, VEHICLE_FUEL_COST, VEHICLE_FUEL_TYPE, VEHICLE_FUEL_DATE, VEHICLE_DISTANCE, FUEL_SHORTAGE, COST_CENTRE FROM `carfleet`.`FUEL`;"
    rows = run_query(query)
    
    databank_fuel = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_FUEL_AMOUNT', 'VEHICLE_FUEL_COST', 'VEHICLE_FUEL_TYPE', 'VEHICLE_FUEL_DATE', 'VEHICLE_DISTANCE', 'FUEL_SHORTAGE', 'COST_CENTRE'])
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_FUEL_AMOUNT', 'VEHICLE_FUEL_COST', 'VEHICLE_FUEL_TYPE', 'VEHICLE_FUEL_DATE', 'VEHICLE_DISTANCE', 'FUEL_SHORTAGE', 'COST_CENTRE'])
      databank_fuel = pd.concat([databank_fuel, df])
    databank_fuel = databank_fuel.set_index('ID')
    st.dataframe(databank_fuel, use_container_width = True)

    
    ## Submit Button `Export to Excel`
    submitted = st.form_submit_button("Export to Excel")

    if submitted:
      ## Export `Fuel` dataframe to Excel Makro file
      export = True

    
#### Outside the form
### Data analysis
## Data analysis for `Vehicles`
if (f"{chosen_id}" == '1'):
  ## Export `Vehicles` dataframe to Excel Makro file
  if export == True:
    # Drop last column (`VEHICLE_IMAGE`)
    databank_vehicles_excel = databank_vehicles.iloc[: , :-1]
    export_excel(sheet = 'Vehicles', column = 'N', columns = [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_TYPE'}, {'header': 'VEHICLE_BRAND'}, {'header': 'VEHICLE_MODEL'}, {'header': 'VEHICLE_SEATS'}, {'header': 'VEHICLE_FUEL_TYPE'}, {'header': 'VEHICLE_COLOUR'}, {'header': 'VEHICLE_CHASIS_NUMBER'}, {'header': 'VEHICLE_MANUFACTURE_YEAR'}, {'header': 'VEHICLE_PURCHASE_DATE'}, {'header': 'VEHICLE_PURCHASE_PRICE'}, {'header': 'VEHICLE_DISPOSITION_YEAR'}, {'header': 'VEHICLE_VENDOR'}, {'header': 'VEHICLE_DUTY'},], length = int(len(databank_vehicles) + 1), data = databank_vehicles_excel)
  
  
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
  
  
  ## Create Report
  #if st.button('Create Report'):
    #print('Report')


## Data analysis for `Repairs`
elif (f"{chosen_id}" == '2'):
  ## Export `Repairs` dataframe to Excel Makro file
  if export == True:
    export_excel(sheet = 'Repairs', column = 'H', columns = [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_REPAIR_DETAILS'}, {'header': 'VEHICLE_REPAIR_DATE'}, {'header': 'VEHICLE_REPAIR_COSTS'}, {'header': 'VEHICLE_SPARE_PARTS'}, {'header': 'VEHICLE_DOWN_TIME'}, {'header': 'SERVICE_CENTRE_PERSON'}, {'header': 'COST_CENTRE'},], length = int(len(databank_repairs) + 1), data = databank_repairs)
    
    
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

  
## Data analysis for `Fuel`
elif (f"{chosen_id}" == '3'):
  ## Export `Fuel` dataframe to Excel Makro file
  if export == True:
    export_excel(sheet = 'Fuel', column = 'H', columns = [{'header': 'VEHICLE_ID'}, {'header': 'VEHICLE_FUEL_AMOUNT'}, {'header': 'VEHICLE_FUEL_COST'}, {'header': 'VEHICLE_FUEL_TYPE'}, {'header': 'VEHICLE_FUEL_DATE'}, {'header': 'VEHICLE_DISTANCE'}, {'header': 'FUEL_SHORTAGE'}, {'header': 'COST_CENTRE'},], length = int(len(databank_fuel) + 1), data = databank_fuel)

  
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

  
