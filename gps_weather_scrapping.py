import requests as r
import json
import config
import pandas as pd

# 34 best cities to visit in France

city_list = ["Mont Saint Michel",
"St Malo",
"Bayeux",
"Le Havre",
"Rouen",
"Paris",
"Amiens",
"Lille",
"Strasbourg",
"Chateau du Haut Koenigsbourg",
"Colmar",
"Eguisheim",
"Besancon",
"Dijon",
"Annecy",
"Grenoble",
"Lyon",
"Gorges du Verdon",
"Bormes les Mimosas",
"Cassis",
"Marseille",
"Aix en Provence",
"Avignon",
"Uzes",
"Nimes",
"Aigues Mortes",
"Saintes Maries de la mer",
"Collioure",
"Carcassonne",
"Ariege",
"Toulouse",
"Montauban",
"Biarritz",
"Bayonne",
"La Rochelle"]

# get coordinates of the cities

base_endpoint = 'https://nominatim.openstreetmap.org/search?'

coordinate_list = []

for i, city in enumerate(city_list):
    params = {'q': city, 'format': 'json'}
    response = r.get(base_endpoint, params= params)

    for search_result in response.json():
        if 'france' in search_result['display_name'].lower():
            coordinate_list.append((city, search_result['lat'],search_result['lon']))
            print(f'{i} request completed')
            break

# get weather forecast within the next 7 days for each city

base_endpoint = 'https://api.openweathermap.org/data/2.5/onecall?'
KEY = config.api_key


def cleaning_dict(forecast_dict):

    clean_dict = {}
    
    for key in forecast_dict.keys():

        if type(forecast_dict[key]) == list:

            for i in forecast_dict[key][0].keys():
                clean_dict[key+'_'+i] = forecast_dict[key][0][i]

        elif type(forecast_dict[key]) == dict:

            for i in forecast_dict[key].keys():
                clean_dict[key+'_'+i] = forecast_dict[key][i]

        else:
            clean_dict[key] = forecast_dict[key]

    return clean_dict

def one_city_request(base_endpoint, KEY, city_loc):
    
    params = {'lat': city_loc[1],
          'lon': city_loc[2],
          'appid': KEY,
          'units': 'metric'
          }

    response = r.get(base_endpoint, params=params)
    return response.json()['daily']

result_list = []

for i, city_loc in enumerate(coordinate_list):
    
    weather_request = one_city_request(base_endpoint, KEY, city_loc)

    for forecast_dict in weather_request:

        base_dict = {'id': i,
                'city': city_loc[0],
                'lat': city_loc[1],
                'lon': city_loc[2],
                }
    
        base_dict.update(cleaning_dict(forecast_dict))
        result_list.append(base_dict)

    print(f'{i} city done')

data_weather = pd.DataFrame(result_list)
data_weather.to_csv('WeatherForecast 2022-09-19.csv')