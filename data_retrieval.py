import pandas as pd
from dask.distributed import Client
import dask.array as da
import dask
import os
from datetime import datetime, timedelta
import numpy as np
import xarray as xr
import redis
import pickle

def mean_by_date(values, dates):
    unique_dates = np.unique(dates)
    mean_values = []

    for date in unique_dates:
        indices = date == dates
        mean_value = np.nanmean(values[indices])
        mean_values.append(mean_value)

    return mean_values, unique_dates


def return_column(product):
    match product:
        case 'L2__CO____':
            column = 'CO_column_number_density'
        case 'L2__HCHO__':
            column = 'tropospheric_HCHO_column_number_density'
        case 'L2__NO2___':
            column = 'tropospheric_NO2_column_number_density'
        case 'L2__O3____':
            column = 'O3_column_number_density'
        case 'L2__SO2___':
            column ='SO2_column_number_density'
        case _:
            raise ValueError('Product not supported')

    return column


def calculate_last_date():
    ds = xr.open_zarr(os.path.join("./db", 'L2__CO____'+'.zarr'), chunks='auto')
    dates = ds['datetime_start'].values
    date = max(dates)
    last_date = datetime.fromtimestamp(date).replace(year=2023).date()

    return last_date


def serialize_data(data):
    return pickle.dumps(data)


def deserialize_data(data):
    return pickle.loads(data)


def by_coordinate(latitude, longitude, product):
    with redis.Redis(host='localhost', port=6379, db=0) as redis_client:
        cache_key = f"{round(latitude,1)}_{round(longitude,1)}_{product}"

        # Check if the result is already in the Redis cache
        if redis_client.exists(cache_key):
            print("Cache hit!")
            cached_data = redis_client.get(cache_key)
            return deserialize_data(cached_data)

        since = datetime.now()
        client = Client(n_workers=3, threads_per_worker=3, memory_limit='4GB')
        dask.config.set({'array.slicing.split_large_chunks': True})
        client.amm.start()

        column = return_column(product)

        ds = xr.open_zarr(os.path.join("./db", product+'.zarr'), chunks='auto')

        lat = da.where(da.isclose(ds['latitude_bounds'].values, np.float64(round(latitude,1))))
        long = da.where(da.isclose(ds['longitude_bounds'].values, np.float64(round(longitude,1))))

        lat = da.compute(lat)
        long = da.compute(long)

        ds = ds.sel(latitude=lat[0][0], longitude=long[0][0])

        dates = ds['datetime_start'].values
        dates = [datetime.fromtimestamp(date).replace(year=2023).date() for date in dates]

        mean_values, unique_dates = mean_by_date(np.array(ds[column].values), np.array(dates))
        to = datetime.now()
        print('Time elapsed', to - since)

        client.close()

        # Save the result in the Redis cache before returning it
        serialized_data = serialize_data((mean_values, unique_dates))
        redis_client.set(cache_key, serialized_data)

        return mean_values, unique_dates


def by_date(latitude: float, longitude: float, product: str, start_date: str, end_date: str):

    with redis.Redis(host='localhost', port=6379, db=0) as redis_client:
        cache_key = f"{round(latitude,1)}_{round(longitude,1)}_{product}_{start_date}_{end_date}"

        # Check if the result is already in the Redis cache
        if redis_client.exists(cache_key):
            print("Cache hit!")
            cached_data = redis_client.get(cache_key)
            return deserialize_data(cached_data)

        epoch = datetime(2010, 1, 1)
        client = Client(n_workers=3, threads_per_worker=3, memory_limit='4GB')
        dask.config.set({'array.slicing.split_large_chunks': False})
        client.amm.start()

        column = return_column(product)

        ds = xr.open_zarr(os.path.join("./db", product+'.zarr'), chunks='auto')

        start = np.float64((datetime.strptime(start_date, '%Y-%m-%d') - epoch).total_seconds())
        end = np.float64((datetime.strptime(end_date, '%Y-%m-%d') - epoch).total_seconds())

        index = da.where((ds['datetime_start'].values >= start) & (ds['datetime_start'].values <= end))
        lat = da.where(da.isclose(ds['latitude_bounds'].values, np.float64(round(latitude,1))))
        long = da.where(da.isclose(ds['longitude_bounds'].values, np.float64(round(longitude,1))))

        index = da.compute(index)
        lat = da.compute(lat)
        long = da.compute(long)

        ds = ds.sel(time=index[0][0], latitude=lat[0][0], longitude=long[0][0])

        dates = ds['datetime_start'].values

        dates = [datetime.fromtimestamp(date).replace(year=2023).date() for date in dates]

        mean_values, unique_dates = mean_by_date(np.array(ds[column].values), np.array(dates))

        client.close()

        # Save the result in the Redis cache before returning it
        serialized_data = serialize_data((mean_values, unique_dates))
        redis_client.set(cache_key, serialized_data)

        return mean_values, unique_dates



