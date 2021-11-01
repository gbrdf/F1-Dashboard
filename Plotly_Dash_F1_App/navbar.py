# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 05:35:21 2021

@author: guibd
"""

import dash_bootstrap_components as dbc
import dash_html_components as html

def create_navbar():
           
        F1_logo = "https://1000logos.net/wp-content/uploads/2021/06/F1-logo.png"
        # defining navbar items
        
        home_button = dbc.NavItem(
            dbc.NavLink('Home',
                        href="/home", 
                        id="home_link",
                        external_link=True,
                        className='navlinks'))
        
        current_season_button = dbc.NavItem(
            dbc.NavLink('Current Season',
                        href="/current_season",
                        id='current_season_link',
                        external_link=True,
                        className='navlinks'))
        
        circuits_button = dbc.NavItem(
            dbc.NavLink('Circuits',
                        href="/circuits",
                        id ='circuits_link',
                        external_link=True,
                        className='navlinks'))
        
        previous_seasons_button = dbc.NavItem(
            dbc.NavLink('Previous Seasons',
                        href="/previous_seasons", 
                        id='previous_seasons_link',
                        external_link=True,
                        className='navlinks'))
        
        extra_button = dbc.NavItem(
            dbc.NavLink('Extra',
                        href="/extra",
                        id='extra_link',
                        external_link=True,
                        className='navlinks'))
        
        telemetry_button = dbc.NavItem(
            dbc.NavLink('Telemetry',
                        href="/telemetry",
                        id='telemetry_link',
                        external_link=True,
                        className='navlinks'))
        
        links = {
            "Home": ["/home", "home_link"],
            "Current Season": ["/current_season", "current_season_link"],
            "Circuits": ["/circuits", "circuits_link"],    
            "Previous Seasons": ["/previous_seasons", "previous_seasons__link"],  
            "Telemetry": ["/telemetry", "telemetry_link"],  
            "Extra": ["/extra", "extra_link"]

        }
        
        
        navbar = dbc.Navbar(
            dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=F1_logo,className = 'logo',height="30px")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="/home",
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(dbc.Nav([dbc.NavLink(x, href=links[x][0], id=links[x][1]) for x in links.keys()],
                                     className='ml-auto work-sans',
                                     navbar=True),
                             id="navbar-collapse", navbar=True),
            ],
            ),
            color="rgb(42,62,66)",
            dark=True,
            style = {'background-color':'#191919'},
            className = 'navbar-change',
            expand= 'lg'
        )
    
    
        return navbar