import requests

GEOCODING_API_KEY = 'iFIpdT1gQsr0nHoGk0ThyQ==H7HUZeuPYzXeyuJb'
WEATHER_API_KEY = 'iFIpdT1gQsr0nHoGk0ThyQ==H7HUZeuPYzXeyuJb'

def get_lat_lon(city, country=None):
    """
    Get latitude and longitude for a given city and optional country.
    """
    api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city}'
    if country:
        api_url += f'&country={country}'
        
    response = requests.get(api_url, headers={'X-Api-Key': GEOCODING_API_KEY})
    if response.status_code == requests.codes.ok:
        data = response.json()
        if data:
            location = data[0]
            return location['latitude'], location['longitude']
    else:
        print("Geocoding API Error:", response.status_code, response.text)
    return None, None

def get_weather_data(lat, lon):
    """
    Get weather data for given latitude and longitude.
    """
    api_url = f'https://api.api-ninjas.com/v1/weather?lat={lat}&lon={lon}'
    response = requests.get(api_url, headers={'X-Api-Key': WEATHER_API_KEY})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Weather API Error:", response.status_code, response.text)
    return None
