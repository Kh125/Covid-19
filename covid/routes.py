from flask import render_template, request
from covid import app
import requests
import os
import csv

urll = "https://covid-193.p.rapidapi.com/"
headers = {
      'x-rapidapi-key': os.getenv('x-rapidapi-key'),
      'x-rapidapi-host': "covid-193.p.rapidapi.com"
      }

url_world = "https://worldometers.p.rapidapi.com/api/coronavirus/world"

headers_world = {
      'x-rapidapi-key': os.getenv('x-rapidapi-key'),
      'x-rapidapi-host': "worldometers.p.rapidapi.com"
      }

@app.route('/country',methods=['GET','POST'])
def country():
  url = urll+'statistics'
  country = "Myanmar"
  if request.method == 'POST':
    if request.form.get('city').lower() == 'south-korea':
      country = 's-korea'
    else:
      country = request.form.get('city')
  querystring = {"country":country}
  response = requests.request("GET", url, headers=headers, params=querystring)
  req = response.json()
  # print(req)

  if req['results'] != 0:
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
      'time':req['response'][0]['time'],
      'result':req['results']
    }
  else:
    country_data = {
      'country':req['parameters']['country'],
      'result':req['results']
    }

  # print(country_data)
  with open('flag.csv','r')as rf:
    csv_reader = csv.reader(rf)
    next(csv_reader)
    for i in csv_reader:
      if country_data['country'] == i[0]:
        # print(i[2])
        country_data['svg'] = i[2]
  return render_template('index.html',data = country_data)

@app.route('/dashboard',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def index():  

  response = requests.request("GET", url_world, headers=headers_world)
  req = response.json()  
  world = {
    'active':req['data']['Active Cases'],
    'critical':req['data']['Critical'],
    'new_case':req['data']['New Cases'],
    'new_death':req['data']['New Deaths'],
    'new_recover':req['data']['New Recovered'],
    'total_case':req['data']['Total Cases'],
    'total_death':req['data']['Total Deaths'],
    'total_recover':req['data']['Total Recovered'],
    'total_test':req['data']['Total Tests'],
    'updated':req['last_update']
  }
  print(world)
  return render_template('dashboard.html', data = world)

