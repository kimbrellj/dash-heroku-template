import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html 
from dash.dependencies import Input, Output



in_port = pd.read_csv('https://raw.githubusercontent.com/kimbrellj/dash-heroku-template/master/dash_ports.csv')

countries = list(in_port.COUNTRY.unique())
ports_country = ['']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '24px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'lightblue',
    'color': 'grey',
    'padding': '24px'
}
app.layout = html.Div([
     html.H1("Port Dashboard",style={'backgroundColor':'lightblue',"text-align": "center","color": "grey"}),
    html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="port-tab",
                        label="Stats by port",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=[
                            html.Label('Please Select a Country',style={'padding-top':'2.5%','fontWeight': 'bold'}),
                            dcc.Dropdown(id='country',options=countries, value=countries[0]),
                            dcc.Graph(id='graph'),
                            html.Label('Please Select a Port',style={'padding-top':'3.5%','fontWeight': 'bold'}),
                            dcc.Dropdown(id='port',),
                            dcc.Graph(id='graph2'),
                            dcc.Graph(id='graph3'),]
                    ),
                   
                ],
            )
        ],
    ),
    
])

@app.callback([Output(component_id="graph",component_property="figure"), 
               Output(component_id="port",component_property="options"),
              Output(component_id="graph2",component_property="figure"),
              Output(component_id="graph3",component_property="figure")],
             [Input(component_id='country',component_property="value"),
             Input(component_id='port',component_property="value")])


def make_figure(country,port):

    Country = in_port.loc[in_port.COUNTRY==country]
    count = in_port.loc[in_port.COUNTRY==country].groupby(['PORT_NAME'])['mmsi'].nunique()
    df = count.to_frame().reset_index().rename(columns={'mmsi':'count'})
    fig = px.bar(df, x='PORT_NAME', y='count')
    ports_country = list(df.PORT_NAME.unique())
    
    try:
        port_df = Country.loc[Country.PORT_NAME==port]
    except NameError:
        port_df = Country.loc[Country.PORT_NAME==ports_country[0]]
                              
    count2 = port_df.groupby(['flag_country'])['mmsi'].nunique()
    df_port = count2.to_frame().reset_index().rename(columns={'mmsi':'count'})
    fig2 = px.bar(df_port, x='flag_country', y='count')
    
    count3 = port_df.groupby(['vessel_type'])['mmsi'].nunique()
    df_type = count3.to_frame().reset_index().rename(columns={'mmsi':'count'})
    fig3 = px.pie(df_type, values='count', names='vessel_type', title='Type of Vessel')
    
    return fig,ports_country,fig2,fig3




if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
