# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 05:57:58 2021

@author: guibd
"""

import dash_html_components as html
from navbar import create_navbar
from master import data_importation
import plotly.express as px
import dash_core_components as dcc 

nav = create_navbar()

header = html.H3('circuits')

data = data_importation()


circuits_gps = data['circuits'][['lat','lng']]
circuit_name = data['circuits']['name']

px.set_mapbox_access_token("pk.eyJ1IjoiZ2JyZGYiLCJhIjoiY2t0b2FpcWxpMGF4MjMwbGdnb3o4ZGJudiJ9.ZEgEpIXkj-R2Xx-4B6rqyw")

fig = px.scatter_mapbox(circuits_gps,
                        lat=circuits_gps['lat'],
                        lon=circuits_gps['lng'],
                        hover_name = circuit_name,
                        color_discrete_sequence=['orange'],
                        zoom=3)
fig.update_layout(mapbox_style="dark")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


circuits_location_map = html.Div([
    
    dcc.Graph(id='circuits_location_map',
              
              figure = fig
        
        )

])

def create_circuits():
    layout = html.Div([
        nav,
        circuits_location_map
    ])
    return layout