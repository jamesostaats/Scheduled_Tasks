import dash  # Primary dash app framework
import dash_core_components as dcc     # Dash core page elements
import dash_html_components as html    # Dash HTML page elements
import dash_bootstrap_components as dbc   # Dash bootstrap elements - same as dcc but looks better
import dash_table    # Interactive data table
from dash.dependencies import Input, Output, State    # Used for callbacks
from flask import send_file, request, Response    # Used to download files to your user's computer
from dash.exceptions import PreventUpdate      # Used to stop callbacks from firing
import pandas as pd    # Pandas!
import numpy as np
import plotly.express as px
import io
from base64 import b64encode
from apscheduler.schedulers.background import BackgroundScheduler  # automatic scheduling function

from tools.sched_functions import sched_marketo_loop

'''

CORE APP SETUP BELOW - YOU CAN MODIFY BUT DO NOT DELETE

'''


scheduler = BackgroundScheduler()
scheduler.add_job(sched_marketo_loop, trigger='interval', seconds=100)
#scheduler.add_job(sched_test_cron, trigger='cron',day_of_week='mon-fri', hour=2)
scheduler.start()

#Change the theme to another bootstrap theme if you'd like
#More themes can be found here https://bootswatch.com/
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])

# Title your app here
app.title = "Scheduled Tasks ECA - AAC"

# Leave dev tools on - this will let you know if something is wrong on the page
# If you are using scheduled jobs, change debug to False both here and at the end of the page
# Otherwise your scheduled jobs will run twice every time
app.enable_dev_tools(debug=True, dev_tools_hot_reload=False,dev_tools_silence_routes_logging=False)



import pandas as pd
from sqlalchemy import create_engine

#### Establishes connection to Postgres
#POSTGRES_ADDRESS = '___the name of your VM - ex lin2dv2nba68_____'
POSTGRES_ADDRESS = 'lin2dv2nba75'
POSTGRES_PORT = 1550
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DBNAME = 'postgres'
postgres_str = 'postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME, password= POSTGRES_PASSWORD, ipaddress=POSTGRES_ADDRESS, port=POSTGRES_PORT, dbname=POSTGRES_DBNAME)
connection = create_engine(postgres_str)


df=pd.read_sql('''SELECT * FROM schedule_task_status''',connection)


#Message Table
message='Current Status of Ongoing Tasks:'
messdf=pd.DataFrame(columns=[message])

dash_messagetable=dash_table.DataTable(id='dash_messtable',
data=messdf.to_dict('records'),
columns=[{"name":i,"id":i} for i in messdf.columns],
style_cell={'textAlign':'center','font_size':'16px'},
style_header={'textAlign':'center','color':'white','background-color':'rgb(30, 30, 30)','border':'1px solid black'})

#Message Table

dash_status_table=dash_table.DataTable(id='dash_statustable',
data=df.to_dict('records'),
columns=[{"name":i,"id":i} for i in df.columns],
style_data={'height':'auto','whiteSpace': 'normal'},
style_data_conditional=([{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
            },
            {'if': {'column_id':'Status','filter_query':'{Status}=Active'},
            'color': 'rgb(0, 128, 0)'}
            ,
            {'if': {'column_id':'Status','filter_query':'{Status}=Failed'},
            'color': 'rgb(184, 0, 0, 0.8)'}
            ,
            {'if': {'column_id':'Status','filter_query':'{Status}=Failed_Notified'},
            'color': 'rgb(85, 85, 255)'}
            
            ]),
style_cell={'textAlign':'center','font_size':'16px'},
style_header={'textAlign':'center','color':'white','background-color':'rgb(30, 30, 30)','border':'1px solid black'})


app.layout = html.Div([
    # Navigation bar is stored here
    dbc.Navbar([
        dbc.NavItem(dbc.NavbarBrand(app.title
            ,className="ml-2"
            ,style={'color':'white'}))],color='primary'),
            html.Br(),

            html.Div(className='row',children=[
            
            ]),
            html.Div(dash_messagetable,style={'textAlign':'center','color':'brown','background-color':'grey','padding':'5px','border':'1px solid black','margin':'50px 50px 50px 50px'}),
            html.Div(dash_status_table,style={'textAlign':'center','color':'brown','background-color':'grey','padding':'5px','border':'1px solid black','margin':'50px 50px 50px 50px'}),
            html.Button('Refresh', id='refresh-val', n_clicks=1,style={'textAlign':'center','background-color':'grey','padding':'5px','border':'1px solid black','margin':'50px 0px 50px 50px'})
            
            ])

@app.callback([
    #Output(component_id='dash_statustable',component_property='columns'),
    Output(component_id='dash_statustable',component_property='data')]
    ,
    [Input(component_id='refresh-val',component_property='n_clicks')
    ])

def update_values(refresh_click):

    if refresh_click>0:
        df=pd.read_sql('''SELECT * FROM schedule_task_status''',connection)
        data=df.to_dict('records'),
        columns=[{"name":i,"id":i} for i in df.columns]
    refresh_click=0

    return data



if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False, host='0.0.0.0', port=3000)