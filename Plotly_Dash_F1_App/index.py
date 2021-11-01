# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 05:49:28 2021

@author: guibd
"""

# In[ ] :

import os
from path_ import app_path

app_p = app_path()

path = app_p # set your own path where is located all app files
os.chdir(path) 

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from home import create_page_home
os.chdir(path) 

from current_season import create_current_season
os.chdir(path) 

from circuits import create_circuits
os.chdir(path) 

from previous_seasons import create_previous_seasons
os.chdir(path) 

from extra import create_extra
os.chdir(path) 

from telemetry import create_telemetry
os.chdir(path)

from app import app
os.chdir(path) #changing current working directory to load csvs


server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/current_season':
        return create_current_season()
    if pathname == '/circuits':
        return create_circuits()
    if pathname =='/previous_seasons':
        return create_previous_seasons()
    if pathname =='/extra':
        return create_extra()
    if pathname =='/telemetry':
        return create_telemetry()
    else:
        return create_page_home()

if __name__ == '__main__':
    app.run_server()

