import zarr
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def find_indexes(longitude, latitude, product):
    store = zarr.open(os.path.join("./db", product + '.zarr'), mode="r")
    precision = 1
    index = np.where(np.logical_and(store['longitude'][:] >= longitude-precision, store['longitude'][:] <= longitude+precision) &
                 np.logical_and(store['latitude'][:] >= latitude-precision, store['latitude'][:] <= latitude+precision) &
                 (store['qa_value'][:] > 0.5)&(store["methane_mixing_ratio_bias_corrected"][:] < 9.9692100e+10))
    return index

def find_clean_data_indexes(product):
    store = zarr.open(os.path.join("./db", product + '.zarr'), mode="r")
    index = np.where((store['qa_value'][:] >= 0.5)&(store["methane_mixing_ratio_bias_corrected"][:] < 9.9692100e+10))
    return index

def data_retrieving(indexes, product, column):
    store = zarr.open(os.path.join("./db", product + '.zarr'), mode="r")
    #print(datetime.fromtimestamp(store[column][indexes].max()))
    #print(datetime.fromtimestamp(store[column][indexes].min()))
    return store[column][indexes]

def dates_and_mean_values_product(longitude, latitude, product):
    index = find_indexes(longitude, latitude, product)
    values = data_retrieving(index, product, "methane_mixing_ratio_bias_corrected")
    dates = data_retrieving(index[0], product, "time")
    dates = np.array([datetime.fromtimestamp(date).replace(year=2023).date() for date in dates])
    unique_dates = np.unique(dates)
    mean_values = []
    
    for date in unique_dates:
        indices = np.where(date == dates)
        mean_value = np.mean(values[indices])
        mean_values.append(mean_value)

    return unique_dates, mean_values

def ww_min_by_product (product):
    return min(data_retrieving(find_clean_data_indexes("L2__CH4___"), "L2__CH4___", "methane_mixing_ratio_bias_corrected"))

def ww_max_by_product (product):
    return max(data_retrieving(find_clean_data_indexes("L2__CH4___"), "L2__CH4___", "methane_mixing_ratio_bias_corrected"))



def main():

    latitude = 41
    longitude = 12

    fig, ax = plt.subplots()
    ax.plot(dates_and_mean_values_product(longitude, latitude, "L2__CH4___")[0], dates_and_mean_values_product(longitude, latitude, "L2__CH4___")[1], label="Trento")
    #ax.plot(dates_and_mean_values_product(longitude, latitude, "L2__CH4___")[0], dates_and_mean_values_product(longitude, latitude, "L2__CH4___")[2], label="World")
    ax.set_xlabel("Date")
    ax.set_ylabel("Methane values")
    # Format the x-axis tick labels
    date_format = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.set_ylim(ww_min_by_product("L2__CH4___"), ww_max_by_product("L2__CH4___"))
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    main()

