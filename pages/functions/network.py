##### `/pages/functions/network.py`
##### HR Staff Portal
##### Open-Source, hostet on https://github.com/DrBenjamin/HRStaffPortal
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
def downzip(url, zip_files, path):
    progress_text = "Downloading Files. Please wait."
    my_bar = st.progress(0, text = progress_text)
    my_bar.progress(0, text = progress_text)
    for i in range(len(zip_files)):
        zip_file = requests.get(url + zip_files[i]).content
        my_bar.progress(int(100 / len(zip_files) * (i + 0.5)), text = progress_text)
        success = True
        zip_file_path = path + zip_files[i]
        while success == False:
            try:
                with open(zip_file_path, 'wb') as handler:
                    handler.write(zip_file)
                with zipfile.ZipFile(zip_file_path) as z:
                    z.extractall(path)
                if os.path.exists(zip_file_path):
                    os.remove(zip_file_path)
                my_bar.progress(int(100 / len(zip_files) * (i + 1)), text = progress_text)
            except:
                success = False



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
    st.write(hostname)
    ip_address = socket.gethostbyname(hostname)

    return ip_address



### Function: google_sheet_credentials = Getting Google Sheet API credentials
@st.cache_resource
def google_sheet_credentials():
    ## Google Sheet API authorization
    output = st.secrets['google']['credentials_file']
    GoogleDriveDownloader.download_file_from_google_drive(file_id = st.secrets['google']['credentials_file_id'],
                                                          dest_path = './credentials.zip', unzip = True)
    client = pygsheets.authorize(service_file = st.secrets['google']['credentials_file'])
    if os.path.exists("credentials.zip"):
        os.remove("credentials.zip")
    if os.path.exists("google_credentials.json"):
        os.remove("google_credentials.json")
    if os.path.exists("__MACOSX"):
        shutil.rmtree("__MACOSX")

    # Return client
    return client
