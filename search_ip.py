import re
import requests
import datetime

#pull a list of ip addresses from log file
found_ips = []
with open('/var/log/anw.pythonanywhere.com.access.log') as access_log:
    for event in access_log:
        event_date_str = re.findall('[0-9]{2}/[A-Z][a-z]{2}/[0-9]{4}', event)
        event_date = datetime.datetime.strptime(event_date_str[0], '%d/%b/%Y')
        if datetime.date.today() - event_date.date() < datetime.timedelta(8):
            found_ips.append(
                [re.findall(
                    "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",
                    event
                    )[0],
                datetime.datetime.strftime(event_date, '%A    %d %B')]
                )
    access_log.close()

search_ips = set(found_ips)

# get ip info from service and write to local file
accessor = []
for i in search_ips:
    ip_lookup = requests.get(f'https://ip.rootnet.in/lookup/{i[0]}').json()
    accessor.append(ip_lookup['ip'] + ' ' + ip_lookup['as']['name'])
with open('/home/anw/mysite/electric-plan/static/ips.txt', 'w') as clear_ips:
    clear_ips.write('IPs: \n')
    clear_ips.close()
with open('/home/anw/mysite/electric-plan/static/ips.txt', 'a') as ip_out:
    for i in accessor:
        ip_out.write(i + '\n')
    ip_out.write('\n All traffic: \n')
    for i in search_ips:
        ip_out.write(i + '\n')        
