import requests
import math
import time
import os
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from databricks_con import query, CreateDataLakeCon
import numpy as np

# Load the .env file
load_dotenv(find_dotenv())

# Read the databrick table
df_rotas = CreateDataLakeCon(query)
print(df_rotas.head(5))

# Load the api token
SECRET_API_KEY = os.environ.get('SECRET_API_KEY')

# Given an adress return the latitude and longitude of the adress
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

# Given a latitude and longitude, returns the adress
def get_address(lat, lng):
    API_KEY = 'YOUR_API_KEY'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={SECRET_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        return data['results'][0]['formatted_address']
    else:
        return None

# Given a origin point and destination, returns the distance between them as a simple line
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

# Given a origin point and destination, returns the shortest route between them
def find_shortest_route(lat1, lon1, lat2, lon2):
    origin = f'{lat1},{lon1}'
    destination = f'{lat2},{lon2}'
    url = "https://maps.googleapis.com/maps/api/directions/json?"
    url += "origin=" + origin + "&destination=" + destination + "&key=" + SECRET_API_KEY
    # Request the API
    response = requests.get(url)
    # Check the status code of the response
    if response.status_code == 200:

        data = response.json()
        # Extract the total distance from the response data
        total_distance = data['routes'][0]['legs'][0]['distance']['text']        
    else:
        print('Error: Unable to retrieve data from the API')
    return total_distance


# Get the latitude and longitude based on the origin and destination
latitude_origin_list = []
longitude_origin_list = []
latitude_destination_list = []
longitude_destination_list = []
origin_dic = {}
destination_dic = {}

# Create a list with lat and long from the origin location
for origin in df_rotas["Local_coleta"]:
    try:
        lat1, lon1 = get_lat_lng(str(origin))
        latitude_origin_list.append(lat1)
        longitude_origin_list.append(lon1)
    except:
        latitude_origin_list.append(np.nan)
        longitude_origin_list.append(np.nan)
        continue

# Create a list with lat and long from the destination location
for destination in df_rotas["Local_entrega"]:
    try:
        lat2, lon2 = get_lat_lng(str(destination))
        latitude_destination_list.append(lat2)
        longitude_destination_list.append(lon2)
    except:
        latitude_destination_list.append(np.nan)
        longitude_destination_list.append(np.nan)
        continue

# Save all the latitudes and longitudes on 2 dictionaries
origin_dic['latitude'] = latitude_origin_list
origin_dic['longitude'] = longitude_origin_list
destination_dic['latitude'] = latitude_destination_list
destination_dic['longitude'] = longitude_destination_list

# Get the shortest route based on the coordinates dictionaries
distance_shortest_route_list = []
for lat1, lon1, lat2, lon2 in zip(origin_dic['latitude'], origin_dic['longitude'], destination_dic['latitude'], destination_dic['longitude']):
    try:
        distance_shortest_route = find_shortest_route(lat1, lon1, lat2, lon2)
        print('Distancia menor caminho:', distance_shortest_route)
        distance_shortest_route_list.append(distance_shortest_route)
    except:
        distance_shortest_route_list.append('Não foi possivel calcular a rota')
        continue
    
# Save it all to a pandas dataframe
df_rotas['Lat_origem'] = origin_dic['latitude']
df_rotas['Lon_origem'] = origin_dic['longitude']
df_rotas['Lat_destino'] = destination_dic['latitude']
df_rotas['Lon_destino'] = destination_dic['longitude']
df_rotas['Distancia'] = distance_shortest_route_list

print(df_rotas.head())
#df_rotas.to_csv('Transporte_rotas_unicas_com_distancias.csv', sep=";")

# Get the distance between origin and destination
#distance = distance_between_coordinates(lat1, lon1, lat2, lon2) * 1.2 # coeficiente de segurança
#print(f'Distancia reta: {round(distance)} Km')