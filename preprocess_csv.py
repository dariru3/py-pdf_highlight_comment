import pandas as pd

df = pd.read_csv('input_folder/AR unchecked check list csv.csv')

df = df.drop('color', axis=1)

print(df.head(10))

df.to_csv('input_folder/processed.csv', index=False)