import pandas as pd

df = pd.read_parquet('data/processed_facets.parquet')
print(df.head(50))