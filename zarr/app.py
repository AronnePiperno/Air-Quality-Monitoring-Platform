# Import the Flask framework and functions from the data_retrieval module
from flask import Flask, request
from data_retrieval import *

# Create a Flask application instance
app = Flask(__name__)


# Route to search data by date range
@app.route("/search_by_date", methods=["GET"])
def search_by_date():
    # Extract parameters from the request URL
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    product = request.args.get("product")

    # Call the by_date function to retrieve data for the specified date range, latitude, and longitude
    mean_values, unique_dates = by_date(latitude, longitude, product, start_date, end_date)

    # Return the mean values and unique dates as a JSON response
    return {"mean_values": mean_values, "unique_dates": unique_dates.tolist()}


# Route to search data by coordinate
@app.route("/search_by_coordinate", methods=["GET"])
def search_by_coordinate():
    # Extract parameters from the request URL
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    product = request.args.get("product")

    # Call the by_coordinate function to retrieve data for the specified coordinate and product
    mean_values, unique_dates = by_coordinate(latitude, longitude, product)

    # Return the mean values and unique dates as a JSON response
    return {"mean_values": mean_values, "unique_dates": unique_dates.tolist()}


# Route to get Air Quality Index (AQI) at a specific coordinate
@app.route("/get_aqi", methods=["GET"])
def get_aqi():
    # Extract parameters from the request URL
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))

    # Call the calc_aqi function to calculate the AQI at the specified coordinate
    AQI = calc_aqi(latitude, longitude)

    # Return the AQI as a JSON response
    return {"AQI": AQI}


# Entry point of the script
if __name__ == "__main__":
    # Run the Flask application on host "0.0.0.0" and port 5000
    app.run(host="0.0.0.0", port=5000, debug=False)
