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

from tools.sched_functions import sched_test, sched_test_cron

'''

CORE APP SETUP BELOW - YOU CAN MODIFY BUT DO NOT DELETE

'''


scheduler = BackgroundScheduler()
scheduler.add_job(sched_test, trigger='interval', seconds=1000)
scheduler.add_job(sched_test_cron, trigger='cron',day_of_week='mon-fri', hour=2)
scheduler.start()

#Change the theme to another bootstrap theme if you'd like
#More themes can be found here https://bootswatch.com/
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])

# Title your app here
app.title = "Territory Geography View"

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


df=pd.read_sql('''SELECT * FROM nast_usa_geo''',connection)

df['NAST_Rep']=df['Rep_NAST'].str[:8]
df.loc[df.NAST_Rep.str.lower().str.find('empty')>=0,'fullname']='Empty Territory'
df['Info']=df['fullname']+' - '+df['Territory Code']

#Drop Down Creation
drop_options_df=df[['Territory Code','Info']].copy()

drop_options_df=drop_options_df.drop_duplicates()
drop_options_df=drop_options_df.sort_values(by='Territory Code')


drop_options_df['label']=drop_options_df['Info']
drop_options_df['value']=drop_options_df['Territory Code']

drop_options_df=drop_options_df[['label','value']]

drop_options_df['label']=drop_options_df['label'].replace(np.NaN,'Nothing')
drop_options_df['value']=drop_options_df['value'].replace(np.NaN,'Nothing')
drop_options_df=drop_options_df.loc[drop_options_df['label']!='Nothing']
drop_options_df=drop_options_df.loc[drop_options_df['value']!='Nothing']

drop_options=drop_options_df.to_dict('records')

#Dropdown Figure
dropdown=dcc.Dropdown(id='SelectTerr',
                      options=drop_options,
                      multi=False,
                      #value='VT107N',
                      style={'width':"100%"})



#Drop Down Creation 2
drop_options_df=df[['SizeSegment']].copy()

drop_options_df=drop_options_df.drop_duplicates()
drop_options_df=drop_options_df.sort_values(by='SizeSegment')


drop_options_df['label']=drop_options_df['SizeSegment']
drop_options_df['value']=drop_options_df['SizeSegment']

drop_options_df=drop_options_df[['label','value']]

drop_options_df['label']=drop_options_df['label'].replace(np.NaN,'Nothing')
drop_options_df['value']=drop_options_df['value'].replace(np.NaN,'Nothing')
drop_options_df=drop_options_df.loc[drop_options_df['label']!='Nothing']
drop_options_df=drop_options_df.loc[drop_options_df['value']!='Nothing']

drop_options=drop_options_df.to_dict('records')

#Dropdown Figure 2
dropdown_2=dcc.Dropdown(id='Size',
                      options=drop_options,
                      multi=False,
                      #value='VT107N',
                      style={'width':"100%"})


#Drop Down Creation 3
drop_options_df=df[['District Code']].copy()

drop_options_df=drop_options_df.drop_duplicates()
drop_options_df=drop_options_df.sort_values(by='District Code')


drop_options_df['label']=drop_options_df['District Code']
drop_options_df['value']=drop_options_df['District Code']

drop_options_df=drop_options_df[['label','value']]

drop_options_df['label']=drop_options_df['label'].replace(np.NaN,'Nothing')
drop_options_df['value']=drop_options_df['value'].replace(np.NaN,'Nothing')
drop_options_df=drop_options_df.loc[drop_options_df['label']!='Nothing']
drop_options_df=drop_options_df.loc[drop_options_df['value']!='Nothing']

drop_options=drop_options_df.to_dict('records')

#Dropdown Figure 3
dropdown_3=dcc.Dropdown(id='District',
                      options=drop_options,
                      multi=False,
                      #value='VT107N',
                      style={'width':"100%"})

#Drop Down Creation 4
drop_options_df=df[['Region Code']].copy()

drop_options_df=drop_options_df.drop_duplicates()
drop_options_df=drop_options_df.sort_values(by='Region Code')


