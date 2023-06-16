import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from geopy.geocoders import Nominatim
import data_retrieval
import base64
import time

def kpis(latitude, longitude, product):
    values, dates = data_retrieval.by_coordinate(latitude, longitude, product)
    location_average = np.mean(values)
    location_average_f = "{:.6f}".format(location_average)
    return location_average_f, values, dates

def graph_setup (dates, values, city, pollutant):
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 4)
    ax.plot(dates, values, label=city)
    ax.set_xlabel("Date")
    ax.set_ylabel(pollutant)
    date_format = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)
    return fig

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )