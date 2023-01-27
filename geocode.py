import requests
import math
import time

SECRET_API_KEY = 'AIzaSyApe4spP6T-B8z-RgNrs6SuNDDNdMdvLRQ='

origin = str(input('Digite o local de origem:'))
destination = str(input('Digite o local de destino:'))

def get_lat_lng(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': SECRET_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        raise ValueError(f'Error: {data["status"]}')
    
def get_address(lat, lng):
    API_KEY = 'YOUR_API_KEY'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={SECRET_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        return data['results'][0]['formatted_address']
    else:
        return None
    
def distance_between_coordinates(lat1, lon1, lat2, lon2):
    earth_radius = 6371 # Earth's radius in kilometers
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c
    return distance


# Get the latitude and longitude based on the origin
lat1, lon1 = get_lat_lng(origin)

# Await
time.sleep(3)
print('calculando..')

# Get the latitude and longitude based on the destination
lat2, lon2 = get_lat_lng(destination)

# Get the distance between origin and destination
distance = distance_between_coordinates(lat1, lon1, lat2, lon2)
print(f'Distancia total: {distance} Km')
