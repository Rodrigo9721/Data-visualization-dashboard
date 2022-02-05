import os
import pandas as pd
import numpy as np
import pickle
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_daq as daq
import json
import platform
from transform_json import Json
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import geopandas as gpd
import pathlib
import xgboost as xgb
import fasttext
from extract_drive import extraer

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

COORDS = gpd.read_file('peru_departamental_simple.geojson')
model1 = pickle.load(open('', 'rb'))
model2 = pickle.load(open('', 'rb'))
model3 = pickle.load(open('', 'rb'))
# model_cat = fasttext.load_model("model_catalyze.bin")
model_11 = fasttext.load_model("")

base_mensual = pd.read_csv('Mensual.csv', sep=',')
contratos = base_mensual[[]]

sanciones = pd.read_csv('Sanciones.csv', sep=',')
sanciones = sanciones[[]]

credito1 = base_mensual[[]] #utiliza la misma base de datos

finanzas = extraer()[0]
cred = extraer()[1]

CG_LOGO = ''

fig_base = go.Figure(data=[
        go.Bar(name='Al Día', x=['Setiembre', 'Octubre','Noviembre', 'Diciembre'], y=[250,250,250,250], marker_color='lightsteelblue'),
        go.Bar(name='Retrasada', x=['Setiembre', 'Octubre','Noviembre', 'Diciembre'], y=[250,250,250,250], marker_color='steelblue'),
        go.Bar(name='Castigada', x=['Setiembre', 'Octubre','Noviembre', 'Diciembre'], y=[250,250,250,250], marker_color='royalblue'),
        go.Bar(name='Judicial', x=['Setiembre', 'Octubre','Noviembre', 'Diciembre'], y=[250,250,250,250], marker_color='#162752'),
       ],
        layout=go.Layout(
        title={'text':'<b>Deuda en el Sistema Financiero Reportada en Equifax</b>', 'xanchor':'center','yanchor':'top', 'x':0.5},
        barmode='stack',
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend={'font':{'color':'black'}},
        font_color='black',
        yaxis=dict(title='Deuda en S/.')
        ))
fig_base2 = go.Figure(data=[
        go.Bar(name='2017', x=['2017'], y=[200],
           marker_color='lightsteelblue'),
        go.Bar(name='2018', x=['2018'], y=[400],
           marker_color='steelblue'),
        go.Bar(name='2019', x=['2019'], y=[600],
           marker_color='royalblue'),
        go.Bar(name='2020', x=['2020'], y=[800],
           marker_color='#162752'),
        go.Bar(name='2021', x=['2021'], y=[1000],
            marker_color='#24346B')
       ],
        layout=go.Layout(
        title={'text':'<b>Historial de Contrataciones</b>', 'xanchor':'center','yanchor':'top', 'x':0.5},
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend={'font':{'color':'black'}},
        font_color='black',
        yaxis=dict(title='Monto en S/.')
        ))

tabla_base= go.Figure(data=[go.Table(
         header=dict(values=['Sector','Tipo', '2017', '2018', '2019', '2020','2021', 'Total'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=15)),
         cells=dict(values=['','','', '', '', '', '', ''],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=15)),
)])
tabla_base.update_layout((
         dict(paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)'
              ))
          )

tabla_finanzas_base = go.Figure(data=[go.Table(
         header=dict(values=['RUC','Año', 'Ratio de Liquidez', 'Prueba Ácida', 'Ratio de Solvencia', 'Ratio de Endeudamiento','ROE'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=15)),
         cells=dict(values=['','','', '', '', '', ''],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=15)),
)])
tabla_finanzas_base.update_layout((
         dict(paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)'
              ))
          )

tabla_credito_base = go.Figure(data=[go.Table(
         header=dict(values=['RUC','Código del Prestamo', 'Linea de Crédito', 'Monto Total del Contrato','Monto del Crédito', 'Monto a Devolver', 'Duración en Días','Cantidad de Cuotas', 'Entidad Contratante','Monto Cobrado', 'Fecha Fin del Contrato', 'Fecha de Devolución','Estatus'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=12)),
         cells=dict(values=['','','', '', '', '', '', '', '', '', '', '',''],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=12)),
)])
tabla_credito_base.update_layout((
         dict(paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)'
              ))
          )

