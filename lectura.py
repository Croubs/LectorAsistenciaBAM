import pandas as pd
from datetime import date

def appendToNewDf(new_df, source_df, dateBrigade):
  for r in range(source_df.shape[0]):
    row = source_df.iloc[r]
    nombre_completo = row['Nombre'].split()
    roles = {'Mercado':'1', 'Colonia':'2', 'Taller':'3'}

    new_df.loc[len(new_df.index)] = [
      nombre_completo[0],
      nombre_completo[1],
      row['Gen.'],
      roles[source_df.columns[2]],
      row['Colonia.1'],
      dateBrigade
    ]

def getDateBrigate(sheet):
  month_dict = {
    'Enero': 1,
    'Frebrero': 2,
    'Marzo': 3,
    'Abril': 4,
    'Mayo': 5,
    'Junio': 6,
    'Julio': 7,
    'Agosto': 8,
    'Septiembre': 9,
    'Octubre': 10,
    'Noviembre': 11,
    'Diciembre': 12
  }

  sheet_name = sheet.split()
  day = sheet_name[0]
  month = month_dict[sheet_name[2]]
  year = date.today().year
  dateBrigade = date(year,month,int(day))

  return dateBrigade.isoformat()

xlsx = pd.ExcelFile('path-to-excel-file')

df = pd.read_excel(xlsx)
asistencia_df = pd.DataFrame(columns=['Nombre','Apellido','Gen.','Rol','Colonia','Fecha'])

for sheet in xlsx.sheet_names:
  dateBrigate = getDateBrigate(sheet)
  df_mercado = df.dropna(subset=['Mercado'])
  df_mercado = df_mercado.dropna(axis='columns')
  appendToNewDf(asistencia_df, df_mercado, dateBrigate)

  df_colonia = df.dropna(subset=['Colonia'])
  df_colonia = df_colonia.dropna(axis='columns')
  appendToNewDf(asistencia_df, df_colonia, dateBrigate)

  df_taller = df.dropna(subset=['Taller'])
  df_taller = df_taller.dropna(axis='columns')
  appendToNewDf(asistencia_df, df_taller, dateBrigate)

# Now you can print or save asistencia_df with all your records together