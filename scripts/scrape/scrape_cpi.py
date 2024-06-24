import sys
import requests as rq
from bs4 import BeautifulSoup as bs
from time import sleep
from time import time
from random import randint
from warnings import warn
import json
import pandas as pd
import os

# URL of webpage to scrape (CPI Index Summary)
# website = https://www.bls.gov/bls/news-release/cpi.htm
# url = 'https://www.bls.gov/news.release/archives/cpi_05152024.htm'

proxy = "http://<YOUR_ZENROWS_API_KEY>:premium_proxy=true&proxy_country=us@proxy.zenrows.com:8001"
proxies = {"http": proxy, "https": proxy}

def scrape_cpi(url):
    # send a GET request to the webpage

    response = rq.get(url, proxies=proxies, verify=False)

    # check if request was successful
    if response.status_code == 200:
        # parse the HTML content of the webpage
        soup = bs(response.content, 'html.parser')

        # check the table caption
        table_caption = soup.find_all('caption')
        target_text = "Table 1. Consumer Price Index for All Urban Consumers (CPI-U): U.S. city average, by expenditure category"
        text_found = False

        for caption in table_caption:
            if target_text in caption.text:
                text_found = True

                # find table corresponding to caption
                table = caption.find_parent('table', attrs={'class':'regular'})


        if text_found:

            # find the table
            # table = soup.find('table', attrs={'class':'regular'})

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

            # name = soup.find(id = 'bodytext')
            # titles = name.find_all('th', class_ = 'stubhead')

            # headers = [header.text for header in titles]
                    
            headers = [th.get_text(strip=True) for th in table.find_all('th')]

            headers = [headers[i] for i in [0, 1, 5, 6, 7, 8, 9, 10, 11, 12]]

            # print(headers)

            df = pd.DataFrame(table_data[:], columns=headers)
            print("Table Scraped: \n")
            print(df.to_string())

            save = input("Save file? (Y/N): ").lower()
            if (save == "y"):
                # scraped format (Mon.Year)            
                dateRange = df.iloc[0].index[-1]
                date = dateRange.split('-')[-1]

                if "." in date:
                    month = date[:3]
                    year = date[4:]
                else:
                    month = date[:3]
                    year = date[3:]

                originalFormat = ["Jan", "Feb", "Mar","Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                txtFormat = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

                if month in originalFormat:
                    month_index = originalFormat.index(month)
                    month = txtFormat[month_index]
                else:
                    month = input("Insert month (month): ")          

                date = month + "_" + year + ".txt"

                current_dir = os.path.dirname(os.path.abspath(__file__))
                folder_path = os.path.join(current_dir, "raw_cpi_data", year)
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, date)

                df.to_csv(file_path, index=False)

    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')    

def main():
    isTrue = True
    while(isTrue):
        url = input("Insert CPI URL: ")
        scrape_cpi(url)
        goAgain = input("Would you link to scrape another URL? (Y/N)?: ").lower()
        if (goAgain != "y"):
            isTrue = False

if __name__ == "__main__":
    main()