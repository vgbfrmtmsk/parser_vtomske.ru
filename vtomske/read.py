import pandas as pd

path = r'D:\work\practice\parser\vtomske\vtomske_processed.csv'

df = pd.read_csv(path, sep=';')


print(df.columns.tolist())
