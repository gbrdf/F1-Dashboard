# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 05:36:39 2021

@author: guibd
"""

import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,
                suppress_callback_exceptions= True,
                external_stylesheets=[dbc.themes.LUX]
                )

server = app.server

