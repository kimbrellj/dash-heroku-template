
import numpy as np
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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])



mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')
context_info = """
According to the American Association of University Women, still in 2022, women working full time only 
make 83 cents on the male dollar. At the current rate of equity improvement, women would not achieve pay 
equity until 2111. This persistent pay gap exists across all races in the United States, but is wider for 
women of color. The gap exists at all levels of work, in almost every industry, and in every U.S. state.

Website: https://www.aauw.org/issues/equity/pay-gap/

According to the GSS Website the General Social Survey (GSS Website Homepage) has studied the growing 
complexity of American society. It is the only full-probability, personal-interview survey designed to 
monitor changes in both social characteristics and attitudes currently being conducted in the United States.
(GSS Website). According to GSS codebook the GSS collects data on contemporary American society to monitor and
explain trends in opinions, attitudes, and behaviors. The GSS has adapted questions from earlier surveys, 
thereby allowing researchers to conduct comparisons for up to 80 years. The codebook also states the data 
contains a standard core of demographic, behavioral, and attitudinal questions, plus topics of special 
interest. Among the topics covered are civil liberties, crime and violence, intergroup tolerance, morality, 
national spending priorities, psychological well-being, social mobility, and stress and traumatic events. 
(GSS Codebook Page 11) The data is collected through an mail and online surveys every even year. 
Great care is taken to ensure questions are asked in similar ways to keep the data as accurate as possible."""
gss_clean.columns
df = gss_clean.groupby('sex').agg({'income':'mean','job_prestige':'mean','socioeconomic_index':'mean','education':'mean'}).round(2).reset_index()
df = df.rename(columns={'sex':'Sex','income':'Mean Income','job_prestige':'Occupational Prestige',
                        'socioeconomic_index':'Socioeconomic Status','education':'Years of Education'})
                        
table = ff.create_table(df)
table.show()
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].astype('category').cat.reorder_categories(['strongly agree','agree','disagree','strongly disagree'])
df = gss_clean.groupby(['sex','male_breadwinner']).size().reset_index()
df
fig_bar = px.bar(df, x='male_breadwinner', y=0,
        labels={'male_breadwinner':'Level of Agreement', '0' :'Number of People who Agree'},
      color='sex',barmode = 'group')
fig_bar.show()
fig_scat = px.scatter(gss_clean, x='job_prestige', y='income', 
                 color = 'sex', 
                 trendline='ols',
                 height=600, width=600,
                 labels={'job_prestige':'Occupational Prestige', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig_scat.show()
figbox1 = px.box(gss_clean, x='income', y = 'sex', color = 'sex',
                   labels={'income':'Income', 'sex':''})
figbox1.update_layout(showlegend=False)
figbox1.show()
figbox2 = px.box(gss_clean, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'job_prestige':'Occupation Prestige', 'sex':''})
figbox2.update_layout(showlegend=False)
figbox2.show()
box = gss_clean[['income','sex','job_prestige']].dropna()
box['job_prestige_cat'] = pd.cut(box.job_prestige,6)
box
fig_box = px.box(box, x='income', y='sex', color='sex', 
             facet_col='job_prestige_cat', facet_col_wrap=2,
             color_discrete_map = {'male':'blue', 'female':'red'},
                labels={'sex':'Sex','income':'Income'})
fig_box.show()
app2 = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
app2.layout = html.Div([
     html.H1("Dashboard Exploring GSS Dataset",style={'backgroundColor':'lightblue',"text-align": "center","color": "grey"}),
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
                        id="Intro-tab",
                        label="Context of GSS Data Set",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=[
                            dcc.Markdown(children = context_info)]
                    ),
                    dcc.Tab(
                        id="Table-tab",
                        label="Table Comparing Males and Females",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=[
                            dcc.Graph(figure=table)],
                    ),
                    dcc.Tab(
                        id="Bar-tab",
                        label="Interactive Level of Agreement by Selected Factor Bar Plot",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=[
                            html.Label('Please Select A Question',style={'padding-top':'2.5%','fontWeight': 'bold'}),
                            dcc.Dropdown(id='question',options=['Job Satisfaction', 'Working Mother Being Able to Have A Good Relatinship with Child', 
                                          'Male Should be the Breadwinner', 'Men are Better Suited for Politics', 'Preschooler Suffers if a Mother Works', 
                                          'Family Life Suffers When Men Overwork'], value='Male Should be the Breadwinner'),
                            html.Label('Please Select A Factor to Group By',style={'padding-top':'3.5%','fontWeight': 'bold'}),
                            dcc.Dropdown(id='factor',options=['Sex','Region','Year of Education'], value='Sex'),
                            dcc.Graph(id='graph')],
                    ),
                    dcc.Tab(
                        id="Scat-tab",
                        label="Income vs Occupational Prestige by Sex",
                        value="tab4",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=[
                            dcc.Graph(figure=fig_scat,style={
                                        'width': '50%','padding-left':'25%', 'padding-right':'25%'})],
                    ),
                    dcc.Tab(
                        id="box2-tab",
                        label="Side by Side Gender Box Plots",
                        value="tab5",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=[
                                html.Div([
                                    html.H3("Distruibtion of Income by Sex"),
                                    dcc.Graph(figure=figbox1)
                                        ], style = {'width': '50%','float':'left'}),
                                html.Div([
                                    html.H3("Distruibtion of Occupational Prestige by Sex"),
                                    dcc.Graph(figure=figbox2)
                                        ], style = {'width': '50%','float':'right'})],
                    ),
                    dcc.Tab(
                        id="fact-tab",
                        label="Distrubition of Income Based on Occuptional Category by Sex",
                        value="tab6",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        style=tab_style, 
                        selected_style=tab_selected_style,
                        children=[
                            dcc.Graph(figure=fig_box,style={
                                        'width': '50%','padding-left':'25%', 'padding-right':'25%'})],
                    ),
                ],
            )
        ],
    ),
    
])

@app2.callback(Output(component_id="graph",component_property="figure"), 
             [Input(component_id='question',component_property="value"),
              Input(component_id='factor',component_property="value")])

def make_figure(question, factor):
    qdict = {'Job Satisfaction':'sat_job', 
              'Working Mother Being Able to Have A Good Relatinship with Child':'relationship', 
              'Male Should be the Breadwinner':'male_breadwinner', 
              'Men are Better Suited for Politics':'men_bettersuited', 
              'Preschooler Suffers if a Mother Works':'child_suffer', 
              'Family Life Suffers When Men Overwork':'men_overwork'}
    key = qdict.get(question)
    gss_clean[key] = gss_clean[key].astype('category').cat.reorder_categories(['strongly agree','agree','disagree','strongly disagree'])
    
    fdict = {'Sex':'sex','Region':'region','Year of Education':'education'}
    key2 = fdict.get(factor)
    
    df = gss_clean.groupby([key2,key]).size().reset_index()
    
    fig = px.bar(df, x=key, y=0,
        labels={key:'Level of Agreement', '0' :'Number of People who Agree'},
      color=key2 ,barmode = 'group')
    
    return fig


if __name__ == '__main__':
    app2.run_server(debug=True)
