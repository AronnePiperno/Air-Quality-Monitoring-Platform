
from dask.distributed import Client
import dask.array as da
import dask
import os
from datetime import datetime, timedelta
import numpy as np
import xarray as xr
import redis
import pickle
import aqi

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
    with Client(n_workers=3, threads_per_worker=3, memory_limit='4GB'):
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
    with redis.Redis(host='redis', port=6379, db=0) as redis_client:
        cache_key = f"{round(latitude,1)}_{round(longitude,1)}_{product}"

        # Check if the result is already in the Redis cache
        if redis_client.exists(cache_key):
            cached_data = redis_client.get(cache_key)
            return deserialize_data(cached_data)

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


        client.close()

        # Save the result in the Redis cache before returning it
        serialized_data = serialize_data((mean_values, unique_dates))
        redis_client.set(cache_key, serialized_data)

        return mean_values, unique_dates


def by_date(latitude: float, longitude: float, product: str, start_date: str, end_date: str):

    with redis.Redis(host='redis', port=6379, db=0) as redis_client:
        cache_key = f"{round(latitude,1)}_{round(longitude,1)}_{product}_{start_date}_{end_date}"

        # Check if the result is already in the Redis cache
        if redis_client.exists(cache_key):
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



def calc_aqi(latitude, longitude):

    CO = np.nanmean(by_coordinate(latitude, longitude, "L2__CO____")[0])
    NO2 = np.nanmean(by_coordinate(latitude, longitude, "L2__NO2___")[0])
    O3 = np.nanmean(by_coordinate(latitude, longitude, "L2__O3____")[0])
    SO2 = np.nanmean(by_coordinate(latitude, longitude, "L2__SO2___")[0])

    # conversion from mol/m^2 to ppm/ppb
    CO = (CO/10)*1e3*28.01*10000
    NO2 = (NO2/10)*1e3*46.01*100
    O3 = (O3/10)*1e3*48.00/8
    SO2 = (SO2/10)*1e2*64.06*10000

    try:
        return aqi.to_aqi([
        (aqi.POLLUTANT_CO_8H, CO),
        (aqi.POLLUTANT_NO2_1H, NO2),
        (aqi.POLLUTANT_O3_1H, O3),
        (aqi.POLLUTANT_SO2_1H, SO2)
        ], algo=aqi.ALGO_MEP)

    except:
        return -1

def main():
    pass


if __name__ == '__main__':
    main()