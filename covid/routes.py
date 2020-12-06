from flask import render_template, request
from covid import app
import requests
import os
import csv

urll = "https://worldometers.p.rapidapi.com/api/coronavirus/country/"
headers = {
      'x-rapidapi-key': os.getenv('x-rapidapi-key'),
      'x-rapidapi-host': "worldometers.p.rapidapi.com"
      }

url_world = "https://worldometers.p.rapidapi.com/api/coronavirus/world"

headers_world = {
      'x-rapidapi-key': os.getenv('x-rapidapi-key'),
      'x-rapidapi-host': "worldometers.p.rapidapi.com"
      }

url_all = "https://worldometers.p.rapidapi.com/api/coronavirus/all/"

headers_all = {
    'x-rapidapi-key':  os.getenv('x-rapidapi-key'),
    'x-rapidapi-host': "worldometers.p.rapidapi.com"
    }


@app.route('/country',methods=['GET','POST'])
def country():
  country = "myanmar"
  if request.method == 'POST':
    if request.form.get('city').lower() == 'south-korea':
      country = 's-korea'
    else:
      country = request.form.get('city').lower()
  url = urll+country 
  response = requests.request("GET", url, headers=headers)
  req = response.json()
  # print(req)

  if 'data' in req:
    country_data = {
      'country':req['data']['Country'],
      'population':req['data']['Population'],
      'new_cases':req['data']['New Cases'],
      'active':req['data']['Active Cases'],
      'critical':req['data']['Critical'],
      'recover':req['data']['Total Recovered'],
      'recover_today':req['data']['New Recovered'],
      'total':req['data']['Total Cases'],
      'death_today':req['data']['New Deaths'],
      'death_total':req['data']['Total Deaths'],
      'total_test':req['data']['Total Tests'],
      'time':req['last_update'],
      'result':'200'
    }
  else:
    country_data = {
      'country':country,
      'result':'404'
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
  return render_template('dashboard.html', data = world)


@app.route('/country-list')
def data_list():
  response = requests.request("GET", url_all, headers=headers_all)
  req = response.json()
  test = []
  country = []
  for rr in range(len(req['data'])):
    country = [
      req['data'][rr]['Country'],
      req['data'][rr]['Active Cases'],
      req['data'][rr]['Critical'],
      req['data'][rr]['New Cases'],
      req['data'][rr]['New Deaths'],
      req['data'][rr]['New Recovered'],
      req['data'][rr]['Total Cases'],
      req['data'][rr]['Total Deaths'],
      req['data'][rr]['Total Recovered'],
      req['data'][rr]['Total Tests'],
      req['data'][rr]['Region'],
    ]
    test.append(country)

  return render_template('country_data.html',test = test,updated_time = req['last_update'])