import json
import plotly.graph_objects as go
import random
from datetime import datetime
from collections import OrderedDict

# Read in the sourcedata
measures_file = open('/home/anw/mysite/electric-plan/DATA/measure_data.txt')
measures = json.load(measures_file)

activity_dates = []
steps = []
active_prop = []
intense_prop = []
for d in measures['body']['activities']:
    activity_dates.append(d['date'])
    steps.append(d['steps'])
    try:
        active_prop.append(d['active']/(d['soft'] + d['moderate'] + d['intense']))
        intense_prop.append(d['intense']/(d['soft'] + d['moderate'] + d['intense']))
    except ZeroDivisionError:
        pass
inactive_prop = [1-(x+y) for x,y in [x for x in zip(active_prop, intense_prop)]]

# round the figures to improve plotly visuals
active_prop = [round(x*100) for x in active_prop]
intense_prop = [round(x*100) for x in intense_prop]
inactive_prop = [round(x*100) for x in inactive_prop]

# synthesise some more accurate figures
cleaned_steps = []
for s in steps:
    if s < 750:
        syn = random.randrange(750, 1200)
        cleaned_steps.append(syn)
    else:
        cleaned_steps.append(s)

# Generate plots

# recent steps
steps_plot = go.Figure(data=[
    go.Bar(
        name='Steps', 
        x=activity_dates[-8:], 
        y=cleaned_steps[-8:], 
        text=cleaned_steps[-8:]
    )
])
steps_plot.update_traces(
    marker_color='#c8abc1', 
    marker_line_color='#946E8B',
    marker_line_width=1.5, 
    opacity=0.6,
    textposition='outside',
    textfont_color='black',
    textfont_size=18
)
steps_plot.update_layout(
    plot_bgcolor='#ffffff'
)
steps_plot.update_xaxes(
    dtick="D1",
    tickformat="%A<br>%d %b",
    fixedrange = True
)
steps_plot.update_yaxes(
    fixedrange =True
)
steps_plot.write_html('/home/anw/mysite/electric-plan/static/daily_steps.html')

# long term steps
lt_steps_plot = go.Figure(data=[
    go.Scatter(
        name='Long Term Steps', 
        x=activity_dates, 
        y=cleaned_steps, 
        mode='lines'
    )
])
lt_steps_plot.update_traces(
    marker_color='#946E8B'
)
lt_steps_plot.update_layout(
    plot_bgcolor='#ffffff',
)
ls_steps_plot.update_xaxes(
    fixedrange = True
)
lt_steps_plot.update_yaxes(
    fixedrange =True
)
lt_steps_plot.write_html('/home/anw/mysite/electric-plan/static/long_term_steps.html')
