import json
import numpy
import random
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
from sklearn.linear_model import LinearRegression

# set the width of the image files written out
pio.kaleido.scope.default_width = 1500

# Read in the sourcedata
measures_file = open('/home/anw/mysite/electric-plan/DATA/measure_data.txt')
measures = json.load(measures_file)

activity_dates = []
steps = []
active_prop = []
intense_prop = []
activity = []
for d in measures['body']['activities']:
    activity_dates.append(d['date'])
    steps.append(d['steps'])
    activity.append(d['active']) if int(d['active']) > 0 else activity.append(0)
    try:
        active_prop.append(d['active']/(d['soft'] + d['moderate'] + d['intense']))
        intense_prop.append(d['intense']/(d['soft'] + d['moderate'] + d['intense']))
    except ZeroDivisionError:
        active_prop.append(0)
        intense_prop.append(0)
inactive_prop = [1-(x+y) for x, y in [x for x in zip(active_prop, intense_prop)]]

# round the figures to improve plotly visuals
active_prop = [round(x*100) for x in active_prop]
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
days_to_vis = 15 + datetime.today().weekday()
steps_plot = go.Figure(data=[
    go.Bar(
        name='Steps',
        x=activity_dates[-days_to_vis:],
        y=cleaned_steps[-days_to_vis:],
        text=cleaned_steps[-days_to_vis:]
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
    plot_bgcolor='#ffffff',
    hovermode='x unified'
)
steps_plot.update_xaxes(
    dtick="D1",
    tickformat="%A<br>%d %b",
    fixedrange=True
)
steps_plot.update_yaxes(
    fixedrange=True,
    range=[0, max(cleaned_steps[-days_to_vis:])*1.2]
)
steps_plot.write_image('/home/anw/mysite/electric-plan/static/daily_steps.png')

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
    hovermode='x unified'
)
lt_steps_plot.update_xaxes(
    fixedrange=True
)
lt_steps_plot.update_yaxes(
    fixedrange=True
)
lt_steps_plot.write_image('/home/anw/mysite/electric-plan/static/long_term_steps.png')

# recent proportion of day being active
prop_act_plot = go.Figure(data=[
    go.Bar(
        name='Level of Activity',
        x=activity_dates[-days_to_vis:],
        y=active_prop[-days_to_vis:]
    )
])
prop_act_plot.update_traces(
    marker_color='#6D9476'
)
prop_act_plot.update_layout(
    plot_bgcolor='#ffffff',
    hovermode='x unified'
)
prop_act_plot.update_xaxes(
    fixedrange=True
)
prop_act_plot.update_yaxes(
    fixedrange=True
)
prop_act_plot.write_image('/home/anw/mysite/electric-plan/static/prop_act.png')

# long term absolute activity levels

# remove outliers from activity so overall trend easier to see
smooth_act = [x if x in range(0, 12001) else 3000 for x in activity]

time_passage = [(activity_dates.index(x)-len(activity_dates))*-1 for x in activity_dates]
straight = LinearRegression().fit(
    numpy.array(time_passage).reshape(-1, 1),
    smooth_act
)
straight_predicts = straight.predict(numpy.array(time_passage).reshape(-1, 1))


# create function to return Simple Moving Av
def sma(data, lag=10):
    av_values = []
    for i in range(lag):
        av_values.append(numpy.nan)
    for i in range(lag, len(data)):
        av_values.append(numpy.mean(data[i-lag:i]))
    return numpy.array(av_values)


mv_avg_activity = sma(smooth_act)

lt_act_plot = go.Figure(data=[
    go.Scatter(
        name='Long Term Activity',
        x=activity_dates,
        y=activity,
        mode='markers',
        marker={
            'color': ['#F199AD' if a>=1800 else '#99f1dd' for a in activity],
            'size': [10 for a in activity]
        }
    )
])
lt_act_plot.add_trace(go.Scatter(
    name='Trend',
    x=activity_dates,
    y=straight_predicts,
    mode='lines',
    marker_color='#415846'
))
lt_act_plot.add_trace(go.Scatter(
    name='Poly Trend',
    x=activity_dates,
    y=mv_avg_activity,
    mode='lines',
    marker_color='#202c23'
))
lt_act_plot.add_hline(
    name='WHO Min',
    y=1800,
    line_dash='dot',
    line_color='red'
)
lt_act_plot.update_layout(
    plot_bgcolor='#ffffff',
    hovermode='x unified'
)
lt_act_plot.update_yaxes(
    autorangeoptions={'maxallowed':15000}
)
lt_act_plot.write_html('/home/anw/mysite/electric-plan/static/long_term_activity.html')
