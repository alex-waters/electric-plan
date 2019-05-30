from django.db import models
from django.utils import timezone
import requests

from plotly.offline import init_notebook_mode, plot, iplot
import plotly.graph_objs as go

now_response = requests.get(
    'https://api.carbonintensity.org.uk/regional/regionid/3'
)
now_data = now_response.json()

nw_intensity = now_data['data'][0]['data'][0]['intensity']['forecast']
fuel_name = now_data['data'][0]['data'][0]['generationmix'][-1]['fuel']
fuel_pc = now_data['data'][0]['data'][0]['generationmix'][-1]['perc']

utc_time = now_data['data'][0]['data'][0]['from']

fcast_response  = requests.get('''
    https://api.carbonintensity.org.uk/regional/intensity/{}/fw24h/regionid/3
    '''.format(utc_time)
)
fcast_data = fcast_response.json()

fcast_display = []
for interval in range(0,20):
    time = fcast_data['data']['data'][interval]['from']
    intensity = fcast_data['data']['data'][interval]['intensity']['forecast']
    wind_pc = fcast_data['data']['data'][interval]['generationmix'][-1]['perc']

    fcast_display.append(time[11:] + ' : ' + str(intensity) + ' ,  ' + str(wind_pc))

times = []
intensities = []
wind = []
nuclear = []
gas = []
for interval in range(0,20):
    times.append(fcast_data['data']['data'][interval]['from'])
    intensities.append(fcast_data['data']['data'][interval]['intensity']['forecast'])
    wind.append(fcast_data['data']['data'][interval]['generationmix'][-1]['perc'])
    nuclear.append(fcast_data['data']['data'][interval]['generationmix'][4]['perc'])
    gas.append(fcast_data['data']['data'][interval]['generationmix'][3]['perc'])
    

ints_dots = go.Scatter(
    x=times,
    y=intensities,
    name='Intensity',
    yaxis='y2'
)
gas_bar = go.Bar(
    x=times,
    y=gas,
    #width=widths,
    name='Gas',
    marker={'color': '#9db6f4'}
)
wind_bar = go.Bar(
    x=times,
    y=wind,
    #width=widths,
    name='Wind',
    marker={'color': '#a5ea89'}
)
nuclear_bar = go.Bar(
    x=times,
    y=nuclear,
    #width=widths,
    name='Nuclear',
    marker={'color': '#ffcb6b'}
)

data_to_plot = [wind_bar, nuclear_bar, gas_bar, ints_dots]
layout = go.Layout(
    title='''
        <b>Carbon Intensity and Energy Sources </b> <br>
        NW England <br>
        (Times are UTC)
    ''',
    barmode='stack',
    yaxis2={
        'overlaying': 'y', 
        'side': 'right', 
        'range': [0, max(intensities)+10],
        'showgrid': False
    }
)

fig = go.Figure(data=data_to_plot, layout=layout)
plot(fig, filename='C:\\Users\\wateal\\Desktop\\electric-plan\\electricplan\\templates\\electricplan\\carbonchart.html')


class CarbonData(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    data_now = nw_intensity
    fuel_name = fuel_name
    fuel_pc = fuel_pc
    fcast_display = fcast_display

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
