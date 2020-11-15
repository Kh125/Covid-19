from flask import render_template, request
import requests
from covid import app

url = "https://covid-193.p.rapidapi.com/statistics"
headers = {
      'x-rapidapi-key': "bce42a815emsh56bee14b9198293p194e08jsne213c82bc0d4",
      'x-rapidapi-host': "covid-193.p.rapidapi.com"
      }

@app.route('/country',methods=['GET','POST'])
def country():
  country = "Myanmar"
  if request.method == 'POST':
    country = request.form.get('city')
  querystring = {"country":country}
  response = requests.request("GET", url, headers=headers, params=querystring)
  req = response.json()
  print(req)

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
      'result':req['results']
    }

  print(country_data)
  return render_template('index.html',data = country_data)


@app.route('/dashboard',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def index():
  return render_template('dashboard.html')