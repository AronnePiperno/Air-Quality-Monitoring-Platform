import xarray as xr
import os


db_path = './db'
pro = 'L2__CO____'
ds = xr.open_zarr(os.path.join(db_path, pro))
print(ds)