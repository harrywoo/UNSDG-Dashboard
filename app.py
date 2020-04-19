import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go    
import plotly
import datetime

sdg = pd.read_csv('data/data_2020.csv', index_col=0)
sdg = sdg.reset_index()
# sdg = pd.read_csv('data/data_rated_SDG.csv', index_col=0)
sdg['date'] = pd.to_datetime(sdg['date'])
# year = sdg['date'].dt.year
# sdg = sdg[year>2019]

company = sdg['COMPANY'].unique()
MA_7day = ['MA_7day_1', 'MA_7day_2', 'MA_7day_3', 'MA_7day_4', 'MA_7day_5',
       'MA_7day_6', 'MA_7day_7', 'MA_7day_8', 'MA_7day_9', 'MA_7day_10',
       'MA_7day_11', 'MA_7day_12', 'MA_7day_13', 'MA_7day_14', 'MA_7day_15',
       'MA_7day_16', 'MA_7day_17']
MA_60day = ['MA_60day_1', 'MA_60day_2',
       'MA_60day_3', 'MA_60day_4', 'MA_60day_5', 'MA_60day_6', 'MA_60day_7',
       'MA_60day_8', 'MA_60day_9', 'MA_60day_10', 'MA_60day_11', 'MA_60day_12',
       'MA_60day_13', 'MA_60day_14', 'MA_60day_15', 'MA_60day_16',
       'MA_60day_17']
SDG_std = ['SDG_1_std', 'SDG_2_std',
       'SDG_3_std', 'SDG_4_std', 'SDG_5_std', 'SDG_6_std', 'SDG_7_std',
       'SDG_8_std', 'SDG_9_std', 'SDG_10_std', 'SDG_11_std', 'SDG_12_std',
       'SDG_13_std', 'SDG_14_std', 'SDG_15_std', 'SDG_16_std', 'SDG_17_std']
SDG_count = ['SDG_1_count', 'SDG_2_count', 'SDG_3_count',
       'SDG_4_count', 'SDG_5_count', 'SDG_6_count', 'SDG_7_count',
       'SDG_8_count', 'SDG_9_count', 'SDG_10_count', 'SDG_11_count',
       'SDG_12_count', 'SDG_13_count', 'SDG_14_count', 'SDG_15_count',
       'SDG_16_count', 'SDG_17_count']

MA_type = ['MA_7day','MA_60day']

sdg_type = ['SDG_1', 'SDG_2', 'SDG_3', 'SDG_4', 'SDG_5', 'SDG_6', 'SDG_7', 'SDG_8', 'SDG_9',
            'SDG_10', 'SDG_11', 'SDG_12', 'SDG_13', 'SDG_14', 'SDG_15', 'SDG_16', 'SDG_17']

data_type = ["SDG", "MA", "STD", "COUNTS"]
data_type_dict = {"SDG":sdg_type, "MA":MA_60day, "STD":SDG_std, "COUNTS":SDG_count}

first_day = sdg.groupby("Ticker").first()["date"].value_counts().index[0]
last_day = sdg.groupby("Ticker").last()["date"].value_counts().index[0]

start_date = last_day - datetime.timedelta(days=30)
end_date = last_day
date_list = sdg[sdg["Ticker"]==sdg.loc[0]["Ticker"]]["date"]
date_dict = date_list.to_dict()
date_str_dict = date_list.dt.date.map(str).to_dict()
date_length = len(date_dict)-1

for index, value in date_str_dict.items():
    if index not in [0, int(date_length/2), date_length]:
        date_str_dict[index] = ""
# date_str_dict

