import json
from datetime import date
import boto3
import pandas as pd
import openpyxl
import requests

s3Client = boto3.client('s3')

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

def lambda_handler(event, context):
    # Get bucket and file name
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Get file
    response = s3Client.get_object(Bucket=bucket, Key=key)
    file = response['Body'].read()

    # Get df
    xlsx = pd.ExcelFile(file)
    df = pd.read_excel(xlsx)
    
    # This will save all records
    asistencia = {
      'Nombre': [],
      'Apellido': [],
      'Gen': [],
      'Rol': [],
      'Colonia': [],
      'Fecha': []
    }
    
    # Get date
    dateBrigade = getDateBrigate(xlsx.sheet_names[0])
    
    # Get schedule by rols
    df_mercado = df.dropna(subset=['Mercado'])
    df_mercado = df_mercado.dropna(axis='columns')
    appendToPayload(asistencia, df_mercado, dateBrigade)
    
    df_colonia = df.dropna(subset=['Colonia'])
    df_colonia = df_colonia.dropna(axis='columns')
    appendToPayload(asistencia, df_colonia, dateBrigade)
    
    df_taller = df.dropna(subset=['Taller'])
    df_taller = df_taller.dropna(axis='columns')
    appendToPayload(asistencia, df_taller, dateBrigade)
    
    # Send data to the API
    payload = json.dumps(asistencia)
    # Remove the print when the API runs
    print(payload)
    
    
    # Uncomment when the API runs
    #access_token = 'Your_token'
    #header = {
    #  'Authorization': 'Bearer ' + access_token
    #}
    
    #response = requests.post('API_url', data=payload, headers=header)
    #print(response.json())