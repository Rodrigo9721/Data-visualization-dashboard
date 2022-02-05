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
from pages import (
    proveedor,
    comite,
    inversionistas,
    Overview
)
from pages.proveedor import update_output_div
from pages.comite import act_grafico, act_grafico2, act_grafico3, act_grafico4,act_grafico5, update_comite_credito
from pages.inversionistas import update_inversionistas
ENTORNO = 'desarrollo' if 'windows' in platform.platform().lower() else 'production'


app = Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True
)
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")], style={'overflow-x':'hidden', 'overflow-y':'auto'}
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-proveedor":
        return proveedor.create_layout(app)
#    elif pathname == "/comite-credito":
#        return comite.create_layout(app)
#    elif pathname == "/inversionistas":
#        return inversionistas.create_layout(app)
    else:
        return Overview.create_layout(app)

@app.callback(
    [Output(component_id='my-output', component_property='children'),
     Output(component_id='Graph1', component_property='value'),
     Output(component_id='Graph2', component_property='value'),
     Output(component_id='Equifax', component_property='figure'),
     Output(component_id='Gobpe', component_property='figure'),
     Output(component_id='Tabla_Gobpe', component_property='figure'),
     Output(component_id='Mapa', component_property='figure'),
     Output(component_id='spinner', component_property='children'),
     Output(component_id='Resumen2', component_property='children'),
     Output(component_id='Resumen1', component_property='children'),
     Output(component_id='Tabla_Sanciones', component_property='figure'),
     Output(component_id='Tabla_Penalidades', component_property='figure'),
     Output(component_id='Donut_Seace', component_property='figure'),
     Output(component_id='Tabla_ES', component_property='figure'),
     Output(component_id='finanzas', component_property='figure'),
     Output(component_id='contrato', component_property='figure')
     ],
    [Input(component_id='my-input', component_property='value'),
     Input(component_id='Button', component_property='n_clicks'),
     Input(component_id='my-input', component_property='n_submit')
     ]
    )
def callback_proveedor(input_value, n_clicks, n_submit):
    return update_output_div(input_value, n_clicks, n_submit)

#@app.callback(
#    [Output('my-output2', 'children'),
#     Output('temp', 'figure'),
#     Output('temp_2', 'figure'),
#     Output('graph_linea', 'figure'),
#     Output('graph_linea2', 'figure'),
#     Output('graph_linea3', 'figure'),
#     Output('cards', 'children'),
#     Output('Bar', 'figure')],
#    [Input('my-input-user', 'value'),
#     Input('my-input-password', 'value'),
#     Input('Button2', 'n_clicks'),
#     Input('my-input-password', 'n_submit'),
#     Input('Bar', 'hoverData'),
#     Input('selector_fecha', 'start_date'),
#     Input('selector_fecha', 'end_date'),
#     Input('selector_fecha_2', 'start_date'),
#     Input('selector_fecha_2', 'end_date'),
#     Input('selector_fecha_3', 'start_date'),
#     Input('selector_fecha_3', 'end_date'),
#     ]) #poder usar las propiedades hoverData, clickData o selectedData
#def update_comite1(user, password, clicks, submits, hoverdata, fecha_min, fecha_max, fecha_min2, fecha_max2, fecha_min3, fecha_max3):
#    return update_comite_credito(user, password, clicks, submits, hoverdata, fecha_min, fecha_max, fecha_min2, fecha_max2, fecha_min3, fecha_max3)
#
#
#@app.callback([Output('my-output3', 'children'),
#               Output('my-output4', 'children'),
#               Output('Historial_Colocaciones', 'figure')],
#              [Input('my-input-user-inv', 'value'),
#               Input('my-input-password-inv', 'value'),
#               Input('my-input-password-inv', 'n_submit'),
#               Input('Button3', 'n_clicks'),])
#def callback_inversionistas(user, password, submit, clicks):
#    return update_inversionistas(user, password, submit, clicks)



PORT = int(os.environ.get("PORT", 8050))

if __name__ == '__main__':
    if (ENTORNO == 'desarrollo'):
        app.run_server(debug=True, port=PORT)
    else:
        app.run_server(debug=True, host='0.0.0.0', port=PORT)