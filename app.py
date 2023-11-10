import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
from prediction import predict


st.title('NYC Parking Ticket Reduction')
st.markdown('Try Your Luck to Reduce Your Parking Ticket Fine.')

parking_data = pd.read_csv('data/parkingdata.csv')

Headers = pd.read_csv('data/Headers.csv')

violation_fine = pd.read_excel('data/ParkingViolationCodes_January2020.xlsx')

selectiondata = {
    'Violation Precinct': pd.read_csv("data/Violation Precinct.csv",header=None),
    'Issuer Precinct': pd.read_csv("data/Issuer Precinct.csv",header=None),
    'License Type': pd.read_csv("data/License Type.csv",header=None),
    'Violation': pd.read_csv("data/Violation.csv",header=None),
    'County': pd.read_csv("data/County.csv",header=None),
    'Issuing Agency': pd.read_csv("data/Issuing Agency.csv",header=None),
    'Issuer Command': pd.read_csv("data/Issuer Command.csv",header=None),
    'Law Section': pd.read_csv("data/Law Section.csv",header=None),
    'Time': pd.read_csv("data/Time.csv",header=None),
    'DayOfWeek': pd.read_csv("data/DayOfWeek.csv",header=None)
}

st.header("Predict")
#
# Best n_estimators: 10
# Test Mean Squared Error: 1.22363904937926

violation_code = st.selectbox('**Select Violation**', selectiondata['Violation'])

fine_amount = st.number_input('Enter Your Fine Amount',min_value=0)

penalty_amount = st.number_input('Enter Your Penalty Amount',min_value=0)

interest_amount = st.number_input('Enter Your Interest Amount',min_value=0)

payment_amount = st.number_input('Enter Your Payment Amount',min_value=0)

amount_due = st.number_input('Enter Your Amount Due',min_value=0)

violation_precint = st.selectbox('**Select Violation Precint**', selectiondata['Violation Precinct'])

issuer_percint = st.selectbox('**Select Issuer Precint**', selectiondata['Issuer Precinct'])

license_type = st.selectbox('**Select License Type**', selectiondata['License Type'])

law_section = st.selectbox('**Select Law Section**', selectiondata['Law Section'])

violation_county = st.selectbox('**Select Violation County**', selectiondata['County'])

issuing_agency = st.selectbox('**Select Issuing Agency**', selectiondata['Issuing Agency'])

issuing_command = st.selectbox('**Select Issuer Command**', selectiondata['Issuer Command'])

violation_date = st.date_input("Enter Violation Date", value=None,format="YYYY/MM/DD",max_value=datetime.today())

violation_time = st.time_input("Enter Violation Time", value=None)

st.text('')
if st.button("Calculate"):

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    actual_fine_amount = violation_fine[violation_fine['VIOLATION DESCRIPTION'] == violation_code]
    if(violation_county == 'New York'):
        actual_fine_amount = actual_fine_amount["Manhattan  96th St. & below\n(Fine Amount $)"]
    else:
        actual_fine_amount = actual_fine_amount["All Other Areas\n(Fine Amount $)"]
    date_string = violation_date.strftime('%Y-%m-%d %H:%M:%S')
    date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    day_of_week = date_obj.strftime('%A')
    violation_time = str(violation_time)
    violation_time = violation_time.split(":")[0]
    parking_data['Fine Amount'] = fine_amount
    parking_data['Penalty Amount'] = penalty_amount
    parking_data['Interest Amount'] = interest_amount
    parking_data['Payment Amount'] = payment_amount
    parking_data['Amount Due'] = amount_due
    parking_data['Violation Precinct'] = violation_precint
    parking_data['Issuer Precinct'] = issuer_percint
    if (int(fine_amount) > int(actual_fine_amount)):
        parking_data['Is_High'] = True
    else:
        parking_data['Is_High'] = False
    parking_data['License Type_' +license_type] = 1
    parking_data['Violation_' +violation_code] = 1
    parking_data['County_' +violation_county] = 1
    parking_data['Issuing Agency_' +issuing_agency] = 1
    parking_data['Issuer Command_' +issuing_command] = 1
    parking_data['Law Section_' +law_section] = 1
    parking_data['Time_' +violation_time+':00'] = 1
    parking_data['DayOfWeek_' +day_of_week] = 1
    result = predict(parking_data)
    st.text(f'Your Price can be Reduced to : ${result[0]}')
    # st.text(parking_data)
    # st.text(violation_time)

st.text('')
st.text('')
st.markdown('Created by Jerry')