tabla_sanciones = go.Figure(data=[go.Table(
         header=dict(values=['Sanción', 'Año', 'Mes','Descripcion', 'Motivos'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=15)),
         cells=dict(values=['','','', '', ''],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=15)),
)])
tabla_sanciones.update_layout((
         dict(paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)'
              ))
          )

tabla_pen = go.Figure(data=[go.Table(
         header=dict(values=['Penalidad', 'Año', 'Mes', 'Motivo','Monto'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=15)),
         cells=dict(values=['','','', '', ''],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=15)),
)])
tabla_pen.update_layout((
         dict(paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)'
              ))
          )

donut = go.Figure(data=[go.Pie(labels=['Clase 1', 'Clase 2', 'Clase 3', 'Clase 4', 'Clase 5','Otros'], values = [100/6,100/6,100/6,100/6,100/6,100/6], hole=.3)])

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Insertar RUC", id='my-input', value='', debounce=True,
                          n_submit=0, minLength='11', maxLength='11')),
        dbc.Col(
            dbc.Button("Buscar", color="secondary", className="button", n_clicks=0, id='Button'),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=CG_LOGO, height="50px")),
                ],
                align="left",
                no_gutters=True
            ),
            href="",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse([
                dbc.Nav([dbc.NavItem(
                    dbc.NavLink("Inicio",
                                href="/")),
                    dbc.NavItem(dbc.NavLink("Proveedores",
                                href="/dash-proveedor", disabled=True)),
                    #dbc.NavItem(dbc.NavLink("Comité de Crédito",
                    #            href="/comite-credito")),
                    #dbc.NavItem(dbc.NavLink("Inversionistas",
                    #            href="/inversionistas")),
                ]),
                search_bar],
                id="navbar-collapse", navbar=True, className='nav-links'),
    ],
    color='#162752', className='shadow-4'
)

geo_df_base = COORDS.set_index('NOMBDEP')
geo_df_base['Recuento'] = range(1,26)
mapa_base = px.choropleth(geo_df_base,
                    geojson=geo_df_base.geometry,
                    locations=geo_df_base.index,
                    color=geo_df_base.Recuento,
                    color_continuous_scale='Blues'
                    )
mapa_base.update_geos(fitbounds="locations", visible=False)
mapa_base.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)',
                    geo_bgcolor='rgba(0,0,0,0)')


tabla_ES = go.Figure(data=[go.Table(
         header=dict(values=['Entidad', 'Ubigeo', 'Inicio', 'Fin', 'Plazo', 'Sanción', 'Resolución'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=15)),
         cells=dict(values=['-', '-', '-', '-', '-', '-', '-'],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=15)),
)])
tabla_ES.update_layout((
         dict(paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)'
              ))
          )


