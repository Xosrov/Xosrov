from html2image import Html2Image
from datetime import datetime
import pathlib
import requests
import os

CURRENT_PATH = pathlib.Path(__file__).parent.resolve()
WEATHER_TOKEN = os.environ["WEATHER_API"]
CITY = "Tehran"

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
]
BASE_COLOR = "rgb(70,18,32)"
ACCENT_COLOR = "rgb(199,62,29)"
SUNNY_COLOR = "rgb(255,209,102)"
RAINY_COLOR = "rgb(38,84,124)"
SNOWY_OTHER_COLOR = "rgb(159,164,169)"

# get time in UTC
now = datetime.utcnow()
day = now.day
month = MONTHS[now.month-1]
year = now.year

# create HTML contents
dateTimeHtml = f'''<html lang="en">
<head>
    <style>
        * {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 25px;
        }}
        body {{
            display: contents;
        }}
        .container {{
            margin: 3px 0 0 5px;
            box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
            background-color: {BASE_COLOR};
            border-radius: 8px 0 0 8px;
            display: flex;
            width: max-content;
            height: 30px;
        }}
        .container .left {{
            background-color: {BASE_COLOR};
            color: white;
            border-radius: 8px 0 0 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 60px;
        }}
        .container .right {{
            box-shadow: -3px 0 6px -4px rgba(0, 0, 0, 0.75);
            background-color: {ACCENT_COLOR};
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 8px 0 0 8px;
            width: 170px;
        }}
        .container .right::after {{
            content: 'UTC';
            font-size: 8px;
            font-style: italic;
            margin-left: 2px;
            margin-top: 12px;
            color: black;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            {day}
        </div>
        <div class="right">
            {month} {year}
        </div>
    </div>
</body>
</html>'''

# current today's weather status
current_weather_stat = None

# base URL for weather api (https://openweathermap.org/current)
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={WEATHER_TOKEN}"
# HTTP request
response = requests.get(url)
weatherData = response.json().get("weather", [{}])[0]
weatherID, weatherType = weatherData.get("id", -1), weatherData.get("main", "")

# https://openweathermap.org/weather-conditions
if weatherID in range(200, 400) or weatherID in range(500, 600):
    current_weather_stat = RAINY_COLOR
elif weatherID in range(600, 800) or weatherID in range(801, 810):
    current_weather_stat = SNOWY_OTHER_COLOR
elif weatherID == 800:
    current_weather_stat = SUNNY_COLOR

# transition html
transitionHtml = f'''
<div style="position: absolute; top: 3px; left: 0px; width:300px; height:30px; box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px; background: {ACCENT_COLOR}; background: linear-gradient(90deg, {ACCENT_COLOR} 0%, {current_weather_stat} 100%);">
</div>
'''

weatherHtml = f'''<html lang="en">
<head>
    <style>
        * {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 25px;
        }}
        body {{
            display: contents;
        }}
        .container {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding-right: 10px;
            border-radius: 0 10px 10px 0;
            margin: 3px 5px 0 0;
            box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
            background-color: {current_weather_stat};
            display: flex;
            width: max-content;
            height: 30px;
            width: 210px;
        }}
        .container::after {{
            content: 'Weather\A@{CITY}';
            white-space: pre;
            font-size: 7px;
            font-style: italic;
            margin-left: 2px;
            margin-top: 12px;
            color: {BASE_COLOR};
        }}
    </style>
</head>
<body>
    <div class="container">
        {weatherType}
    </div>
</body>
</html>'''

# generate images
htmi = Html2Image()
htmi._output_path = CURRENT_PATH.joinpath("images")
htmi.screenshot(
    size=(235, 36),
    html_str=dateTimeHtml,
    save_as="date.png",
)
htmi.screenshot(
    size=(300, 36),
    html_str=transitionHtml,
    save_as="transition.png",
)
htmi.screenshot(
    size=(225, 36),
    html_str=weatherHtml,
    save_as="weather.png",
)