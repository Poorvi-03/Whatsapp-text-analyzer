import streamlit as st
import re
import numpy as np
import pandas as pd
import preprocess
import stats
import matplotlib.pyplot as plt
import datetime as dt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue() #this function returns the entire content of the file

data = bytes_data.decode("utf-8") #this method is used to convert from one encoding scheme to the desired scheme



#sending file 'data' for further preprocessing
df = preprocess.preprocess(data)
#where first preprocess is the file name and other a function residing in it

# *******************DONE WITH preprocess.py*****************************


# fetch unique users
user_list = df['User'].unique().tolist()

# removing the groupnotification

user_list.remove('Group Notification')

# including overall,this will be responsible for showcasing the  overall chat group analysis

user_list.insert(0, "Overall")

selected_user = st.sidebar.selectbox(
        "Show analysis with respect to", user_list)

st.title("Whattsapp chat analysis for " +selected_user)
if st.sidebar.button("Show Analysis"):

        # getting the stats of the selected user from the stats script

        num_messages, num_words, media_omitted, links = stats.fetchstats(
            selected_user, df)

        # first phase is to showcase the basic stats like number of users,number of messages,number of media shared and all,so for that i requrire the 4 columns

        col1, col2, col3, col4 = st.beta_columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total No.of Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(media_omitted)

        with col4:
            st.header("Total Links Shared")
            st.title(links)

        # finding the busiest users in the group

        if selected_user == 'Overall':

            # dividing the space into two columns
            # first col is the bar chart and the second col is the dataframe representing the

            st.title('Most Busy Users')
            busycount, newdf = stats.fetchbusyuser(df)
            fig, ax = plt.subplots()
            col1, col2 = st.beta_columns(2)
            with col1:
                ax.bar(busycount.index, busycount.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(newdf)

        # Word Cloud

        st.title('Word Cloud')
        df_img = stats.createwordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        st.pyplot(fig)

        # most common words in the chat

        most_common_df = stats.getcommonwords(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most commmon words')
        st.pyplot(fig)

        # Emoji Analysis

        emoji_df = stats.getemojistats(selected_user, df)
        emoji_df.columns = ['Emoji', 'Count']

        st.title("Emoji Analysis")

        col1, col2 = st.beta_columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            emojicount = list(emoji_df['Count'])
            perlist = [(i/sum(emojicount))*100 for i in emojicount]
            emoji_df['Percentage use'] = np.array(perlist)
            st.dataframe(emoji_df)

        # Monthly timeline

        st.title("Monthly Timeline")
        time = stats.monthtimeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time['Time'], time['Message'], color='green')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        # Activity maps

        st.title("Activity Maps")

        col1, col2 = st.beta_columns(2)

        with col1:

            st.header("Most Busy Day")

            busy_day = stats.weekactivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

        with col2:

            st.header("Most Busy Month")
            busy_month = stats.monthactivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)


    
