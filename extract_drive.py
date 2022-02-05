from Google import Create_Service
import pandas as pd
from io import StringIO
import numpy as np

def extraer():
    CLIENT_SECRET_FILE = 'client_secret_dash_demo.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    sheet_id = ''
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    byteData = service.files().export_media(
        fileId=sheet_id,
        mimeType='text/csv'
    ).execute()
    
    sheet_id2=''

    byteData2 = service.files().export_media(
        fileId=sheet_id2,
        mimeType='text/csv'
    ).execute()

    byte_to_string = str(byteData,'utf-8')
    data = StringIO(byte_to_string)
    finanzas=pd.read_csv(data)
    finanzas.replace(r'\.', '', inplace=True, regex=True)
    finanzas.replace(r'\,', '.', inplace=True, regex=True)
    
    finanzas['RUC'] = finanzas['RUC'].astype(str)
    finanzas['CAJA_VN'] = finanzas['CAJA_VN'].astype(float)
    finanzas['INV'] = finanzas['INV'].astype(float)
    finanzas['ACTIVO_CORRIENTE'] = finanzas['ACTIVO_CORRIENTE'].astype(float)
    finanzas['ACTIVO_NO_CORRIENTE'] = finanzas['ACTIVO_NO_CORRIENTE'].astype(float)
    finanzas['PASIVO_CORRIENTE'] = finanzas['PASIVO_CORRIENTE'].astype(float)
    finanzas['CAPITAL'] = finanzas['CAPITAL'].astype(float)
    finanzas['ACTIVO_TOTAL'] = finanzas['ACTIVO_TOTAL'].astype(float)
    finanzas['PASIVO_TOTAL'] = finanzas['PASIVO_TOTAL'].astype(float)
    finanzas['PATRIMONIO_TOTAL'] = finanzas['PATRIMONIO_TOTAL'].astype(float)
    finanzas['U_NETA'] = finanzas['U_NETA'].astype(float)
    
    finanzas['Ratio_Liquidez'] = finanzas['ACTIVO_CORRIENTE'] / finanzas['PASIVO_CORRIENTE']
    finanzas['Prueba_Acida'] = (finanzas['ACTIVO_CORRIENTE'] - finanzas['INV']) / finanzas['PASIVO_CORRIENTE']
    finanzas['Ratio_Solvencia'] = finanzas['ACTIVO_TOTAL'] / finanzas['PASIVO_TOTAL']
    finanzas['Ratio_Endeudamiento'] = finanzas['PASIVO_TOTAL'] / finanzas['PATRIMONIO_TOTAL']
    finanzas['ROE'] = finanzas['U_NETA'] / finanzas['PATRIMONIO_TOTAL']
    finanzas['Ratio_Liquidez'] = finanzas['Ratio_Liquidez'].round(2)
    finanzas['Prueba_Acida'] = finanzas['Prueba_Acida'].round(2)
    finanzas['Ratio_Solvencia'] = finanzas['Ratio_Solvencia'].round(2)
    finanzas['Ratio_Endeudamiento'] = finanzas['Ratio_Endeudamiento'].round(2)
    finanzas['ROE'] = finanzas['ROE'].round(2)
    finanzas = finanzas.fillna('Falta Información')

    byte_to_string2 = str(byteData2,'utf-8')
    data2 = StringIO(byte_to_string2)
    credito=pd.read_csv(data2)
    credito['RUC'] = credito['RUC'].astype(str)
    

    return finanzas, credito

