# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 05:58:22 2021

@author: guibd
"""

import dash_html_components as html
from navbar import create_navbar
import dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_core_components as dcc
from app import app
from master import data_importation
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

nav = create_navbar()

header = html.H3('previous seasons')

data = data_importation()

df_circuits = data['circuits'][['circuitId','country']]
df_races = data['races'][['year','circuitId','raceId','round','name']]
df_races = df_races.rename(columns={'round':'round_nb'})
df_drivers = data['drivers'][['driverId','driverRef','forename','surname','nationality','url']]
df_drivers = df_drivers.rename(columns = {'nationality':"driver_nationality",'url':'driver_url'}) 

merge_tb1 = pd.merge(df_circuits,df_races,how='inner',on='circuitId')
merge_tb1 = merge_tb1.sort_values(by=['raceId'])

# merge table 2 : results and constructors 

merge_tb2 = pd.merge(data['results'], data['constructors'], how='inner', on ='constructorId' )

# adding drivers in merg_tb2
# first we need to rename variables with the same name which doesn't return the same data in both tables 

merge_tb2 = merge_tb2.rename(columns = {
    'name' :'constructor_name', 'nationality':'constructor_nationality',
    'url':'constructor_url'})

merge_tb2 = merge_tb2.drop(['time','milliseconds','fastestLap','fastestLapSpeed','fastestLapTime','rank','number','laps','position','positionText'],axis=1)

# create the GP_summary df

GP_summary = pd.merge(merge_tb2,df_drivers, how='inner',on='driverId')

# addings status 

GP_summary = pd.merge(GP_summary,data['status'],how='inner',on='statusId')

# adding GP name 

GP_summary = pd.merge(GP_summary,df_races,how='inner',on='raceId')

# droping URLs columns for lisibility and total data size 

GP_summary = GP_summary.drop(['constructor_url','driver_url'], axis = 1)
GP_summary['Drivers'] = (GP_summary['forename'] +[' '] +GP_summary['surname']).apply(str)

data['results']["win_Y_N"] = (data['results']["positionOrder"] == 1 ).astype(int)
GP_summary = pd.merge(GP_summary, data['results'][['resultId','win_Y_N']], how = 'inner', on='resultId')
GP_summary = GP_summary.rename(columns={'win_Y_N': 'race_won'})
GP_summary["name"]= GP_summary["name"].str.replace('Grand Prix', "GP")


sub_df = GP_summary[['Drivers','points','name','round_nb','year']]
groups = sub_df.groupby(['Drivers','year'])['points'].apply(list).apply(np.cumsum)
groups = groups.reset_index(name ='points_earned')


championship_graph = html.Div([
    
    html.Div([
        
        html.Label(['Driver Championship Overview']),
        
    dcc.Dropdown(id="dropdown1",
        
        options = [
                        {'label' : 2021,  'value': 2021},
                        {'label' : 2020,  'value': 2020},
                        {'label' : 2019,  'value': 2019},
                        {'label' : 2018,  'value': 2018},
                        {'label' : 2017,  'value': 2017},
                        {'label' : 2016,  'value': 2016},
                        {'label' : 2015,  'value': 2015},
                        {'label' : 2014,  'value': 2014},
                        {'label' : 2013,  'value': 2013},
                        {'label' : 2012,  'value': 2012},
                        {'label' : 2011,  'value': 2011},
                        {'label' : 2010,  'value': 2010},
                        {'label' : 2009,  'value': 2009},
                        {'label' : 2008,  'value': 2008},
                        {'label' : 2007,  'value': 2007},
                        {'label' : 2006,  'value': 2006},
                        {'label' : 2005,  'value': 2005},
                        {'label' : 2004,  'value': 2004},
                        {'label' : 2003,  'value': 2003},
                        {'label' : 2002,  'value': 2002},
                        {'label' : 2001,  'value': 2001},
                        {'label' : 2000,  'value': 2000},

                     
            ],
        
        optionHeight=35,
        value = 2021,
        multi = False, 
        searchable = True,
        style={'width':'50%'}
                 
                 ),
        
        ]),
    
    dbc.Col(
                dcc.Graph(id='graph1'),
                width = 12,
                style={'width': '200vh', 'height': '90vh'},
  
                
            
)
    
])
        

def create_previous_seasons():
    layout = html.Div([
        nav,
        header,
        championship_graph
    ])
    return layout

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='dropdown1', component_property='value')]
)

def drivers_points_per_round(dropdown1):
    
    list_of_race = list(GP_summary[GP_summary['year']==dropdown1].name.unique())
    
    sub_df_1 = groups[groups['year']==dropdown1]

    fig = go.Figure()


    for i in sub_df_1.index:
    
        fig.add_trace(go.Scatter
                      (x=list_of_race,
                                 y = sub_df_1['points_earned'].loc[i],
                                 name = sub_df_1['Drivers'].loc[i],
                                 mode ='lines+markers',
                                 marker = dict(size = 10,
                                               line = dict(width = 2)),
                                 line = dict(width = 5))
                      ),
        fig.update_layout(hovermode="x")


    return fig
