# %%
import pandas as pd

df = pd.read_parquet('../../data/gold/indicators.parquet')

df.head(25)

df
# %%

df.isna().sum()