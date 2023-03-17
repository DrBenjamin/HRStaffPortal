##### `pages/2 - 🛠_Workshops.py`
##### HR Staff Portal
##### Open-Source, hosted on https://github.com/DrBenjamin/HRStaffPortal
##### Please reach out to ben@benbox.org for any questions
#### Loading needed Python libraries
import streamlit as st
import mysql.connector
import os
import pandas as pd
import numpy as np
from datetime import datetime, date
import sys
sys.path.insert(1, "pages/functions/")
from functions import header
from functions import check_password
from functions import landing_page
from functions import generateID
from functions import generate_qrcode
from functions import save_img
from functions import load_file
from functions import build_employees
from functions import rebuild_confirmation
from functions import confirmed_query
from network import send_mail
from network import get_ip
from network import google_sheet_credentials
sys.path.insert(2, "pages/modules/")
from streamlit_image_select import image_select




#### Streamlit initial setup
desc_file = open('DESCRIPTION', 'r')
lines = desc_file.readlines()
print(lines[3])
try:
    st.set_page_config(
        page_title = "Workshops",
        page_icon = st.secrets['custom']['facility_image_thumbnail'],
        layout = "centered",
        initial_sidebar_state = "expanded",
        menu_items = {
            'Get Help': st.secrets['custom']['menu_items_help'],
            'Report a bug': st.secrets['custom']['menu_items_bug'],
            'About': '**HR Staff Portal** (' + lines[3] + ')\n\n' + st.secrets['custom']['facility'] + ' (' +
                     st.secrets['custom']['facility_abbreviation'] + ')' + ', ' + st.secrets['custom'][
                         'address_line1'] + '\n' + st.secrets['custom']['address_line2'] + '\n\n' + st.secrets['custom'][
                         'contact_tel1'] + '\n\n' + st.secrets['custom']['contact_tel2'] + '\n\n' + st.secrets['custom'][
                         'contact_tel3'] + '\n\n' + st.secrets['custom']['contact_mail1_desc'] + ': ' +
                     st.secrets['custom']['contact_mail1'] + '\n\n' + st.secrets['custom']['contact_mail2_desc'] + ': ' +
                     st.secrets['custom']['contact_mail2'] + '\n\nAdministrator: ' + st.secrets['custom'][
                         'contact_admin'] + '\n\n-----------'
        }
    )
except Exception as e:
    print(e)



#### Query parameters
## Get query params
# html_query = st.experimental_get_query_params()
# if len(html_query) > 1:
#  print(html_query['workshop'][0])
#  print(html_query['eno'][0])
# st.experimental_set_query_params(eno = "xxxxxx")




#### Initialization of session states
## Session states
if ('admin' not in st.session_state):
    st.session_state['admin'] = False
if ('header' not in st.session_state):
    st.session_state['header'] = True


## Created Workshop states
if ('workshop' not in st.session_state):
    st.session_state['workshop'] = '00000'




#### Functions
### Function: run_query = Initial SQL Connection
def init_connection():
    ## Initialize connection
    try:
        return mysql.connector.connect(**st.secrets["mysql_benbox"])
    except:
        print("An exception occurred in function `init_connection`")
        st.error(body = 'Databank connection timeout!', icon = "🚨")
        st.stop()



### Function: run_query = SQL query
def run_query(query):
    with conn.cursor() as cur:
        # Perform query
        try:
            cur.execute(query)
            return cur.fetchall()

        except:
            print('An exception occurred in function `run_query` with query \"' + query + '\"')



### Function: lastID = checks for last ID number in Table (to add data after)
def lastID(url):
    query = "SELECT MAX(ID) FROM %s;" % (url)
    rows = run_query(query)

    # Check for ID
    for row in rows:
        if (row[0] != None):
            id = int(row[0]) + 1
        else:
            id = 1
            break

    # Return ID
    return id




