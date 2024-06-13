import pandas as pd
df = pd.read_csv('testing.txt')
print(df.T.to_string())