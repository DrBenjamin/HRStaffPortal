##### `/pages/functions/network.py`
##### HR Staff Portal
##### Open-Source, hosted on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to benjamin.gross@giz.de for any questions
#### Loading needed Python libraries
import streamlit as st
import pygsheets
import os
import shutil
import deepl
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from google_drive_downloader import GoogleDriveDownloader
import zipfile
import requests




#### All shared network functions
### Function downzip = Download and unzip zip files
def downzip(url, zip_files, path, secure = False):
    for i in range(len(zip_files)):
        if secure == True:
            zip_file = requests.get(url + zip_files[i], verify = st.secrets['custom']['certificate']).content
        else:
            zip_file = requests.get(url + zip_files[i]).content
        zip_file_path = path + zip_files[i]
        x_times = 0
        while x_times < 4:
            x_times += 1
            try:
                with open(zip_file_path, 'wb') as handler:
                    handler.write(zip_file)
                with zipfile.ZipFile(zip_file_path) as z:
                    z.extractall(path)
                if os.path.exists(zip_file_path):
                    os.remove(zip_file_path)
                x_times = 4
            except:
                print(x_times)



### Function: trans = DeepL translation
def trans(input, target_lang):
    translator = deepl.Translator(st.secrets["deepl"]["key"])
    result = translator.translate_text(input, target_lang = target_lang)
    return result



### Function: send_mail = Email sending
def send_mail(subject, body, receiver, attachment = None):
    ## Creating the SMTP server object by giving SMPT server address and port number
    smtp_server = smtplib.SMTP(st.secrets['mail']['smtp_server'], st.secrets['mail']['smtp_server_port'])

    # setting the ESMTP protocol
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
    msg['From'] = st.secrets['mail']['user']
    msg['To'] = receiver
    msg['Cc'] = ''
    msg['Subject'] = subject

    # Setup text
    msg.attach(MIMEText(body))

    # Setup attachment
    if attachment != None:
        record = MIMEBase('application', 'octet-stream')
        record.set_payload(attachment)
        encoders.encode_base64(record)
        record.add_header('Content-Disposition', 'attachment', filename = 'QRCode.png')
        msg.attach(record)


    ## Sending the mail by specifying the from and to address and the message
    try:
        smtp_server.sendmail(st.secrets['mail']['user'], receiver, msg.as_string())

        # Priting a message on sending the mail
        print('Mail successfully sent')

        # Terminating the server
        smtp_server.quit()
    except:
        print("An exception occurred in function `send_mail`")
        st.error(body = 'Mail connection timeout!', icon = "🚨")



### Function: get_ip() = Get own ip address
def get_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return ip_address