colors = {'background': '#111111', 'text': '#7FDBFF','button':'#FFFF00'}
app = dash.Dash()
server = app.server
app.layout = html.Div([
        html.Br(),
        html.Br(),
        # header and logo
        html.Div([
            html.H1('SDG Time Series', className = 'ten columns', style = {'margin-top': 10,'margin-left': 15, 'color': colors['text']}),

            html.Img(
                src = 'https://images.squarespace-cdn.com/content/5c036cd54eddec1d4ff1c1eb/1557908564936-YSBRPFCGYV2CE43OHI7F/GlobalAI_logo.jpg?content-type=image%2Fpng',
                style = {
                    'height': '11%',
                    'width': '11%',
                    'float': 'right',
                    'position': 'relative',
                    'margin-top': 11,
                    'margin-right': 0
                },
                className = 'two columns'        
            )  
        ], className = 'row'),

        html.Br(),
        html.Br(),
        html.Br(),
        
    
        # select the company 
        html.Div([
            html.H3('Select the company:', style={'paddingRight':'30px','color': '#9999FF'}),
            dcc.Dropdown(
            id = 'company',
            options = [{'label':i, 'value':i} for i in company],
            value = 'apple inc'
            )
        ], style={"width": "25%"}),
        
        # select the type of MA you want to see
        html.Div([
            html.H3('Select the data type:', style={'paddingRight':'30px','color': '#9999FF'}),
            dcc.Dropdown(
            id = 'data_type',
            options = [{'label':i, 'value':i} for i in data_type],
            value = data_type[0]
            )
        ], style={"width": "25%"}),
        
        # select time range of MA time series
        html.Div([
            html.H3('Select the time zone:', style={'paddingRight':'30px','color': '#9999FF'}),
            dcc.Slider(id="current_date", min=0, max=date_length, value=date_length,
                                 marks=date_str_dict)],style={"width": "50%"}),
    
        # Scatter chart
        html.Div([
             html.H3('Time series of MA_sdg you selected', style={'paddingRight':'30px','color': colors['text']}),
        html.Div([
                dcc.Graph(id = 'scatter')
            ], className = 'twelve columns'),
        ], className = 'row',style={"height" : '50vh', "width" : "70%",'margin-left': 0, 
                                    'margin-right': 0,'margin-top':0,'margin-bottom':0}),
        html.Br(), 
        # Histogram chart
        html.Div([
             html.H3('Distribution of SDG you selected', style={'paddingRight':'30px','color': colors['text']}),
        html.Div([
                dcc.Graph(id = 'histogram')
            ], className = 'twelve columns'),
        ], className = 'row',style={"height" : '50vh', "width" : "70%",'margin-left': 0, 
                                    'margin-right': 0,'margin-top':0,'margin-bottom':0}),
        html.Br(),
        # Heatmap
        html.Div([
             html.H3('Distribution of SDG you selected', style={'paddingRight':'30px','color': colors['text']}),
        html.Div([
                dcc.Graph(id = 'heatmap')
            ], className = 'twelve columns'),
        ], className = 'row',style={"height" : '50vh', "width" : "70%",'margin-left': 0, 
                                    'margin-right': 0,'margin-top':0,'margin-bottom':0}),
        html.Br(),

],style = {'backgroundColor': colors['background']}) 
        



@app.callback(
    Output('scatter', 'figure'),
    [Input('company', 'value'), Input('data_type', 'value'), Input('current_date', 'value')])
def update_figure(company, data_type, current_date):
    df = sdg[sdg['COMPANY'] == company]

    current_date = date_dict[current_date]
#     current_date = last_day
    start_date = current_date - datetime.timedelta(days=30)

    df = df[(df["date"]>=start_date) & (df["date"]<=current_date)]
    
    trace = [go.Scatter(x=df["date"], y=df[x], mode='lines',
                            marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ) for x in data_type_dict[data_type]]
    return {"data": trace,
            "layout": go.Layout(plot_bgcolor = colors['background'],
                  paper_bgcolor = colors['background'],font = {'color': colors['text']},title="Daily line chart of SDG", colorway=['#fdae61', '#abd9e9'],
                                yaxis={"title": "Rate"}, xaxis={"title": "Date"})}

@app.callback(
    Output('histogram', 'figure'),
    [Input('company', 'value'), Input('data_type', 'value'), Input('current_date', 'value')])
def update_figure(company, data_type, current_date):
    df = sdg[sdg['COMPANY'] == company]
    current_date = date_dict[current_date]

#     current_date = last_day
    start_date = current_date - datetime.timedelta(days=30)

    df = df[(df["date"]>=start_date) & (df["date"]<=current_date)]
    
    trace = [go.Histogram(x=df[x]) for x in data_type_dict[data_type]]
    return {"data": trace,
            "layout": go.Layout(plot_bgcolor = colors['background'],
                  paper_bgcolor = colors['background'],font = {'color': colors['text']},title="Daily histogram of SDG", colorway=['#fdae61', '#abd9e9'],
                                yaxis={"title": "Rate"}, xaxis={"title": "Date"})}

@app.callback(
    Output('heatmap', 'figure'),
    [Input('company', 'value'), Input('data_type', 'value'), Input('current_date', 'value')])
def update_figure(company, data_type, current_date):
    df = sdg[sdg['COMPANY'] == company]
    
    current_date = date_dict[current_date]
#     current_date = last_day
    date = current_date - datetime.timedelta(days=1)
    df = df[df["date"]==date]
    
    trace = [go.Heatmap(z=df[sdg_type])]
    return {"data": trace,
            "layout": go.Layout(plot_bgcolor = colors['background'],
                  paper_bgcolor = colors['background'],font = {'color': colors['text']},title="Daily heatmap of SDG", colorway=['#fdae61', '#abd9e9'], 
                                yaxis={"title": "Rate"}, xaxis={"title": "Date"})}

if __name__ == '__main__':
    app.run_server()