def create_layout(app):
    return html.Div([
            navbar,
            html.Br(),
            dbc.Spinner(html.Div(id='spinner'), color='#162752', type='grow'),
            html.Br(),
            html.P('Historial con Credigob', style={'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'center', "border":"1px grey solid", 'font':{'color':'black', 'size':'25'}, 'font-weight': 'bold'}, className='shadow-5'),
            dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id='contrato', figure=tabla_credito_base)], style={'margin-left':'auto', 'margin-right':'auto', "border":"0.5px grey solid", 'width':'5'}, className='shadow-5'))]),
            html.Br(),
            html.P(id='my-output', children='', style={'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'center', "border":"1px grey solid", 'font':{'color':'black', 'size':'20'}, 'font-weight': 'bold'}, className='shadow-5'),
            dbc.Row([
                dbc.Col(html.Div(children=[daq.Gauge(id='Graph1',color={'gradient': 'True',"ranges": {'green': [0, 25], "yellow": [25, 50], "orange": [50, 75], 'red': [75, 100]}},showCurrentValue=True,value=50,label='Probabilidad de Sanción (%)',max=100,min=0),
                                           html.Div([dbc.Row([dbc.Col([html.Span(className='dot muybueno',
                                                                               style={ "border":"0.5px grey solid"})], width={'offset':1}),
                                                            dbc.Col([html.P('Muy Bueno')]),
                                                            dbc.Col([html.Span(className='dot bueno',
                                                                               style={"border": "0.5px grey solid"})], width={'offset':1}),
                                                            dbc.Col([html.P('Bueno')]),
                                                            dbc.Col([html.Span(className='dot regular',
                                                                               style={"border": "0.5px grey solid"})], width={'offset':1}),
                                                            dbc.Col([html.P('Regular')]),
                                                            dbc.Col([html.Span(className='dot riesgoso',
                                                                               style={"border": "0.5px grey solid"})], width={'offset':1}),
                                                            dbc.Col([html.P('Riesgoso')]),
                                                            ]),
                                                    dbc.Row([dbc.Col([html.Ul(id='List1', children=[html.Li(id='Resumen1', style={'font-weight':'normal'})])], width={"size": 8, "offset": 2})])])
                                                            ],style={ "border":"0.5px grey solid", 'margin-left':'auto', 'margin-right':'auto', 'font-weight': 'bold'}, className='shadow-5')),
                dbc.Col(html.Div(children=[daq.Gauge(id='Graph2',color={'gradient': 'True',"ranges": {'green': [0, 10], "yellow": [10, 20], "orange": [20, 30], 'red': [30, 100]}},showCurrentValue=True,value=50,label='Días de Retraso Estimados',max=100,min=0),
                                           html.Div([dbc.Row([dbc.Col([html.Span(className='dot muybueno',
                                                                                style={"border": "0.5px grey solid"})], width={'offset':1}),
                                                             dbc.Col([html.P('Muy Bueno')]),
                                                             dbc.Col([html.Span(className='dot bueno',
                                                                                style={"border": "0.5px grey solid"})], width={'offset':1}),
                                                             dbc.Col([html.P('Bueno')]),
                                                             dbc.Col([html.Span(className='dot regular',
                                                                                style={"border": "0.5px grey solid"})], width={'offset':1}),
                                                             dbc.Col([html.P('Regular')]),
                                                             dbc.Col([html.Span(className='dot riesgoso',
                                                                                style={"border": "0.5px grey solid"})], width={'offset':1}),
                                                             dbc.Col([html.P('Riesgoso')]),
                                                             ]),
                                                    dbc.Row([dbc.Col([html.Ul(id='List2', children=[html.Li(id='Resumen2', style={'font-weight':'normal'})])], width={"size": 8, "offset": 2})])])
                                                           ],style={ "border":"0.5px grey solid", 'margin-left':'auto', 'margin-right':'auto', 'font-weight': 'bold'}, className='shadow-5'))
                    ]),
            html.Br(),
            html.P('Finanzas de la Empresa',
               style={'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'center', "border": "1px grey solid",
                      'font': {'color': 'black'}, 'font-weight': 'bold', 'font-size': '20px'}, className='shadow-5'),
            dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id='finanzas', figure=tabla_finanzas_base)], style={'margin-left':'auto', 'margin-right':'auto', "border":"0.5px grey solid", 'width':'5'}, className='shadow-5'))]),
            html.Br(),
            dbc.Row([
            dbc.Col(html.Div(children=[dcc.Graph(id='Equifax', figure=fig_base)], style={'margin-left':'auto', 'margin-right':'auto'}))], style={"border":"0.5px grey solid"}, className='shadow-5'),
            html.Br(),
            dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id='Gobpe',figure=fig_base2)], style={'margin-left':'auto', 'margin-right':'auto'}))], style={"border":"0.5px grey solid"}, className='shadow-5'),
            html.Br(),
            html.P('Historial de Sanciones y Penalidades',
               style={'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'center', "border": "1px grey solid",
                      'font': {'color': 'black'}, 'font-weight': 'bold', 'font-size': '20px'}, className='shadow-5'),
            dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id='Tabla_Sanciones',figure=tabla_sanciones)], style={'margin-left':'auto', 'margin-right':'auto', "border":"0.5px grey solid", 'width':'5'}, className='shadow-5')),
                     dbc.Col(html.Div(children=[dcc.Graph(id='Tabla_Penalidades',figure=tabla_pen)], style={'margin-left':'auto', 'margin-right':'auto', "border":"0.5px grey solid", 'width':'5'}, className='shadow-5'))]),
            html.Br(),
            html.P('Detalles de Contrataciones',
               style={'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'center', "border": "1px grey solid",
                      'font': {'color': 'black'}, 'font-weight': 'bold', 'font-size': '20px'}, className='shadow-5'),
            # dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id='Tabla_Gobpe',figure=tabla_base)], style={'margin-left':'auto', 'margin-right':'auto', "border":"0.5px grey solid", 'width':'5'}, className='shadow-5')),
            #         dbc.Col(html.Div(children=[dcc.Graph(id='Mapa',figure=mapa_base)], style={'margin-left':'auto', 'margin-right':'auto', "border":"0.5px grey solid", 'width':'5'}, className='shadow-5'))
            #          ]),
            dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id='Donut_Seace', figure=donut)],
                                  style={'margin-left': 'auto', 'margin-right': 'auto', "border": "0.5px grey solid",
                                         'width': '5'}, className='shadow-5')),
                    dbc.Col(html.Div(children=[dcc.Graph(id='Mapa', figure=mapa_base)],
                                  style={'margin-left': 'auto', 'margin-right': 'auto', "border": "0.5px grey solid",
                                         'width': '5'}, className='shadow-5'))
                    ]),
            html.Br(),
            dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id='Tabla_Gobpe',figure=tabla_base)], style={'margin-left':'auto', 'margin-right':'auto', "border":"0.5px grey solid", 'width':'5'}, className='shadow-5'))]),
            html.Br(),
            html.P('Sanciones de las Entidades Contratantes',
               style={'margin-left': 'auto', 'margin-right': 'auto', 'text-align': 'center', "border": "1px grey solid",
                      'font': {'color': 'black'}, 'font-weight': 'bold', 'font-size': '20px'}, className='shadow-5'),
            dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id='Tabla_ES',figure=tabla_ES)], style={'margin-left':'auto', 'margin-right':'auto', "border":"0.5px grey solid", 'width':'5'}, className='shadow-5'))]),
            ])



