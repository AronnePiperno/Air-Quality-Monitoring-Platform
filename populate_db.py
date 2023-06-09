import glob
import os
import xarray as xr

output_dir = './data'
db_path = './db'
resized_path = './resized'

db = xr.open_mfdataset(resized_path + '/*.nc', combine='nested', concat_dim='time')
db.to_zarr(os.path.join(db_path, 'L2__HCHO__'), mode='w', consolidated=True)

delete_files = glob.glob(resized_path + '/*.nc')

for file in delete_files:
    os.remove(file)
