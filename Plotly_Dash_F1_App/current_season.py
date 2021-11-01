# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 05:57:01 2021

@author: guibd
"""

import dash_html_components as html
from navbar import create_navbar
from master import data_importation
import pandas as pd
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px 

nav = create_navbar()
header = html.H3('current season')
data = data_importation()

# data manipulation

df_circuits = data['circuits'][['circuitId','country']]
df_races = data['races'][['year','circuitId','raceId','round','name']]
df_races = df_races.rename(columns={'round':'round_nb'})
df_drivers = data['drivers'][['driverId','driverRef','forename','surname','nationality','url']]
df_drivers = df_drivers.rename(columns = {'nationality':"driver_nationality",'url':'driver_url'}) 

merge_tb1 = pd.merge(df_circuits,df_races,how='inner',on='circuitId')
merge_tb1 = merge_tb1.sort_values(by=['raceId'])

# merge table 2 : results and constructors 

merge_tb2 = pd.merge(data['results'], data['constructors'], how='inner', on ='constructorId' )

# adding drivers in merge_tb2
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

# current season driver standings

current_season = GP_summary[GP_summary['year']==GP_summary['year'].max()]

current_season['Drivers'] = (current_season['forename'] +[' '] +current_season['surname']).apply(str)
df_current_season = current_season.groupby(['Drivers','round_nb','name'], as_index = False ).sum()
cumul_points = current_season.groupby(['Drivers','round_nb','name'], as_index = False ).sum().groupby('driverId', as_index = False ).points.cumsum()
win_nb = current_season.groupby(['Drivers','round_nb','name'], as_index = False ).sum().groupby('driverId', as_index = False ).race_won.cumsum()
df_current_season = pd.concat([df_current_season, cumul_points, win_nb], axis = 1)
df_current_season = df_current_season.rename(columns={df_current_season.columns[-1]: 'total_win_nb'})

cols = []
count = 1
for column in df_current_season.columns:
    if column == 'total_win_nb':
        cols.append(f'total_win_nb_{count}')
        count+=1
        continue
    cols.append(column)
df_current_season.columns = cols

df_current_season = df_current_season.rename(columns = {'total_win_nb_1' : 'race_won', 'total_win_nb_2'  :'total_win_nb'})


cols = []
count = 1
for column in df_current_season.columns:
    if column == 'points':
        cols.append(f'points_{count}')
        count+=1
        continue
    cols.append(column)
df_current_season.columns = cols

# subsetting  data to create a df containing informations about the current season only

df_current_season = df_current_season.rename(columns = {'points_1' : 'points', 'points_2'  :'cumulative_points'})
df_current_season['points_to_date'] = df_current_season.groupby(['Drivers'])['cumulative_points'].transform(max)
df_current_season['nb_of_wins'] = df_current_season.groupby(['Drivers'])['total_win_nb'].transform(max)


df_current_standings = df_current_season.loc[df_current_season.reset_index().groupby(['Drivers'])['points_to_date'].idxmax()].sort_values('points_to_date', ascending = False)
df_current_standings['rank'] = df_current_standings['points_to_date'].rank(method = 'first',ascending = False).astype(int)
df_current_standings = df_current_standings[['rank','Drivers','points_to_date','nb_of_wins']]
df_current_standings = df_current_standings.rename(columns = {'rank':'Rank',  'points_to_date':'Points', 'nb_of_wins':'Wins'})


# constructor standings for the current season

data['constructor_standings'] = data['constructor_standings'].rename(columns={'points':'constructor_points'})

data['races'] = data['races'].rename(columns={'name':'GP_name'})

df_constructor_standings = pd.merge(data['races'], data['constructor_standings'], how='inner', on ='raceId')

data['constructors'] = data['constructors'].rename(columns={'name': 'constructor_name'})

df_constructor_standings = pd.merge(data['constructors'], df_constructor_standings, how='inner', on ='constructorId')
df_constructor_standings = df_constructor_standings.drop(['url_x','url_y'], axis = 1)

constructor_standings_2020 = df_constructor_standings[df_constructor_standings['year']==2021]
constructor_standings_2020.groupby('constructorId').constructor_points.max()
constructor_standings_2020['constructor_points'] = constructor_standings_2020.groupby(['constructorId'])['constructor_points'].transform(max)

current_CS = df_constructor_standings[df_constructor_standings['year']==df_constructor_standings['year'].max()]
current_CS['points_to_date'] = current_CS.groupby(['constructorId'])['constructor_points'].transform(max)

current_CS = current_CS.iloc[current_CS.reset_index().groupby(['constructorId'])['points_to_date'].idxmax()].sort_values('points_to_date', ascending = False)
current_CS['rank'] = current_CS['points_to_date'].rank(method = 'first',ascending = False).astype(int)
current_CS =current_CS[['rank','constructor_name','points_to_date']]
current_CS = current_CS.rename(columns={'rank':'Rank','constructor_name':'Constructor','points_to_date':'Points'})


# plot 1 : standings (barplot)


fig1 = go.Figure(data = [
    go.Bar(name = 'number of wins',
           x = df_current_standings['Drivers'],
           y =df_current_standings['Wins'],
           # orientation ='h',
           text = df_current_standings['Wins']),
    
    go.Bar(name = 'points to date',
           x= df_current_standings['Drivers'],
           y = df_current_standings['Points'],
           # orientation = 'h',
           text = df_current_standings['Points'])
    
    ])

fig1.update_layout(barmode='group')
fig1.update_yaxes(type="log")
fig1.update_layout(yaxis={'visible': False, 'showticklabels': False})
fig1.update_traces(textposition='auto')
fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig1.update_layout(title = str(df_current_season['year'].unique()) + ' Season Standings')

# sunburst of win recap for the current season

fig2 = px.sunburst(current_season, path=['year','constructor_name','Drivers'], values = 'race_won')

fig2.update_layout(margin = dict(t=0, l=0, r=0, b=0))
fig2.update_traces(hoverinfo='label', textinfo='label+value', textfont_size=20,
              marker=dict(line=dict(color='#000000', width=1)))
fig2.update_traces(insidetextorientation='auto')
fig2.update_layout(uniformtext=dict(minsize=8),
                    margin = dict(t=6, l=6, r=6, b=6)


# app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])


current_season_table_drivers = dash_table.DataTable(

                            id = 'dt1',
                            data = df_current_standings.to_dict('record'),
                            columns = [{'id': c , 'name' : c }for c in df_current_standings.columns],
                         
                        
                            style_cell={'textAlign': 'left',
                                        'padding': '5px',
                                        'backgroudColor':'#DCDCDC'
                            },
                            
                            style_header={
                                'backgroundColor': 'darkgrey',
                                'fontWeight': 'bold'
                            },
                        
                             style_cell_conditional=[
                            
                                 {'if': {'filter_query': '{Rank} = 1'},
                                
                                'backgroundColor': 'gold',
                        
                            },
                        
                                 {'if': {'filter_query': '{Rank} = 2'},
                                  
                                'backgroundColor': 'silver',
                        
                            },
                              
                                 {'if': {'filter_query': '{Rank} = 3'},
                                  
                                'backgroundColor': 'peru',
                        
                            },
                            ],
                                
                            
                            style_as_list_view=True,
                            
                            page_action='native',
                            page_current= 0,
                            page_size= 10,
                            
                            ),


current_season_table_constructors = dash_table.DataTable(

                            id = 'dt2',
                            data = current_CS.to_dict('record'),
                            columns = [{'id': c , 'name' : c }for c in current_CS.columns],
                         
                        
                            style_cell={'textAlign': 'left',
                                        'padding': '5px',
                                        'backgroudColor':'#DCDCDC'
                            },
                            
                            style_header={
                                'backgroundColor': 'darkgrey',
                                'fontWeight': 'bold'
                            },
                        
                             style_cell_conditional=[
                            
                                 {'if': {'filter_query': '{Rank} = 1'},
                                
                                'backgroundColor': 'gold',
                        
                            },
                        
                                 {'if': {'filter_query': '{Rank} = 2'},
                                  
                                'backgroundColor': 'silver',
                        
                            },
                              
                                 {'if': {'filter_query': '{Rank} = 3'},
                                  
                                'backgroundColor': 'peru',
                        
                            },
                            ],
                                
                            
                            style_as_list_view=True,
                            
                            page_action='native',
                            page_current= 0,
                            page_size= 10,
                            
                            ),

current_season_plot = dcc.Graph(
                        id='plot1',
                        figure = fig1,
                        ),

current_season_wins = dcc.Graph(
    id = 'sunburst1',
    figure = fig2
    ),




def create_current_season():
    
    layout = html.Div([
        
        
        nav,
        
        dbc.Row(
            
            [
                
                dbc.Col(
                    current_season_table_drivers,
                    style={'width': '50%', 'height': '50%'}
                ),
                
                                
                dbc.Col(
                    current_season_table_constructors,
                    style={'width': '50%', 'height': '50%'}
                ),
            
                
            ]),
            
            dbc.Row(
                
                [
                            
                dbc.Col(
                    current_season_wins,
                    style={'width': '50%', 'height': '50%'}
                    ),
                
                
                dbc.Col(
                    current_season_plot,
                    style={'width': '50%', 'height': '70%'}
                ),
                
                ]
                
                )


    ])

    return layout












