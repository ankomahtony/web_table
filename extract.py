from bs4 import BeautifulSoup
from docxtpl import RichText
import csv
from urllib.request import urlopen
import streamlit as st

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
    # rt = RichText();
    # print(output_rows)
