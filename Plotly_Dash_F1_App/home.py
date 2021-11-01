# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 05:56:28 2021

@author: guibd
"""

import dash_html_components as html
from navbar import create_navbar
import dash_bootstrap_components as dbc
import dash

nav = create_navbar()

header = html.H3('F1 dashboard Home page')

# app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])

jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H2("Formula One Dashboard", className="display-3"),
                html.P(
                    "A Dashboard with data viz and statistics about Formula One, "
                    "based on data provided by the Ergast API: "
                    "http://ergast.com/mrd/",
                    className="lead",
                ),
                 html.P(dbc.Button("🡆",
                                   id='API_link',
                                   color="dark", 
                                   className="ml-auto",
                                   href ='http://ergast.com/mrd/',
                                   target = "_blank"
                                   )
                        ),

                 html.P(
                    "All files and code are available on my github: "
                    "https://github.com/gbrdf/F1-Dashboard",
                    className="lead",
                ),
                 html.P(dbc.Button("🡆",
                                   id='GitH_link',
                                   color="dark", 
                                   className="ml-auto",
                                   href ='https://github.com/gbrdf/F1-Dashboard',
                                   target ="_blank"
                                   )
                        ),
                 
            ],
            fluid=True,
        )
    ],
    fluid=True,
)

    
def create_page_home():
    layout = html.Div([
        nav,
        jumbotron,
        
    ])
    return layout