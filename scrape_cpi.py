import sys
import requests as rq
from bs4 import BeautifulSoup as bs
from time import sleep
from time import time
from random import randint
from warnings import warn
import json
import pandas as pd

# URL of webpage to scrape (CPI Index Summary)
url = 'https://web.archive.org/web/20240531084626/https://www.bls.gov/news.release/cpi.t01.htm'

# send a GET request to the webpage
response = rq.get(url)

# check if request was successful
if response.status_code == 200:
    # parse the HTML content of the webpage
    soup = bs(response.content, 'html.parser')

    # find the table
    table = soup.find('table')

    # iterate over each row in the table
    rows = table.find_all('tr')

    # empty list storing data
    table_data = []

    # retrieve column headers
    header0 = table.find_all('tr')[0].find_all('th')
    header1 = table.find_all('tr')[1].find_all('th')
    header_row0 = [header.text.strip() for header in header0]
    header_row1 = [header.text.strip() for header in header1]
    
    header_row1.insert(0, header_row0[1])
    header_row1.insert(0,header_row0[0])

    table_data.append(header_row1)




    for i in rows:
        category = i.find('th')
        data = i.find_all('td')
        if category:
            category_text = category.text.strip()

            # data for each column
            row = [td.text.strip() for td in data]

            row.insert(0, category_text)
            table_data.append(row)

    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    df = df.drop([df.index[0], df.index[1]])
    print(df)

    print("Column names:", df.columns.values)
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')    
