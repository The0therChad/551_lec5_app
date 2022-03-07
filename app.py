import dash
import dash_bootstrap_components as dbc
import altair as alt
from vega_datasets import data
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

cars = data.cars()


# app = dash.Dash(
#     __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# )

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# app.layout = html.Div("I am alive!!", style={"color": "red"})

## Plotting
def plot_cars(xcol="Horsepower", ycol="Acceleration"):
    chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(x=xcol, y=ycol, tooltip="Horsepower")
        .interactive()
    )
    return chart.to_html()


plot1 = html.Iframe(
    id="scatter",
    srcDoc=plot_cars(),
    style={"border-width": "0", "width": "100%", "height": "400px"},
)


## Layout Components

# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Page 2", href="#"),
#                 dbc.DropdownMenuItem("Page 3", href="#"),
#             ],
#             nav=True,
#             in_navbar=True,
#             label="More",
#         ),
#     ],
#     brand="NavbarSimple",
#     brand_href="#",
#     color="primary",
#     dark=True,
# )


app.layout = dbc.Container(
    [
        dbc.Alert("Hello Bootstrap!", color="success"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="ycol",
                        value="Horsepower",
                        options=[
                            {"label": i, "value": i}
                            for i in cars.columns
                            if i not in ["Name"]
                        ],
                        clearable=False,
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="xcol",
                        value="Acceleration",
                        options=[
                            {"label": i, "value": i}
                            for i in cars.columns
                            if i not in ["Name"]
                        ],
                        clearable=False,
                    )
                ),
            ]
        ),
        plot1,
    ]
)


@app.callback(
    Output("scatter", "srcDoc"), Input("xcol", "value"), Input("ycol", "value")
)
def update_output(xcol, ycol):
    return plot_cars(xcol, ycol)


if __name__ == "__main__":
    app.run_server(debug=True)