def calculate_aqi(pollutant, concentration):
    # Define AQI breakpoints and corresponding index values for each pollutant
    # The values below are for the United States AQI, which may vary for other regions
    if concentration < 0 or concentration == np.nan:
        return
    breakpoints = {
        "CO": [0, 4.4, 9.4, 12.4, 15.4, 30.4, 40.4, 50.4, 90.4],
        "NO2": [0, 53, 100, 360, 649, 1249, 1649, 2049, 4049],
        "O3": [0, 54, 70, 85, 105, 200, 264, 325, 604],
        "SO2": [0, 35, 75, 185, 304, 604, 804, 1004, 2004],
    }
    index_values = [0, 50, 100, 150, 200, 300, 400, 500]

    # Find the breakpoint category for the pollutant concentration
    for i in range(1, len(breakpoints[pollutant])):
        print(i)
        if concentration <= breakpoints[pollutant][i]:
            break

    # Calculate the AQI for the pollutant
    aqi = ((index_values[i] - index_values[i - 1]) / (breakpoints[pollutant][i] - breakpoints[pollutant][i - 1])) * (
            concentration - breakpoints[pollutant][i - 1]
    ) + index_values[i - 1]

    return aqi


def calculate_overall_aqi(latitude, longitude):
    last_date = str(calculate_last_date())
    pre_last_date = str(datetime.strptime(last_date, '%Y-%m-%d').date() - timedelta(days=1))
    pollutants_data = {
        "CO": by_date(latitude, longitude, "L2__CO____", pre_last_date, last_date)[0],
        "NO2": by_date(latitude, longitude, "L2__NO2___", pre_last_date, last_date)[0],
        "O3": by_date(latitude, longitude, "L2__O3____", pre_last_date, last_date)[0],
        "SO2": by_date(latitude, longitude, "L2__SO2___", pre_last_date, last_date)[0]
    }
    print(pollutants_data['CO'])
    print(pollutants_data['NO2'])
    print(pollutants_data['O3'])
    print(pollutants_data['SO2'])

    aqi_values = []

    for pollutant, concentration in pollutants_data.items():
        if not concentration:
            continue
            print('here')
        else:
            concentration = float(concentration[0])

        print('there')
        aqi = calculate_aqi(pollutant, concentration)
        aqi_values.append(aqi)

    # Calculate the AQI as the highest AQI value among all pollutants
    overall_aqi = max(aqi_values)
    return overall_aqi


import aqi
def calc_aqi(latitude, longitude):
    last_date = str(calculate_last_date() - timedelta(days=2))
    pre_last_date = str(datetime.strptime(last_date, '%Y-%m-%d').date() - timedelta(days=1))


    CO = 0 if np.isnan(by_date(latitude, longitude, "L2__CO____", pre_last_date, last_date)[0][0]) or by_date(latitude, longitude, "L2__CO____", pre_last_date, last_date)[0][0] < 0 else by_date(latitude, longitude, "L2__CO____", pre_last_date, last_date)[0][0]
    NO2 = 0 if np.isnan(by_date(latitude, longitude, "L2__NO2___", pre_last_date, last_date)[0][0]) or by_date(latitude, longitude, "L2__NO2___", pre_last_date, last_date)[0][0] < 0 else by_date(latitude, longitude, "L2__NO2___", pre_last_date, last_date)[0][0]
    O3 = 0 if np.isnan(by_date(latitude, longitude, "L2__O3____", pre_last_date, last_date)[0][0]) or by_date(latitude, longitude, "L2__O3____", pre_last_date, last_date)[0][0] < 0 else by_date(latitude, longitude, "L2__O3____", pre_last_date, last_date)[0][0]
    SO2 = 0 if np.isnan(by_date(latitude, longitude, "L2__SO2___", pre_last_date, last_date)[0][0]) or by_date(latitude, longitude, "L2__SO2___", pre_last_date, last_date)[0][0] < 0 else by_date(latitude, longitude, "L2__SO2___", pre_last_date, last_date)[0][0]

    # conversion from mol/m^2 to ppm/ppb
    CO = (CO/10)*1e3*28.01
    NO2 = (NO2/10)*1e3*46.01
    O3 = (O3/10)*1e3*48.00/5
    SO2 = (SO2/10)*1e2*64.06

    print(CO, NO2, O3, SO2)
    try:
        aq = aqi.to_aqi([
        (aqi.POLLUTANT_CO_8H, 0.9),
        (aqi.POLLUTANT_NO2_1H, NO2),
        (aqi.POLLUTANT_O3_1H, O3),
        (aqi.POLLUTANT_SO2_1H, SO2)
        ], algo=aqi.ALGO_MEP)
        print(aq)
    except:
        return 0

def main():
    print(calc_aqi(11.1, 11.12))
    #print(by_date(46.07, 11.12, "L2__CO____", '2023-06-15', '2023-06-16'))


if __name__ == '__main__':
    main()