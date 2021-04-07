import requests
import json

sid = "ny_genm nwon"
sdate = "2021010100"
edate = "2021010200"
data = {
    "sid":sid,
    "sdate":sdate,
    "edate":edate
    }
resp = requests.post('https://hrly.nrcc.cornell.edu/stnHrly', json=data)
j = resp.json()

for x in j:
    print(j[x])

#print(resp.json())

with open('data.txt', 'w') as outfile:
    json.dump(j, outfile, indent=4, sort_keys=True)

outfile.close()