def update_output_div(input_value, n_clicks, n_submit):  # 1 input -> 1 argumento
    global contratos
    global sanciones
    global credito1
    global finanzas
    global cred

    if len(input_value) == 1 and n_clicks + n_submit == 0:
        return 'Esperando RUC', 50, 50, fig_base, fig_base2, tabla_base, mapa_base, '', '', '', tabla_sanciones, tabla_pen , donut, tabla_ES, tabla_finanzas_base, tabla_credito_base
    elif len(input_value) == 11 and n_clicks + n_submit > 0:
        ruc = input_value

        # RUCS1 = contratos['RUC']
        # contratos_gr = model1.predict(contratos.iloc[:, 1:])
        # contratos_gr = pd.DataFrame([RUCS1,contratos_gr])
        contratos_c = contratos[contratos['RUC'] == int(ruc)]
        predecir_contratos = contratos_c.iloc[:, 1:]
        prediction1 = model1.predict(predecir_contratos)
        if int(prediction1) > 0:
            output1 = int(float(round(prediction1[0], 0)))
        else:
            output1 = 0

        # RUCS2 = sanciones['RUC']
        # sanciones_gr = model2.predict(sanciones.iloc[:, 1:])
        # sanciones_gr = pd.DataFrame([RUCS2, sanciones_gr])
        sanciones_c = sanciones[sanciones['RUC'] == int(ruc)]
        predecir_sanciones = sanciones_c.iloc[:, 1:]
        prediction2 = model2.predict_proba(predecir_sanciones)[:, 1]
        try:
            output2 = round(prediction2[0] * 100, 2)
        except:
            output2 = 0

        # RUCS3 = credito1['RUC']
        # credito1_gr = model3.predict(credito1.iloc[:, 1:])
        # credito1_gr = pd.DataFrame([RUCS3, credito1_gr])
        credito1_c = credito1[credito1['RUC'] == int(ruc)]
        predecir_credito1 = credito1_c.iloc[:, 1:]
        prediction3 = model3.predict(predecir_credito1)
        if int(prediction3) > 0:
            output3 = int(float(round(prediction3[0], 0)))
        else:
            output3 = 0

        # RUCS4 = credito2['RUC']
        # credito2_gr = model4.predict(credito2.iloc[:, 1:])
        # credito2_gr = pd.DataFrame([RUCS3, credito2_gr])
        # credito2_c = credito2[credito2['RUC'] == int(ruc)]
        # predecir_credito2 = credito2_c.iloc[:, 1:]
        # prediction4 = model4.predict_proba(predecir_credito2)[:, 1]
        # output4 = round(prediction4[0] * 100, 2)

        equifax = Json(ruc).org_data_equifax()

        fig = go.Figure(data=[
            go.Bar(name='Al Día', x=equifax['period'], y=equifax['debt_situation_day'],
                   marker_color='lightsteelblue'),
            go.Bar(name='Retrasada', x=equifax['period'], y=equifax['debt_situation_delay'],
                   marker_color='steelblue'),
            go.Bar(name='Castigada', x=equifax['period'], y=equifax['debt_situation_judicial'],
                   marker_color='royalblue'),
            go.Bar(name='Judicial', x=equifax['period'], y=equifax['debt_situation_punish'],
                   marker_color='#162752'),
        ],
            layout=go.Layout(
                title={'text': '<b>Deuda en el Sistema Financiero Reportada en Equifax (soles)', 'xanchor': 'center', 'yanchor': 'top', 'x': 0.5},
                barmode='stack',
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend={'font': {'color': 'black'}},
                font_color='black'
            ))

        SC = Json(ruc).org_data_seace(model_11)
        seace = SC[0]
        fig2 = go.Figure(data=[
            go.Bar(name='2017', x=seace['Año'][seace['Año'] == '2017'], y=seace['Monto'][seace['Año'] == '2017'],
                   marker_color='lightsteelblue'),
            go.Bar(name='2018', x=seace['Año'][seace['Año'] == '2018'], y=seace['Monto'][seace['Año'] == '2018'],
                   marker_color='steelblue'),
            go.Bar(name='2019', x=seace['Año'][seace['Año'] == '2019'], y=seace['Monto'][seace['Año'] == '2019'],
                   marker_color='royalblue'),
            go.Bar(name='2020', x=seace['Año'][seace['Año'] == '2020'], y=seace['Monto'][seace['Año'] == '2020'],
                   marker_color='#162752'),
            go.Bar(name='2021', x=seace['Año'][seace['Año'] == '2021'], y=seace['Monto'][seace['Año'] == '2021'],
                   marker_color='#24346B'),
        ],
            layout=go.Layout(
                title={'text': '<b>Monto Anual de las Contrataciones (soles)', 'xanchor': 'center', 'yanchor': 'top', 'x': 0.5},
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend={'font': {'color': 'black'}},
                font_color='black',
                font=dict(
                    color='black',
                    size=10)
            ))
        fig2.update_xaxes(tickangle = 0)

        tabla_gp = SC[3]
        tabla_gp_ = go.Figure(data=[go.Table(columnwidth = [200,80,80,80,80,80,80,80],
            header=dict(values=['Entidad', '2017', '2018', '2019', '2020', '2021', 'Total'],
                        fill_color='#162752',
                        align='left',
                        font=dict(color='white', size=15)),
            cells=dict(values=[tabla_gp['entidad_contratante'], tabla_gp['2017'], tabla_gp['2018'], tabla_gp['2019'], tabla_gp['2020'], tabla_gp['2021'],
                               tabla_gp['Total']],
                       fill_color='lightsteelblue',
                       align='left',
                       font=dict(color='black', size=15),
                       height=30
                       )
        )])

        tabla_gp_.update_layout((
            dict(paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)',

                 )),
                 title_text = '<b>Historial de Contrataciones',
            legend_font_size = 10,
            title = {'y':0.9,
                     'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'}
        )

        datos_mapa = SC[2]
        geo = COORDS.merge(datos_mapa, how='left', left_on='NOMBDEP', right_on='Región').set_index('NOMBDEP')
        geo.replace(np.nan, 0, inplace=True)
        geo['Recuento'] = geo['Recuento'].astype(int)
        del (geo['Región'])

        mapa = px.choropleth(geo,
                             geojson=geo.geometry,
                             locations=geo.index,
                             color=geo.Recuento,
                             color_continuous_scale='Blues'
                             )
        mapa.update_geos(fitbounds="locations", visible=False)
        mapa.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, paper_bgcolor='rgba(0,0,0,0)',
                    geo_bgcolor='rgba(0,0,0,0)',
                    title_text = '<b>Ubicación Geográfica de las Contrataciones',
                    title = {'y':0.95,
                     'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})

        G = Json(ruc).org_data_gobpe()
        Sanc = G[0]
        Pen = G[1]

        tabla_sanc_ = go.Figure(data=[go.Table(
                                             header=dict(
                                                 values=['Sanción', 'Año', 'Mes','Descripcion', 'Motivos'],
                                                 fill_color='#162752',
                                                 align='left',
                                                 font=dict(color='white', size=15)),
                                             cells=dict(values=[Sanc['Sanción'], Sanc['Año'], Sanc['Mes'], Sanc['Descripcion'], Sanc['Motivos']],
                                                        fill_color='lightsteelblue',
                                                        align='left',
                                                        font=dict(color='black', size=15),
                                                        height=30
                                                        )
                                             )])

        tabla_sanc_.update_layout((
            dict(paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)',

                 ))
        )

        tabla_pen_ = go.Figure(data=[go.Table(
            header=dict(
                values=['Penalidad', 'Año', 'Mes', 'Motivo','Monto'],
                fill_color='#162752',
                align='left',
                font=dict(color='white', size=15)),
            cells=dict(values=[Pen['Penalidad'], Pen['Año'], Pen['Mes'], Pen['Motivo'], Pen['Monto']],
                       fill_color='lightsteelblue',
                       align='left',
                       font=dict(color='black', size=15),
                       height=30
                       )
        )])

        tabla_pen_.update_layout((
            dict(paper_bgcolor='rgba(0,0,0,0)',
                 plot_bgcolor='rgba(0,0,0,0)',

                 ))
        )

        clases_c = SC[4]
        donut_clases = go.Figure(data=[go.Pie(labels=clases_c['SE'], values = clases_c['Desc'], hole=.3)])
        donut_clases.update_layout(
            title_text = '<b>Objeto de los Contratos',
            legend_font_size = 10,
            title = {'y':0.9,
                     'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'}
        )

        ES = SC[5]

        tabla_ES_ = go.Figure(data=[go.Table(columnwidth = [200,80,60,60,80,60,160],
         header=dict(values=['Entidad', 'Ubigeo', 'Inicio', 'Fin', 'Plazo', 'Sanción', 'Resolución'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=15)),
         cells=dict(values=[ES['Entidad'], ES['Ubigeo'], ES['Inicio'], ES['Fin'], ES['Plazo'], ES['Sanción'], ES['Resolución']],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=15),
                    height=30)
        )])
        tabla_ES_.update_layout((
         dict(paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)'
              ))
          )

        finanzas_c = finanzas[finanzas['RUC'] == ruc]
        if finanzas_c.empty:
            finanzas_c = pd.DataFrame([[ruc, '2021', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información']], columns=['RUC', 'YEAR', 'Ratio_Liquidez', 'Prueba_Acida', 'Ratio_Solvencia', 'Ratio_Endeudamiento', 'ROE'])
            tabla_finanzas = go.Figure(data=[go.Table(
             header=dict(values=['RUC','Año', 'Ratio de Liquidez', 'Prueba Ácida', 'Ratio de Solvencia', 'Ratio de Endeudamiento','ROE'],
                         fill_color='#162752',
                         align='left',
                         font=dict(color='white', size=15)),
             cells=dict(values=[finanzas_c['RUC'], finanzas_c['YEAR'], finanzas_c['Ratio_Liquidez'], finanzas_c['Prueba_Acida'], finanzas_c['Ratio_Solvencia'], finanzas_c['Ratio_Endeudamiento'], finanzas_c['ROE']],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=15),
                    height=30)
                    )])
            tabla_finanzas.update_layout((
                    dict(paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                    ))
                     )
        else:
            tabla_finanzas = go.Figure(data=[go.Table(
             header=dict(values=['RUC','Año', 'Ratio de Liquidez', 'Prueba Ácida', 'Ratio de Solvencia', 'Ratio de Endeudamiento','ROE'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=15)),
            cells=dict(values=[finanzas_c['RUC'], finanzas_c['YEAR'], finanzas_c['Ratio_Liquidez'], finanzas_c['Prueba_Acida'], finanzas_c['Ratio_Solvencia'], finanzas_c['Ratio_Endeudamiento'], finanzas_c['ROE']],
                fill_color='lightsteelblue',
                align='left',
                font=dict(color='black', size=15),
                height=30)
                )])
            tabla_finanzas.update_layout((
                dict(paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
                ))
                 )
        
        cred_c = cred[cred['RUC']==ruc]
        if cred_c.empty:
            cred_c = pd.DataFrame([[ruc, 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información', 'Sin Información']], columns=['RUC','Código del Prestamo', 'Linea de Crédito', 'Monto Total del Contrato','Monto del Crédito', 'Monto a Devolver', 'Duración en Días','Cantidad de Cuotas', 'Entidad Contratante','Monto Cobrado', 'Fecha Fin del Contrato', 'Fecha de Devolución','Estatus'])
            tabla_credito = go.Figure(data=[go.Table(
                header=dict(values=['RUC','Código del Prestamo', 'Linea de Crédito', 'Monto Total del Contrato','Monto del Crédito', 'Monto a Devolver', 'Duración en Días','Cantidad de Cuotas', 'Entidad Contratante','Monto Cobrado', 'Fecha Fin del Contrato', 'Fecha de Devolución','Estatus'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=11)),
                cells=dict(values=[cred_c['RUC'], cred_c['Código del Prestamo'], cred_c['Linea de Crédito'], cred_c['Monto Total del Contrato'],cred_c['Monto del Crédito'], cred_c['Monto a Devolver'], cred_c['Duración en Días'],cred_c['Cantidad de Cuotas'], cred_c['Entidad Contratante'], cred_c['Monto Cobrado'], cred_c['Fecha Fin del Contrato'], cred_c['Fecha de Devolución'],cred_c['Estatus']],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=12),
                    height=30),
                )])
            tabla_credito.update_layout((
                dict(paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
                ))
            )
        else:
            tabla_credito = go.Figure(data=[go.Table(
                header=dict(values=['RUC','Código del Prestamo', 'Linea de Crédito', 'Monto Total del Contrato','Monto del Crédito', 'Monto a Devolver', 'Duración en Días','Cantidad de Cuotas', 'Entidad Contratante','Monto Cobrado', 'Fecha Fin del Contrato', 'Fecha de Devolución','Estatus'],
                     fill_color='#162752',
                     align='left',
                     font=dict(color='white', size=11)),
                cells=dict(values=[cred_c['RUC'], cred_c['PRESTAMO'], cred_c['LINEA_DE_CREDITO'], cred_c['MONTO_ADJUDICADO'],cred_c['MONTO_TOTAL_DEL_CONTRATO'], cred_c['MONTO_A_DEVOLVER'], cred_c['DURACION'],cred_c['CANTIDAD_DE_COUTAS'], cred_c['ENTIDAD_CONTRATANTE'], cred_c['MONTO_FINAL_COBRADO'], cred_c['FECHA_FIN_CONTRATO_1'], cred_c['FECHA_DEVOLUCION'],cred_c['ESTATUS_SOLICITUD']],
                    fill_color='lightsteelblue',
                    align='left',
                    font=dict(color='black', size=12),
                    height=30),
                )])
            tabla_credito.update_layout((
                dict(paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
                ))
            )


        return 'Se espera que el proveedor {} contrate {} veces con el Estado el próximo mes.\n\n\n'.format(ruc,
                                                                                             output1), output2, output3, fig, fig2, tabla_gp_, mapa, '',\
                                                                                            'Dado el comportamiento previo del proveedor, se estima que podría incurrir en {} días de retraso en un crédito durante el presente mes aproximadamente'.format(output3), 'Basándonos en su historial como proveedor, estimamos una probabilidad del {}% de sanción durante el presente año'.format(output2), tabla_sanc_, tabla_pen_, donut_clases, tabla_ES_, tabla_finanzas, tabla_credito
    else:
        return 'Esperando RUC', 50, 50, fig_base, fig_base2, tabla_base, mapa_base, '', '','', tabla_sanciones, tabla_pen , donut, tabla_ES, tabla_finanzas_base, tabla_credito_base
