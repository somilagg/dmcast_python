import requests
import json

sid = "ny_genm nwon"
# YYYYMMDDHH
sdate = "2020070100"
edate = "2020070500"
data = {
    "sid":sid,
    "sdate":sdate,
    "edate":edate
    }
resp = requests.post('https://hrly.nrcc.cornell.edu/stnHrly', json=data)
j = resp.json()
j_mat = []
print(j['hrlyFields'])
for h in j['hrlyData']:
    for e in range(len(h)):
        h[e] = str(h[e])
    j_mat.append(h)
    print h[0][0:1]

#print(j_mat)


with open('data.txt', 'w') as outfile:
    json.dump(j, outfile, indent=4, sort_keys=True)

outfile.close()