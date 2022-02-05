import json
import pandas as pd
import fasttext
from main import main
from spanish_word_freq import SpanishWordFreq
import numpy as np
import string
import re
from io import StringIO


filePath = "CREA_total.TXT"
spanishWords = SpanishWordFreq(filePath)

clases_catalyze_dict = {
    "__label__0":"MANUFACTURA",
    "__label__1":"COMERCIO",
    "__label__2":"AGRICULTURA, GANADERIA, CAZA, SILVICULTURA Y PESCA",
    "__label__3":"CONSTRUCCION",
    "__label__4":"AGUA Y ELECTRICIDAD",
    "__label__5":"ADMINISTRACION PUBLICA Y DEFENSA",
    "__label__6":"TRANSPORTE",
    "__label__7":"ALOJAMIENTO Y RESTAURANTES",
    "__label__8":"AMBIENTE",
    "__label__9":"TELECOMUNICACIONES Y SERVICIOS DE INFORMACION",
    "__label__10":"TURISMO",
    "__label__11":"OTROS SERVICIOS",
    "__label__12":"EXTRACCION DE MINERALES"
}

clases_dict_11 = {
"__label__0":"TRANSPORTE",
"__label__1":"INSUMOS DE PRIMERA NECESIDAD",
"__label__2":"INSUMOS/SERVICIOS AGROPECUARIOS O VETERINARIOS",
"__label__3":"INFRAESTRUCTURA",
"__label__4":"COMBUSTIBLE E INSUMOS QUIMICOS",
"__label__5":"MATERIALES, EQUIPOS Y/O VEHICULOS",
"__label__6":"SEGUROS",
"__label__7":"ACTIVIDADES ADMINISTRATIVAS",
"__label__8":"LIMPIEZA Y SEGURIDAD",
"__label__9":"INSUMOS/SERVICIOS DE SALUD",
"__label__10":"INSUMOS/SERVICIOS EDUCATIVOS",
}

MONTHS = [
    'Ene',
    'Feb',
    'Mar',
    'Abr',
    'May',
    'Jun',
    'Jul',
    'Ago',
    'Sep',
    'Oct',
    'Nov',
    'Dic'
]

years = ['2020', '2021']

def create_dates(years):
    STANDAR = []
    for i in years:
        for k in reversed(MONTHS):
            STANDAR.append('{} {}'.format(k, i))
    return STANDAR


