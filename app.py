from flask import Flask, render_template, request, url_for
from forms import LocationForm
import requests
import json
import os

# Start the Flask app
app = Flask(__name__)

# Generate a CSRF Secret Key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
city = ""
state = ""
mood = ""

@app.route('/success', methods=["GET","POST"])
def homepage():
    # Get the API key
    api_key = os.environ.get('API_KEY')
    # print(api_key)
    weather_data = []
    
    # Final Location Attributes we want
    city = location['city']
        
    # Make the request
    url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}'
    r = requests.get(
        url.format(city, state, api_key))

    # Get a dict of JSON data
    weather_JSON = r.json()

    # Parsing JSON is fun
    weather = {
        'main': weather_JSON['weather'][0]['main'],
        'description': weather_JSON['weather'][0]['description'],
        'temperature': weather_JSON['main']['temp'],
        'icon': r['weather']['0']['icon'],
    }
    weather_data.append(weather)
    # print("\n", r.json(), "\n")
    
    return render_template('weather.html', weather=weather_data)

@app.route("/", methods = ['GET', 'POST'])
def Location():
    form = LocationForm()
    if form.validate_on_submit() and request.method == "POST":
        location = {
            'city': LocationForm.city.data,
            'state': LocationForm.state.data,
            'mood': LocationForm.mood.data,
        }
        
        return url_for('/success')
    return render_template('location.html', form=form)

if __name__ == '__main__':
    app.run()