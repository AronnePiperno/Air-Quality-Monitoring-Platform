from fastapi import FastAPI, HTTPException
from geopy.geocoders import Nominatim
import pandas as pd
from enum import Enum
import requests

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
        response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product={pro}")
        values, dates = response.json()["mean_values"], response.json()["unique_dates"]
        if df is None:
            df = pd.DataFrame({pro: values})
        else:
            df[pro] = values

    df["dates"] = dates
    df = df.fillna("")

    return {"data": df}

@app.get("/items/{city}/{product}")
async def read_item_prod(city: str, product: ProductName):

    latitude, longitude = find_coordinates(city)
    if product is ProductName.CO:
        response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__CO____")
        values, dates = response.json()["mean_values"], response.json()["unique_dates"]

    elif product is ProductName.HCHO:
        response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__HCHO__")
        values, dates = response.json()["mean_values"], response.json()["unique_dates"]

    elif product is ProductName.NO2:
        response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__NO2___")
        values, dates = response.json()["mean_values"], response.json()["unique_dates"]

    elif product is ProductName.O3:
        response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__O3____")
        values, dates = response.json()["mean_values"], response.json()["unique_dates"]

    elif product is ProductName.SO2:
        response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__SO2___")
        values, dates = response.json()["mean_values"], response.json()["unique_dates"]
    else:
        raise HTTPException(status_code=404, detail="Product not found")

    data = pd.DataFrame({product: values})

    data["dates"] = dates

    data = data.fillna("")

    return {"data": data}

@app.get("/items/{city}/{product}/{city_comparison}")
async def read_item_comp(city: str, product: ProductName, city_comparison: str):

        latitude, longitude = find_coordinates(city)
        latitude_comparison, longitude_comparison = find_coordinates(city_comparison)

        if product is ProductName.CO:
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__CO____")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude_comparison}&longitude={longitude_comparison}&product=L2__CO____")
            values_comparison, dates_comparison = response.json()["mean_values"], response.json()["unique_dates"]

        elif product is ProductName.HCHO:
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__HCHO__")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude_comparison}&longitude={longitude_comparison}&product=L2__HCHO__")
            values_comparison, dates_comparison = response.json()["mean_values"], response.json()["unique_dates"]

        elif product is ProductName.NO2:
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__NO2___")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude_comparison}&longitude={longitude_comparison}&product=L2__NO2___")
            values_comparison, dates_comparison = response.json()["mean_values"], response.json()["unique_dates"]

        elif product is ProductName.O3:
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__O3____")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude_comparison}&longitude={longitude_comparison}&product=L2__O3____")
            values_comparison, dates_comparison = response.json()["mean_values"], response.json()["unique_dates"]

        elif product is ProductName.SO2:
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product=L2__SO2___")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]
            response = requests.get(f"http://zarr_db:5000/search_by_coordinate?latitude={latitude_comparison}&longitude={longitude_comparison}&product=L2__SO2___")
            values_comparison, dates_comparison = response.json()["mean_values"], response.json()["unique_dates"]
        else:
            raise HTTPException(status_code=404, detail="Product not found")

        data = pd.DataFrame({city: values, city_comparison: values_comparison})

        data["dates"] = dates
        data = data.fillna("")

        return {"data": data}

@app.get("/items/{city}/{product}/{start_date}/{end_date}")
async def read_item_date(city: str, product: ProductName, start_date: str, end_date: str):

        latitude, longitude = find_coordinates(city)

        if product is ProductName.CO:
            response = requests.get(f"http://zarr_db:5000/search_by_date?latitude={latitude}&longitude={longitude}&product=L2__CO____&start_date={start_date}&end_date={end_date}")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]

        elif product is ProductName.HCHO:
            response = requests.get(f"http://zarr_db:5000/search_by_date?latitude={latitude}&longitude={longitude}&product=L2__HCHO__&start_date={start_date}&end_date={end_date}")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]

        elif product is ProductName.NO2:
            response = requests.get(f"http://zarr_db:5000/search_by_date?latitude={latitude}&longitude={longitude}&product=L2__NO2___&start_date={start_date}&end_date={end_date}")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]

        elif product is ProductName.O3:
            response = requests.get(f"http://zarr_db:5000/search_by_date?latitude={latitude}&longitude={longitude}&product=L2__O3____&start_date={start_date}&end_date={end_date}")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]

        elif product is ProductName.SO2:
            response = requests.get(f"http://zarr_db:5000/search_by_date?latitude={latitude}&longitude={longitude}&product=L2__SO2___&start_date={start_date}&end_date={end_date}")
            values, dates = response.json()["mean_values"], response.json()["unique_dates"]
        else:
            raise HTTPException(status_code=404, detail="Product not found")

        data = pd.DataFrame({product: values})

        data["dates"] = dates
        data = data.fillna("")

        return {"data": data}

@app.get("/AQI/{city}")
async def read_item_AQI(city: str):

        latitude, longitude = find_coordinates(city)

        response = requests.get(f"http://zarr_db:5000/get_aqi?latitude={latitude}&longitude={longitude}")
        value = response.json()["AQI"]

        data = {"AQI": value}

        return {"data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)