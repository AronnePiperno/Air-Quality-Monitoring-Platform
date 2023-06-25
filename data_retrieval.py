from dask.distributed import Client
import dask.array as da
import dask
import os
import zarr
from datetime import datetime
import numpy as np
import xarray as xr
def by_qa_value():
    pass

def mean_by_date(values, dates):
    unique_dates = np.unique(dates)
    mean_values = []

    for date in unique_dates:
        indices = np.where(date == dates)
        mean_value = np.nanmean(values[indices])
        mean_values.append(mean_value)

    return mean_values, unique_dates

def by_coordinate(latitude, longitude, product, precision = 0.5):
    since = datetime.now()
    client = Client(n_workers=3, threads_per_worker=3, memory_limit='10GB')
    dask.config.set({'array.slicing.split_large_chunks': False})
    client.amm.start()


    match product:
        case 'L2__CH4___':
            column = 'CH4_column_volume_mixing_ratio_dry_air'
        case 'L2__CO____':
            column = 'CO_column_number_density'
        case 'L2__HCHO__':
            column = 'tropospheric_HCHO_column_number_density'
        case 'L2__NO2___':
            column = 'tropospheric_NO2_column_number_densityn'
        case 'L2__O3____':
            column = 'O3_column_number_density'
        case 'L2__SO2___':
            column ='SO2_column_number_density'
        case _:
            raise ValueError('Product not supported')



    ds = xr.open_zarr(os.path.join("./db", product+'.zarr'), chunks='auto')


    lat = da.where(da.isclose(ds['latitude_bounds'].values, np.float64(round(latitude,1))))
    long = da.where(da.isclose(ds['longitude_bounds'].values, np.float64(round(longitude,1))))
    print("longpasf",type(longitude))
    lat = da.compute(lat)
    long = da.compute(long)
    print(lat)
    print(long)
    print(type(ds["longitude_bounds"].values[0][0]))
    ds = ds.sel(latitude=lat[0][0], longitude=long[0][0])


    dates = ds['datetime_start'].values
    dates = [datetime.fromtimestamp(date).replace(year=2023).date() for date in dates]

    mean_values, unique_dates = mean_by_date(np.array(ds[column].values), np.array(dates))
    '''index = da.where(
        da.logical_and(store['longitude'][:] >= longitude - precision, store['longitude'][:] <= longitude + precision) &
        da.logical_and(store['latitude'][:] >= latitude - precision, store['latitude'][:] <= latitude + precision) &
        (store['qa_value'][:] > 0.5) &
        (store[column][:] < 9.9692100e+10))
    index = da.compute(index)'''
    """
    db = zarr.open(os.path.join('./db', product + '.zarr'))

    dates = db['datetime_start'][index[0][0]]
    dates = [datetime.fromtimestamp(date).replace(year=2023).date() for date in dates]

    mean_values, unique_dates = mean_by_date(np.array(db[column][index[0]]), np.array(dates))"""
    to = datetime.now()
    print('Time elapsed', to - since)
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
    print(by_coordinate(45.4641943, 9.189634, 'L2__CO____'))
    #main()