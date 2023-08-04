# Import necessary libraries and modules
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from geopy.geocoders import Nominatim
import base64
import seaborn as sns
import pandas as pd
import requests


# Define a function to fetch data for a given location and product
def kpis(latitude, longitude, product):
    # Fetch data from the DB
    response = requests.get(
        f"http://zarr_db:5000/search_by_coordinate?latitude={latitude}&longitude={longitude}&product={product}")
    values, dates = response.json()["mean_values"], response.json()["unique_dates"]
    dates = [' '.join(date.split()[1:3]) for date in dates]
    location_average = np.nanmean(values)
    location_average_f = "{:.6f}".format(location_average)
    return location_average_f, values, dates


# Define a function to set up and return a graph
def graph_setup(df, product):
    # Filter out zero and negative values from the DataFrame
    df = df[df[0] > 0]

    # Process product name for display
    product = product.rstrip('_')
    product = product.split('_')[-1]

    # Create a boxplot and a line chart
    fig, ax = plt.subplots(1, 2, figsize=(25, 5), gridspec_kw={'width_ratios': [1, 2]})
    box_color = 'black'
    boxplot = ax[0].boxplot(df, boxprops=dict(color=box_color, facecolor="#ffffff"), widths=0.4, patch_artist=True)
    ax[0].patch.set_alpha(0)
    plt.setp(boxplot['medians'], color='#a98467')
    ax[0].set_xlabel("{}".format(product))
    ax[0].set_title('{} Boxplot'.format(product), size=20)
    ax[0].axes.set_facecolor('white')
    ax[0].set_facecolor('white')

    ax[1].plot(df.index, df[0], alpha=0.5, color="#000000", linewidth=2, marker='o', markersize=4)
    ax[1].set_title("{} trend".format(product), size=20)
    ax[1].set_ylim(min(df[0]) * 0.99, max(df[0]) * 1.01)
    ax[1].set_ylabel("{} values".format(product))

    # Customize the style
    sns.set_style("darkgrid", rc={
        'figure.facecolor': '#f5f3f4',
        'axes.facecolor': '#ffffff',
        'axes.edgecolor': '#000000',
        'axes.labelcolor': '#000000',
        'xtick.color': '#000000',
        'ytick.color': '#000000',
        'grid.color': '#cccccc'
    })

    return fig


# Define a function to set up and return a comparison graph
def graph_comparison_setup(df, city, city_comparison, product):
    # Initialize a geolocator to retrieve latitude and longitude of the comparison city
    geolocator_comparison = Nominatim(user_agent="MyApp")
    location_comparison = geolocator_comparison.geocode(city_comparison)

    # Handle case where the geolocator fails to find the comparison city
    if location_comparison is None:
        st.error("I'm sorry, I could not find this city!")

    longitude_comparison = location_comparison.longitude
    latitude_comparison = location_comparison.latitude

    # Fetch KPIs for the comparison city
    mean_comparison, values_comparison, dates_comparison = kpis(latitude_comparison, longitude_comparison, product)

    # Create DataFrames for comparison
    df_comparison = pd.DataFrame(values_comparison, dates_comparison)
    df_boxplot_comparison = df_comparison[df_comparison[0] > 0]
    df_boxplot = df[df[0] > 0]

    # Process product name for display
    product = product.rstrip('_')
    product = product.split('_')[-1]

    # Create a boxplot and a line chart for comparison
    fig, ax = plt.subplots(1, 2, figsize=(25, 5), gridspec_kw={'width_ratios': [1, 2]})
    box_color = 'black'
    boxplot1 = ax[0].boxplot([df_boxplot[0], df_boxplot_comparison[0]],
                             boxprops=dict(color=box_color, facecolor="#ffffff"), widths=0.4, patch_artist=True,
                             labels=[city, city_comparison])
    ax[0].patch.set_alpha(0)
    plt.setp(boxplot1['medians'], color='#a98467')
    ax[0].set_xlabel("{}".format(product))
    ax[0].set_title('{} Boxplot'.format(product), size=20)
    ax[0].axes.set_facecolor('white')
    ax[0].set_facecolor('white')

    ax[1].plot(df.index, df[0], alpha=0.5, color="#000000", linewidth=2, marker='o', markersize=4, label=city)
    ax[1].plot(df_comparison.index, df_comparison[0], alpha=0.5, color="#FF0000", linewidth=2, marker='o', markersize=4,
               label=city_comparison)
    ax[1].set_title("{} trend".format(product), size=20)
    ax[1].set_ylabel("{} values".format(product))
    ax[1].legend()

    # Customize the style
    sns.set_style("darkgrid", rc={
        'figure.facecolor': '#f5f3f4',
        'axes.facecolor': '#ffffff',
        'axes.edgecolor': '#000000',
        'axes.labelcolor': '#000000',
        'xtick.color': '#000000',
        'ytick.color': '#000000',
        'grid.color': '#cccccc'
    })

    return fig


# Define a function to add a background image to the Streamlit app
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


# Define a function to get a color based on value ranges
def get_color(value):
    color_ranges = [
        {'min_value': 0, 'max_value': 25, 'color': '#00FF00'},
        {'min_value': 25, 'max_value': 50, 'color': '#FFFF00'},
        {'min_value': 50, 'max_value': 75, 'color': '#FFA500'},
        {'min_value': 75, 'max_value': 999, 'color': '#FF0000'},
    ]

    for color_range in color_ranges:
        if color_range['min_value'] <= value <= color_range['max_value']:
            return color_range['color']
    return '#FFFFFF'


# Define a function to get air quality based on color
def get_quality(color):
    if color == '#00FF00':
        return 'Good'
    elif color == '#FFFF00':
        return 'Fair'
    elif color == '#FFA500':
        return 'Poor'
    elif color == '#FF0000':
        return 'Very Poor'
    else:
        return 'Data not available'


if __name__ == '__main__':
    pass
