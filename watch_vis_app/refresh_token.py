import requests
import json

with open('~/mysite/electric-plan/DATA/token_file.txt') as tf:
    token_json = json.load(tf)

refresh_token = token_json['body']['refresh_token']

refresh = requests.post(
    'https://wbsapi.withings.net/v2/oauth2',
    params={
        'action': 'requesttoken',
        'client_id': '95bfd632cd4112df1aeb5a1d12c384298a0c2a3c66a088f803ba96d0bc6cec4f',
        'client_secret': '6d37e257732d47dccf5f9c228bc63f18cb3e5c50372e3a3a6c5c4232ff178c6a',
        'grant_type': 'refresh_token',
        'refresh_token': '{}'.format(refresh_token)
    }
)

refresh_json = json.dumps(refresh.json())
token_file = open('~/mysite/electric-plan/DATA/token_file.txt', 'w')
token_file.write(refresh_json)
token_file.close()
