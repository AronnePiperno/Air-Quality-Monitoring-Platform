from fastapi import FastAPI, HTTPException
import data_retrieval
from geopy.geocoders import Nominatim
import pandas as pd
from enum import Enum

app = FastAPI()

class ProductName(str, Enum):
    CO =  "L2__CO____"
    HCHO = "L2__HCHO__"
    NO2 = "L2__NO2___"
    O3 = "L2__O3____"
    SO2 = "L2__SO2___"

def find_coordinates(city):
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude



@app.get("/items/{city}")
async def read_item(city: str):
    latitude, longitude = find_coordinates(city)
    products = ["L2__CO____", "L2__HCHO__", "L2__NO2___", "L2__O3____", "L2__SO2___"]
    df = None
    for pro in products:
        values, dates = data_retrieval.by_coordinate(latitude, longitude, pro)
        if df is None:
            df = pd.DataFrame({pro: values})
        else:
            df[pro] = values

    df = df.set_index(dates)
    df = df.fillna("")

    return {"data": df}

@app.get("/items/{city}/{product}")
async def read_item_prod(city: str, product: ProductName):

    latitude, longitude = find_coordinates(city)
    if product is ProductName.CO:
        values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__CO____")

    elif product is ProductName.HCHO:
        values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__HCHO__")

    elif product is ProductName.NO2:
        values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__NO2___")

    elif product is ProductName.O3:
        values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__O3____")

    elif product is ProductName.SO2:
        values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__SO2___")
    else:
        raise HTTPException(status_code=404, detail="Product not found")



    data = pd.DataFrame({product: values})


    data = data.set_index(dates)
    data = data.fillna("")

    return {"data": data}

@app.get("/items/{city}/{product}/{city_comparison}")
async def read_item_comp(city: str, product: ProductName, city_comparison: str):

        latitude, longitude = find_coordinates(city)
        latitude_comparison, longitude_comparison = find_coordinates(city_comparison)

        if product is ProductName.CO:
            values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__CO____")
            values_comparison, dates_comparison = data_retrieval.by_coordinate(latitude_comparison, longitude_comparison, "L2__CO____")

        elif product is ProductName.HCHO:
            values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__HCHO__")
            values_comparison, dates_comparison = data_retrieval.by_coordinate(latitude_comparison, longitude_comparison, "L2__HCHO__")

        elif product is ProductName.NO2:
            values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__NO2___")
            values_comparison, dates_comparison = data_retrieval.by_coordinate(latitude_comparison, longitude_comparison, "L2__NO2___")

        elif product is ProductName.O3:
            values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__O3____")
            values_comparison, dates_comparison = data_retrieval.by_coordinate(latitude_comparison, longitude_comparison, "L2__O3____")

        elif product is ProductName.SO2:
            values, dates = data_retrieval.by_coordinate(latitude, longitude, "L2__SO2___")
            values_comparison, dates_comparison = data_retrieval.by_coordinate(latitude_comparison, longitude_comparison, "L2__SO2___")
        else:
            raise HTTPException(status_code=404, detail="Product not found")

        data = pd.DataFrame({product: values, city_comparison: values_comparison})

        data = data.set_index(dates)
        data = data.fillna("")

        return {"data": data}

@app.get("/items/{city}/{product}/{start_date}/{end_date}")
async def read_item_date(city: str, product: ProductName, start_date: str, end_date: str):

        latitude, longitude = find_coordinates(city)

        if product is ProductName.CO:
            values, dates = data_retrieval.by_date(latitude, longitude, "L2__CO____", start_date, end_date)

        elif product is ProductName.HCHO:
            values, dates = data_retrieval.by_date(latitude, longitude, "L2__HCHO__", start_date, end_date)

        elif product is ProductName.NO2:
            values, dates = data_retrieval.by_date(latitude, longitude, "L2__NO2___", start_date, end_date)

        elif product is ProductName.O3:
            values, dates = data_retrieval.by_date(latitude, longitude, "L2__O3____", start_date, end_date)

        elif product is ProductName.SO2:
            values, dates = data_retrieval.by_date(latitude, longitude, "L2__SO2___", start_date, end_date)
        else:
            raise HTTPException(status_code=404, detail="Product not found")

        data = pd.DataFrame({product: values})

        data = data.set_index(dates)
        data = data.fillna("")

        return {"data": data}

