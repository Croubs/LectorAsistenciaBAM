import pandas as pd

df = pd.read_excel('./Rol de Octubre.xlsx')

df_mercado = df.dropna(subset=['Mercado'])
df_mercado = df_mercado.dropna(axis='columns')
print(df_mercado)

df_colonia = df.dropna(subset=['Colonia'])
df_colonia = df_colonia.dropna(axis='columns')
print(df_colonia)

df_taller = df.dropna(subset=['Taller'])
df_taller = df_taller.dropna(axis='columns')
print(df_taller)

