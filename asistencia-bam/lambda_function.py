import json
from datetime import date
import boto3
import pandas as pd
import openpyxl
# import requests

s3Client = boto3.client('s3')

def appendDataToPayload(payload:list, source_df:pd.DataFrame, dateBrigade:str, rol:int ):
    # Get the rol name
    rol_name = 'Mercado' if rol == 1 else 'Colonia' if rol == 2 else 'Taller'

    # Filter by rol name
    source_df = source_df.dropna(subset=[rol_name])
    source_df = source_df.dropna(axis='columns')

    # Iterate the df
    for r in range(source_df.shape[0]):
        row = source_df.iloc[r]
        # Separate the name and the last name
        nombre_completo = row['Nombre'].split()

        # Append the data
        payload['Nombre'].append(nombre_completo[0])
        payload['Apellido'].append(nombre_completo[1])
        payload['Gen'].append(row['Gen.'])
        payload['Rol'].append(rol)
        payload['Colonia'].append(row['Colonia.1'])
        payload['Fecha'].append(dateBrigade)

def getDateBrigate(sheet: str):
    # Month dict, translate the months to your language
    month_dict = {
      'Enero': 1,
      'Febrero': 2,
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
    
    # Separate the date
    # Sheet name example: '16 de Enero'
    sheet_name = sheet.split()
    day = sheet_name[0]
    month = month_dict[sheet_name[2]]
    year = date.today().year
    # Create a date object with the date
    dateBrigade = date(year,month,int(day))
    
    # Return the date -> '2024-01-16'
    return dateBrigade.isoformat()

def lambda_handler(event, context):
    # Get bucket and file name
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Get file
    response = s3Client.get_object(Bucket=bucket, Key=key)
    file = response['Body'].read()

    # Get the excel
    xlsx = pd.ExcelFile(file)
    # Get df
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
    # 1 - Mercado, 2 - Colonia, 3 - Taller
    for rol in range(1,4):
        appendDataToPayload(asistencia, df, dateBrigade, rol)
    
    # Prepair the payload
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