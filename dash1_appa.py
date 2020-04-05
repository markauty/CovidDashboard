import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import covid1 as cov
import datetime
#import time
#import plotly.express as px


recalchour=2  #this is the hour of the day that the code starts displaying the days cases

DEFAULT_PLOTLY_COLORS=['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                       'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                       'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                       'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                       'rgb(188, 189, 34)', 'rgb(23, 190, 207)']
#set date
#datestr=datetime.datetime.now().strftime("%Y%m%d")
#Download population data
print(cov.download_population_Data())
#Read in the population data
populationdata=cov.Read_Population_Data('PopulationData.xls').copy()

#download latest cases
#print(cov.Download_Latest_Cases_To_File(datestr))

csvfiles=cov.Get_List_of_CSV_Files()
datestr=csvfiles[-1]
incidencelog2, proplog2,ranklog2,propbydate2=cov.Create_Incidence_Dataframes(populationdata,csvfiles)
print('ranklog2')
print(ranklog2['Date'].values.tolist())

proplog2.sort_values(by=datestr,ascending=False, inplace=True)

print('Done')




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)
app.title = 'Marks COVID Plots'

#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')


app.layout = html.Div([
    dcc.Interval(
            id='interval-component',
            interval=1*1000*60*60*24, # in milliseconds  every day
            n_intervals=0
        ),
    html.Div(id='hidden-div', style={'display':'none'}),
    html.H1(children="Mark's COVID Plots"),
    html.Label('Pick a date'),


    #add a dropdown pulling dates
    dcc.Dropdown(
        id='dropdown_dates',
        options=[
            {'label': str(i)[:10], 'value': str(i)[:10].replace("-","")} for i in ranklog2['Date'].unique()
        ],
        value=datestr,
        ),
    html.Label(children='Pick an area for more information:'),


    #add a dropdown pulling county data
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': i, 'value': i} for i in incidencelog2['AREA'].unique()
        ],
        value=['Liverpool','Wirral','Cheshire West and Chester'],multi=True,
        ),



    #show the chart of all areas infection values for date
    dcc.Graph(
        id='main_chart_graph',
    ),



    #show the chart of areas over time
    dcc.Graph(id='live-update-graph'),


    #show the chart of rank positions over time
    dcc.Graph(id='live-update-graph2'),
])


#Callbacks



## Callback for proportion by date chart.
@app.callback(
    Output(component_id='live-update-graph', component_property='figure'),
    [Input('dropdown', 'value'), Input('dropdown_dates','value')]
)
def update_output_div(input_value1,value2):
    if input_value1=='':
        input_value1='Barnet'
    mylist=[]
    for n in input_value1:
        mylist.append(dict(x=propbydate2['Date'],name=n,
                    y=propbydate2[n],
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },

                ))
    fig={
            'data': mylist,
            'layout': dict(
                xaxis={'title': 'Date','type': 'category'},
                yaxis={'title': '%'},
                margin={'l': 40, 'b': 40, 't': 50, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                title= 'Recorded Infections % of population'
            )
        }
    return fig



## Callback for ranking by date chart.
@app.callback(
    Output(component_id='live-update-graph2', component_property='figure'),
    [Input('dropdown', 'value'), Input('dropdown_dates','value')]
)
def update_output_div_copy(input_value1, value2):
    if input_value1=='':
        input_value1='Barnet'
    mylist=[]
    for n in input_value1:
        mylist.append(dict(x=ranklog2['Date'],name=n,
                    y=ranklog2[n],
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                ))
    fig={
            'data': mylist,

            'layout': dict(
                xaxis={'title': 'Date','type': 'category'},
                yaxis={'title': 'rank position','autorange': "reversed"},
                margin={'l': 40, 'b': 40, 't': 50, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                title='Rank relative to other areas',

            )
        }
    return fig





## Callback for infection percentage by area.
@app.callback(
    Output(component_id='main_chart_graph', component_property='figure'),
    [Input(component_id='dropdown_dates', component_property='value'),
    Input('dropdown', 'value')]
)
def update_mainchart_div(input_value,selected_areas):
    proplog2.sort_values(by=input_value,ascending=False, inplace=True)
    areaslist=proplog2['AREA'].tolist()

    #get position of key values. Get number of columns
    #change colour accordingly.
    colours=['lightblue'] * len(areaslist)
    colour=0
    for n in selected_areas:
        for m in range(len(areaslist)):
            if areaslist[m]==n:
                colours[m]=DEFAULT_PLOTLY_COLORS[colour]
                if colour==9:
                    colour==0
                else:
                    colour +=1

    figure={
            'data': [go.Bar(x=proplog2['AREA'], y=proplog2[input_value], marker=dict(color=colours))],
            'layout':
            go.Layout(title='Recorded Infections percent of Population ' + input_value,
                      barmode='group',
                      xaxis=dict(tickangle=-45),
                      margin={'l': 40, 'b': 150, 't': 50, 'r': 10},)
        }

    return figure

#try  to make auto-updating
@app.callback(Output(component_id='dropdown_dates',component_property='options'),
              [Input('interval-component', 'n_intervals')])
def update_database(n):
    #only do anything at specific hour of the day
    curr_hour = datetime.now().hour
    if curr_hour==recalchour:
        csvfiles=cov.Get_List_of_CSV_Files()
        datestr=csvfiles[-1]
        global incidencelog2, proplog2,ranklog2,propbydate2
        incidencelog2, proplog2,ranklog2,propbydate2=cov.Create_Incidence_Dataframes(populationdata,csvfiles)
        proplog2.sort_values(by=datestr,ascending=False, inplace=True)
        return [{'label': str(i)[:10], 'value': str(i)[:10].replace("-","")} for i in ranklog2['Date'].unique()]



if __name__ == '__main__':
    print("got here")

    app.run_server(debug=True)
