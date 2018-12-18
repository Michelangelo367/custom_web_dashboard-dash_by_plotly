"""
Avinash Pasupulate
avinash.pasupulate@gmail.com
14th December 2018

Creating interface for searching through IT transaction records
"""

#importing required packages
import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import urllib
from dash.dependencies import Input, Output, State, Event
from jellyfish import damerau_levenshtein_distance as dl_dist
from jellyfish import metaphone as mtp

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
            html.P(children='please use "eq<<space>>)" as a prefix for filter searches'),
            style={'padding': '5px', 'color': '#1d3d3d', 'font-weight': 'bold',
                   'text-align': 'left'},
        ),


        html.Div(
            html.A(
                html.Button("Export to CSV", id='search_btn2', n_clicks=0),
                id='download-link',
                download="rawdata.csv",
                href="",
                target="_blank"),
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
    dff = df
    for i in filtering_expression:
        if 'eq' in i:
            value = i.split(' eq ')[1].lower()
            column_name = i.split(' eq ')[0]
            #dff['value'] = dff['value'].astype(str)
            dff = dff.loc[dff[column_name].str.split(" ").apply(lambda x: any([int(dl_dist(mtp(value), mtp(i))) <= 1 for i in x]))]
    return dff.to_dict('rows')



#for csv export

@app.callback(
    Output('download-link', 'href'),
    [Input('test_div', 'filtering_settings')]
)
def download_table(filtering_settings):
    filtering_expression = filtering_settings.split(' && ')
    dff = df
    for i in filtering_expression:
        if 'eq' in i:
            value = i.split(' eq ')[1].lower()
            column_name = i.split(' eq ')[0]
            dff = dff.loc[dff[column_name].str.split(" ").apply(
                lambda x: any([int(dl_dist(mtp(value), mtp(i))) <= 1 for i in x]))]
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string.encode('utf-8'))
    return csv_string


if __name__ == '__main__':
    app.run_server(debug=True)
