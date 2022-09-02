import requests
import config
import json

def get_weather():
    r = requests.get('https://api.weather.yandex.ru/v2/forecast', params=config.payload_weather, headers=config.weather_key)
    weather_data = r.json()['fact']
    return weather_data

def get_city_coord(city):
    payload = {'geocode' : city, 'apikey' : config.geo_key, 'format' : 'json'}
    r = requests.get('https://geocode-maps.yandex.ru/1.x', params=payload)
    geo = json.loads(r.text)
    return geo['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()

def get_weather_by_city(city):
    coordinates = get_city_coord(city)
    r = requests.get('https://api.weather.yandex.ru/v2/forecast', params={'lat': coordinates[1], 'lon': coordinates[0], 'lang': 'ru_RU', 'limit': '1'}, headers=config.weather_key)
    weather_data = r.json()['fact']
    return [weather_data, city]


get_weather_by_city('Калининград')
