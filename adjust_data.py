# Takes in txt input file for dataframe, inverts table (row: month-year; column: expediture category), selects

import pandas as pd
import os
df = pd.read_csv('may_2024.txt')

output_file = "testing.txt"

headers = df.iloc[:,0]
headers_row = headers.to_frame().transpose()
headers_row.to_csv(output_file, mode = 'a', header = False)
# print(headers_row)

# print(len(df.index))

# result = df.iloc[:, 0]
# print(result)

files = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

for year in years:
    for month in months:
        # Construct the path to the text file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_dir, "raw_cpi_data", year)
        file_path = os.path.join(folder_path, f"{month + '_' + year}.txt")

        # Check if the file exists before trying to open it
        if os.path.exists(file_path):
            try:
                # Read the content of the file
                df = pd.read_csv(file_path)
                # Process the file content as needed
                print(f"Processing {file_path}")
                # For example, you can print the first few lines
                # print(df.head()) 

                # deletes comma in string
                df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: float(str(x).replace(',', '')))

                # select column for appropriate month of data
                select_column = df.iloc[:,3]
                single_row_df = select_column.to_frame().transpose()

                # headers = df.iloc[:,0]
                # headers_row = headers.to_frame().transpose()
                # print(headers_row)

                single_row_df.to_csv(output_file, mode = 'a', header = False)

            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        else:
            print(f"File {file_path} does not exist")