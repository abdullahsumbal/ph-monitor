import re
data = '5/4/2019 8:06:05 AM	6.8533411026001	8.68220329284668	25	Good	1/1/2014 12:00:00 AM	7	100'

m = re.search('\d+/\d+/\d+\s*\d+:\d+:\d+\s*(PM{1}|AM{1})\s+\d+\.\d+', data)


if m:
    data = m.group(0)
    print(data)
    print(re.findall('\d+\.\d+', data))
else:
    print("found nothing")

