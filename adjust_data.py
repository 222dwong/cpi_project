# Takes in txt input file for dataframe, inverts table (row: month-year; column: expediture category), selects

import pandas as pd
df = pd.read_csv('may_2024.txt')
df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: float(str(x).replace(',', '')))

# select column for appropriate month of data
select_column = df.iloc[:,3]
single_row_df = select_column.to_frame().transpose()
print(single_row_df)

#
result = df.T.iloc[2].to_string(index=False).strip()
headers = ','.join(df.iloc[:, 0])

'''with open('testing.txt', 'a') as file:
    file.write('Year-Month,' + headers + '\n')
    file.write('2024-05,' + ','.join(result.split()) + '\n')'''