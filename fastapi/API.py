from fastapi import FastAPI, HTTPException
from geopy.geocoders import Nominatim
import pandas as pd
from enum import Enum
import requests
from datetime import datetime

# Create a FastAPI app
app = FastAPI()


# Define an enumeration class for product names
class ProductName(str, Enum):
    CO = "L2__CO____"
    HCHO = "L2__HCHO__"
    NO2 = "L2__NO2___"
    O3 = "L2__O3____"
    SO2 = "L2__SO2___"


# Function to find latitude and longitude coordinates of a city
def find_coordinates(city):

    try:
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(city)
        return location.latitude, location.longitude
    except:
        raise HTTPException(status_code=404, detail="City not found.")


# Endpoint to retrieve data for all products for a specific city
@app.get("/items/{city}")
async def read_item(city: str):
    latitude, longitude = find_coordinates(city)

    products = [pro.value for pro in ProductName]
    df = None
    for pro in products:
        response = requests.get(
            f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product={pro}")
        values, dates = response.json()["mean_values"], response.json()["unique_dates"]
        if df is None:
            df = pd.DataFrame({pro: values})
        else:
            df[pro] = values

    df["dates"] = dates
    df = df.fillna("")

    return {"data": df}


# Endpoint to retrieve data for a specific product in a specific city
@app.get("/items/{city}/{product}")
async def read_item_prod(city: str, product: ProductName):
    latitude, longitude = find_coordinates(city)

    response = requests.get(
        f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product={product.value}")
    values, dates = response.json()["mean_values"], response.json()["unique_dates"]

    data = pd.DataFrame({product: values})

    data["dates"] = dates
    data = data.fillna("")

    return {"data": data}


# Endpoint to retrieve and compare data for a specific product between two cities
@app.get("/items/{city}/{product}/{city_comparison}")
async def read_item_comp(city: str, product: ProductName, city_comparison: str):
    latitude, longitude = find_coordinates(city)

    latitude_comparison, longitude_comparison = find_coordinates(city_comparison)

    response = requests.get(
        f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product={product.value}")
    values, dates = response.json()["mean_values"], response.json()["unique_dates"]
    response = requests.get(
        f"http://zarr_db:5000/search_by_coordinate?latitude={latitude_comparison}&longitude={longitude_comparison}&product={product.value}")
    values_comparison, dates_comparison = response.json()["mean_values"], response.json()["unique_dates"]

    data = pd.DataFrame({city: values, city_comparison: values_comparison})

    data["dates"] = dates
    data = data.fillna("")

    return {"data": data}


# Endpoint to retrieve data for a specific product in a specific city within a date range
@app.get("/items/{city}/{product}/{start_date}/{end_date}")
async def read_item_date(city: str, product: ProductName, start_date: str, end_date: str):
    latitude, longitude = find_coordinates(city)

    # Check if the date format is valid
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")

    response = requests.get(
        f"http://zarr_db:5000/search_by_date?latitude={latitude}&longitude={longitude}&product={product.value}&start_date={start_date}&end_date={end_date}")
    values, dates = response.json()["mean_values"], response.json()["unique_dates"]

    data = pd.DataFrame({product: values})

    data["dates"] = dates
    data = data.fillna("")

    return {"data": data}


# Endpoint to retrieve Air Quality Index (AQI) for a specific city
@app.get("/AQI/{city}")
async def read_item_AQI(city: str):
    latitude, longitude = find_coordinates(city)

    response = requests.get(f"http://zarr_db:5000/get_aqi?latitude={latitude}&longitude={longitude}")
    value = response.json()["AQI"]

    data = {"AQI": value}

    return {"data": data}


# Run the FastAPI app using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