#### Main Program
### Logged in state (Workshops page)
if check_password():
    ### Header
    header(title = 'Workshops page', data_desc = 'workshops data', expanded = st.session_state['header'])


    ## Open databank connection
    conn = init_connection()

    # Get workshop data
    query = "SELECT WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_FACILITATOR_EMAIL, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES, WORKSHOP_ATTENDEES_CONFIRMED FROM idcard.WORKSHOP;"
    rows = run_query(query)

    # Creating pandas dataframe
    databank_workshop = pd.DataFrame(
        columns = ['WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_FACILITATOR',
                   'WORKSHOP_FACILITATOR_EMAIL', 'WORKSHOP_DATE', 'WORKSHOP_DURATION', 'WORKSHOP_ATTENDEES',
                   'WORKSHOP_ATTENDEES_CONFIRMED'])
    for row in rows:
        df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]],
                          columns = ['WORKSHOP_ID', 'WORKSHOP_TITLE', 'WORKSHOP_DESCRIPTION', 'WORKSHOP_FACILITATOR',
                                     'WORKSHOP_FACILITATOR_EMAIL', 'WORKSHOP_DATE', 'WORKSHOP_DURATION',
                                     'WORKSHOP_ATTENDEES', 'WORKSHOP_ATTENDEES_CONFIRMED'])
        databank_workshop = pd.concat([databank_workshop, df])
    databank_workshop = databank_workshop.sort_values('WORKSHOP_DATE', ascending = False)
    id_list = []
    for i in range(len(databank_workshop)):
        id_list.append(i + 1)
    databank_workshop.insert(0, "ID", id_list, True)
    databank_workshop = databank_workshop.set_index('ID')


    ## Google Sheet update
    # Open the spreadsheet and the first sheet
    #client = google_sheet_credentials()
    #if client != 'Exception':
        #sh = client.open_by_key(st.secrets['google']['spreadsheet_id'])
        #wks = sh.sheet1

        # Read the worksheet and get a pandas dataframe
        #try:
            #data = wks.get_as_df()
        #except:
            # print('Exception in read of Google Sheet')
    
        # Creating numpy array
        #numb = np.array(databank_workshop)
    
        # Converting dates to string
        #numb[:, [5]] = numb[:, [5]].astype('str')
    
        # Converting numby array to list
        #numb = numb.tolist()
    
        # Update the worksheet with the numpy array values at a specific range
        #try:
            #wks.update_values(crange = 'A2', values = numb)
        #except:
            #print('Exception in write of Google Sheet')



    ### Existing workshop
    st.title('Workshop data')


    ## Workshop selectbox
    workshop_title = [str(title) + ' (' for title in list(databank_workshop['WORKSHOP_TITLE'])]
    workshop_date = [str(date) + ')' for date in list(databank_workshop['WORKSHOP_DATE'])]
    workshops = [i + j for i, j in zip(workshop_title, workshop_date)]
    workshops.insert(0, 'New Workshop')
    if st.session_state['workshop'] == '00000':
        index_workshop = 0
    else:
        index_workshop = int(st.session_state['workshop'])
    index_workshop = st.selectbox(label = "Which workshop do you want to select?", options = range(len(workshops)),
                                  format_func = lambda x: workshops[x], index = index_workshop)


    ## Show specific workshop
    if index_workshop > 0:
        checkbox_val = st.checkbox(label = 'Edit Mode', value = False)
        with st.expander(label = '', expanded = True):
            st.header('Workshop')


            ## Form to view and enter workshop data
            with st.form('Workshop'):
                update = False
                title = st.text_input(label = 'Title',
                                      value = databank_workshop._get_value(index_workshop, 'WORKSHOP_TITLE'),
                                      disabled = not checkbox_val)
                if (databank_workshop._get_value(index_workshop, 'WORKSHOP_TITLE') != title):
                    update = True
                desc = st.text_input(label = 'Description',
                                     value = databank_workshop._get_value(index_workshop, 'WORKSHOP_DESCRIPTION'),
                                     disabled = not checkbox_val)
                if (databank_workshop._get_value(index_workshop, 'WORKSHOP_DESCRIPTION') != desc):
                    update = True
                facilitator = st.text_input(label = 'Facilitator', value = databank_workshop._get_value(index_workshop,
                                                                                                        'WORKSHOP_FACILITATOR'),
                                            disabled = not checkbox_val)
                if (databank_workshop._get_value(index_workshop, 'WORKSHOP_FACILITATOR') != facilitator):
                    update = True
                facilitator_email = st.text_input(label = 'Email address',
                                                  value = databank_workshop._get_value(index_workshop,
                                                                                       'WORKSHOP_FACILITATOR_EMAIL'),
                                                  disabled = not checkbox_val)
                if (databank_workshop._get_value(index_workshop, 'WORKSHOP_FACILITATOR_EMAIL') != facilitator_email):
                    update = True
                date = st.date_input(label = 'Date',
                                     value = databank_workshop._get_value(index_workshop, 'WORKSHOP_DATE'),
                                     disabled = not checkbox_val)
                if (databank_workshop._get_value(index_workshop, 'WORKSHOP_DATE') != date):
                    update = True
                duration = st.text_input(label = 'Duration',
                                         value = databank_workshop._get_value(index_workshop, 'WORKSHOP_DURATION'),
                                         disabled = not checkbox_val)
                if (databank_workshop._get_value(index_workshop, 'WORKSHOP_DURATION') != duration):
                    update = True

                submitted = st.form_submit_button('Save changes on Workshop data')
                if submitted:
                    ## Update workshop data
                    if update == True:
                        query = "UPDATE `idcard`.`WORKSHOP` SET WORKSHOP_TITLE = '%s', WORKSHOP_DESCRIPTION = '%s', WORKSHOP_FACILITATOR = '%s', WORKSHOP_FACILITATOR_EMAIL = '%s', WORKSHOP_DATE = '%s', WORKSHOP_DURATION = '%s' WHERE WORKSHOP_ID = '%s';" % (
                        title, desc, facilitator, facilitator_email, date, duration, workshop[0][1])
                        run_query(query)
                        conn.commit()

                        # Set updating Google Sheet
                        st.session_state['updateGoogleSheet'] = True

                        # Reload
                        st.experimental_rerun()


                    ## No changes, no database update
                    else:
                        st.warning(body = 'Not sumitted, as no new Workshop data was entered!', icon = "⚠️")


            ## Image select with attendees
            st.write('**Employees not confirmed:**')

            # Getting employee data which is needed for not confirmed
            not_confirmed = databank_workshop._get_value(index_workshop, 'WORKSHOP_ATTENDEES').split(' ')
            not_confirmed_query = ""
            for row in not_confirmed:
                if len(not_confirmed_query) == 0:
                    not_confirmed_query = not_confirmed_query + "EMPLOYEE_NO = " + "'" + row + "'"
                else:
                    if row != '':
                        not_confirmed_query = not_confirmed_query + " OR EMPLOYEE_NO = " + "'" + row + "'"
            query = "SELECT ID, ID, FORENAME, SURNAME, EMPLOYEE_NO, IMAGE FROM `idcard`.`IMAGEBASE` WHERE %s;" % (
                not_confirmed_query)
            rows = run_query(query)

            # Add placeholder
            image_placeholder = load_file('images/placeholder.png')
            databank_attendee = pd.DataFrame(
                columns = ['ID_INDEX', 'ID', 'FORENAME', 'SURNAME', 'EMPLOYEE_NO', 'IMAGE'])
            df = pd.DataFrame([[1, 0, 'None', '', 'xxxxxx', image_placeholder]],
                              columns = ['ID_INDEX', 'ID', 'FORENAME', 'SURNAME', 'EMPLOYEE_NO', 'IMAGE'])
            databank_attendee = pd.concat([databank_attendee, df])

            # Adding other
            id = 1
            for row in rows:
                id += 1
                df = pd.DataFrame([[id, row[1], row[2], row[3], row[4], row[5]]],
                                  columns = ['ID_INDEX', 'ID', 'FORENAME', 'SURNAME', 'EMPLOYEE_NO', 'IMAGE'])
                databank_attendee = pd.concat([databank_attendee, df])
            databank_attendee = databank_attendee.set_index('ID_INDEX')

            # Collect images from employee data
            images = []
            attendees_desc = []
            date = str(datetime.now()).replace(':', '_')
            for i in range(len(databank_attendee)):
                image_filename = 'images/temp' + date + str(i + 1) + '.png'
                images.append(image_filename)
                save_img(data = databank_attendee._get_value(i + 1, 'IMAGE'), filename = image_filename)
                attendees_desc.append(
                    databank_attendee._get_value(i + 1, 'FORENAME') + ' ' + databank_attendee._get_value(i + 1,
                                                                                                         'SURNAME') + ' (' + databank_attendee._get_value(
                        i + 1, 'EMPLOYEE_NO') + ')')

            # Show selectable images
            if len(images) > 1:
                attendee_option = image_select(label = 'Which employee should be confirmed?', images = images,
                                               captions = attendees_desc, index = 0, return_value = 'index')
            else:
                attendee_option = 0
                st.info(body = 'Invite Employees to this Workshop!', icon = "ℹ")

            # Delete temp images
            for i in range(len(databank_attendee)):
                if os.path.exists('images/temp' + date + str(i + 1) + '.png'):
                    os.remove('images/temp' + date + str(i + 1) + '.png')


            ## Rewriting lists to databank
            # Rebuildung confirmed and not_confirmed
            if st.button('Confirm selected'):
                confirmed, not_confirmed = rebuild_confirmation(option_attendee = attendee_option,
                                                                confirmed = databank_workshop._get_value(index_workshop,
                                                                                                         'WORKSHOP_ATTENDEES_CONFIRMED'),
                                                                not_confirmed = databank_workshop._get_value(
                                                                    index_workshop, 'WORKSHOP_ATTENDEES'),
                                                                employee = databank_attendee._get_value(
                                                                    attendee_option + 1, 'EMPLOYEE_NO'))

                # Update workshop data
                query = "UPDATE `idcard`.`WORKSHOP` SET WORKSHOP_ATTENDEES = '%s', WORKSHOP_ATTENDEES_CONFIRMED = '%s' WHERE WORKSHOP_ID = '%s';" % (
                not_confirmed, confirmed, databank_workshop._get_value(index_workshop, 'WORKSHOP_ID'))
                run_query(query)
                conn.commit()

                # Write to databank idcard table TRAINING
                id = lastID(url = '`idcard`.`TRAINING`')
                query = "INSERT INTO `idcard`.`TRAINING`(ID, EMPLOYEE_NO, WORKSHOP_ID) VALUES (%s, '%s', '%s');" % (
                id, databank_attendee._get_value(attendee_option + 1, 'EMPLOYEE_NO'),
                databank_workshop._get_value(index_workshop, 'WORKSHOP_ID'))
                run_query(query)
                conn.commit()

                # Reload
                st.experimental_rerun()


            ## Show confirmed
            st.write('**Employees confirmed:**')

            # Getting employee data which is needed for confirmed
            if databank_workshop._get_value(index_workshop, 'WORKSHOP_ATTENDEES_CONFIRMED') is not None:
                query = confirmed_query(databank_workshop._get_value(index_workshop, 'WORKSHOP_ATTENDEES_CONFIRMED'))
                confirmed_attendees = run_query(query)

                # Columns
                col1, col2, col3 = st.columns(3, gap = 'large')
                with col1:
                    for i in range(0, len(confirmed_attendees), 3):
                        st.image(confirmed_attendees[i][3],
                                 caption = confirmed_attendees[i][0] + ' ' + confirmed_attendees[i][1] + ' (' +
                                           confirmed_attendees[i][2] + ')')

                with col2:
                    for i in range(1, len(confirmed_attendees), 3):
                        st.image(confirmed_attendees[i][3],
                                 caption = confirmed_attendees[i][0] + ' ' + confirmed_attendees[i][1] + ' (' +
                                           confirmed_attendees[i][2] + ')')

                with col3:
                    for i in range(2, len(confirmed_attendees), 3):
                        st.image(confirmed_attendees[i][3],
                                 caption = confirmed_attendees[i][0] + ' ' + confirmed_attendees[i][1] + ' (' +
                                           confirmed_attendees[i][2] + ')')
            else:
                st.info(body = 'Confirm Employees after attending!', icon = "ℹ️")


            ## Multiselect to invite employees for workshop
            # Get employee data for filling the employee multiselect
            query = "SELECT ima.ID, ima.FORENAME, ima.SURNAME, ima.EMPLOYEE_NO, ima.JOB_TITLE, emp.EMPLOYEE_EMAIL FROM `idcard`.`IMAGEBASE` As ima LEFT JOIN `idcard`.`EMPLOYEE` AS emp ON emp.EMPLOYEE_NO = ima.EMPLOYEE_NO;"
            rows = run_query(query)

            # Building employees for multiselect which are not already in the confirmed list
            names, already_in = build_employees(data = rows,
                                                not_confirmed = databank_workshop._get_value(index_workshop,
                                                                                             'WORKSHOP_ATTENDEES'),
                                                confirmed = databank_workshop._get_value(index_workshop,
                                                                                         'WORKSHOP_ATTENDEES_CONFIRMED'))

            st.write('**Employees to invite:**')
            options = st.multiselect(label = 'Which Employee(s) do you want to add?', options = names)
            mail_addresses = [option.split('(', 1)[1][:-1] for option in options]
            new_in = [option.split(', ', 1)[1][:6] for option in options]
            attendees = ' '.join(already_in) + ' ' + ' '.join(new_in)


            ## Invite button
            if st.button('Invite selected'):
                ## Update workshop data
                query = "UPDATE `idcard`.`WORKSHOP` SET WORKSHOP_ATTENDEES = '%s' WHERE WORKSHOP_ID = '%s';" % (
                attendees, databank_workshop._get_value(index_workshop, 'WORKSHOP_ID'))
                run_query(query)
                conn.commit()


                ## Send mail to new attendees
                i = 0
                for mail in mail_addresses:
                    qrcode = generate_qrcode(data = str(
                        'https://' + get_ip() + ':8501/Workshops?workshop=' + databank_workshop._get_value(
                            index_workshop, 'WORKSHOP_ID')))
                    send_mail(subject = 'Invitation to workshop ' + databank_workshop._get_value(index_workshop,
                                                                                                 'WORKSHOP_TITLE'),
                              body = 'Hello colleague,\n\nthis is an invitation to the workshop ' + databank_workshop._get_value(
                                  index_workshop, 'WORKSHOP_TITLE') + ' on ' + str(
                                  databank_workshop._get_value(index_workshop, 'WORKSHOP_DATE')) + ' (' + str(
                                  databank_workshop._get_value(index_workshop,
                                                               'WORKSHOP_DURATION')) + ' days).\n\nDetails: ' + databank_workshop._get_value(
                                  index_workshop,
                                  'WORKSHOP_DESCRIPTION') + '\n\nBest regards\n\n' + databank_workshop._get_value(
                                  index_workshop, 'WORKSHOP_FACILITATOR') + '\n\n', receiver = mail,
                              attachment = qrcode)
                    send_mail(subject = 'Registration to workshop ' + databank_workshop._get_value(index_workshop,
                                                                                                   'WORKSHOP_TITLE'),
                              body = 'Hello facilitator,\n\nthis is the qrcode for the workshop ' + databank_workshop._get_value(
                                  index_workshop, 'WORKSHOP_TITLE') + ' on ' + str(
                                  databank_workshop._get_value(index_workshop, 'WORKSHOP_DATE')) + ' (' + str(
                                  databank_workshop._get_value(index_workshop,
                                                               'WORKSHOP_DURATION')) + ' days) for the employee ' +
                                     names[i] + '.\n\nDetails: ' + databank_workshop._get_value(index_workshop,
                                                                                                'WORKSHOP_DESCRIPTION') + '\n\nBest regards\n\nHR Staff Portal\n\n',
                              receiver = databank_workshop._get_value(index_workshop, 'WORKSHOP_FACILITATOR_EMAIL'),
                              attachment = qrcode)
                    i += 1

                # Rerun
                st.experimental_rerun()



    ### Show new workshop entry form
    else:
        ## Input form
        with st.form('Workshop new', clear_on_submit = True):
            st.header('New workshop entry')
            st.write('Here you can enter a new workshop.')


            ## Workshop data entry
            id = lastID(url = '`idcard`.`WORKSHOP`')
            workshop_id = generateID(id)
            st.text_input(label = 'ID', value = id, disabled = True)
            st.text_input(label = 'Workshop ID', value = workshop_id, disabled = True)
            workshop_title = st.text_input(label = 'Title', disabled = False)
            workshop_description = st.text_input(label = 'Description', disabled = False)
            workshop_facilitator = st.text_input(label = 'Facilitator', disabled = False)
            workshop_facilitator_email = st.text_input(label = 'Email address', disabled = False)
            workshop_date = st.date_input(label = 'Date', min_value = date(2023, 1, 1))
            workshop_duration = st.text_input(label = 'Duration', disabled = False)


            ## Multiselect to choose employees for workshop
            # Get employee data for filling the employee multiselect
            query = "SELECT ima.ID, ima.FORENAME, ima.SURNAME, ima.EMPLOYEE_NO, ima.JOB_TITLE, emp.EMPLOYEE_EMAIL FROM `idcard`.`IMAGEBASE` As ima LEFT JOIN `idcard`.`EMPLOYEE` AS emp ON emp.EMPLOYEE_NO = ima.EMPLOYEE_NO;"
            rows = run_query(query)

            # Building employees for  multiselect
            row = []
            names = []

            # Concenate employee data
            for row in rows:
                if row[5] is None:
                    names.append(str(row[1] + ' ' + row[2] + ', ' + row[3] + ', ' + row[4] + ' ('')'))
                else:
                    names.append(str(row[1] + ' ' + row[2] + ', ' + row[3] + ', ' + row[4] + ' (' + row[5] + ')'))

            # Populate options
            options = st.multiselect(label = 'Which Employee(s) do you want to select?', options = names)

            # Extract mail addresses
            mail_addresses = [option.split('(', 1)[1][:-1] for option in options]

            # Extract employee numbers
            employee_no = [option.split(', ', 1)[1] for option in options]
            employees = [employee_n.split(', ', 1)[0] for employee_n in employee_no]


            ## Form Submit button
            submitted = st.form_submit_button(label = 'Submit new Workshop')
            if submitted:
                ## Write workshop data
                id = lastID(url = '`idcard`.`WORKSHOP`')
                workshop_id = generateID(id)
                query = "INSERT INTO `idcard`.`WORKSHOP`(ID, WORKSHOP_ID, WORKSHOP_TITLE, WORKSHOP_DESCRIPTION, WORKSHOP_FACILITATOR, WORKSHOP_FACILITATOR_EMAIL, WORKSHOP_DATE, WORKSHOP_DURATION, WORKSHOP_ATTENDEES) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                id, workshop_id, workshop_title, workshop_description, workshop_facilitator, workshop_facilitator_email,
                workshop_date, workshop_duration, ' '.join(employees))
                run_query(query)
                conn.commit()


                ## Set updating Google Sheet
                st.session_state['updateGoogleSheet'] = True


                ## Send mail to attendees
                i = 0
                for mail in mail_addresses:
                    qrcode = generate_qrcode(
                        data = str('https://' + get_ip() + ':8501/Workshops?workshop=' + workshop_id))
                    send_mail(subject = 'Invitation to workshop ' + workshop_title,
                              body = 'Hello colleague,\n\nthis is an invitation to the workshop ' + workshop_title + ' on ' + str(
                                  workshop_date) + ' (' + workshop_duration + ' days).\n\nDetails: ' + workshop_description + '\n\nBest regards\n\n' + workshop_facilitator + '\n\n',
                              receiver = mail, attachment = qrcode)
                    send_mail(subject = 'Registration to workshop ' + workshop_title,
                              body = 'Hello facilitator,\n\nthis is the qrcode for the workshop ' + workshop_title + ' on ' + str(
                                  workshop_date) + ' (' + workshop_duration + ' days) for the employee ' + options[
                                         i] + '.\n\nDetails: ' + workshop_description + '\n\nBest regards\n\nHR Staff Portal\n\n',
                              receiver = workshop_facilitator_email, attachment = qrcode)
                    i += 1


                ## Reload
                st.session_state['workshop'] = workshop_id
                st.experimental_rerun()
                
    
    
    ### Show Google Sheet Workshop data
    #with st.expander('Workshop data'):
        #duplicate_cols = data.columns[data.columns.duplicated()]
        #data.drop(columns = duplicate_cols, inplace = True)
        #databank_workshop_edited = st.experimental_data_editor(data)
    



### Logged out state (Workshops page)
else:
    ## Landing page
    landing_page('Workshops page.')
