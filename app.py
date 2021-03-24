import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import os
from datetime import datetime
from bs4 import BeautifulSoup
from docxtpl import RichText
import csv
from urllib.request import urlopen

# CSS
@st.cache(suppress_st_warning=True)
def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")
remote_css("https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css")
# End CSS


def remove_html_n(text):
    """Remove \n from a string"""
    import re
    clean = re.compile('\n')
    return re.sub(clean, '', text)

def remove_html_space(text):
    """Remove spaces from a string"""
    import re
    clean = re.compile('  ')
    return re.sub(clean, '', text)
#
@st.cache
def load_data_csv(html):
    html = urlopen(html)
    html = html.read().decode("utf-8")
    html = remove_html_n(html)
    html = remove_html_space(html)
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find("table")


    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('th')
        columns += table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)

    with open('dataset.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)


st.title("Download an CSV form of Data From A Website")

html_url = st.text_input("Enter the url of the website here")

try:
  load_data_csv(html_url)
  df_web = pd.read_csv('dataset.csv', thousands=',')
  st.write(df_web)
  st.write(html_url)
except:
  st.write("An exception occurred: Might be wrong URL or URL has no table")

file_type = st.selectbox('Type of File',['csv','excel'])
csv = st.checkbox('CSV')
excel = st.checkbox('Excel')
if st.button("Download"):
    from pathlib import Path
    path_to_download_folder = str(os.path.join(Path.home(), "Downloads/Web_data"))

    if not os.path.exists(path_to_download_folder):
        os.makedirs(path_to_download_folder)

    fileName = 'file'+str(datetime.now())
    df_web = pd.read_csv('dataset.csv', thousands=',')
    if csv and excel:
        df_web.to_csv(path_to_download_folder+'/'+fileName+'.csv', index = False)
        df_web.to_excel(path_to_download_folder+'/'+fileName+'.xlsx', index = False)
        st.markdown('You have just downloaded excel and csv format of your data and you can find it in your Downloads/Web_data Folder')
    elif csv:
        df_web.to_csv(path_to_download_folder+'/'+fileName+'.csv', index = False)
        st.markdown('You have just downloaded csv format of your data and you can find it in your Downloads/Web_data Folder')
    elif excel:
        df_web.to_excel(path_to_download_folder+'/'+fileName+'.xlsx', index = False)
        st.markdown('You have just downloaded excel format of your data and you can find it in your Downloads/Web_data Folder')
    else:
        st.markdown('You did choose file type so nothing was downloaded')
