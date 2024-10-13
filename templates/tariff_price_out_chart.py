import requests
import datetime as dt
from PIL import Image, ImageDraw, ImageFont

api_url = '''https://api.octopus.energy/v1/products/SILVER-24-07-01/electricity-tariffs/E-1R-SILVER-24-07-01-G/standard-unit-rates/'''

oct_response = requests.get(str(api_url))
oct_data = oct_response.json()

first_record = dt.datetime.strptime(
    oct_data['results'][0]['valid_to'][0:10], '%Y-%m-%d'
).date()

if first_record == dt.datetime.today().date():
    todays = oct_data['results'][0]['value_inc_vat']
    tmws = 'Unavailable'
elif first_record == dt.datetime.today().date() + dt.timedelta(days=1):
    todays = oct_data['results'][1]['value_inc_vat']
    tmws = oct_data['results'][0]['value_inc_vat']
else:
    todays = 'Check Elsewhere'
    tmws = 'Check Elsewhere'

todays = round(float(todays)) if type(todays) != str else todays
tmws = round(float(tmws)) if type(tmws) != str else tmws

im = Image.new(mode='RGB', size=(1000, 100), color=(255,255,255))
fnt = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 40)
ImageDraw.Draw(im).text(
    xy=(0,0),text='TODAY: '+str(todays), fill=(1,1,1) ,font=fnt)
ImageDraw.Draw(im).text(
    xy=(0,40),text='TOMORROW: '+str(tmws),fill=(1,1,1) ,font=fnt)
im.save('/home/anw/mysite/electric-plan/static/elec_prices.png')
