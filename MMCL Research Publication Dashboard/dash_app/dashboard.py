import dash
from dash.dependencies import Input, Output, State
from app.data_loader import DataLoader
from dash import Dash, dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px

class DashApp:
    def __init__(self, server):
        self.server = server
        self.app = Dash(__name__, server=server, routes_pathname_prefix='/dash/', external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.data_loader = DataLoader('app/data/AcadResearchDatasetWithCountry.csv')
        self.data_loader.connect()
        self.PLOTLY_LOGO = "https://i.imghippo.com/files/8hU5H1724158029.png"
        self.palette_dict = {
            'MITL': 'red',
            'ETYCB': 'yellow',
            'CCIS': 'green',
            'CAS': 'blue',
            'CHS': 'orange'
        }
        self.all_sdgs = [
            'SDG 1', 'SDG 2', 'SDG 3', 'SDG 4', 'SDG 5', 'SDG 6', 'SDG 7', 
            'SDG 8', 'SDG 9', 'SDG 10', 'SDG 11', 'SDG 12', 'SDG 13', 
            'SDG 14', 'SDG 15', 'SDG 16', 'SDG 17'
        ]
        self.all_status = [
            'WAITING FOR PUBLICATION', 'UNDER EVALUATION', 
            'TO BE PRESENTED', 'ACCEPTED', 'PUBLISHED'
        ]

        self.setup_layout()
        self.register_callbacks()

    def get_total_counts(self):
        count = len(self.data_loader.get_unique_values('Title'))
        return str(count)

    def setup_layout(self):
        navbar = dbc.Navbar(
            [
                dbc.NavbarBrand(
                    html.Img(src=self.PLOTLY_LOGO, height="50px"),
                    href="#",
                    style={"display": "flex", "alignItems": "center", "margin":"0px 0px 0px 30px"}
                ),
                dbc.Nav(
                    [
                        dbc.NavLink("Home", external_link=True, href="/", style={"color": "white", "margin": "10px"}),
                        dbc.NavLink("Analytics", active=True, href="/dash", style={"color": "white", "margin": "10px"}),
                    ],
                    navbar=True,
                    pills=True
                ),
                dbc.Col(width=9),
                dbc.Col(
                    dbc.DropdownMenu(
                        children=[dbc.DropdownMenuItem("Sign out", href="#")],
                        nav=True,
                        in_navbar=True,
                        label=html.Img(src=self.PLOTLY_LOGO, height="40px", style={"borderRadius": "50%"}),  
                        style={"color": "white", "display": "flex", "alignItems": "center", "textAlign": "right"}
                    ),
                    width="auto"
                ),
            ],
            color="#2e266d",
            dark=True,
            style={"height": "60px", "padding": "15px", "width": "100vw", "position": "fixed", "top": "0", "left": "0", "zIndex": "1000"}
        )

        college = html.Div(
            [
                dbc.Label("Select College:"),
                dbc.Checklist(
                    id="college",
                    options=[{'label': value, 'value': value} for value in self.data_loader.get_unique_values('College')],
                    value=self.data_loader.get_unique_values('College'),
                    inline=True,
                ),
            ],
            className="mb-4",
        )

        status = html.Div(
            [
                dbc.Label("Select Status:"),
                dbc.Checklist(
                    id="status",
                    options=[{'label': value, 'value': value} for value in self.data_loader.get_unique_values('PUBLISHED')],
                    value=self.data_loader.get_unique_values('PUBLISHED'),
                    inline=True,
                ),
            ],
            className="mb-4",
        )

        slider = html.Div(
            [
                dbc.Label("Select Years"),
                dcc.RangeSlider(
                    min=self.data_loader.get_min_value('Year'), 
                    max=self.data_loader.get_max_value('Year'), 
                    step=1, 
                    id="years",
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    value=[self.data_loader.get_min_value('Year'), self.data_loader.get_max_value('Year')],
                    className="p-0",
                ),
            ],
            className="mb-4",
        )

        button = html.Div(
            [
                dbc.Button("Reset", color="primary", id="reset_button"),
            ],
            className="d-grid gap-2",
        )

        grid = dag.AgGrid(
            id="grid",
            columnDefs=[{"field": col} for col in self.data_loader.get_all_data().columns],
            rowData=self.data_loader.get_all_data().to_dict("records"),
            defaultColDef={
                "flex": 1,
                "minWidth": 120,
                "sortable": True,
                "resizable": True,
                "filter": True
            },
            dashGridOptions={"rowSelection": "multiple"},
        )

        controls = dbc.Card(
            [
                html.H4("Filters", style={"margin": "20px 0px"}),
                college, status, slider, button
            ],
            body=True,
            style={"height": "100vh", "display": "flex", "flexDirection": "column"}
        )
        upper_dash = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Total Research Publications", style={'textAlign': 'center'}),
                        html.H2(str(len(self.data_loader.get_all_data())), style={'textAlign': 'center', 'fontSize': '60px'}),
                    ], style={'border': '1px solid black', 'padding': '20px', 'height': '100%'})
                ], width=3),

                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H6("SCOPUS", style={'textAlign': 'center'}),
                            html.H3(str(len(self.data_loader.filter_data('Scopus or Non-Scopus', 'Scopus', invert=False))), style={'textAlign': 'center'})
                        ], style={'textAlign': 'center', 'border': '1px solid black', 'padding': '20px'}), width=3),
                        
                        dbc.Col(html.Div([
                            html.H6("JOURNAL", style={'textAlign': 'center'}),
                            html.H3(str(len(self.data_loader.filter_data('Publication Format', 'Proceeding', invert=True))), style={'textAlign': 'center'})
                        ], style={'textAlign': 'center', 'border': '1px solid black', 'padding': '20px'}), width=3),
                        
                        dbc.Col(html.Div([
                            html.H6("PUBLISHED", style={'textAlign': 'center'}),
                            html.H3(str(len(self.data_loader.filter_data('PUBLISHED','PUBLISHED',invert=False))), style={'textAlign': 'center'})
                        ], style={'textAlign': 'center', 'border': '1px solid black', 'padding': '20px'}), width=3),

                        dbc.Col(html.Div([
                            html.H6("ON-GOING", style={'textAlign': 'center'}),
                            html.H3(str(len(self.data_loader.filter_data_by_list('PUBLISHED',['PUBLISHED','ACCEPTED'],invert=True))), style={'textAlign': 'center'})
                        ], style={'textAlign': 'center', 'border': '1px solid black', 'padding': '20px'}), width=3),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H6("NON-SCOPUS", style={'textAlign': 'center'}),
                            html.H3(str(len(self.data_loader.filter_data('Scopus or Non-Scopus', 'Scopus', invert=True))), style={'textAlign': 'center'})
                        ], style={'textAlign': 'center', 'border': '1px solid black', 'padding': '20px'}), width=3),
                        
                        dbc.Col(html.Div([
                            html.H6("PROCEEDINGS", style={'textAlign': 'center'}),
                            html.H3(str(len(self.data_loader.filter_data('Publication Format', 'Proceeding', invert=False))), style={'textAlign': 'center'})
                        ], style={'textAlign': 'center', 'border': '1px solid black', 'padding': '20px'}), width=3),
                        
                        dbc.Col(html.Div([
                            html.H6("NEW", style={'textAlign': 'center'}),
                            html.H3(len(self.data_loader.filter_data('PUBLISHED','ACCEPTED',invert=False)), style={'textAlign': 'center'})
                        ], style={'textAlign': 'center', 'border': '1px solid black', 'padding': '20px', 'height': '100%'}), width=6),
                    ]),
                ], width=9),
            ])
        ], style={'marginBottom': '20px'})

        main_dash = dbc.Container([
            # Added by Nicole Cabansag
            dbc.Row([
                dbc.Col([
                    html.Div(id='world_map_chart', children=[])
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='college_line_plot'), width=8, style={"height": "400px", "overflow": "hidden"}),
                dbc.Col(dcc.Graph(id='college_pie_chart'), width=4, style={"height": "400px", "overflow": "hidden"})
            ], style={"margin": "20px", "padding": "10px"}),

            dbc.Row([
                dbc.Col(dcc.Graph(id='scopus_bar_plot', style={"margin": "5px"}), width=6, style={"height": "450px", "overflow": "hidden", "border": "1px solid #ddd", "padding": "20px"}),
                dbc.Col(dcc.Graph(id='publication_format_bar_plot', style={"margin": "5px"}), width=6, style={"height": "450px", "overflow": "hidden", "border": "1px solid #ddd", "padding": "20px"}),
            ])
        ], fluid=True)

        tab2_content = dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Graph(id='sdg_bar_chart'), width=12, style={"height": "400px", "overflow": "hidden"}),
                dbc.Col(
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='author_contribution_chart'), width=6,style={"height": "400px", "overflow": "hidden"}),
                        dbc.Col(dcc.Graph(id='research_status_chart'), width=6,style={"height": "400px", "overflow": "hidden"})]

                    ),
                    width=12,style={"height": "400px", "overflow": "hidden", "marginTop":"20px"}
                )
                
            ], style={"marginTop": "20px"}),
        ])

        tab1 = dbc.Tab(main_dash, label="Overview")
        tab2 = dbc.Tab(tab2_content, label="Contributions")
        tab3 = dbc.Tab([grid], label="Grid", className="p-4")
        tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3]))

        self.app.layout = html.Div([
            navbar,
            dbc.Container(
                [
                    dbc.Row([
                        dbc.Col(controls, width=2),
                        dbc.Col([upper_dash,tabs], width=10),
                    ], style={"paddingTop": "60px"})
                ],
                fluid=True,
                className="dbc dbc-ag-grid",
                style={"margin": "20px", "overflow": "hidden"}
            )
        ])

    def update_world_map(self, selected_colleges, selected_status, selected_years): # Added by Nicole Cabansag
        df = self.data_loader.get_filtered_data(selected_colleges, selected_status, selected_years)

        if 'Country' not in df.columns or df['Country'].isnull().all():
            return dcc.Graph()  

        country_counts = df.groupby('Country').size().reset_index(name='Count')

        fig = px.choropleth(
            country_counts,
            locations='Country',  
            locationmode='country names', 
            color='Count',  
            hover_name='Country',  
            color_continuous_scale=px.colors.sequential.Plasma,  
            title="International Conference Distribution"
        )

        fig.update_layout(
            width=1300,  # Adjust width
            height=600,  # Adjust height
            geo=dict(showframe=False, showcoastlines=False),
            title_x=0.5  
        )


        return dcc.Graph(figure=fig)
    
    def update_line_plot(self, selected_colleges, selected_status, selected_years):
        df = self.data_loader.get_filtered_data(selected_colleges, selected_status, selected_years)
        
        if len(selected_colleges) == 1:
            grouped_df = df.groupby(['Program/Cluster', 'Year']).size().reset_index(name='TitleCount')
            color_column = 'Program/Cluster'
            title = f'Number of Publications for {selected_colleges[0]}'
        else:
            grouped_df = df.groupby(['College', 'Year']).size().reset_index(name='TitleCount')
            color_column = 'College'
            title = 'Number of Publications per College'

        fig_line = px.line(
            grouped_df, 
            x='Year', 
            y='TitleCount', 
            color=color_column, 
            markers=True,
            color_discrete_map=self.palette_dict
        )
        
        fig_line.update_layout(
            title=title,
            xaxis_title='Academic Year',
            yaxis_title='Number of Publications',
            template='plotly_white',
            margin=dict(l=0, r=0, t=30, b=0),
            height=400,
            showlegend=True  
        )

        return fig_line

    def update_pie_chart(self, selected_colleges, selected_status, selected_years):
        df = self.data_loader.get_filtered_data(selected_colleges, selected_status, selected_years)
        
        if len(selected_colleges) == 1:
            college_name = selected_colleges[0]
            filtered_df = df[df['College'] == college_name]
            detail_counts = filtered_df.groupby('Program/Cluster').size()
            title = f'Number of Publications for {college_name}'
        else:
            detail_counts = df.groupby('College').size()
            title = 'Number of Publications per College'
        
        fig_pie = px.pie(
            names=detail_counts.index,
            values=detail_counts,
            color=detail_counts.index,
            color_discrete_map=self.palette_dict,
            labels={'names': 'Category', 'values': 'Number of Publications'},
        )

        fig_pie.update_layout(
            title=title,
            template='plotly_white',
            margin=dict(l=0, r=0, t=30, b=0),
            height=400
        )

        return fig_pie

    def update_scopus_bar_plot(self, selected_colleges, selected_status, selected_years): # Modified by Nicole Cabansag
        df = self.data_loader.get_filtered_data(selected_colleges, selected_status, selected_years) 
        grouped_df = df.groupby(['College', 'Scopus or Non-Scopus', 'Publication Format']).size().reset_index(name='Count')
        grouped_df['Scopus & Format'] = grouped_df['Scopus or Non-Scopus'] + ' (' + grouped_df['Publication Format'] + ')'

        fig_bar = px.bar(
            grouped_df,
            x='College',
            y='Count',
            color='Scopus & Format', 
            barmode='stack',  
            labels={'Count': 'Number of Research Papers'},
            title='Scopus vs. Non-Scopus per College with Publication Format'
        )

        fig_bar.update_layout(
            xaxis_title='College',
            yaxis_title='Number of Research Papers',
            xaxis_tickangle=-45,
            template='plotly_white',
            margin=dict(l=0, r=0, t=30, b=0),
            height=400
        )

        return fig_bar

    def update_publication_format_bar_plot(self, selected_colleges, selected_status, selected_years):
        df = self.data_loader.get_filtered_data(selected_colleges, selected_status, selected_years)
        
        grouped_df = df.groupby(['Publication Format', 'College']).size().reset_index(name='Count')
        
        fig_bar = px.bar(
            grouped_df,
            x='College',
            y='Count',
            color='Publication Format',
            barmode='group',
            labels={'Count': 'Number of Publications'},
            title='Journal vs. Proceeding Research Papers per College'
        )

        fig_bar.update_layout(
            xaxis_title='College',
            yaxis_title='Number of Publications',
            xaxis_tickangle=-45,
            template='plotly_white',
            margin=dict(l=0, r=0, t=30, b=0),
            height=400
        )

        return fig_bar
    
    def update_author_contribution_chart(self, selected_colleges, selected_status, selected_years):
        df = self.data_loader.get_filtered_data(selected_colleges, selected_status, selected_years)

        if 'Authors' not in df.columns:
            return px.bar(title='No Author Data Available')

        author_contributions = df['Authors'].value_counts().reset_index()
        author_contributions.columns = ['Authors', 'Count']

        top_10_authors = author_contributions.head(10)

        fig_bar = px.bar(
            top_10_authors,
            x='Count',
            y='Authors',
            orientation='h',  
            title='Top 10 Author Contributions',
            labels={'Count': 'Number of Contributions', 'Author': 'Author'},
            text='Count'
        )

        fig_bar.update_layout(
            xaxis_title='Number of Contributions',
            yaxis_title='Author',
            yaxis=dict(autorange='reversed'),
            template='plotly_white',
            margin=dict(l=0, r=0, t=30, b=0),
            height=400
        )

        return fig_bar
    
    def process_sdgs(self, sdgs):
        """Process SDGs by splitting and stripping whitespace."""
        return [sdg.strip() for sdg in sdgs.split(';')]
    
    def update_sdg_chart(self, selected_colleges, selected_status, selected_years):
        df = self.data_loader.get_filtered_data(selected_colleges, selected_status, selected_years)
        
        if df.empty:
            print("DataFrame is empty after filtering")
            return px.bar(title="No data available")


        df_copy = df.copy()

        df_copy = df_copy.set_index('College')['SDG Targeted'].str.split(';').apply(pd.Series).stack().reset_index(name='SDG_Targeted')
        df_copy['SDG_Targeted'] = df_copy['SDG_Targeted'].str.strip()
        df_copy = df_copy.drop(columns=['level_1'])
        sdg_count = df_copy.groupby(['SDG_Targeted', 'College']).size().reset_index(name='Count')
        pivot_df = sdg_count.pivot(index='SDG_Targeted', columns='College', values='Count').reindex(self.all_sdgs).fillna(0)
        pivot_df['Total'] = pivot_df.sum(axis=1)
        pivot_df = pivot_df.sort_values(by='Total', ascending=False).drop(columns='Total')
        pivot_df = pivot_df.reindex(self.all_sdgs)

        if pivot_df.empty:
            print("Pivot DataFrame is empty after processing")
            return px.bar(title="No data available")

        fig = go.Figure()

        for college in pivot_df.columns:
            fig.add_trace(go.Bar(
                y=pivot_df.index,
                x=pivot_df[college],
                name=college,
                orientation='h',
                marker_color=self.palette_dict.get(college, 'grey') 
            ))

        fig.update_layout(
            barmode='stack',  
            xaxis_title='Count',
            yaxis_title='SDG Targeted',
            title='Colleges Targeting Each SDG',
            yaxis=dict(
                autorange='reversed',  
                tickvals=self.all_sdgs,  
                ticktext=self.all_sdgs  
            )
        )
        
        return fig

    def update_research_status_chart(self, selected_colleges, selected_status, selected_years):
        df = self.data_loader.get_filtered_data(selected_colleges, selected_status, selected_years)
        
        if df.empty:
            print("DataFrame is empty after filtering")
            return px.bar(title="No data available")

        status_count = df.groupby(['PUBLISHED', 'College']).size().reset_index(name='Count')
        pivot_df = status_count.pivot(index='PUBLISHED', columns='College', values='Count').reindex(self.all_status).fillna(0)
        pivot_df['Total'] = pivot_df.sum(axis=1)
        pivot_df = pivot_df.sort_values(by='Total', ascending=False).drop(columns='Total')
        pivot_df = pivot_df.reindex(self.all_status)

        if pivot_df.empty:
            print("Pivot DataFrame is empty after processing")
            return px.bar(title="No data available")

        fig = go.Figure()

        for college in pivot_df.columns:
            fig.add_trace(go.Bar(
                y=pivot_df.index,
                x=pivot_df[college],
                name=college,
                orientation='h',
                marker_color=self.palette_dict.get(college, 'grey') 
            ))

        fig.update_layout(
            barmode='stack',  
            xaxis_title='Count',
            yaxis_title='Research Status',
            title='Colleges Research Status',
            yaxis=dict(
                autorange='reversed',  
                tickvals=self.all_status,  
                ticktext=self.all_status  
            )
        )
        
        return fig
    
    def register_callbacks(self):
        self.app.callback( # Added by Nicole Cabansag
            Output('world_map_chart', 'children'),
            [Input('college', 'value'),
             Input('status', 'value'),
             Input('years', 'value')]
        )(self.update_world_map)

        self.app.callback(
            Output('college_line_plot', 'figure'),
            [
                Input('college', 'value'),
                Input('status', 'value'),
                Input('years', 'value')
            ]
        )(self.update_line_plot)

        self.app.callback(
            Output('college_pie_chart', 'figure'),
            [
                Input('college', 'value'),
                Input('status', 'value'),
                Input('years', 'value')
            ]
        )(self.update_pie_chart)

        self.app.callback(
            Output('scopus_bar_plot', 'figure'),
            [
                Input('college', 'value'),
                Input('status', 'value'),
                Input('years', 'value')
            ]
        )(self.update_scopus_bar_plot)

        self.app.callback(
            Output('publication_format_bar_plot', 'figure'),
            [Input('college', 'value'), 
             Input('status', 'value'), 
             Input('years', 'value')]
        )(self.update_publication_format_bar_plot)

        self.app.callback(
            Output('grid', 'rowData'),
            [
                Input('college', 'value'),
                Input('status', 'value'),
                Input('years', 'value')
            ]
        )(self.update_grid)
        self.app.callback(
            Output('author_contribution_chart', 'figure'),
            [
                Input('college', 'value'),
                Input('status', 'value'),
                Input('years', 'value')
            ]
        )(self.update_author_contribution_chart)

        self.app.callback(
            Output('sdg_bar_chart', 'figure'),
            [
                Input('college', 'value'),
                Input('status', 'value'),
                Input('years', 'value')
            ]
        )(self.update_sdg_chart)

        self.app.callback(
            Output('research_status_chart', 'figure'),
            [
                Input('college', 'value'),
                Input('status', 'value'),
                Input('years', 'value')
            ]
        )(self.update_research_status_chart)


    def update_grid(self, selected_colleges, selected_status, selected_years):
        df = self.data_loader.get_filtered_data(selected_colleges, selected_status, selected_years)
        return df.to_dict("records")

    def run(self, debug=False):
        self.app.run_server(debug=debug)

def create_dash_app(flask_server):
    dash_app = DashApp(flask_server)
    return dash_app.app