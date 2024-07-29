import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "absolute",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
years = list(range(2010, 2025))

colleges = ['CAS', 'CCIS', 'CHS', 'MITL', 'ETYCB', 'MITL']
options_list = [{'label': college, 'value': college} for college in set(colleges)]
options_list.insert(0, {'label': 'All', 'value': 'All'})  # Add "All" at the beginning

status = ['Published', 'For Evaluation', 'To Publish']
status_list = [{'label': status_item, 'value': status_item} for status_item in set(status)]
status_list.insert(0, {'label': 'All', 'value': 'All'}) 

sidebar = html.Div(
    [
        html.H4("📊MMCL Research Publications Dashboard", className="display-7"),
        html.Hr(),
        html.P(
            "FILTERS", className="text-muted"
        ),
        html.Div([
            html.P("Colleges", style={'margin': '0', 'padding': '0px'}),
            dcc.Checklist(
                id='college-checklist',
                options=options_list,  # Populate checklist options from the list
                value=['All'],  # Default selected value
                style={'padding':'10px'}
            ),
        ], style={'border': '2px solid black', 'margin': '5px', 'padding': '5px', 'border-radius': '10px'}),
        html.Div([
            html.P("Year", style={'margin': '0px', 'padding': '0px'}),
            dcc.RangeSlider(
                id='year-slider',
                min=min(years),
                max=max(years),
                step=1,
                value=[min(years), max(years)],
                marks={min(years): str(min(years)), max(years): str(max(years))},
                tooltip={"placement": "bottom", "always_visible": True},
            ),
        ], style={'border': '2px solid black', 'margin': '5px', 'padding': '5px', 'border-radius': '10px'}),
        html.Div([
            html.P("Status", style={'margin': '0', 'padding': '0px'}),
            dcc.Checklist(
                id='status-checklist',
                options=status_list,  # Populate checklist options from the list
                value=['All'],  # Default selected value
                style={'padding':'10px'}
            ),
        ], style={'border': '2px solid black', 'margin': '5px', 'padding': '5px', 'border-radius': '10px'})
    ],
    style=SIDEBAR_STYLE,
)

@app.callback(
    Output('college-checklist', 'value'),
    [Input('college-checklist', 'value')]
)
def update_college_checklist(selected_values):
    if "All" in selected_values:
        if len(colleges) + 1 != len(selected_values):
            return [college for college in colleges] + ['All']
        else:
            return selected_values
    else:
        return selected_values

@app.callback(
    Output('status-checklist', 'value'),
    [Input('status-checklist', 'value')]
)
def update_status_checklist(selected_values):
    if "All" in selected_values:
        if len(status) + 1 != len(selected_values):
            return [status_item for status_item in status] + ['All']
        else:
            return selected_values
    else:
        return selected_values

@app.callback(
    Output('page-content', 'children'),
    [Input('year-slider', 'value'),
     Input('college-checklist', 'value'),
     Input('status-checklist', 'value')]
)
def update_output(selected_years, college_values, status_values):
    return f'Selected Year Range: {selected_years[0]} - {selected_years[1]} | Selected Colleges: {", ".join(college_values)} | Selected Status: {", ".join(status_values)}'

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([sidebar, content])

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
