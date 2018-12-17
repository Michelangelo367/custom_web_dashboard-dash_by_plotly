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
import jellyfish as j
import dash_table
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import dash_table_experiments as dt

# importing css stylesheet through cdn
external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# creating application for the interface
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)


app.layout = html.Div(
    [
        html.Div(
            html.H1(children='Transaction Query Tool'),
            style={'padding-bottom': '5px', 'color': '#1d3d3d', 'font-weight': 'bold',
                   'height': '100px', 'text-align': 'center'},
        ),

        html.Div(
            html.Button("Export to CSV", id='search_btn2', n_clicks=0),
            style={'text-align': 'center', 'padding-top': '10px', 'border-radius': '25px',
                   'justify-content': 'center'}),

        html.Div(
            dash_table.DataTable(
                id='test_div',
                columns=[{"name": i, 'id': i} for i in df.columns],
                filtering_settings='',
                filtering='be'
            ),
            style={'padding-top': '50px'}
        ),

    ],
    style={'background-color': '#FFFDF1', 'padding': '50px', 'border-radius': '10px'}
)


@app.callback(
   Output('test_div', 'data'),
   [Input('test_div', 'filtering_settings')]
)
def out_table(filtering_settings):
    filtering_expression = filtering_settings.split(' && ')
    dff = df.head(20)
    for i in filtering_expression:
        if 'eq' in i:
            value = i.split(' eq ')[1].lower()
            column_name = i.split(' eq ')[0]
            dff = dff.loc[dff[column_name].apply(lambda x: int(j.damerau_levenshtein_distance(j.metaphone(value)
                                                                                              , j.metaphone(x))) <= 1)]
    return dff.to_dict('rows')


'''
#for csv export

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
