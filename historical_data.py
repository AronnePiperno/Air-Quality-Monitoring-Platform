import glob
import os
from sentinel5dl import search, download
import multiprocessing
import xarray as xr
import threading
import time

def multi_download(output_dir: str, result: dict) -> None:
    with multiprocessing.Pool(10) as pool:
        pool.starmap(download, map(
            lambda product: ((product,), output_dir),
            result.get('products')
        ))

def resize_db(path_in: str, path_out: str) -> None:
    while True:
        time.sleep(10)
        print("resizing db")
        try:
            filestmp = glob.glob(path_in + '/*.tmp')
            if len(filestmp) == 0:
                print("exit resizing db")
                break
            files = glob.glob(path_in + '/*.nc')

            for file in files:
                file_name = file.split('/')[-1]
                ds = xr.open_dataset(file, group='PRODUCT')
                ds.to_netcdf(path_out + '/' + file_name, mode='w', encoding={'time_utc': {'dtype': 'S1'}})
                os.remove(file)
        except:
            print("Error resizing db")
            continue

def main():
    products = ['L2__CH4___',
                'L2__CO____',
                'L2__HCHO__',
                'L2__NO2___',
                'L2__O3____',
                'L2__SO2___'
                ]
    begin = '2023-05-14T20:00:00.000Z'
    end = '2023-05-16T23:59:59.999Z'
    output_dir = './data'
    db_path = './db'
    resized_path = './resized'

    for pro in products:
        result = search(
            begin_ts=begin,
            end_ts=end,
            product=pro,
            processing_level='L2',
            processing_mode='Offline'
        )
        print("debug")

        t1 = threading.Thread(target=multi_download, args=(output_dir, result))
        t2 = threading.Thread(target=resize_db, args=(output_dir, resized_path))
        t1.start()
        t2.start()

        t1.join()
        t2.join()


        db = xr.open_mfdataset(resized_path + '/*.nc', combine='nested', concat_dim='time')
        db.to_zarr(os.path.join(db_path, pro+"TEST"), mode='w', consolidated=True)

        delete_files = glob.glob(resized_path + '/*.nc')

        for file in delete_files:
            os.remove(file)
        """
        files = glob.glob(resized_path + '/*.nc')

        to_database(first=True, file=files[0], db_path=db_path, product=pro+"TEST")

        for file in files:
            if file == files[0]:
                continue
            to_database(first=False, file=file, db_path=db_path, product=pro+"TEST")
"""


def to_database(first: bool, file: str, db_path: str, product: str) -> None:
    timestep_db = xr.open_dataset(file, group='PRODUCT')
    if first:
        timestep_db.to_zarr(os.path.join(db_path, product), mode='w', consolidated=True)
    else:
        db = xr.open_zarr(os.path.join(db_path, product))
        shutil.rmtree(os.path.join(db_path, product))
        x1 = xr.combine_by_coords([db, timestep_db])
        x1.to_zarr(os.path.join(db_path, product), mode='w', consolidated=True)
    os.remove(file)


if __name__ == '__main__':
    main()
