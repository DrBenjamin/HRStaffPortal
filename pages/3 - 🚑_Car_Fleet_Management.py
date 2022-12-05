##### `3 - 🚑_Car_Fleet_Management.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions



#### Loading neded Python libraries
import streamlit as st
import extra_streamlit_components as stx
import pandas as pd
import mysql.connector
import subprocess
import io
import sys
import os



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
      st.header("Audie")
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
    
  ## Submit Button `Test`
  submitted = st.form_submit_button("Test")

  if submitted:
    ## Printing
    #toprint = bytes("databank_fuel", 'utf-8')
    #lpr =  subprocess.Popen("/usr/bin/lpr", stdin = subprocess.PIPE)
    #lpr.stdin.write(toprint)
    os.startfile("files/TestFile.txt", "print")

    #st.write("Printed.")
    
    towrite = io.BytesIO()
    databank_fuel.to_excel(towrite)  # write to BytesIO buffer
    towrite.seek(0)
    #_io.BytesIO
    
    # make an fd to pass to write() method as a parameter
    file_descriptor = os.open("./TestFile.txt", os.O_CREAT|os.O_RDWR)
    # writing the byte code into the file
    os.write(file_descriptor, towrite.getvalue())
    # closing the file
    os.close(file_descriptor)
    print ("The file is closed successfully!!")


    
#### Out side of the form
### Data Analysis
## Data analysis for `Vehicles`
if (f"{chosen_id}" == '1'):
  st.write('Data analysis for vehicles')
  
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
  
  # Show repair costs per incident
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

  # Calculate average fuel consumption per Vehicle
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
  
  # Show fuel consumption of one vehicle
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

  
