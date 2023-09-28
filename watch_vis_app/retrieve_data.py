import requests
import json
from datetime import datetime, timedelta

with open('token_file.txt') as tf:
    token_json = json.load(tf)

access_token = token_json['body']['access_token']

# Activity measures
first_date = datetime.strftime(
    datetime.today() - timedelta(days=150),
    format='%Y-%m-%d'
)
todays_date = datetime.strftime(
    datetime.today(),
    format='%Y-%m-%d'
)
measure_call = requests.post(
    'https://wbsapi.withings.net/v2/measure',
    headers={'Authorization': 'Bearer '+str(access_token)},
    data={
        'action': 'getactivity',
        'startdateymd': first_date,
        'enddateymd': todays_date
    }
)

measure_json = json.dumps(measure_call.json())
if measure_call.json()['status'] == 0:
    measure_file = open('/home/anw/mysite/electric-plan/DATA/measure_data.txt', 'w')
    measure_file.write(measure_json)
    measure_file.close()
else:
    print(' Error retrieving data')

# Sleep hr
sleep_call = requests.post(
    'https://wbsapi.withings.net/v2/sleep',
    headers={'Authorization': 'Bearer '+str(access_token)},
    data={
        'action': 'get',
        'startdate': 1659307440,
        'enddate': 1667324441,
        'data_fields': 'hr'
    }
)

sleep_json = json.dumps(sleep_call.json())
sleep_file = open('/home/anw/mysite/electric-plan/DATA/sleep_data.txt', 'w')
sleep_file.write(sleep_json)
sleep_file.close()

# Sleep summary
sleep_sumy_call = requests.post(
    'https://wbsapi.withings.net/v2/sleep',
    headers={'Authorization': 'Bearer '+str(access_token)},
    data={
        'action': 'getsummary',
        'startdateymd': '2022-08-01',
        'enddateymd': '2022-11-02'
    }
)

sleep_sumy_json = json.dumps(sleep_sumy_call.json())
sleep_sumy_file = open('/home/anw/mysite/electric-plan/DATA/sleep_sumy_data.txt', 'w')
sleep_sumy_file.write(sleep_sumy_json)
sleep_sumy_file.close()
