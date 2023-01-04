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
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders




#### All shared network functions
### Function: trans = DeepL translation
def trans(input, target_lang):
	translator = deepl.Translator(st.secrets["deepl"]["key"])
	result = translator.translate_text(input, target_lang = target_lang) 
	return result



### Function: send_mail = Email sending
def send_mail(subject, body, receiver, attachment):
  ## Creating the SMTP server object by giving SMPT server address and port number
  smtp_server = smtplib.SMTP(st.secrets['mail']['smtp_server'], st.secrets['mail']['smtp_server_port'])
  
  #setting the ESMTP protocol
  smtp_server.ehlo() 
  
  # Setting up to TLS connection
  smtp_server.starttls() 
  
  # Calling the ehlo() again as encryption happens on calling startttls()
  smtp_server.ehlo() 
  
  # Logging into out email id
  smtp_server.login(st.secrets['mail']['user'], st.secrets['mail']['password'])
  
  
  ## Message to be send
  msg = MIMEMultipart()  # create a message
  
  # Setup the parameters of the message
  msg['From'] = sender
  msg['To'] = receiver
  msg['Cc'] = ''
  msg['Subject'] = subject
  
  # Setup text
  msg.attach(MIMEText(body))
  
  # Setup attachment 
  record = MIMEBase('application', 'octet-stream')
  record.set_payload(attachment)
  encoders.encode_base64(record)
  record.add_header('Content-Disposition', 'attachment', filename = 'QRCode.png')
  msg.attach(record)
  
  
  ## Sending the mail by specifying the from and to address and the message 
  smtp_server.sendmail(st.secrets['mail']['user'], receiver, msg.as_string())
  
  # Priting a message on sending the mail
  print('Successfully the mail is sent')
  
  # Terminating the server
  smtp_server.quit()
