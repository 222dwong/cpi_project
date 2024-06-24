import pandas as pd
import numpy as np
import re

input_file_cpi = 'cpi_by_category.txt'
input_file_weight = 'cpi.weight_by_category.txt'

# Read and clean the CPI data
df_cpi = pd.read_csv(input_file_cpi)
print(df_cpi.head(3).T)

# Convert all columns (except the first one) to string type
for column in df_cpi.columns[1:]:
    df_cpi[column] = df_cpi[column].astype(str)

# Remove non-numeric characters for decimal points from all columns except the first one
for column in df_cpi.columns[1:]:
    df_cpi[column] = df_cpi[column].str.replace(r'[^\d.]', '', regex=True)

# Replace empty strings with NaN
for column in df_cpi.columns[1:]:
    df_cpi[column] = df_cpi[column].replace('', np.nan)

# Convert the cleaned columns back to float
for column in df_cpi.columns[1:]:
    df_cpi[column] = df_cpi[column].astype(float)

print(df_cpi.head(3).T)


# Read and clean the weight data
df_weight = pd.read_csv(input_file_weight)
print(df_weight.head(3).T)

# Remove unwanted characters and numbers in column headers, replace spaces with underscores, and convert to lowercase for both dataframes
def clean_column_names(columns):
    columns = columns.str.replace(r'[\d,()]+', '', regex=True)  # Remove numbers, commas, and parentheses
    columns = columns.str.replace("'", "")  # Remove single quotes
    columns = columns.str.replace(' ', '_')  # Replace spaces with underscores
    columns = columns.str.lower()  # Convert to lowercase
    return columns

def clean_first_column(df):
    df.iloc[:, 0] = df.iloc[:, 0].str.lower().str.replace('.', '_')

def format_weight_column(value):
    # Match pattern "relativeimportancedec_2013" and replace with "relative_importance_dec_2013"
    return re.sub(r'(\w)([A-Z])', r'\1_\2', value).lower()

# Apply formatting to the first column of the weights table
df_weight.iloc[:, 0] = df_weight.iloc[:, 0].apply(format_weight_column)

df_cpi.columns = clean_column_names(df_cpi.columns)
df_weight.columns = clean_column_names(df_weight.columns)

clean_first_column(df_cpi)
clean_first_column(df_weight)

print("CPI DataFrame with updated column headers and cleaned first column:")
print(df_cpi.head(3).T)

print("Weight DataFrame with updated column headers and cleaned first column:")
print(df_weight.head(3).T)

# Define custom file names
output_file_cpi = 'cpi_cleaned.txt'
output_file_weight = 'weight_cleaned.txt'

df_cpi.to_csv(output_file_cpi, mode = 'a', header = False)
df_weight.to_csv(output_file_weight, mode = 'a', header = False)