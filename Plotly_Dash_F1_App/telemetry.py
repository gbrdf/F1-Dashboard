# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 15:05:27 2021

@author: guillaume
"""

import dash_html_components as html
from navbar import create_navbar
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app
import fastf1 as ff1
from fastf1 import plotting
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from master import data_importation
import dash_bootstrap_components as dbc

data = data_importation()

data['races'][data['races']['year']==2020][['name','round']] # list of all GP of the selected season 
    
    
race = ff1.get_session(2020,14,'R') #instead of the name of the GP you can call the round number
laps = race.load_laps(with_telemetry=True)
laps['round'] = 14 # fill round column with the same round number as above 


# getting track lenght for all the 2020 Grand Prix

df_tracks = pd.merge(data['circuits'], data['races'], how='inner', on='circuitId')
df_tracks.columns

df_tracks = df_tracks.rename(columns={'name_x':'track_name','name_y':'gp_name'})
df_tracks = df_tracks.drop(['url_x','url_y'],axis=1)

df_tracks_length = df_tracks[df_tracks['year']==2020][['round','track_name','circuitId','gp_name']]

df_tracks_length[['round','track_name','gp_name']].sort_values(by='round')

length_lst_2020 = [
    4318,
    4381,
    5891,
    4675,
    7004,
    5793,
    5245,
    5848,
    5148,
    4653,
    4909,
    5338,
    5412,
    5281
    ]

# length_test = pd.concat(df_tracks_length['round'], df_tracks_length['track_name', ]

# df_tracks_length[['track_name','round']].sort_values(by='round').track_name.unique()

length_dict = (dict(zip(df_tracks_length[['track_name','round']].sort_values(by='round').track_name.unique(), length_lst_2020)))

df_tracks_length = df_tracks_length.sort_values(by='round')

df_tracks_length['track_length'] = df_tracks_length['track_name'].map(length_dict)   

laps['track_length'] = np.nan

laps['track_length'] = np.where(laps[laps['round']==14], df_tracks_length[df_tracks_length['round']==14]['track_length'],0)

laps['LapTime'] = (laps['LapTime'] / np.timedelta64(1,'s')).apply(float)

laps['AVSpeed'] = (laps['track_length'] / laps['LapTime'] * 3.6)

laps['InPit'] = np.where(laps['PitInTime'].isnull(),0,1)
laps['OutPit'] = np.where(laps['PitOutTime'].isnull(),0,1)


PS_nb_D1 = laps[(laps["Driver"]=="HAM") & (laps["InPit"]==1)]['LapNumber']
PS_nb_D2 = laps[(laps["Driver"]=="VER") & (laps["InPit"]==1)]['LapNumber']


plot_data = [
    go.Scatter(
        x=laps[laps['Driver']=="HAM"]['LapNumber'],
        y=laps[laps['Driver']=="HAM"]['AVSpeed'],
        name = str("HAM")+' Av Speed',
        mode='lines',
        line = dict(color=ff1.plotting.team_color(laps[laps['Driver']=="HAM"]['Team'].iloc[0])) 

    ),
    go.Scatter(
        x=laps[laps['Driver']=="VER"]['LapNumber'],
        y=laps[laps['Driver']=="VER"]['AVSpeed'],
        name = str("VER")+' Av Speed',
        mode='lines',
        line = dict(color=ff1.plotting.team_color(laps[laps['Driver']=="VER"]['Team'].iloc[0])) 

    ),
]

plot_layout = go.Layout(
        xaxis={"type": "category",'visible': False, 'showticklabels': False},
        title='Average Speed Comparison',
        hovermode = 'x',
        
    )
avspeedplot = go.Figure(data=plot_data, layout=plot_layout)

for i in PS_nb_D1:

    avspeedplot.add_vline(x= i, 
                  line_width=3,
                  line_dash="dot",
                  line_color = ff1.plotting.team_color(laps[laps['Driver']=="HAM"]['Team'].iloc[0])
                  )

for j in PS_nb_D2:

    avspeedplot.add_vline(x= j, 
                  line_width=3,
                  line_dash="dash",
                  line_color = ff1.plotting.team_color(laps[laps['Driver']=="VER"]['Team'].iloc[0])

                  )



nav = create_navbar()

header = html.h5('this is a demo')

av_speed_plot = dcc.Graph(
                        id='avspeedplot',
                        figure = avspeedplot,
                        ),




def create_telemetry():
    
    layout = html.Div([
        
        nav,
        
        header,
        
        dbc.Row(
                
                dbc.Col(
                    av_speed_plot,
                    style={'width': '80%', 'height': '65%'}
                ),
                
            ),    
        
        
        dbc.Row(
            
            )
        
        
        ])
        
    
       

    return layout
