import requests
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime
from django.db import models

# TO DO : Add a gauge chart to see whether current intensity is relatively high

# These lines get the current live data. this is useful for checking forecast accuracy.
# TO DO : add in an accuracy check and display result to the frontend

# now_response = requests.get(
#     'https://api.carbonintensity.org.uk/regional/regionid/3'
# )
# now_data = now_response.json()
#
# nw_intensity = now_data['data'][0]['data'][0]['intensity']['forecast']
# fuel_name = now_data['data'][0]['data'][0]['generationmix'][-1]['fuel']
# fuel_pc = now_data['data'][0]['data'][0]['generationmix'][-1]['perc']
#
# utc_time = now_data['data'][0]['data'][0]['from']


class CarbonData(models.Model):

    title = models.CharField(max_length=200)
    text = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

    def get_data(self):
        utc_time = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%MZ')

        fcast_response = requests.get('''
            https://api.carbonintensity.org.uk/regional/intensity/{}/fw24h/regionid/3
            '''.format(utc_time)
                                      )
        fcast_data = fcast_response.json()

        times = []
        intensities = []
        wind = []
        nuclear = []
        gas = []
        solar = []
        # quite risky positional references here, TO DO : make it safer
        for interval in range(0, 40):
            times.append(fcast_data['data']['data'][interval]['from'])
            intensities.append(fcast_data['data']['data'][interval]['intensity']['forecast'])
            wind.append(fcast_data['data']['data'][interval]['generationmix'][-1]['perc'])
            nuclear.append(fcast_data['data']['data'][interval]['generationmix'][4]['perc'])
            gas.append(fcast_data['data']['data'][interval]['generationmix'][3]['perc'])
            solar.append(fcast_data['data']['data'][interval]['generationmix'][-2]['perc'])

        return times, intensities, wind, nuclear, gas, solar

    def gen_chart(self):
        times, intensities, wind, nuclear, gas, solar = self.get_data()
        ints_line = go.Scatter(
            x=times,
            y=intensities,
            name='Intensity',
            line={'width': 4, 'smoothing': 1.0, 'shape': 'spline'},
            yaxis='y2'
        )
        gas_bar = dict(
            x=times,
            y=gas,
            name='Gas',
            mode='lines',
            line={'width': 0},
            marker={'color': '#9db6f4'},
            stackgroup='one'
        )
        wind_bar = dict(
            x=times,
            y=wind,
            name='Wind',
            mode='lines',
            line={'width': 0},
            marker={'color': '#a0db8e'},
            stackgroup='one'
        )
        nuclear_bar = dict(
            x=times,
            y=nuclear,
            name='Nuclear',
            mode='lines',
            line={'width': 0},
            marker={'color': '#ffcb6b'},
            stackgroup='one'
        )
        solar_bar = dict(
            x=times,
            y=solar,
            name='Solar',
            mode='lines',
            line={'width': 0},
            marker={'color': '#ffff66'},
            stackgroup='one'
        )

        data_to_plot = [wind_bar, nuclear_bar, gas_bar, solar_bar, ints_line]
        layout = go.Layout(
            # strange string formatting is needed to get the plotly title right
            title='''
                    <b>     Carbon Intensity and Energy Sources </b> <br>
                NW England <br>
                (Times are UTC)
            ''',
            yaxis={
                'title': 'Contribution to Energy Generated %'
            },
            yaxis2={
                'title': 'Carbon Intensity gCO2/kWh',
                'overlaying': 'y',
                'side': 'right',
                'range': [0, max(intensities) + 10],
                'showgrid': False
            }
        )

        fig = go.Figure(data=data_to_plot, layout=layout)

        return fig

    def update_chart(self):
        chart = self.gen_chart()
        plot(
            chart,
            filename='electricplan/templates/electricplan/carbonchart.html',
            auto_open=False
        )
