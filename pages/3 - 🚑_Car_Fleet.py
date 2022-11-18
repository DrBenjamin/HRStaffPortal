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
      databank_repairs = databank_repairs.append(df)
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
      databank_fuel = databank_fuel.append(df)
    databank_fuel = databank_fuel.set_index('ID')
    st.dataframe(databank_fuel, use_container_width = True)
    

  ## Submit Button `Edit Vehicles`
  submitted = st.form_submit_button("Edit")
  if submitted:
    st.write("Edited.")
