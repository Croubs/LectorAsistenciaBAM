import pandas as pd
from datetime import date
import requests
import json

def appendToPayload(payload, source_df, dateBrigade):
  for r in range(source_df.shape[0]):
    row = source_df.iloc[r]
    nombre_completo = row['Nombre'].split()
    roles = {'Mercado':'1', 'Colonia':'2', 'Taller':'3'}

    payload['Nombre'].append(nombre_completo[0])
    payload['Apellido'].append(nombre_completo[1])
    payload['Gen'].append(row['Gen.'])
    payload['Rol'].append(roles[source_df.columns[2]])
    payload['Colonia'].append(row['Colonia.1'])
    payload['Fecha'].append(dateBrigade)

def getDateBrigade(sheet):
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

xlsx = pd.ExcelFile('../1deOctubre.xlsx')

df = pd.read_excel(xlsx)
asistencia = {
  'Nombre': [],
  'Apellido': [],
  'Gen': [],
  'Rol': [],
  'Colonia': [],
  'Fecha': []
}

for sheet in xlsx.sheet_names:
  dateBrigade = getDateBrigade(sheet)
  df_mercado = df.dropna(subset=['Mercado'])
  df_mercado = df_mercado.dropna(axis='columns')
  appendToPayload(asistencia, df_mercado, dateBrigade)

  df_colonia = df.dropna(subset=['Colonia'])
  df_colonia = df_colonia.dropna(axis='columns')
  appendToPayload(asistencia, df_colonia, dateBrigade)

  df_taller = df.dropna(subset=['Taller'])
  df_taller = df_taller.dropna(axis='columns')
  appendToPayload(asistencia, df_taller, dateBrigade)

# Now you can print or save asistencia_df with all your records together
access_token = 'Your access token'
header = {
  'Authorization': 'Bearer ' + access_token
}

payload = json.dumps(asistencia)

response = requests.post('API_url', data=payload, headers=header)
print(response.json())