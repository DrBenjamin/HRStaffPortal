##### `/pages/functions/network.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import pandas as pd
import io
import os
import deepl
import smtplib




#### All shared network functions
### Function: trans = DeepL translation
def trans(input, target_lang):
	translator = deepl.Translator(st.secrets["deepl"]["key"])
	result = translator.translate_text(input, target_lang = target_lang) 
	return result



