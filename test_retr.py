import glob
import os

import zarr
from sentinel5dl import search, download
import multiprocessing
import xarray as xr
import threading
import time
from dask.distributed import Client
import xoak
import cartopy.crs as ccrs
import dask.array as da
import numpy as np
import dask
"""
ds = xr.open_zarr('./db/L2__CH4___testtest', consolidated=True)
ds.xoak.set_index(['latitude', 'longitude'], "scipy_kdtree")
ds_selection = ds.xoak.sel(latitude=55.0, longitude=55.0, method="nearest")
print(ds_selection)
"""
def main():
        client = Client(n_workers=3, threads_per_worker=3, memory_limit='10GB')
        dask.config.set({'array.slicing.split_large_chunks': False})
        client.amm.start()

        store = xr.open_zarr('./db/L2__CH4___.zarr', chunks='auto')

        longitude = 55.0
        latitude = 55.0
        precision = 0.5
        index = da.where(
                (store['qa_value'][:] > 0.5) &
                (store["methane_mixing_ratio"][:] < 9.9692100e+10))
        index = da.compute(index)
        print(index)

        store.to_zarr('./db/ripperoni', consolidated=True)
        print(store)

if __name__ == "__main__":
        main()
        #ds = xr.open_zarr('./db/L2__CH4___testtest', consolidated=True)
        #print(ds)
        #ds = ds.dropna(dim="methane_mixing_ratio_bias_corrected", how="all")
        #print(ds)

