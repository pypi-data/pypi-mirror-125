import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go


def df_to_table(df):
    """Transforms a dataFrame into an html table for Dash
    """
    return html.Table(
        # Header
        [
            html.Tr([
                html.Th(col) for col in df.columns
                     ])] +

        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in df.columns
                ]
            )
            for i in range(len(df))
        ]
    )

  
def indicator(color, text, id_value):
    """returns top indicator div
    """
    return html.Div(
        [

            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id=id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",

    )


def NamedDropdown(name, **kwargs):
    return html.Div(
        style={"margin": "10px 0px"},
        children=[
            html.P(children=f"{name}", style={"margin-left": "3px"}),
            dcc.Dropdown(**kwargs),
        ],
    )


def OnOffButton(name, **kwargs):
    return html.Div(
        # style={"margin": "auto"},
        children=[
            daq.PowerButton(**kwargs)
        ],
    )


def simpleButton(name, **kwargs):
    return html.Div(
        # style={"margin": "auto"},
        children=[
            daq.StopButton(**kwargs)
        ],
    )


def circle_number(value, max_value=100):
    values = [max_value - value, value]
    colors = ['rgba(0, 0, 0, 0)', "crimson"]  # "rgb(204, 255, 255)"]
    direction = 'clockwise'
    rotation = 0 if value >= max_value / 2 else 360 / max_value * value

    data = [go.Pie(
        values=values,
        hole=.9,
        showlegend=False,
        marker={'colors': colors},
        textinfo="none",
        direction=direction,
        rotation=rotation,
    )]

    layout = go.Layout(
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        width=70,
        height=70,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[
            {
                "font": {"size": 15, "color": "crimson"},
                "showarrow": False,
                "text": value,
                "align": "center",
            },
        ],
    )
    return {"data": data, "layout": layout}
