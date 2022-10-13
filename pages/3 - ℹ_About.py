##### `3 - ℹ_About.py`
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions


#### Loading neded Python libraries
import streamlit as st
import streamlit.components.v1 as stc


## Header
st.title('About')
st.subtitle('Kamuzu Central Hospital')
st.write('Private Bag 149,')
st.write('Lilongwe, MALAWI')
st.write('tel: +265 1 753 400')
st.write('tel: +265 1 753 555')
st.write('tel: +265 1 753 744')


## Sidebar
# Sidebar Header Image
st.sidebar.image('images/MoH.png')
