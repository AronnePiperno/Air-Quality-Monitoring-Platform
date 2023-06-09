import zarr
import os
import numpy as np
import timeit


start = timeit.default_timer()
zarr_store = zarr.open(os.path.join('./db', 'L2__CH4___.zarr'), mode='r')
latitude = zarr_store['latitude'][:]
longitude = zarr_store['longitude'][:]
qa_value = zarr_store['qa_value'][:]


precision = 1


index = np.where(
        (latitude[0:latitude.shape[0]//3] >= 45.4641943 - precision) &
        (latitude[0:latitude.shape[0]//3] <= 45.4641943 + precision) &
        (longitude[0:longitude.shape[0]//3] >= 9.189634 - precision) &
        (longitude[0:longitude.shape[0]//3] <= 9.189634 + precision) &
        (qa_value[0:qa_value.shape[0]//3] > 0.5)
)
print(index)

stop = timeit.default_timer()
print('Time: ', stop - start)