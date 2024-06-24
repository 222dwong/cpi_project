import pandas as pd

input_file_cpi = 'cpi_by_category.txt'
input_file_weight = 'cpi.weight_by_category.txt'

df = pd.read_csv(input_file_cpi)
print(df)
df = pd.read_csv(input_file_weight)
print(df)