drop_options_df['label']=drop_options_df['Region Code']
drop_options_df['value']=drop_options_df['Region Code']

drop_options_df=drop_options_df[['label','value']]

drop_options_df['label']=drop_options_df['label'].replace(np.NaN,'Nothing')
drop_options_df['value']=drop_options_df['value'].replace(np.NaN,'Nothing')
drop_options_df=drop_options_df.loc[drop_options_df['label']!='Nothing']
drop_options_df=drop_options_df.loc[drop_options_df['value']!='Nothing']

drop_options=drop_options_df.to_dict('records')

#Dropdown Figure 4
dropdown_4=dcc.Dropdown(id='Region',
                      options=drop_options,
                      multi=False,
                      #value='VT107N',
                      style={'width':"100%"})



#Message Table
message='Use filters above to view specific alignments'
messdf=pd.DataFrame(columns=[message])

dash_messagetable=dash_table.DataTable(id='dash_messtable',
data=messdf.to_dict('records'),
columns=[{"name":i,"id":i} for i in messdf.columns],
style_cell={'textAlign':'center','font_size':'16px'},
style_header={'textAlign':'center','color':'white','background-color':'rgb(30, 30, 30)','border':'1px solid black'})

df[['Latitude', 'Longitude']]=df[['Latitude', 'Longitude']].replace(np.NaN,'Nothing')
df.loc[(df['Latitude']!='Nothing')&(df['Longitude']!='Nothing')]

df[['Latitude', 'Longitude']]=df[['Latitude', 'Longitude']].astype('float')

df_simple=df[['Latitude','Longitude','Zip']]
df_simple['Info']='USA Zip Code'
df_simple=df_simple.drop_duplicates()

#Scatterplot Figure
plottitle='USA Zip Code Alignment'
fig=px.scatter_mapbox(df_simple,zoom=2,lat='Latitude',lon='Longitude',color_continuous_scale=px.colors.cyclical.IceFire,color='Info',hover_name='Zip',hover_data=['Info'],mapbox_style='carto-positron')
fig=fig.update_layout(title=plottitle)

#html download
buffer = io.StringIO()

#figs_to_html=dict(values=[fig,table])
fig.write_html(buffer)

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app.layout = html.Div([
    # Navigation bar is stored here
    dbc.Navbar([
        dbc.NavItem(dbc.NavbarBrand(app.title
            ,className="ml-2"
            ,style={'color':'white'}))],color='primary'),
            html.Br(),

            html.Div(className='row',children=[
            
            html.Div(children=[
            html.Div(children=[html.H5('Input Zip Code:'),dcc.Input(id='Zip',placeholder="USA 5-Digit Zip")],style={'textAlign':'left','color':'black','padding':'5px','margin':'50px 50px 50px 50px'})#,className='six columns'
            ]),
            html.Div(children=[
            html.Div(children=[html.H5('Select Size Segment:'),dropdown_2],style={'textAlign':'left','color':'black','padding':'5px','margin':'50px 50px 50px 50px'})#,className='six columns'
            ]),
            html.Div(children=[
            html.Div(children=[html.H5('Select Territory Code:'),dropdown],style={'textAlign':'left','color':'black','padding':'5px','margin':'50px 50px 50px 50px'})#,className='six columns'
            ]),
            html.Div(children=[
            html.Div(children=[html.H5('Select District:'),dropdown_3],style={'textAlign':'left','color':'black','padding':'5px','margin':'50px 50px 50px 50px'})#,className='six columns'
            ]),
            html.Div(children=[
            html.Div(children=[html.H5('Select Region:'),dropdown_4],style={'textAlign':'left','color':'black','padding':'5px','margin':'50px 50px 50px 50px'})#,className='six columns'
            ])
            ]),
            html.Div(dash_messagetable,style={'textAlign':'center','color':'brown','background-color':'grey','padding':'5px','border':'1px solid black','margin':'50px 50px 50px 50px'}),
            dcc.Graph(id='Account Map',figure=fig),
            html.Div(html.A(
                html.Button("Download HTML Map File"), 
                id="download",
                href="data:text/html;base64," + encoded,
                download="territory_geography.html"
            ),style={'textAlign':'center','color':'brown','background-color':'grey','padding':'5px','border':'1px solid black','margin':'50px 50px 50px 50px'})
            
            ])

