# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 05:58:52 2021

@author: guibd
"""

import dash_html_components as html
from navbar import create_navbar
import dash_core_components as dcc
from dash.dependencies import Input, Output
from app import app


nav = create_navbar()

header = html.H3('extra data')

extra_tabs =  html.Div([
    
        dcc.Tabs(
            id="tabs-with-classes",
            value='tab-2',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[
                
                dcc.Tab(
                    
                    label='Race Session',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                      
                    
                ),
                
                dcc.Tab(
                    label='Qualifying Session',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                
                dcc.Tab(
                    label='Other',
                    value='tab-3', className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
              
            ]),
        html.Div(id='tabs-content-classes')
        
    ])






def create_extra():
    layout = html.Div([
        nav,
        header,
        extra_tabs,
    ])
    return layout

@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            
            
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Qualifying Session')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Other')
        ])

