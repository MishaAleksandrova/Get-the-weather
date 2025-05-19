import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from geosky import geo_plug
from functools import lru_cache

@lru_cache(maxsize=1)
def get_all_cities():
    raw_data = geo_plug.all_State_CityNames('all')
    if isinstance(raw_data, str):
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError as e:
            print("Error decoding city list:", e)
            return []
    return raw_data

def city_autocomplete(request):
    term = request.GET.get('term', '').lower()
    all_cities = get_all_cities()

    print("Type of all_cities:", type(all_cities))
    print("First item preview:", all_cities[0] if all_cities else "No cities found")

    matches = []
    for city_dict in all_cities:
        for city_name, aliases in city_dict.items():
            if term in city_name.lower():
                matches.append(city_name)
            else:
                for alias in aliases:
                    if term in alias.lower():
                        matches.append(alias)
    return JsonResponse(matches[:10], safe=False)

def home(request):
    weather_data = None
    error = None

    if 'city' in request.GET:
        city = request.GET['city']
        api_key = "79bb528cf5d847e5995ab79942021f82"
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': f"{data['name']}, {data['sys']['country']}",
                'temperature': round(data['main']['temp'], 2),
                'feels_like': round(data['main']['feels_like'], 2),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
        else:
            error = "City not found"

    return render(request, 'weather/home.html', {
        'weather_data': weather_data,
        'error': error,
    })


