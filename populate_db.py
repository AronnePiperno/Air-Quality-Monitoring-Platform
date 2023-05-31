import glob
import os
import xarray as xr


def to_database(first: bool, file: str, db_path: str, product: str) -> None:

    timestep_db = xr.open_dataset(file, group='PRODUCT')
    if first:
        timestep_db.to_zarr(os.path.join(db_path, product), mode='w', consolidated=True)
    else:
        timestep_db.to_zarr(os.path.join(db_path, product), mode='a', consolidated=True)
    os.remove(file)


output_dir = './data'
db_path = './db'
pro = 'L2__CO____TIME'
files = glob.glob(output_dir + '/*.nc')
#to_database(first=True, file=files[0], db_path=db_path, product=pro)

for file in files:
    to_database(first=False, file=file, db_path=db_path, product=pro)


