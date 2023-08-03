from flask import Flask, request, jsonify
from data_retrieval import *
import numpy as np

app = Flask(__name__)

@app.route("/search_by_date", methods=["GET"])
def search_by_date():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    product = request.args.get("product")

    mean_values, unique_dates = by_date(latitude, longitude, product, start_date, end_date)

    return {"mean_values": mean_values, "unique_dates": unique_dates.tolist()}

@app.route("/search_by_coordinate", methods=["GET"])
def search_by_coordinate():
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    product = request.args.get("product")

    mean_values, unique_dates = by_coordinate(latitude, longitude, product)

    return {"mean_values": mean_values, "unique_dates": unique_dates.tolist()}


@app.route("/get_aqi", methods=["GET"])
def get_aqi():
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))

    AQI = calc_aqi(latitude, longitude)

    return {"AQI": AQI}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)





