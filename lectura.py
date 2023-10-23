import pandas as pd

def appendToNewDf(new_df, source_df):
  for r in range(source_df.shape[0]):
    row = source_df.iloc[r]
    nombre_completo = row['Nombre'].split()
    roles = {'Mercado':'1', 'Colonia':'2', 'Taller':'3'}

    new_df.loc[len(new_df.index)] = [
      nombre_completo[0],
      nombre_completo[1],
      row['Gen.'],
      roles[source_df.columns[2]],
      row['Colonia.1']
    ]

df = pd.read_excel('../Rol de Octubre.xlsx')
asistencia_df = pd.DataFrame(columns=['Nombre','Apellido','Gen.','Rol','Colonia'])

df_mercado = df.dropna(subset=['Mercado'])
df_mercado = df_mercado.dropna(axis='columns')
appendToNewDf(asistencia_df, df_mercado)

df_colonia = df.dropna(subset=['Colonia'])
df_colonia = df_colonia.dropna(axis='columns')
appendToNewDf(asistencia_df, df_colonia)

df_taller = df.dropna(subset=['Taller'])
df_taller = df_taller.dropna(axis='columns')
appendToNewDf(asistencia_df, df_taller)

print(asistencia_df)