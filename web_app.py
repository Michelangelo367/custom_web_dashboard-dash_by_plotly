"""
Avinash Pasupulate
avinash.pasupulate@gmail.com
14th December 2018

Creating interface for searching through IT transaction records
"""

#importing required packages
import os
import dash
import copy
import time
import urllib.parse
import dash_table
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event

#importing css stylesheet through cdn
external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

#creating application for the interface
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)


app.layout = html.Div(
    [
        html.Div(
            html.H1(children='Transaction Query Tool'),
            style={'padding-bottom': '10px', 'color': '#1d3d3d', 'font-weight': 'bold',
                   'height': '100px', 'text-align': 'center'},
        ),

        html.Div(
            html.P('Please enter a search query:'),
            style={'font-weight': 'bold', 'width': '20%', 'display': 'inline-block', 'padding-right': '5px'}),

        html.Div(
            dcc.Input(
                id='search_input',
                placeholder='Enter search key',
                type='Text',
                value='California'
            ),
            style={'width': '20%', 'color': '#1d3d3d', 'display': 'inline-block', 'padding-right': '10px'}),

        html.Div(
            html.Button("Submit", id='search_btn1', n_clicks=0),
            style={'background-color': 'white', 'display': 'inline-block',
                   'color': '#ffffff', 'border-radius': '25px', 'border': 'none'}),

        html.Div(
            dash_table.DataTable(
                id='test_div',
                columns=[{"name": i, 'id': i} for i in df.columns],
                filtering_settings=''
            ),
            style={'padding-top': '100px'}
        ),

        html.Div(
            html.Button("Export to CSV", id='search_btn2', n_clicks=0),
            style={'text-align': 'center', 'padding-top': '50px', 'border-radius': '25px',
                   'justify-content': 'center'})
    ],
    style={'background-color': '#FFFDF1', 'padding': '50px', 'border-radius': '10px'}
)


@app.callback(
   Output('test_div', 'data'),
   [],
   [State('search_input', 'value')],
   [Event('search_btn1', 'click')]
)
def out_table(value):
    dff = df.loc[df.State == value]
    return dff.to_dict('rows')


'''
@app.callback(
   Output('search_btn2', 'n_clicks'),
   [Input('search_input', 'value')]
)
def download_table(value):
    dff = df.loc[df.State == value]
    csv_string = dff.to_csv('table_data.csv', index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string
'''


if __name__ == '__main__':
    app.run_server(debug=True)
