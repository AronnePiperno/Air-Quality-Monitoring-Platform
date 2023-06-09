from dask.distributed import Client
import dask.array as da
import dask
import os
import zarr
from datetime import datetime
import numpy as np
def by_qa_value():
    pass

def mean_by_date(values, dates):
    unique_dates = np.unique(dates)
    mean_values = []

    for date in unique_dates:
        indices = np.where(date == dates)
        mean_value = np.mean(values[indices])
        mean_values.append(mean_value)

    return mean_values, unique_dates

def by_coordinate(latitude, longitude, product, precision = 0.5):

    client = Client(n_workers=3, threads_per_worker=3, memory_limit='10GB')
    dask.config.set({'array.slicing.split_large_chunks': False})
    client.amm.start()

    qa_value = da.from_zarr(os.path.join('./db', product + '.zarr'), component='qa_value', chunks='auto')
    latitude_arr = da.from_zarr(os.path.join('./db', product + '.zarr'), component='latitude', chunks='auto')
    longitude_arr = da.from_zarr(os.path.join('./db', product + '.zarr'), component='longitude', chunks='auto')

    match product:
        case 'L2__CH4___':
            column = 'methane_mixing_ratio_bias_corrected'
        case 'L2__CO____':
            column = 'carbonmonoxide_total_column'
        case 'L2__HCHO__':
            column = 'formaldehyde_tropospheric_vertical_column'
        case 'L2__NO2___':
            column = 'nitrogendioxide_tropospheric_column'
        case 'L2__O3____':
            column = 'ozone_total_vertical_column'
        case 'L2__SO2___':
            column ='sulfurdioxide_total_vertical_column'
        case _:
            raise ValueError('Product not supported')

    pollutant = da.from_zarr(os.path.join('./db', product + '.zarr'), component=column, chunks='auto')
    """
    index = np.where(
        (latitude_arr[500:] >= latitude - precision) &
        (latitude_arr[500:] <= latitude + precision) &
        (longitude_arr[500:] >= longitude - precision) &
        (longitude_arr[500:] <= longitude + precision) &
        (qa_value[500:] > 0.5) &
        (pollutant[500:] < 100000)
    )
    """
    store = zarr.open(os.path.join("./db", product+'.zarr'), mode="r")
    print(store['longitude'].shape)
    print(store['latitude'].shape)
    print(store['qa_value'].shape)
    print(store[column].shape)

    shape = store['longitude'].shape[0]
    index = da.where(
        da.logical_and(store['longitude'][:] >= longitude - precision, store['longitude'][:] <= longitude + precision) &
        da.logical_and(store['latitude'][:] >= latitude - precision, store['latitude'][:] <= latitude + precision) &
        (store['qa_value'][:] > 0.5) &
        (store[column][:] < 9.9692100e+10))
    index = da.compute(index)

    db = zarr.open(os.path.join('./db', product + '.zarr'))

    print('---------------------------------')
    print(index)
    print('---------------------------------')

    dates = db['time'][index[0][0]]
    dates = [datetime.fromtimestamp(date).replace(year=2023).date() for date in dates]

    print('---------------------------------')
    print(db[column][index[0]])
    print(dates)
    print('---------------------------------')

    dict = {'dates':dates}

    mean_values, unique_dates = mean_by_date(np.array(db[column][index[0]]), np.array(dates))

    return mean_values, unique_dates


def by_date(date):
    pass

def by_time(time):
    pass

def by_product(product):
    pass


def main():
    by_coordinate(45.4641943, 9.189634, 'L2__CH4___')

if __name__ == '__main__':
    main()