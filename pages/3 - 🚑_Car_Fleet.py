##### `3 - 🚑_Car_Fleet.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions



#### Loading neded Python libraries
import streamlit as st
import pandas as pd
import mysql.connector



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
### Function: run_query = SQL Connection
## Initialize connection
def init_connection():
  return mysql.connector.connect(**st.secrets["mysql"])
## Perform query
def run_query(query):
  with conn.cursor() as cur:  
    cur.execute(query)
    return cur.fetchall()
## Use local databank carfleet with Table REPAIRS
# Open databank connection
conn = init_connection()



#### Main Program
### Title
st.title("KCH Car Fleet")


### Form for showing Car Fleet Data
with st.form("Car Fleet Management", clear_on_submit = True):
  ## Create tabs
  tab1, tab2, tab3 = st.tabs(["Vehicles", "Repairs", "Fuel Consumption"])
      
  ## tab `Vehicles data`
  with tab1:
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
    
        
  ## tab `Repair data`
  with tab2:
    st.title('Repairs')
    
    ## Get repair data
    query = "SELECT ID, VEHICLE_ID, VEHICLE_REPAIR, VEHICLE_SPARE_PARTS, VEHICLE_DOWN_TIME FROM `carfleet`.`REPAIRS`;"
    rows = run_query(query)
    
    databank_repairs = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_REPAIR', 'VEHICLE_SPARE_PARTS', 'VEHICLE_DOWN_TIME'])
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_REPAIR', 'VEHICLE_SPARE_PARTS', 'VEHICLE_DOWN_TIME'])
      databank_repairs = pd.concat([databank_repairs, df])
    databank_repairs = databank_repairs.set_index('ID')
    st.dataframe(databank_repairs, use_container_width = True)
    
        
  ## tab `Fuel Consumption data`
  with tab3:
    st.title('Fuel Consumption')
    
    ## Get fuel consumption data
    query = "SELECT ID, VEHICLE_ID, VEHICLE_FUEL, VEHICLE_DISTANCE, VEHICLE_FUEL_SHORTAGE FROM `carfleet`.`FUEL`;"
    rows = run_query(query)
    
    databank_fuel = pd.DataFrame(columns = ['ID', 'VEHICLE_ID', 'VEHICLE_FUEL', 'VEHICLE_DISTANCE', 'VEHICLE_FUEL_SHORTAGE'])
    for row in rows:
      df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4]]], columns = ['ID', 'VEHICLE_ID', 'VEHICLE_FUEL', 'VEHICLE_DISTANCE', 'VEHICLE_FUEL_SHORTAGE'])
      databank_fuel = pd.concat([databank_fuel, df])
    databank_fuel = databank_fuel.set_index('ID')
    st.dataframe(databank_fuel, use_container_width = True)
    
    ## Average Fuel Consumption Chart
    # Checking for unique Vehicles IDs
    vehicle = []
    i = 0
    while i < len(databank_fuel):
      if i > 0:
        x = 0
        double = False
        for x in range(len(vehicle)):
          if (vehicle[x] == databank_fuel['VEHICLE_ID'][i + 1]):
            double = True
        if (double != True):    
          vehicle.append(databank_fuel['VEHICLE_ID'][i + 1])
      else:
        vehicle.append(databank_fuel['VEHICLE_ID'][i + 1])
      i += 1

    # Calculate average fuel consumption per Vehicle
    data_fuel_rate_average = pd.DataFrame(columns = ['Vehicle ID', 'Average Fuel Consumption'])
    for i in range(len(vehicle)):
      query = "SELECT ID, VEHICLE_ID, VEHICLE_FUEL, VEHICLE_DISTANCE FROM `carfleet`.`FUEL` WHERE VEHICLE_ID = %s;" %(vehicle[i])
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
    st.bar_chart(data_fuel_rate_average, x = vehicle)
    

  ## Submit Button `Edit Vehicles`
  submitted = st.form_submit_button("Edit")
  if submitted:
    st.write("Edited.")


    
### Out side of the form