@app.callback([Output(component_id='Account Map',component_property='figure'),
    Output(component_id='SelectTerr',component_property='options'),
    Output(component_id='Size',component_property='options'),
    Output(component_id='District',component_property='options'),
    Output(component_id='Region',component_property='options'),
    Output(component_id='download',component_property='href')],
    Output(component_id='dash_messtable',component_property='columns')
    ,
    [Input(component_id='Zip',component_property='value'),
    Input(component_id='SelectTerr',component_property='value'),
    Input(component_id='Size',component_property='value'),
    Input(component_id='District',component_property='value'),
    Input(component_id='Region',component_property='value'),
    ])

def update_values(zipcode, territory, size, district, region):

    df=pd.read_sql('''SELECT * FROM nast_usa_geo''',connection)

    df['NAST_Rep']=df['Rep_NAST'].str[:8]
    df.loc[df.NAST_Rep.str.lower().str.find('empty')>=0,'fullname']='Empty Territory'
    df['Info']=df['fullname']+' - '+df['Territory Code']

    if zipcode == None:
        zipcode=''
    if territory == None:
        territory=''
    if size == None:
        size=''
    if district == None:
        district=''
    if region == None:
        region=''

    message='Use filters above to view specific alignments'
    messdf=pd.DataFrame(columns=[message])
    mess_columns=[{"name":i,"id":i} for i in messdf.columns]


    
    if len(size)>0:
        df=df.loc[df['SizeSegment']==size]
        message='Viewing Size: '+size
        messdf=pd.DataFrame(columns=[message])
        mess_columns=[{"name":i,"id":i} for i in messdf.columns]


    if len(region)>0:
        df=df.loc[df['Region Code']==region]
        message='Viewing Region: '+region
        messdf=pd.DataFrame(columns=[message])
        mess_columns=[{"name":i,"id":i} for i in messdf.columns]

    if len(district)>0:
        df=df.loc[df['District Code']==district]
        message='Viewing District: '+district
        messdf=pd.DataFrame(columns=[message])
        mess_columns=[{"name":i,"id":i} for i in messdf.columns]

    if len(territory)>0:
        df=df.loc[df['Territory Code']==territory]
        message='Viewing Territory: '+territory
        messdf=pd.DataFrame(columns=[message])
        mess_columns=[{"name":i,"id":i} for i in messdf.columns]

    if (len(zipcode)==5):
        df=df.loc[df['Zip']==zipcode]
        message='Viewing Zip: '+zipcode
        messdf=pd.DataFrame(columns=[message])
        mess_columns=[{"name":i,"id":i} for i in messdf.columns]

    df[['Latitude', 'Longitude','Zip','Info']]=df[['Latitude', 'Longitude','Zip','Info']].replace(np.NaN,'Nothing')
    df.loc[(df['Info']!='Nothing')&(df['Zip']!='Nothing')&(df['Latitude']!='Nothing')&(df['Longitude']!='Nothing')]

    df[['Latitude', 'Longitude']]=df[['Latitude', 'Longitude']].astype('float')

    df_simple=df[['Latitude','Longitude','Zip']]
    df_simple['Info']='USA Zip Code'
    df_simple=df_simple.drop_duplicates()

    #Drop Down Creation
    drop_options_df=df[['Territory Code','Info']].copy()

    drop_options_df=drop_options_df.drop_duplicates()
    drop_options_df=drop_options_df.sort_values(by='Territory Code')

    drop_options_df['label']=drop_options_df['Info']
    drop_options_df['value']=drop_options_df['Territory Code']

    drop_options_df=drop_options_df[['label','value']]

    drop_options_df['label']=drop_options_df['label'].replace(np.NaN,'Nothing')
    drop_options_df['value']=drop_options_df['value'].replace(np.NaN,'Nothing')
    drop_options_df=drop_options_df.loc[drop_options_df['label']!='Nothing']
    drop_options_df=drop_options_df.loc[drop_options_df['value']!='Nothing']

    terr_options=drop_options_df.to_dict('records')

    #Drop Down Creation 2
    drop_options_df=df[['SizeSegment']].copy()

    drop_options_df=drop_options_df.drop_duplicates()
    drop_options_df=drop_options_df.sort_values(by='SizeSegment')

    drop_options_df['label']=drop_options_df['SizeSegment']
    drop_options_df['value']=drop_options_df['SizeSegment']

    drop_options_df=drop_options_df[['label','value']]

    drop_options_df['label']=drop_options_df['label'].replace(np.NaN,'Nothing')
    drop_options_df['value']=drop_options_df['value'].replace(np.NaN,'Nothing')
    drop_options_df=drop_options_df.loc[drop_options_df['label']!='Nothing']
    drop_options_df=drop_options_df.loc[drop_options_df['value']!='Nothing']

    size_options=drop_options_df.to_dict('records')

    #Drop Down Creation 3
    drop_options_df=df[['District Code']].copy()

    drop_options_df=drop_options_df.drop_duplicates()
    drop_options_df=drop_options_df.sort_values(by='District Code')

    drop_options_df['label']=drop_options_df['District Code']
    drop_options_df['value']=drop_options_df['District Code']

    drop_options_df=drop_options_df[['label','value']]

    drop_options_df['label']=drop_options_df['label'].replace(np.NaN,'Nothing')
    drop_options_df['value']=drop_options_df['value'].replace(np.NaN,'Nothing')
    drop_options_df=drop_options_df.loc[drop_options_df['label']!='Nothing']
    drop_options_df=drop_options_df.loc[drop_options_df['value']!='Nothing']

    district_options=drop_options_df.to_dict('records')

    #Drop Down Creation 4
    drop_options_df=df[['Region Code']].copy()

    drop_options_df=drop_options_df.drop_duplicates()
    drop_options_df=drop_options_df.sort_values(by='Region Code')

    drop_options_df['label']=drop_options_df['Region Code']
    drop_options_df['value']=drop_options_df['Region Code']

    drop_options_df=drop_options_df[['label','value']]

    drop_options_df['label']=drop_options_df['label'].replace(np.NaN,'Nothing')
    drop_options_df['value']=drop_options_df['value'].replace(np.NaN,'Nothing')
    drop_options_df=drop_options_df.loc[drop_options_df['label']!='Nothing']
    drop_options_df=drop_options_df.loc[drop_options_df['value']!='Nothing']

    region_options=drop_options_df.to_dict('records')

    df=df[['Latitude','Longitude','Zip','Info']]

    
    #Figure
    figure=px.scatter_mapbox(df,zoom=2,lat='Latitude',lon='Longitude',color_continuous_scale=px.colors.cyclical.IceFire,color='Info',hover_name='Zip',hover_data=['Info'],mapbox_style='carto-positron')
    figure=figure.update_layout(title=plottitle)


    if (len(zipcode)<5)&(len(territory)==0)&(len(size)==0)&(len(district)==0)&(len(region)==0):
        figure=px.scatter_mapbox(df_simple,zoom=2,lat='Latitude',lon='Longitude',color_continuous_scale=px.colors.cyclical.IceFire,color='Info',hover_name='Zip',hover_data=['Info'],mapbox_style='carto-positron')
        figure=figure.update_layout(title=plottitle)
        message=['Use filters above to view specific alignments']
        messdf=pd.DataFrame(columns=message)
        mess_columns=[{"name":i,"id":i} for i in messdf.columns]

    #html download
    buffer = io.StringIO()
    figure.write_html(buffer)
    html_bytes = buffer.getvalue().encode()
    encoded = b64encode(html_bytes).decode()
    href="data:text/html;base64," + encoded

    
    return figure, terr_options, size_options, district_options, region_options,href,mess_columns



if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False, host='0.0.0.0', port=3000)