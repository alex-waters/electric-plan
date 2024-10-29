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
    todays = (oct_data['results'][0]['valid_to'][0:10], oct_data['results'][0]['value_inc_vat'])
    tmws = ('Next', 'Unavailable')
elif first_record == dt.datetime.today().date() + dt.timedelta(days=1):
    todays = [oct_data['results'][1]['valid_to'][0:10], oct_data['results'][1]['value_inc_vat']]
    tmws = [oct_data['results'][0]['valid_to'][0:10], oct_data['results'][0]['value_inc_vat']]
else:
    todays = ['Not Fetched', 'Check Elsewhere']
    tmws = ['Not Fetched', 'Check Elsewhere']

todays[1] = round(float(todays[1])) if type(todays[1]) != str else todays
tmws[1] = round(float(tmws[1])) if type(tmws[1]) != str else tmws

im = Image.new(mode='RGB', size=(1000, 100), color=(255,255,255))
fnt = (ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 40),
       ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 45)
)
ImageDraw.Draw(im).text(
    xy=(0,0),text=str(todays[0]), fill=(1,1,1) ,font=fnt[0])
ImageDraw.Draw(im).text(
    xy=(250,0),text=str(todays[1]), fill=(85,119,109) ,font=fnt[1])
ImageDraw.Draw(im).text(
    xy=(0,40),text=str(tmws[0]),fill=(1,1,1) ,font=fnt[0])
ImageDraw.Draw(im).text(
    xy=(250,40),text=str(tmws[1]), fill=(85,119,109) ,font=fnt[1])
im.save('/home/anw/mysite/electric-plan/static/elec_prices.png')
