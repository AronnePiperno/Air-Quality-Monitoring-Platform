import os
import xarray as xr
import glob
while True:
    try:
        ds = xr.open_zarr(os.path.join("./db", "L2__CO____"))
        print(ds)
        break
    except:
        print("not yet")
        continue