# Chat after export looks like
# 06/11/21, 7:50 pm - Rahul Jamia: #Senior jawab do🤣

import streamlit as st
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


def getstring(text):      # line 45
    return text.split('\n')[0]

def gettimeanddate(string):   # line 25
    string = string.split(',')
    date,time = string[0],string[1]
    time = time.split('-')
    time = time[0].strip()

    return  date+ " " +time

def preprocess(data):
    pattern ='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[a,p]m\s-\s'
    messages = re.split(pattern,data)[1:]  #['Rahul Jamia: #Senior jawab do🤣']
    dates= re.findall(pattern,data)  #[' 06/11/21, 7:50 pm - ']

    #creating dataframe for messages and their dates
    df = pd.DataFrame({'user_messages': messages,
                       'message_date': dates})

    df['message_date']=df['message_date'].apply(
        lambda text: gettimeanddate(text))
    df.rename(columns={'message_date':'date'},inplace =True)

    users=[]
    messages =[]

    for message in df['user_messages']:

        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append('Group Notification')
            messages.append(entry[0])

    df['User'] = users
    df['message'] = messages

    df['message'] = df['message'].apply(lambda text: getstring(text))

    df = df.drop(['user_messages'], axis=1)
    df = df[['message', 'date', 'User']]

    df = df.rename(columns={'message': 'Message',
                            'date': 'Date'})

    
    df['Only_date'] = pd.to_datetime(df['Date']).dt.date

    df['Year'] = pd.to_datetime(df['Date']).dt.year

    df['Month_num'] = pd.to_datetime(df['Date']).dt.month

    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()

    df['Day'] = pd.to_datetime(df['Date']).dt.day

    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()

    df['Hour'] = pd.to_datetime(df['Date']).dt.hour

    df['Minute'] = pd.to_datetime(df['Date']).dt.minute

    return df

   #Now this df will get returned to app.py line 22

    