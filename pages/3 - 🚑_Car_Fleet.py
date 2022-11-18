##### `3 - 🚑_Car_Fleet.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions



import streamlit as st


st.title("KCH Car Fleet")

## Form for showing Employee input fields 
    with st.form("Car Fleet Management", clear_on_submit = True):
      ## Create tabs
      tab1, tab2, tab3 = st.tabs(["Vehicles", "Repairs", "Fuel Consumption"])
      
      ## tab `Master data`
      with tab1:
        st.title('Vehicles')
        
      ## tab `Master data`
      with tab1:
        st.title('Repairs')
        
      ## tab `Master data`
      with tab1:
        st.title('Fuel Consumption')
