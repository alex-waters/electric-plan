from django.db import models
from django.utils import timezone
import requests

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