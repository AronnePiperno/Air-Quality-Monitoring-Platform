from fastapi import FastAPI
import data_retrieval
from geopy.geocoders import Nominatim

app = FastAPI()

def find_coordinates(city):
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude



@app.get("/items/{city}")
async def read_item(city: str):

    latitude, longitude = find_coordinates(city)
    values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__CH4___")
    return {"values": values}

