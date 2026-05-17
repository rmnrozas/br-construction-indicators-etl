# %%
import pandas as pd

df = pd.read_parquet('../../data/gold/indicators.parquet')

df
# %%

df['indicator'].unique()