import re
import requests
import datetime

found_ips = []
with open('/var/log/anw.pythonanywhere.com.access.log') as access_log:
    for event in access_log:
        event_date_str = re.findall('[0-9]{2}/[A-Z][a-z]{2}/[0-9]{4}', event)
        event_date = datetime.datetime.strptime(event_date_str[0], '%d/%b/%Y')
        if event_date.date() == datetime.date.today() - datetime.timedelta(days=1):
            found_ips.append(re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",
                event
                )[0])
    access_log.close()         

search_ips = set(found_ips)

accessor = []
for i in search_ips:
    ip_lookup = requests.get(f'https://ip.rootnet.in/lookup/{i}').json()
    accessor.append(ip_lookup['ip'] + ' ' + ip_lookup['as']['name'])
with open('ips.txt', 'w') as clear_ips:
    clear_ips.write('IPs: \n')
    clear_ips.close()
with open('ips.txt', 'a') as ip_out:
    for i in accessor:
        ip_out.write(i + '\n')
        