from fastapi import FastAPI
import data_retrieval
from geopy.geocoders import Nominatim
import pandas as pd

app = FastAPI()

def find_coordinates(city):
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude



@app.get("/items/{city}")
async def read_item(city: str):

    latitude, longitude = find_coordinates(city)
    products = ["L2__CH4___", "L2__CO____", "L2__HCHO__", "L2__NO2___", "L2__O3____", "L2__SO2___"]
    df = None
    for pro in products:
        values, dates = data_retrieval.by_coordinate(latitude, longitude, pro)
        if df is None:
            df = pd.DataFrame({pro: values})
        else:
            df[pro] = values

    df = df.set_index(dates)
    df = df.fillna("")

    return {"df": df}

@app.get("/items/{city}?product={products}")
async def read_item(city: str, products: list[str]):

    latitude, longitude = find_coordinates(city)
    df = None
    for pro in products:
        values, dates = data_retrieval.by_coordinate(latitude, longitude, pro)
        if df is None:
            df = pd.DataFrame({pro: values})
        else:
            df[pro] = values

    df = df.set_index(dates)
    df = df.fillna("")

    return {"df": df}

