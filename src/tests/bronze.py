# %%
import pandas as pd

df_sinapi_raw = pd.read_json('../../data/raw/ibge/sinapi/20260425_response.json')

df_sinapi_raw.head()
# %%
df_sinapi_raw.columns
# %%
df_sinapi_raw.shape
# %%
df_sinapi = df_sinapi_raw.copy()

# Remoção de colunas desnecessárias
df_sinapi = df_sinapi.drop(['MC', 'NC', 'NN', 'D1C', 'D1N', 'D3N'], axis=1)

# Transformação colunas 
new_columns = df_sinapi.iloc[0]

df_sinapi.columns = new_columns

# Remoção da primeira linha duplicada
df_sinapi = df_sinapi.drop(index=0)
# %%
df_sinapi.to_parquet('../../data/bronze/sinapi.parquet', engine='pyarrow')
