import json
import numpy
import pandas as pd
import random
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# set the width of the image files written out
pio.kaleido.scope.default_width = 1500

# Read in the sourcedata
measures_file = open('/home/anw/mysite/electric-plan/DATA/measure_data.txt')
measures = json.load(measures_file)
# Turn measures['body']['activities'] into a daily DataFrame and fill missing dates with zero rows

measures_df = pd.DataFrame(measures["body"]["activities"]).copy()

measures_df["date"] = pd.to_datetime(measures_df["date"])
measures_df = measures_df.sort_values("date").drop_duplicates("date", keep="last")

yesterday = datetime.today().date() - timedelta(days=1)
full_date_range = pd.date_range(
    start=measures_df["date"].min(),
    end=yesterday,
    freq="D"
)

measures_df = (
    measures_df
    .set_index("date")
    .reindex(full_date_range)
    .rename_axis("date")
    .reset_index()
)

numeric_cols = measures_df.select_dtypes(include="number").columns
measures_df[numeric_cols] = measures_df[numeric_cols].fillna(0)

measures_df["date"] = measures_df["date"].dt.strftime("%Y-%m-%d")
measures_df['active_prop'] = measures_df['active']/(
        measures_df['soft'] + measures_df['moderate'] + measures_df['intense'])

# round the figures to improve plotly visuals
measures_df['active_prop'] = [round(x*100) for x in measures_df['active_prop']]

# synthesise some more accurate figures to deal with unlikely counts
cleaned_steps = []
for s in measures_df['steps']:
    if s < 750:
        syn = random.randrange(750, 1200)
        cleaned_steps.append(syn)
    else:
        cleaned_steps.append(s)

date_stamped = list(zip(measures_df['date'], measures_df['active']))
# Generate plots

# recent steps
days_to_vis = 15 + datetime.today().weekday()
steps_plot = go.Figure(data=[
    go.Bar(
        name='Steps',
        x=measures_df['date'][-days_to_vis:],
        y=cleaned_steps[-days_to_vis:],
        text=cleaned_steps[-days_to_vis:],
        marker=dict(
            color=measures_df['active'][-days_to_vis:],
            colorscale='Magma',
            cmid=1800,
            showscale=True
        )
    )
])
steps_plot.update_traces(
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
steps_plot.write_image(
    '/home/anw/mysite/electric-plan/static/daily_steps.png',
    format='png'
)

# long term steps
# removed as not easily readable or insightful

# lt_steps_plot = go.Figure(data=[
#     go.Scatter(
#         name='Long Term Steps',
#         x=activity_dates,
#         y=cleaned_steps,
#         mode='lines'
#     )
# ])
# lt_steps_plot.update_traces(
#     marker_color='#946E8B'
# )
# lt_steps_plot.update_layout(
#     plot_bgcolor='#ffffff',
#     hovermode='x unified'
# )
# lt_steps_plot.update_xaxes(
#     fixedrange=True
# )
# lt_steps_plot.update_yaxes(
#     fixedrange=True
# )
# lt_steps_plot.write_image(
#     '/home/anw/mysite/electric-plan/static/long_term_steps.png',
#     format='png'
# )

# recent proportion of day being active
prop_act_plot = go.Figure(data=[
    go.Bar(
        name='Level of Activity',
        x=measures_df['date'][-days_to_vis:],
        y=measures_df['active_prop'][-days_to_vis:]
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
    fixedrange=True,
    dtick="D1",
    tickformat="%A<br>%d %b"
)
prop_act_plot.update_yaxes(
    fixedrange=True,
    title='Active Minutes'
)
prop_act_plot.write_html(
    '/home/anw/mysite/electric-plan/static/prop_act.html'
)

# dial guages

guage_wk =  8 + datetime.today().weekday()
week_rag_status = go.Figure(data=[
    go.Indicator(
        mode="gauge+number+delta",
        value=numpy.median(measures_df['active'][-guage_wk:]),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Week Av Active Seconds", 'font': {'size': 24}},
        delta={'reference': numpy.median(measures_df['active']), 'increasing': {'color': '#99f1dd'}},
        gauge={
            'axis': {'range': [None, numpy.percentile(measures_df['active'], 90)], 'tickcolor': '#6D9476'},
            'bar': {'color': '#6D9476'},
            'steps': [
                {'range': [0, 1800], 'color': '#F199AD'},
                {'range': [1800, 3000], 'color': '#F2B199'},
                {'range': [3000, 5000], 'color': '#b5db8d'},
                {'range': [5000, 50000], 'color': '#51a560'}
            ]
        }
    )
])
week_rag_status.write_image('/home/anw/mysite/electric-plan/static/week_rag_guage.png')

guage_mnth = 30 + datetime.today().weekday()
month_rag_status = go.Figure(data=[
    go.Indicator(
        mode="gauge+number+delta",
        value=numpy.median(measures_df['active'][-guage_mnth:]),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Month Av Active Seconds", 'font': {'size': 24}},
        delta={'reference': numpy.median(measures_df['active']), 'increasing': {'color': '#99f1dd'}},
        gauge={
            'axis': {'range': [None, numpy.percentile(measures_df['active'], 90)], 'tickcolor': '#6D9476'},
            'bar': {'color': '#6D9476'},
            'steps': [
                {'range': [0, 1800], 'color': '#F199AD'},
                {'range': [1800, 3000], 'color': '#F2B199'},
                {'range': [3000, 5000], 'color': '#b5db8d'},
                {'range': [5000, 50000], 'color': '#51a560'}
            ]
        }
    )
])
month_rag_status.write_image('/home/anw/mysite/electric-plan/static/month_rag_guage.png')

# long term absolute activity levels

# remove saturdays
weekday_dates = [x[0] for x in date_stamped if datetime.strptime(x[0], '%Y-%m-%d').weekday() != 5]
weekday_act = [x[1] for x in date_stamped if datetime.strptime(x[0], '%Y-%m-%d').weekday() != 5]

# remove outliers from activity so overall trend easier to see
smooth_act = [x if x in range(0, 12001) else 3000 for x in weekday_act]

time_passage = [(weekday_act.index(x)-len(weekday_act))*-1 for x in weekday_act]
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
        # remove saturdays (ideally edit this to one-step operation)
        x=weekday_dates,
        y=weekday_act,
        mode='markers',
        marker={
            'color': ['#99f1dd' if a>=1800 else '#F199AD' for a in weekday_act],
            'size': [10 for a in weekday_act],
        }
    )
])
lt_act_plot.add_trace(go.Scatter(
    name='Trend',
    x=weekday_dates,
    y=straight_predicts,
    mode='lines',
    marker_color='#415846'
))
lt_act_plot.add_trace(go.Scatter(
    name='Poly Trend',
    x=weekday_dates,
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
