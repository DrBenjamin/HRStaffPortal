##### Workshops.py
##### Kamazu Central Hospital (KCH) HR Staff Portal Prototype
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions


#### Loading neded Python libraries
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import math
from datetime import datetime
import mysql.connector
import sys

## Header
st.title('Workshop Page')

## Sidebar
# Sidebar Header Image
st.sidebar.image('images/MoH.png')
