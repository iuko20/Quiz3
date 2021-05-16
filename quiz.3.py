import requests
import json
import sqlite3
conn = sqlite3.connect('weather_tb.sqlite')
c = conn.cursor()

# ბაზაში აღწერილია 5 დღის ამინდის პროგნოზი თბილისისთვის

c.execute('''CREATE TABLE IF NOT EXISTS weather 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature INTEGER,
        weather VARCHAR(10),
        date_time INTEGER
        )''')


city = 'Tbilisi'
key = 'f099f68a4e7105f4c4cd1f61bb1aef46'
payload = {'q': city, 'appid': key, 'units': 'metric'}

r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=payload)

res = r.json()
with open('weather.json', 'w') as f:
    json.dump(res, f, indent=4)

print(r.headers)
print("სტატუს კოდია:", r.status_code)
print("დედაქალაქის ტემპერატურაა:", res['list'][0]['main']['temp'], "  დრო და თარიღი:", res['list'][0]['dt_txt'])
print("ქარის სიჩქარეა: ", res['list'][0]['wind']['speed'])

all_rows = []
for each in res['list']:
    temperature = each['main']['temp']
    weather = each['weather'][0]['main']
    date_time = each['dt_txt']
    row = (temperature, weather, date_time)
    all_rows.append(row)

c.executemany('INSERT INTO weather (temperature, weather, date_time) VALUES (?, ?, ?)', all_rows)
conn.commit()
