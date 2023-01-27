import requests

SECRET_API_KEY = 'AIzaSyApe4spP6T-B8z-RgNrs6SuNDDNdMdvLRQ='

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
    
# Get the latitude and longitude based on the adress
lat, lng = get_lat_lng('1600 Amphitheatre Parkway, Mountain View, CA')
print(f'Latitude: {lat}, Longitude: {lng}')

# Get the adress base on latitude and longitude
lat, lng = '-33.8688' , '151.2093'
address = get_address(lat, lng)
print(address)