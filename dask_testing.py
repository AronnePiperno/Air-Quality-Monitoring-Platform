import dask.array as da
import zarr
import dask
from dask.distributed import Client
import xarray as xr
import numpy as np
import timeit
if __name__ == '__main__':
    """#client = Client()
    dask.config.set({'array.slicing.split_large_chunks': False})
    zarr_ds = zarr.open('./db/L2__CH4___.zarr')
    
    # Specify chunk sizes for Dask arrays
    chunk_size = (10000,10000,10000)  # Adjust this value based on your available memory

    # Load data as Dask arrays with specified chunk size
    qa_value = da.from_zarr(zarr_ds["qa_value"], chunks=chunk_size)
    latitude = da.from_zarr(zarr_ds["latitude"], chunks=chunk_size)
    longitude = da.from_zarr(zarr_ds["longitude"], chunks=chunk_size)

    precision = 0.05

    # Compute the index in smaller chunks
    index = da.where(
        (latitude >= 45.4641943 - precision) &
        (latitude <= 45.4641943 + precision) &
        (longitude >= 9.189634 - precision) &
        (longitude <= 9.189634 + precision) &
        (qa_value > 0.5)
    )

    # Compute and print the index
    indeces = da.compute(index)
    print(indeces)"""
    since = timeit.default_timer()
    client = Client(n_workers=3, threads_per_worker=3, memory_limit='10GB')
    dask.config.set({'array.slicing.split_large_chunks': False})
    client.amm.start()
    #ds = xr.open_zarr('./db/L2__CH4___.zarr', chunks=1000000)

    """
    qa_value = ds['qa_value']
    latitude = ds['latitude']
    longitude = ds['longitude']
"""

    qa_value = da.from_zarr('./db/L2__CH4___.zarr', component='qa_value', chunks='auto')
    latitude = da.from_zarr('./db/L2__CH4___.zarr', component='latitude', chunks='auto')
    longitude = da.from_zarr('./db/L2__CH4___.zarr', component='longitude', chunks='auto')
    #qa_value.persist()
    #latitude.persist()
    #longitude.persist()


    precision = 1


    """
    for i in range(0, latitude.shape[0]):
        index = da.where(
            (latitude[i] >= 45.4641943 - precision) &
            (latitude[i] <= 45.4641943 + precision) &
            (longitude[i] >= 9.189634 - precision) &
            (longitude[i] <= 9.189634 + precision) &
            (qa_value[i] > 0.5)
        )
        indeces = da.compute(index)


    print(indeces)
    """

    print(qa_value.shape[0])
    index = da.where(
        (latitude >= 45.4641943 - precision) &
        (latitude <= 45.4641943 + precision) &
        (longitude >= 9.189634 - precision) &
        (longitude <= 9.189634 + precision) &
        (qa_value > 0.5)
        )
    index = da.compute(index)
    
    """
    index = np.where(
        qa_value > 0.5)
    print(index)
    """
    to = timeit.default_timer()
    print('Time: ', to - since)

    print(index)
    client.close()