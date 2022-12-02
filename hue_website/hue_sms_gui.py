import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import boto3

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
resource = boto3.resource("dynamodb", "us-east-1")
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def generate_colors_dict(colors):
    colors_dict = {}
    for color_entry in colors:
        for color, value in color_entry.items():
            color = color.title()
            if color not in colors_dict:
                colors_dict[color] = int(value)
            else:
                colors_dict[color] += int(value)
    return colors_dict


def get_color_rgb_dict():
    table = resource.Table("ColorsRGB")
    color_rgb_dict = {color_rgb['Color']: (int(color_rgb['R']), int(color_rgb['G']), int(color_rgb['B'])) for color_rgb
                      in table.scan(AttributesToGet=['Color', 'R', 'G', 'B'])["Items"]}
    return color_rgb_dict


color_RGB_dict = get_color_rgb_dict()


def generate_pie_chart_dependencies(color_RGB_dict):
    table = resource.Table("HueLightUserData")
    colors_user_data = [pn["Colors"] for pn in table.scan(AttributesToGet=['Colors'])["Items"]]
    color_totals_dict = generate_colors_dict(colors_user_data)
    labels, sizes, colors = [], [], []
    for color in color_totals_dict:
        if color_totals_dict[color] > 10:
            labels.append(color.title())
            sizes.append(color_totals_dict[color])
            colors.append(color.title())
    pie_chart_colors_RGB = {color:px.colors.label_rgb(color_RGB_dict[color]) for color in color_totals_dict}
    return labels, sizes, pie_chart_colors_RGB


def setup():
    labels, sizes, pie_chart_colors_RGB = generate_pie_chart_dependencies(color_RGB_dict)
    fig = px.pie(names=labels, values=sizes, color=labels, color_discrete_map=pie_chart_colors_RGB, width=1500,
                 height=900)

    app.layout = html.Div(children=[
        html.Div([
            html.Div([html.H1(children='Moravian Color Choices'),
                      dcc.Graph(
                          id='colors-graph',
                          figure=fig
                      ),
                      dcc.Interval(
                          id='interval-component',
                          interval=1 * 10000,
                          n_intervals=0
                      )
                      ], className='ten columns'),

        ], className='row')])


@app.callback(Output('colors-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    labels, sizes, pie_chart_colors_RGB = generate_pie_chart_dependencies(color_RGB_dict)
    fig = px.pie(names=labels, values=sizes, color=labels, color_discrete_map=pie_chart_colors_RGB)

    # change Font Size for PieChart/Legend
    fig.update_layout(font=dict(size=15))
    fig.update_traces(textposition='inside', textinfo='label+percent')
    return fig


if __name__ == '__main__':
    setup()
    app.run_server(host='0.0.0.0', port=8000)
