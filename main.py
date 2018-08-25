import requests
import csv
import folium
from folium.plugins import HeatMap
from folium.plugins import FloatImage

# Create Map Object
m = folium.Map(
    location = [23.1229948, 120.1313],
    zoom_start = 11,
)

# IMG Insert
FloatImage('xv@30pt.png', bottom = 5, left = 3).add_to(m)

# Camera Information
url = "https://od.moi.gov.tw/api/v1/rest/datastore/A01010000C-000674-011"
camera_info = requests.get(url).json()
info = camera_info['result']['records']

# Mark down Camera Location With Red Tag
for i in range(1, len(info)):
    if info[i]['CityName'] == "臺南市" or info[i]['CityName'] == "高雄市":
        if str(info[i]['limit']) == "":
            info[i]['limit'] = "未知"
        folium.Marker(
            location = [float(info[i]['Latitude']), float(info[i]['Longitude'])],
            popup = info[i]['CityName'] + " " + info[i]['RegionName'] + " " + info[i]['Address'],
            tooltip = "速限：" + str(info[i]['limit']),
            icon = folium.Icon(color = 'black', icon = 'camera', prefix = 'fa')
        ).add_to(m)

# Input A1 Event
data = []
with open('NPA_TMA1.csv', 'r', encoding = 'utf-8-sig') as A1_file:
    A1_rows = csv.DictReader(A1_file)
    for event in A1_rows:
        if event['發生地點'][0:3] == "臺南市" or event['發生地點'][0:3] == "高雄市":
            folium.Marker(
                location = [float(event['緯度']), float(event['經度'])],
                popup = event['發生時間'] + "</br>" + event['發生地點'] + "</br>" + event['死亡受傷人數'] + " " + event['車種'],
                tooltip = "A1類事故",
                icon = folium.Icon(color = 'red', icon = 'car', prefix = 'fa')
                # Hit Map with Time
            ).add_to(m)
            data.append([float(event['緯度']), float(event['經度']), 0.1])

# Input A2 Event
with open('NPA_TMA2.csv', 'r', encoding = 'utf-8-sig') as A2_file:
    A2_rows = csv.DictReader(A2_file)
    for event in A2_rows:
        if event['發生地點'][0:3] == "臺南市" or event['發生地點'][0:3] == "高雄市":
            data.append([float(event['緯度']), float(event['經度']), 0.1])

m.add_child(HeatMap(data = data, max_zoom = 12, radius = 18))
m.save("opt.html")