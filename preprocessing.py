import harp
"""
filename = './data/S5P_OFFL_L2__CH4____20230530T002422_20230530T020552_29150_03_020500_20230531T162852.nc'

operations = ';'.join([
    "CH4_column_volume_mixing_ratio_dry_air_validity>50",
    "keep(latitude_bounds,longitude_bounds,CH4_column_volume_mixing_ratio_dry_air)",
    "derive(CH4_column_volume_mixing_ratio_dry_air [ppb])"
    #"derive(latitude {latitude})",
    #"derive(longitude {longitude})",
])

product = harp.import_product(filename, operations)
print(product)

product.to_xarray().to_netcdf('./resized/test.nc')
"""
"""
import xarray as xr

ds = xr.open_dataset('./resized/test.nc')
ds.to_zarr('./resized/test.zarr')
"""
"""
import xarray as xr

ds = xr.open_zarr('./resized/test.zarr')

index = ds.sel(longitude_bounds=9.189634, latitude_bounds=45.4641943, method='nearest')
#print(ds)
"""
"""
filename_1 = './data/S5P_OFFL_L2__CH4____20230530T002422_20230530T020552_29150_03_020500_20230531T162852.nc'
filename_2 = './data/S5P_OFFL_L2__CH4____20230530T121452_20230530T135622_29157_03_020500_20230601T045107.nc'
operations = ';'.join([
    "CH4_column_volume_mixing_ratio_dry_air_validity>50",
    "derive(CH4_column_volume_mixing_ratio_dry_air [ppb])",
    "derive (datetime_stop {time})",
    "bin_spatial(1801,-90,0.1,3601,-180,0.1)",
    "derive(latitude {latitude})",
    "derive(longitude {longitude})",
    "keep(latitude_bounds,longitude_bounds,CH4_column_volume_mixing_ratio_dry_air)"
    ])
reduce_operations=";".join([
    "squash(time, (latitude, longitude, latitude_bounds, longitude_bounds))",
    "bin()"
])

#product = harp.import_product(filename, operations = operations,post_operations="bin(); squash(time, (latitude,longitude)")
product_1 = harp.import_product(filename_1, operations = operations, reduce_operations=reduce_operations)
product_2 = harp.import_product(filename_2, operations = operations, reduce_operations=reduce_operations)

product_1.to_xarray().to_netcdf('./resized/reduced.nc')
product_2.to_xarray().to_netcdf('./resized/reduced_2.nc')"""

import xarray as xr
"""
ds_1 = xr.open_dataset('./resized/reduced.nc')
ds_2 = xr.open_dataset('./resized/reduced_2.nc')

ds = xr.concat([ds_1, ds_2], dim='time')
ds.to_zarr('./resized/xarrayconcat.zarr')
"""

"""

operations = ';'.join([
    "CH4_column_volume_mixing_ratio_dry_air_validity>50",
    "derive(CH4_column_volume_mixing_ratio_dry_air [ppb])",
    "derive (datetime_stop {time})",
    "bin_spatial(1801,-90,0.1,3601,-180,0.1)",
    "derive(latitude {latitude})",
    "derive(longitude {longitude})",
    "keep(latitude_bounds,longitude_bounds,CH4_column_volume_mixing_ratio_dry_air)"
    ])
reduce_operations=";".join([
    "squash(time, (latitude, longitude)",
    "bin()"
])

filename = './data/S5P_OFFL_L2__CO_____20230517T212614_20230517T230744_28978_03_020500_20230519T111618.nc'


operations = ';'.join([
    "CO_column_number_density_validity>50",
    "derive(CO_column_number_density [mol/m^2])",
    "derive (datetime_stop {time})",
    "bin_spatial(1801,-90,0.1,3601,-180,0.1)",
    "derive(latitude {latitude})",
    "derive(longitude {longitude})",
    "keep(datetime_start, latitude_bounds,longitude_bounds,CO_column_number_density)"
    ])

reduce_operations=";".join([
    "squash(time, (latitude, longitude)",
    "bin()"
])

product = harp.import_product(filename, operations = operations, reduce_operations=reduce_operations)

product.to_xarray().to_zarr('./resized/HOOO.zarr')

ds = xr.open_zarr('./resized/HOOO.zarr')



filename = './data/S5P_OFFL_L2__CO_____20230518T004914_20230518T023045_28980_03_020500_20230519T143627.nc'


operations = ';'.join([
    "CO_column_number_density_validity>50",
    "derive(CO_column_number_density [mol/m^2])",
    "derive (datetime_stop {time})",
    "bin_spatial(1801,-90,0.1,3601,-180,0.1)",
    "derive(latitude {latitude})",
    "derive(longitude {longitude})",
    "keep(datetime_start, latitude_bounds,longitude_bounds,CO_column_number_density)"
    ])

reduce_operations=";".join([
    "squash(time, (latitude, longitude)",
    "bin()"
])

product = harp.import_product(filename, operations = operations, reduce_operations=reduce_operations)

product = product.to_xarray()

ds = xr.open_zarr('./resized/HOOO.zarr')
product.to_zarr('./resized/HOOO.zarr', mode='a', append_dim='time')


ds  = xr.open_zarr('./resized/HOOO.zarr')

print(ds)"""
"""
# calculate time of exectution
import time
start_time = time.time()

ds = xr.open_zarr('./resized/HOOO.zarr')
print(ds['datetime_start'][:].values)

from datetime import datetime
datetime = datetime.fromtimestamp(ds['datetime_start'].values[0])
print(datetime)

import numpy as np

lat = np.where((ds['latitude_bounds'].values == round(45.5641943, 1)))
long = np.where((ds['longitude_bounds'].values == round(9.289634, 1)))
print(round(45.5641943, 1))
print(lat)
ds = ds.sel(longitude = long[0], latitude = lat[0])
print(ds)

print("--- time %s seconds ---" % (time.time() - start_time))"""
"""
op_val = "CH4_column_volume_mixing_ratio_dry_air_validity"
op_der = "CH4_column_volume_mixing_ratio_dry_air"
op_measure = '[ppb]'

operations = ';'.join([
    f"{op_val}>50",
    f"derive({op_der} {op_measure})",
    "derive (datetime_stop {time})",
    "bin_spatial(1801,-90,0.1,3601,-180,0.1)",
    "derive(latitude {latitude})",
    "derive(longitude {longitude})",
    f"keep(datetime_start, latitude_bounds,longitude_bounds,{op_der})"
])

reduce_operations = ";".join([
    "squash(time, (latitude, longitude)",
    "bin()"
])

ds = harp.import_product('./data/S5P_OFFL_L2__CH4____20230518T073515_20230518T091645_28984_03_020500_20230519T234258.nc', operations = operations, reduce_operations=reduce_operations)
print(ds)
"""

#ds = harp.import_product('./data/S5P_OFFL_L2__SO2____20230612T131207_20230612T145337_29342_03_020401_20230614T110126.nc')
#ds = xr.open_zarr('./db/L2__CH4___.zarr')
#print(ds['datetime_start'])

ds = xr.open_zarr('./db/L2__CH4___.zarr')
import numpy as np
index = ds.dropna("CH4_column_volume_mixing_ratio_dry_air", how="all").indexes["time"]