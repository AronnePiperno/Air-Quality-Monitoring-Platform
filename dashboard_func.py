import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from geopy.geocoders import Nominatim
import data_retrieval
import base64
import seaborn as sns
import time
import pandas as pd

def kpis(latitude, longitude, product):
    values, dates = data_retrieval.by_coordinate(latitude, longitude, product)
    location_average = np.nanmean(values)
    location_average_f = "{:.6f}".format(location_average)
    return location_average_f, values, dates


def graph_setup (df, values, dates, product):

    df = df[df[0] > 0]
    
    product = product.rstrip('_')
    product = product.split('_')[-1]

    # Boxplot
    fig, ax = plt.subplots(1,2, figsize=(35, 12), gridspec_kw={'width_ratios': [1, 2]})
    box_color = 'black'
    boxplot = ax[0].boxplot(df, boxprops=dict(color=box_color, facecolor="#ffffff"), widths=0.4, patch_artist=True)
    ax[0].patch.set_alpha(0)
    plt.setp(boxplot['medians'], color='#a98467')
    ax[0].set_xlabel("{}".format(product))
    ax[0].set_title('{} Boxplot'.format(product), size=20)
    ax[0].axes.set_facecolor('white')
    ax[0].set_facecolor('white')

    # Line Chart
    ax[1].plot(df.index, df[0], # by default area charts are stacked
            alpha=0.5,
            color="#000000",
            linewidth=2,              # Increase the line width
            marker='o',               # Add markers to data points
            markersize=4) # increasing the figsize is another workaround for improving the legend location

    ax[1].set_title("{} trend".format(product), size=20)
    ax[1].set_ylim(min(df[0])*0.99, max(df[0])*1.01)
    ax[1].set_ylabel("{} values".format(product))

    sns.set_style("darkgrid", rc = {'figure.facecolor': '#f5f3f4',
        'axes.facecolor': '#ffffff',  # Set axes background color to light gray
        'axes.edgecolor': '#000000',  # Set axes edge color to black
        'axes.labelcolor': '#000000',  # Set axis label color to black
        'xtick.color': '#000000',  # Set x-axis tick label color to black
        'ytick.color': '#000000',  # Set y-axis tick label color to black
        'grid.color': '#cccccc'  # Set grid line color to light gray
    })

    return fig, ax


def graph_comparison_setup (df, city, city_comparison, product):

    geolocator_comparison = Nominatim(user_agent="MyApp")
    location_comparison = geolocator_comparison.geocode(city_comparison)
    longitude_comparison = location_comparison.longitude
    latitude_comparison = location_comparison.latitude
    mean_comparison, values_comparison, dates_comparison = kpis(latitude_comparison, longitude_comparison, product)
    df_comparison = pd.DataFrame(values_comparison, dates_comparison)
    df_boxplot_comparison = df_comparison[df_comparison[0] > 0]
    df_boxplot = df[df[0] > 0]

    product = product.rstrip('_')
    product = product.split('_')[-1]

    # Boxplot
    fig, ax = plt.subplots(1,2, figsize=(35, 12), gridspec_kw={'width_ratios': [1, 2]})
    box_color = 'black'
    boxplot1 = ax[0].boxplot([df_boxplot[0],df_boxplot_comparison[0]], boxprops=dict(color=box_color, facecolor="#ffffff"), widths=0.4, patch_artist=True, labels=[city, city_comparison])
    ax[0].patch.set_alpha(0)
    plt.setp(boxplot1['medians'], color='#a98467')
    ax[0].set_xlabel("{}".format(product))
    ax[0].set_title('{} Boxplot'.format(product), size=20)
    ax[0].axes.set_facecolor('white')
    ax[0].set_facecolor('white')

    # Line Chart

    df_merged = pd.merge(df, df_comparison, left_index=True, right_index=True)
    
    ax[1].plot(df.index, df[0], # by default area charts are stacked
            alpha=0.5,
            color="#000000",
            linewidth=2,              # Increase the line width
            marker='o',               # Add markers to data points
            markersize=4,
            label=city) # increasing the figsize is another workaround for improving the legend location
    
    ax[1].plot(df_comparison.index, df_comparison[0],
            alpha=0.5,
            color="#FF0000",
            linewidth=2,
            marker='o',
            markersize=4,
            label=city_comparison)  # Add this line
    
    ax[1].set_title("{} trend".format(product), size=20)
    ax[1].set_ylim(min(values)*0.99, max(values)*1.01)
    ax[1].set_ylabel("{} values".format(product))
    ax[1].legend()

    sns.set_style("darkgrid", rc = {'figure.facecolor': '#f5f3f4',
        'axes.facecolor': '#ffffff',  # Set axes background color to light gray
        'axes.edgecolor': '#000000',  # Set axes edge color to black
        'axes.labelcolor': '#000000',  # Set axis label color to black
        'xtick.color': '#000000',  # Set x-axis tick label color to black
        'ytick.color': '#000000',  # Set y-axis tick label color to black
        'grid.color': '#cccccc'  # Set grid line color to light gray
    })

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
