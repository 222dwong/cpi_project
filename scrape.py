import sys
import requests as rq
from bs4 import BeautifulSoup as bs
from time import sleep
from time import time
from random import randint
from warnings import warn
import json
import pandas as pd

# URL of webpage to scrape (CPI Index Summary from web.archive.org)
# url = 'https://web.archive.org/web/20240602054955/https://www.bls.gov/news.release/archives/cpi_02132020.htm'

def scrape_cpi(url):
    # send a GET request to the webpage
    response = rq.get(url)

    # check if request was successful
    if response.status_code == 200:
        # parse the HTML content of the webpage
        soup = bs(response.content, 'html.parser')

        # find the table
        table = soup.find('table', attrs={'class':'regular'})

        # skip tbody to avoid repeating headings
        tbody = table.find('tbody')

        # iterate over each row in the table
        rows = tbody.find_all('tr')

        # empty list storing data
        table_data = []

        # iterate through each row
        for row in rows:
            category = row.find('th')
            data = row.find_all('td')
            if category:
                category_text = category.text.strip()

                # data for each column)
                row = [td.text.strip() for td in data]
                
                row.insert(0, category_text)
                table_data.append(row)

        # headers = [th.get_text(strip=True) for th in table.find_all('th')]

        name = soup.find(id = 'bodytext')
        titles = name.find_all('th', class_ = 'stubhead')

        headers = [header.text for header in titles]

        headers = [headers[i] for i in [0, 1, 5, 6, 7, 8, 9, 10, 11, 12]]

        # print(headers)

        df = pd.DataFrame(table_data[:], columns=headers)
        print("Table Scraped: \n")
        print(df.to_string())

        save = input("Save file? (Y/N): ")
        if (save == "Y" or save == "y"):
            # scraped format (Mon.Year)            
            date = df.iloc[0].index[-1][-8:]
            month = date[:3]
            year = date[4:]

            originalFormat = ["Jan", "Feb", "Mar","Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            txtFormat = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

            if month in originalFormat:
                month_index = originalFormat.index(month)
                month = txtFormat[month_index]
            else:
                month = input("Insert month (month_): ")          

            date = month + "_" + year + ".txt"

            df.to_csv(date, index=False)

    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')    

def main():
    isTrue = True
    while(isTrue):
        url = input("Insert CPI URL: ")
        scrape_cpi(url)
        goAgain = input("Would you link to scrape another URL? (Y/N)?: ")
        if (goAgain != "Y" or goAgain != "y"):
            isTrue = False

if __name__ == "__main__":
    main()