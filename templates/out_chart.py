import requests
import pickle
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot

utc_time = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%MZ')

fcast_response = requests.get('''
    https://api.carbonintensity.org.uk/regional/intensity/{}/fw48h/regionid/3
    '''.format(utc_time)
                                )
fcast_data = fcast_response.json()

extracted = {
    'times': [],
    'intensities': [],
    'wind': [],
    'nuclear': [],
    'gas': [],
    'solar': [],
    'biomass': [],
    'coal': [],
    'hydro': [],
    'imported': []
}

for interval in fcast_data['data']['data']:

    extracted['times'].append(
        interval['from'])
    extracted['intensities'].append(
        interval['intensity']['forecast'])
    for mix in interval['generationmix']:
        try:
            extracted[mix['fuel']].append(mix['perc'])
        except KeyError:
            pass


ints_line = dict(
    x=extracted['times'],
    y=extracted['intensities'],
    name='Intensity',
    line={'width': 4, 'smoothing': 1.0, 'shape': 'spline'},
    yaxis='y2',
    marker_color='#001c49'
)
wind_bar = dict(
    x=extracted['times'],
    y=extracted['wind'],
    name='Wind',
    mode='lines',
    line={'width': 0},
    marker={'color': '#a0db8e'},
    stackgroup='one'
)
hydro_bar = dict(
    x=extracted['times'],
    y=extracted['hydro'],
    name='Hydro',
    mode='lines',
    line={'width': 0},
    marker={'color': '#a8c6db'},
    stackgroup='one'
)
solar_bar = dict(
    x=extracted['times'],
    y=extracted['solar'],
    name='Solar',
    mode='lines',
    line={'width': 0},
    marker={'color': '#ffff66'},
    stackgroup='one'
)
nuclear_bar = dict(
    x=extracted['times'],
    y=extracted['nuclear'],
    name='Nuclear',
    mode='lines',
    line={'width': 0},
    marker={'color': '#ffcb6b'},
    stackgroup='one'
)
gas_bar = dict(
    x=extracted['times'],
    y=extracted['gas'],
    name='Gas',
    mode='lines',
    line={'width': 0},
    marker={'color': '#9db6f4'},
    stackgroup='one'
)
biom_bar = dict(
    x=extracted['times'],
    y=extracted['biomass'],
    name='Biomass',
    mode='lines',
    line={'width': 0},
    marker={'color': '#ae9872'},
    stackgroup='one'
)
coal_bar = dict(
    x=extracted['times'],
    y=extracted['coal'],
    name='Coal',
    mode='lines',
    line={'width': 0},
    marker={'color': '#1e1e1e'},
    stackgroup='one'
)
imported_bar = dict(
    x=extracted['times'],
    y=extracted['imported'],
    name='Imported',
    mode='lines',
    line={'width': 0},
    marker={'color': '#848484'},
    stackgroup='one'
)


data_to_plot = [
    solar_bar, hydro_bar, wind_bar, nuclear_bar, gas_bar,
    biom_bar, coal_bar, imported_bar, ints_line
]
layout = go.Layout(
    # strange string formatting is needed to get the plotly title right
    title='''
            <b> Sources of electricity and carbon intensity </b> <br> NW England <br> (Times are UTC)
    ''',
    yaxis={
        'title': 'Electricity from this source (%)',
        'showgrid': False
    },
    yaxis2={
        'title': 'Carbon Intensity gCO2/kWh',
        'overlaying': 'y',
        'side': 'right',
        'range': [0, max(extracted['intensities']) + 10],
        'showgrid': False
    },
    plot_bgcolor='#ffffff'
)

fig = go.Figure(data=data_to_plot, layout=layout)
fig.update_layout(
    xaxis_showgrid=False, 
    yaxis_showgrid=False, 
    hovermode='x unified'
)
fig.write_html('templates/carbon_plot.html')
