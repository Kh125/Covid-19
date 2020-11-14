from flask import Flask, render_template, request
from random import choice
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/',methods=['GET','POST'])
def index():
  country = "Myanmar"
  if request.method == 'POST':
    country = request.form.get('city')

  url = "https://covid-193.p.rapidapi.com/statistics"
  querystring = {"country":country}

  headers = {
      'x-rapidapi-key': "bce42a815emsh56bee14b9198293p194e08jsne213c82bc0d4",
      'x-rapidapi-host': "covid-193.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  req = response.json()
  print(req)
  response = response.text
  country_data = {
    'country':req['response'][0]['country'],
    'continent':req['response'][0]['continent'],
    'population':req['response'][0]['population'],
    'new_cases':req['response'][0]['cases']['new'],
    'active':req['response'][0]['cases']['active'],
    'recover':req['response'][0]['cases']['recovered'],
    'total':req['response'][0]['cases']['total'],
    'death_today':req['response'][0]['deaths']['new'],
    'death_total':req['response'][0]['deaths']['total'],
    'total_test':req['response'][0]['tests']['total'],
    'day':req['response'][0]['day'],
    'time':req['response'][0]['time']
  }
  print(country_data)
  return render_template('index.html',data = country_data)


app.run(host='0.0.0.0', port=8080)