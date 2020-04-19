import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import pymongo
import dns
import json
import dash_bootstrap_components as dbc
from yahoofinancials import YahooFinancials
import quandl 
import pyfolio as pf    
import chart_studio.plotly as py    
import plotly.graph_objs as go    
import plotly    
import plotly.io as pio    
from plotly import tools
import backtrader as bt
from ib_insync import *
import datetime
import base64
import io
from PIL import Image
import urllib
import requests
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
import pandas as pd
import os
import re

# util.startLoop()


df_theme = pd.read_csv('UNGC_SDG_antonyms - March12.csv', encoding = 'utf-8')
feature = df_theme.columns.values.tolist()
feature.remove('Unnamed: 0')
df_theme = df_theme.dropna()

# set the color of the wordcloud gray-ish to make the entire dash harmonic
def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())



filePath = r"SDG outliers_specific (no rank)_results"
files = os.listdir(filePath)
# files.remove('.DS_Store')

SDG_info = []
update_SDG_info = []
company = []
date = []
SDG = []
for i in files:
    path = 'SDG outliers_specific (no rank)_results/' + i
    if os.path.isdir(path):
        inf = os.listdir(path)
        SDG_info.extend(inf)
for i  in SDG_info:
    if 'pdf' in i:
        update_SDG_info.append(i)
pattern = r'^(.*)\s+\((\d+.*)\).*(\d{4}-\d{2}-\d{2})\.\w+'
for string in update_SDG_info:
    info = re.findall(pattern, string)
    company.append(info[0][0])
    date.append(info[0][2])
    SDG.append(info[0][1])

out_result = pd.DataFrame({'SDG_number':SDG,
                         'Company_name':company,
                         'Date':date})

date = sorted(set(date))
company = sorted(set(company))
# set color for different parts
colors = {'background': '#111111', 'text': '#7FDBFF','button':'#FFFF00'}

app = dash.Dash()
server = app.server
#app.css.append_css({'remove'})
app.layout = html.Div(
    children = [
        html.H1(children = 'Wordcloud of SDG Keywords', style = {'color' : colors['text'],
                                                                 'width' : '50%', 
                                                                 'display': 'inline-block',
                                                                 'margin-top': 10,
                                                                 'margin-left': 10}),
        html.Img(
                src = 'https://images.squarespace-cdn.com/content/5c036cd54eddec1d4ff1c1eb/1557908564936-YSBRPFCGYV2CE43OHI7F/GlobalAI_logo.jpg?content-type=image%2Fpng',
                style = {
                    'height': '4.4%',
                    'width': '11%',
                    'float': 'right',
                    'margin-top': 20,
                    'margin-right': 20,
                    'display': 'inline-block' 
                }),
        html.Br(),
        html.Div([
            html.H6('Select an SDG to visualize its keywords', 
                    style = {'color': '#9999FF'}),
            # dropdown
            dcc.Dropdown(
                id = 'SDGnumber',
                options = [{'label':i, 'value':i} for i in feature],
                # value = '1. No Poverty' # next row sets the initial value showed in the dropdown box null
                searchable = False,
                # set the initial text
                placeholder = "Please select a feature"
                # set height
                #optionHeight = 40
            )
        ], style = {"width": "30%",'margin-left': 10,'display': 'inline-block'}),
         html.Div([
            html.H6('Also select a company name please', 
                    style = {'color': '#9999FF'}),
            # dropdown
            dcc.Dropdown(
                id = 'company_name',
                options = [{'label':i, 'value':i} for i in company],
                # value = '1. No Poverty' # next row sets the initial value showed in the dropdown box null
                searchable = False,
                # set the initial text
                placeholder = "Please select a feature"
                # set height
                #optionHeight = 40
            )
        ], style = {"width": "30%",'margin-left': 10,'display': 'inline-block'}),
        html.Div([
            html.H6('Also select a date please', 
                    style = {'color': '#9999FF'}),
            # dropdown
            dcc.Dropdown(
                id = 'date',
                options = [{'label':i, 'value':i} for i in date],
                # value = '1. No Poverty' # next row sets the initial value showed in the dropdown box null
                searchable = False,
                # set the initial text
                placeholder = "Please select a feature"
                # set height
                #optionHeight = 40
            )
        ], style = {"width": "30%",'margin-left': 10,'display': 'inline-block'}),
        
        html.Br(),
        html.Br(),
        html.Br(),
        # graph
        html.Div(id="graph-container", children=[
            html.H6('Visualized Results:', style={'color': colors['text'],
                                                  'margin-left': 10,
                                                  'width': '30%'}),
            html.Div(html.Img(id='Graph', style={}), style={
                'margin-left': 300, 'margin-right': 10}),
            html.Div(dcc.Graph(id='urlTable')),
            html.Div(dcc.Graph(id='timeTable'))], style={'display':'block'})
    ], style={'backgroundColor': colors['background'], 'height': '100vh'})
image_dir = 'images/'
csv_dir = 'SDG outliers_specific (no rank)_results/'


@app.callback(
    Output('graph-container', 'style'),
    [Input('SDGnumber', 'value'), Input('company_name', 'value'), Input('date', 'value')])
def hide_graph(SDG_number, company_name, date):
    filename = image_dir+f'{SDG_number}_{company_name}_{date}.png'
    if os.path.exists(filename):
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('Graph', 'src'),
    [Input('SDGnumber', 'value'), Input('company_name', 'value'), Input('date', 'value')])
def update_graph(SDG_number, company_name, date):
    return encode_image(image_dir+f'{SDG_number}_{company_name}_{date}.png')


@app.callback(
    Output('urlTable', 'figure'),
    [Input('SDGnumber', 'value'), Input('company_name', 'value'), Input('date', 'value')])
def update_table(SDG_number, company_name, date):
    SDG_number = re.findall("\d+", SDG_number)[0]
    SDG_dir = csv_dir + "SDG"+str(SDG_number)+" result(unranked)/"
    file_names = os.listdir(SDG_dir)
    p_url = re.compile(company_name+r'\ all\ url.+\.csv')
    url_filename = [s for s in file_names if p_url.match(s)][0]
    url_df = pd.read_csv(SDG_dir+url_filename)
    data = go.Table(
        header=dict(values=['Link'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=url_df.T.iloc[1:],  # 2nd column
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left'))
    layout = go.Layout(plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'], title=dict(text='Url Link',
                                                                      font=dict(color='white')), height=600)
    return {"data": [data], "layout": layout}


@app.callback(
    Output('timeTable', 'figure'),
    [Input('SDGnumber', 'value'), Input('company_name', 'value'), Input('date', 'value')])
def update_table(SDG_number, company_name, date):
    SDG_number = re.findall("\d+", SDG_number)[0]
    SDG_dir = csv_dir + "SDG"+str(SDG_number)+" result(unranked)/"
    file_names = os.listdir(SDG_dir)
    p_time = re.compile(company_name+r'\ time.+\.csv')

    time_filename = [s for s in file_names if p_time.match(s)][0]
    time_df = pd.read_csv(SDG_dir+time_filename)
    data = go.Table(
        header=dict(values=['Index', 'Company', 'Date', 'SDG'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=time_df.T,  # 2nd column
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left'))
    layout = go.Layout(plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'], title=dict(text='Time Series',
                                                                      font=dict(color='white')), height=600)
    return {"data": [data], "layout": layout}


if __name__ == '__main__':
    app.run_server()