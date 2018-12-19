import os
import dash
import dash_table
import urllib.parse
import pandas as pd
from io import StringIO
import dash_core_components as dcc
import dash_html_components as html
from jellyfish import metaphone as mtp
from dash.dependencies import Input, Output
from jellyfish import damerau_levenshtein_distance as dl_dist

cwd = os.getcwd()
external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

PSIZE = 10
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)

app.layout = html.Div(
    children=[
                    html.Div(
                        html.H1(children='Transaction Query Tool'),
                        style={'padding-bottom': '5px', 'color': '#1d3d3d', 'font-weight': 'bold',
                               'height': '100px', 'text-align': 'center'},
                    ),

                    html.Div(
                        html.P(children='please use "eq<<space>>" as a prefix for filter searches'),
                        style={'padding': '5px', 'color': '#1d3d3d', 'font-weight': 'bold',
                               'text-align': 'left', 'font-size': '12px'},
                    ),

                    html.Div(
                        html.A(
                            html.Button("Export to CSV", id='search_btn2', n_clicks=0),
                            id='download-link',
                            download="rawdata.csv",
                            href="",
                            target="_blank"),
                        style={'text-align': 'center', 'padding-top': '10px', 'border-radius': '25px',
                               'justify-content': 'center', 'font_weight': 'bold'}),

                    html.Div(
                        id="row_num",
                        style={'textAlign': 'right', 'padding_top': '50px'},
                    ),

                    html.Div(
                        id='load',
                    ),

                    html.Div(
                        dash_table.DataTable(
                            id='test_div',
                            columns=[{"name": i, 'id': i} for i in df.columns],
                            filtering_settings='',
                            filtering='be',
                            pagination_settings={'current_page': 0, 'page_size': PSIZE},
                            pagination_mode='be',
                            style_header={'backgroundColor': '#1d3d3d', 'color': 'white',
                                          'font_weight': 'bold', 'textAlign': 'center'},
                            style_cell={'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal',
                                        'textAlign': 'left', 'backgroundColor': '#efefef'},
                        ),
                        style={'padding-top': '5px'}
                    ),
                ],
    style={'background-color': '#FFFDF1', 'padding': '50px', 'border-radius': '10px'})


def generate_table(filtering_settings):
    filtering_expression = filtering_settings.split(' && ')
    dff = df
    for i in filtering_expression:
        if 'eq' in i:
            value = i.split(' eq ')[1].lower()
            column_name = i.split(' eq ')[0]
            dff = dff.astype(str)
            dff = dff.loc[dff[column_name].str.split(" ").apply(
                lambda x: any([int(dl_dist(mtp(value), mtp(j))) <= 1 for j in x]))]
    return dff


@app.callback(
   Output('test_div', 'data'),
   [Input('test_div', 'filtering_settings'),
    Input('test_div', 'pagination_settings')]
)
def out_table(filtering_settings, pagination_settings):
    dff = generate_table(filtering_settings)
    return dff.iloc[pagination_settings['current_page']*pagination_settings['page_size']:
                    (pagination_settings['current_page']+1)*pagination_settings['page_size']].to_dict('rows')


@app.callback(
    Output('download-link', 'href'),
    [Input('test_div', 'filtering_settings')]
)
def download_table(filtering_settings):
    dff = generate_table(filtering_settings)
    dff.to_csv(StringIO(), index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + urllib.parse.quote(StringIO().getvalue())
    return csv_string


@app.callback(
    Output('row_num', 'children'),
    [Input('test_div', 'filtering_settings')],
)
def r_count(filtering_settings):
    dff = generate_table(filtering_settings)
    return html.Div([dcc.Markdown('''Total rows loaded: {}'''.format(len(dff)))])


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})


if __name__ == '__main__':
    app.run_server(debug=True)