class Json():
    def __init__(self, name):
        self.name = name

    def org_data_equifax(self):
        STANDAR = create_dates(years)
        eq = json.load(open('{}[Equifax].json'.format(self.name), encoding='utf8'))
        ruc = eq['number_id']
        try:
            if eq['debt']['historic_debt'] is not {} and bool(eq['debt']['historic_debt']):
                deuda = pd.DataFrame(eq['debt']['historic_debt']['values'], columns = eq['debt']['historic_debt']['columns'])
                deuda = deuda[deuda['period'].isin(STANDAR)]
                del(deuda['percent'])
                deuda.replace(',', '', regex=True, inplace=True)
                deuda['calificacion'] = deuda.apply(lambda x:
                                                    -1 if x['type_calification'] == 'SCAL' else (0 if x['type_calification'] == 'PER'
                                                                                                 else (1 if x['type_calification'] == 'DUD'
                                                                                                       else (2 if x['type_calification'] == 'DEF'
                                                                                                             else(3 if x['type_calification'] == 'CPP'
                                                                                                                  else (4 if x['type_calification'] == 'NOR' else -1))))), axis=1)
                del(deuda['type_calification'])
                deuda.replace('debt_situation_','', regex=True, inplace=True)
                deuda=deuda.iloc[::-1]
                deuda = deuda.replace('-',0)
                deuda['debt_situation_day'] = deuda['debt_situation_day'].astype(int)
                deuda['debt_situation_delay'] = deuda['debt_situation_delay'].astype(int)
                deuda['debt_situation_judicial'] = deuda['debt_situation_judicial'].astype(int)
                deuda['debt_situation_punish'] = deuda['debt_situation_punish'].astype(int)
            else:
                deuda = pd.DataFrame([['Ene 2021',0,0,0,0,0,0,0,0,0]],columns=["period","type_calification","percent","number_entities","debt_situation_day","debt_situation_delay","debt_situation_judicial","debt_situation_total","debt_situation_punish","days_delay"])
                del(deuda['percent'])
                del(deuda['type_calification'])
        except:
            deuda = pd.DataFrame([['Ene 2021',0,0,0,0,0,0,0,0,0]],columns=["period","type_calification","percent","number_entities","debt_situation_day","debt_situation_delay","debt_situation_judicial","debt_situation_total","debt_situation_punish","days_delay"])
            del(deuda['percent'])
            del(deuda['type_calification'])

        return deuda

    def org_data_gobpe(self):
        gob = json.load(open('{}[Gobpe].json'.format(self.name), encoding='utf8'))
        try:
            if gob['contratacionesT01'] is not {} and bool(gob['contratacionesT01']):
                contrataciones = pd.DataFrame(gob['contratacionesT01'])
                contrataciones = contrataciones[['desCatObj2', 'desContProv', 'nomEntCont', 'montoOrigen', 'fecBaseCont']]
                contrataciones.columns=['Tipo', 'Descripción', 'Entidad', 'Monto', 'Fecha']
                split = contrataciones.apply(lambda x: x['Fecha'].split('-'), axis=1).tolist()
                split = pd.DataFrame(split, columns=['Año','Mes1','Día'])
                del(split['Día'])
                CONTRATACIONES = pd.concat([contrataciones, split], axis=1)
                CONTRATACIONES['Mes'] = CONTRATACIONES.apply(lambda x: 'Enero' if x['Mes1'] =='01' else ('Febrero' if x['Mes1'] =='02' else ('Marzo' if x['Mes1'] =='03' else ('Abril' if x['Mes1'] =='04' else ('Mayo' if x['Mes1'] =='05' else ('Junio' if x['Mes1'] =='06' else ('Julio' if x['Mes1'] =='07' else ('Agosto' if x['Mes1'] =='08' else('Setiembre' if x['Mes1'] =='09' else ('Octubre' if x['Mes1'] =='10' else ('Noviembre' if x['Mes1'] =='11' else ('Diciembre' if x['Mes1'] =='12' else 'Nada'))))))))))), axis=1)
                CONTRATACIONES2 = CONTRATACIONES.groupby(['Año', 'Mes1','Mes']).sum().reset_index()
                CONTRATACIONES2['Año'] = CONTRATACIONES2['Año'].astype(int)
                CONTRATACIONES2 = CONTRATACIONES2[CONTRATACIONES2['Año'] > 2016]
            else:
                CONTRATACIONES = pd.DataFrame([['-', '-', '-', '-', '-', '-', '-', '-']], columns=['Tipo', 'Descripción', 'Entidad', 'Monto', 'Fecha', 'Año', 'Mes1', 'Mes'])
            entidades = CONTRATACIONES.groupby(['Año','Entidad']).sum().reset_index()
            entidades = entidades.iloc[::-1]
        except:
            CONTRATACIONES = pd.DataFrame([['-', '-', '-', '-', '-', '-', '-', '-']], columns=['Tipo', 'Descripción', 'Entidad', 'Monto', 'Fecha', 'Año', 'Mes1', 'Mes'])
            entidades = CONTRATACIONES.groupby(['Año','Entidad']).sum().reset_index()
            entidades = entidades.iloc[::-1]
        try:
            if gob['estadisticaT01']['seccionSancionF01']['sancionesT01'] is not {} and bool(gob['estadisticaT01']['seccionSancionF01']['sancionesT01']):
                sanciones = pd.DataFrame(gob['estadisticaT01']['seccionSancionF01']['sancionesT01'])
                sanciones = sanciones[['numInhab', 'fechaIni', 'descripcion', 'motivos']]
                sanciones['motivos'] = sanciones['motivos'].apply(lambda x: ', '.join(x))
                fecha_sanc = sanciones.apply(lambda x: x['fechaIni'].split('/'), axis=1).tolist()
                fecha_sanc = pd.DataFrame(fecha_sanc, columns=['Día', 'Mes', 'Año'])
                fecha_sanc = fecha_sanc[['Año', 'Mes']]
                sanciones = pd.concat([sanciones, fecha_sanc], axis=1)
                sanciones = sanciones[['numInhab', 'Año', 'Mes','descripcion', 'motivos']]
                sanciones.columns = ['Sanción', 'Año', 'Mes','Descripcion', 'Motivos']
            else:
                sanciones = pd.DataFrame([['0000000', '-', '-','-','-']], columns=['Sanción', 'Año', 'Mes','Descripcion', 'Motivos'])
        except:
            sanciones = pd.DataFrame([['0000000', '-', '-','-','-']], columns=['Sanción', 'Año', 'Mes','Descripcion', 'Motivos'])

        try:
            if gob['estadisticaT01']['seccionPenalidadF01']['penalidadesT01'] is not {} and bool(gob['estadisticaT01']['seccionPenalidadF01']['penalidadesT01']):
                penalidades = pd.DataFrame(gob['estadisticaT01']['seccionPenalidadF01']['penalidadesT01'])
                penalidades = penalidades[['id', 'fecha', 'causal','montoTexto']]
                fecha_pen = penalidades.apply(lambda x: x['fecha'].split('/'), axis=1).tolist()
                fecha_pen = pd.DataFrame(fecha_pen, columns=['Día', 'Mes', 'Año'])
                fecha_pen = fecha_pen[['Año', 'Mes']]
                penalidades = pd.concat([penalidades, fecha_pen], axis=1)
                penalidades = penalidades[['id', 'Año', 'Mes', 'causal','montoTexto']]
                penalidades.columns = ['Penalidad', 'Año', 'Mes', 'Motivo','Monto']
            else:
                penalidades = pd.DataFrame([['00000','-','-','-','0']], columns=['Penalidad', 'Año', 'Mes', 'Motivo','Monto'])
        except:
            penalidades = pd.DataFrame([['00000','-','-','-','0']], columns=['Penalidad', 'Año', 'Mes', 'Motivo','Monto'])

        return sanciones, penalidades


    def org_data_seace(self, model):
        ubigeos = pd.read_excel('')
        ubigeos['RUC'] = ubigeos['RUC'].astype(str)  #Para el mapa

        seace = json.load(open('{}[Seace].json'.format(self.name), encoding='utf8'))
        try:
            if seace['awarding'] is not {} and bool(seace['awarding']):
                contratos = pd.DataFrame(seace['awarding']['rows'], columns=seace['awarding']['cols'])
                contratos = contratos[['ruc entidad', 'entidad','fechabuenapro', 'descripcionitem', 'objetocontractual','montoadjudicadosoles']]
                contratos.columns = ['Ruc_entidad','Entidad', 'Fecha', 'Descripción', 'Tipo', 'Monto']
                contratos['Ruc_entidad'] = contratos['Ruc_entidad'].astype(str)
                contratos['Monto'] = contratos['Monto'].astype(int)
            else:
                contratos = pd.DataFrame([['','','','','',0]], columns=['Ruc_entidad','Entidad', 'Fecha', 'Descripción', 'Tipo', 'Monto'])
        except:
            contratos = pd.DataFrame([['','','','','',0]], columns=['Ruc_entidad','Entidad', 'Fecha', 'Descripción', 'Tipo', 'Monto'])

        try:
            if seace['order'] is not {} and bool(seace['order']):
                ordenes = pd.DataFrame(seace['order']['rows'], columns=seace['order']['cols'])
                ordenes = ordenes[['ruc entidad', 'entidad','fecha emision', 'descripcion orden', 'objeto contractual','monto']]
                ordenes.columns = ['Ruc_entidad','Entidad', 'Fecha', 'Descripción', 'Tipo','Monto']
                ordenes['Monto'] = ordenes['Monto'].astype(int)
                ordenes['Ruc_entidad'] = ordenes['Ruc_entidad'].astype(str)
            else:
                ordenes = pd.DataFrame([['','','','','',0]], columns=['Ruc_entidad','Entidad', 'Fecha', 'Descripción', 'Tipo','Monto'])    
        except:
            ordenes = pd.DataFrame([['','','','','',0]], columns=['Ruc_entidad','Entidad', 'Fecha', 'Descripción', 'Tipo','Monto'])

        contratos = pd.concat([contratos, ordenes], axis=0)
        entidades = pd.read_excel('', '')
        entidades = entidades[['ruc_contratante', 'Sector', 'entidad_contratante']]
        entidades['ruc_contratante'] = entidades['ruc_contratante'].astype(str)
        entidades_sanc = pd.read_excel('')
        entidades_sanc['RUC'] = entidades_sanc['RUC'].astype(str)
        ENT = contratos['Ruc_entidad'].unique().tolist()
        ES = entidades_sanc[entidades_sanc['RUC'].isin(ENT)].reset_index()
        if ES.empty:
            ES = pd.DataFrame([['-', '-', '-', '-', '-', '-', '-']], columns=['Entidad', 'Ubigeo', 'Inicio', 'Fin', 'Plazo', 'Sanción', 'Resolución'])
        else:
            ES = ES[['Entidad', 'Ubigeo', 'Inicio', 'Fin', 'Plazo', 'Sanción', 'Resolución']]
            ES['Inicio'] = ES['Inicio'].astype(str).str[0:7]
            ES['Fin'] = ES['Fin'].astype(str).str[0:7]

        

        final = pd.merge(contratos, entidades, left_on='Ruc_entidad', right_on='ruc_contratante')
        final = pd.merge(final, ubigeos, left_on='Ruc_entidad', right_on='RUC')
        del (final['ruc_contratante'])
        del (final['RUC'])

        split = final.apply(lambda x: x['Fecha'].split('-'), axis=1).tolist()
        split = pd.DataFrame(split, columns=['Año', 'Mes1', 'Día'])
        del (split['Día'])

        final = pd.concat([split, final], axis=1)
        final['Mes'] = final.apply(lambda x: 'Enero' if x['Mes1'] =='01' else ('Febrero' if x['Mes1'] =='02' else ('Marzo' if x['Mes1'] =='03' else ('Abril' if x['Mes1'] =='04' else ('Mayo' if x['Mes1'] =='05' else ('Junio' if x['Mes1'] =='06' else ('Julio' if x['Mes1'] =='07' else ('Agosto' if x['Mes1'] =='08' else('Setiembre' if x['Mes1'] =='09' else ('Octubre' if x['Mes1'] =='10' else ('Noviembre' if x['Mes1'] =='11' else ('Diciembre' if x['Mes1'] =='12' else 'Nada'))))))))))), axis=1)
        final['Año'] = final['Año'].astype(int)
        final = final[final['Año']>2016].sort_values(by=['Año', 'Mes1'], ascending=False)
        _D = final[['Año', 'Descripción']]
        _D['Descripción'] = _D['Descripción'].str.lower()
        _D['Desc'] = _D['Descripción'].apply(lambda x: main(x.split(), spanishWords))
        _D['SE'] = _D['Desc'].apply(lambda x: clases_dict_11[model.predict(x)[0][0]])
        _D_ = _D.groupby(['SE']).agg('count').reset_index() #Si se quiere por año, ponerlo antes de Clase en la lista del groupby
        _D_ = _D_[['SE', 'Desc']].sort_values('Desc', ascending = False).reset_index()
        
        
        a = ['2017','2018','2019','2020', '2021'] ## ACTUALIZAR A MEDIDA QUE PASE EL TIEMPO
        final2 = final.groupby(['Año']).sum().reset_index()
        final2['Año'] = final2['Año'].astype(str)
        presentes = final2['Año'].unique().tolist()
        faltantes = np.setdiff1d(a, presentes)
        for i in range(len(faltantes)):
            final2.loc[len(final2)] = [faltantes[i], 0, 0]        

        final3 = final.groupby(['Región']).count().reset_index()
        final3['Recuento'] = final3['Mes']  #No importa la columna, todas son iguales
        final3 = final3[['Región','Recuento']]

        final4 = final
        final4['Año'] = final4['Año'].astype(str)
        final4 = final4.pivot_table('Monto', ['entidad_contratante'], 'Año').reset_index()
        final4.fillna(0, inplace=True)
        final4['Total'] = final4.sum(axis=1)
        final4 = final4.round(0)
        f= [column for column in final4.columns if column in a]
        faltantes = np.setdiff1d(a, f)
        for faltante in faltantes:
            final4[faltante] = float(0)
        final4 = final4[['entidad_contratante',a[0], a[1], a[2], a[3], a[4], 'Total']]
        return final2, final, final3, final4, _D_, ES

# ejemplo = Json('20601831440')
# print(ejemplo.org_data_seace(model2)[0])



def inversionistas():
    inv = pd.read_excel('', '')
    inv.columns = ['ID', 'CLIENTE', 'MONTO', 'INTERES', 'MONTO_A_DEVOLVER', 'FONDO', 'MES', 'MES1','DURACION', 'FECHA_CANCELAR', 'RETRASO', 'ESTADO']
    inv['RETRASO'] = inv.apply(lambda x: 0 if int(x['RETRASO']) < 0 else int(x['RETRASO']), axis=1)
    inv2 = inv.groupby(['MES', 'MES1']).count().reset_index()
    inv2['MONTO_A_DEVOLVER'] = inv2['MONTO_A_DEVOLVER'].astype(int)
    inv2 = inv2.sort_values(by=['MES1'], ascending=True)
    del (inv2['ID'])
    return inv2

