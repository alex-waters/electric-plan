import requests
import datetime as dt
from PIL import Image, ImageDraw, ImageFont

api_url = '''https://api.octopus.energy/v1/products/SILVER-24-07-01/electricity-tariffs/E-1R-SILVER-24-07-01-G/standard-unit-rates/'''

oct_response = requests.get(str(api_url))
oct_data = oct_response.json()

print_queue = []
for r in oct_data['results'][0:5]:
    record_date = dt.datetime.strptime(
        r['valid_to'][0:10], '%Y-%m-%d'
    ).date()
    if record_date >= dt.datetime.today().date():
        print_queue.append(list(
            [dt.datetime.strftime(record_date, '%A %d %b'),
             round(float(r['value_inc_vat']))]
        ))
print_queue.reverse()       # reverse is for printed image to have asc dates

im = Image.new(mode='RGB', size=(1000, 300), color=(255,255,255))
fnt = (ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 40),
       ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 45)
)
for p in enumerate(print_queue):        # enumeration is to calc the y position in the image
    y_pos = p[0]*50
    ImageDraw.Draw(im).text(
        xy=(0,y_pos),text=str(p[1][0]), fill=(1,1,1) ,font=fnt[0])
    ImageDraw.Draw(im).text(
        xy=(350,y_pos),text=str(p[1][1]), fill=(85,119,109) ,font=fnt[1])

im.save('/home/anw/mysite/electric-plan/static/elec_prices.png')
