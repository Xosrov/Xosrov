from datetime import datetime
import requests
import pathlib
import os

README_FILE = pathlib.Path(__file__).parent.resolve().joinpath("README.md")
WEATHER_TOKEN = os.environ["WEATHER_API"]
CITY = "Karlsruhe"

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

# get time in UTC
now = datetime.utcnow()
day = now.day
month = MONTHS[now.month-1]
year = now.year
hour = now.hour
minute = now.minute

# base URL for weather api (https://openweathermap.org/current)
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={WEATHER_TOKEN}"
# HTTP request
response = requests.get(url)
weatherData = response.json().get("weather", [{}])[0]
weatherID, weatherType = weatherData.get("id", -1), weatherData.get("main", "")

mermaid = f'''mermaid
mindmap
  root((Hello!))
    )Weather(
        ({weatherType})
        ({weatherData["description"]})
    {{{{Local}}}}
        (Updated {hour:02d}:{minute:02d} UTC)
        ({day} {month} {year})
    Location
        ({CITY})
'''

readme_text = ""
with open(README_FILE, 'r', encoding="UTF-8") as f:
    readme_text = f.read()

start = readme_text.find("```")
end = readme_text.find("```", start+1)
readme_text = readme_text[:start+3] + mermaid + readme_text[end:]

with open(README_FILE, "w", encoding="UTF-8") as f:
    f.write(readme_text)
