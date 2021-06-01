#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 09:39:55 2021

@author: mspann
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import plotly

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


df = pd.read_csv("/home/mspann/Redistricting/Registered/new/Weldcutdown.csv")  
#df = pd.read_csv("/home/mspann/Redistricting/Registered/Weld.csv")  

#df['dates'].astype(object)
df['RESIDENTIAL_ZIP_CODE'] = df['RESIDENTIAL_ZIP_CODE'].astype(str)

locator = Nominatim(user_agent='myGeocoder')

# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

# 2- - create location column

df['location'] = df['RESIDENTIAL_ADDRESS'] + "," + df['RESIDENTIAL_CITY'] + "," + df['RESIDENTIAL_STATE'] + "," + df['RESIDENTIAL_ZIP_CODE']

df['gcode'] = df.location.apply(locator.geocode)


# 3 - create longitude, laatitude and altitude from location column (returns tuple)
df['point'] = df['gcode'].apply(lambda loc: tuple(loc.point) if loc else None)

# 4 - split point column into latitude, longitude and altitude columns
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)


map = px.scatter_mapbox(df, 
                                lat="latitude", 
                                lon="longitude",                    
                                hover_data={'latitude': False,
                                            'longitude': False,
                                            },
                                size="SIZE",
                                zoom=10.5
                                
                                )
map.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(
        bearing=0,
        
    ),
    margin=dict(l=0,r=50,t=60,b=40),
    title = "Colorado",
    titlefont=dict(
            family='sans-serif, monospace',
            size=15,
            color='#090909'
            ),
    )

app.layout = dbc.Container(
                html.Div([
                html.H2('Colorado Secretary of State Registered Voter List'),
                                 html.P('Open Source'),
                                 html.P(''),                  
                  dbc.Row([
                      dbc.Col(
                          html.Div(
                              
                              dcc.Graph(
                                  id="Map Graphic",
                                  figure=map, 
                                  style={'height':'100vh'}
                                 )),
                          )
                        ])
    ]),fluid = True
)



if __name__ == "__main__":
    app.run_server()
    