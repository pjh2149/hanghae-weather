from flask import Flask, render_template
import requests

app = Flask(__name__)

lat = 37.41043
lon = 127.13716
r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=3d9290fe0f2425345dc583eb4d290e52&units=metric")

result = r.json()
temperature = result["main"]["temp"]
description = result["weather"][0]["description"]
humidity = result["main"]["humidity"]
wind_speed = result["wind"]["speed"]
# wind speed 단위 = meter / second
image = result["weather"][0]["icon"]

print(result)
print(temperature)
print(description)
print(humidity)
print(image)
print(wind_speed)

@app.route('/')
def home():
    return render_template('index.html', result=result, temperature=temperature, description=description,
                           humidity=humidity, wind_speed=wind_speed, image=image)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
