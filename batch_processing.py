import glob
import os
from sentinel5dl import search, download
import multiprocessing
import xarray as xr


def main():
    products = [
                #'L2__CH4___',
                'L2__CO____',
                'L2__HCHO__',
                'L2__NO2___',
                'L2__O3____',
                'L2__SO2___'
                ]
    begin = '2023-05-22T00:00:00.000Z'
    end = '2023-05-22T23:59:59.999Z'
    output_dir = './data'
    db_path = './db'


    for pro in products:
        result = search(
            begin_ts=begin,
            end_ts=end,
            product=pro,
            processing_level='L2',
            processing_mode='Near real time'
        )
        print("debug")
        with multiprocessing.Pool(10) as pool:
            pool.starmap(download, map(
                 lambda product: ((product,), output_dir),
                 result.get('products')
             ))

        files = glob.glob(output_dir + '/*.nc')

        to_database(first=True, file=files[0], db_path=db_path, product=pro+"BATCH")

        for file in files:
            if file == files[0]:
                continue
            to_database(first=False, file=file, db_path=db_path, product=pro+"BATCH")


def to_database(first: bool, file: str, db_path: str, product: str) -> None:
    timestep_db = xr.open_dataset(file, group='PRODUCT')
    if first:
        timestep_db.to_zarr(os.path.join(db_path, product), mode='w', consolidated=True)
    else:
        timestep_db.to_zarr(os.path.join(db_path, product), mode='a', consolidated=True, append_dim='scanline')
    os.remove(file)


if __name__ == '__main__':
    main()
