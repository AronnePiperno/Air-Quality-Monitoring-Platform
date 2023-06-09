import glob
import os
from sentinel5dl import search, download
import multiprocessing
import xarray as xr
import threading
import time
from dask.distributed import Client


def multi_download(output_dir: str, result: dict) -> None:
    with multiprocessing.Pool(10) as pool:
        pool.starmap(download, map(
            lambda product: ((product,), output_dir),
            result.get('products')
        ))


def resize_db(path_in: str, path_out: str) -> None:
    while True:
        time.sleep(20)
        print("resizing db")
        current_file = ''
        try:

            if len(glob.glob(path_in + '/*.nc')) == 0 and len(glob.glob(path_in + '/*.tmp')) == 0:
                print("exit resizing db")
                break

            files = glob.glob(path_in + '/*.nc')
            for file in files:
                current_file = file
                file_name = file.split('/')[-1]
                ds = xr.open_dataset(file, group='PRODUCT')
                ds.to_netcdf(path_out + '/' + file_name, mode='w', format="NETCDF4",
                             encoding={'time_utc': {'dtype': 'S1'}})
                os.remove(file)
        except:
            print("Error resizing db")
            print('Current file', current_file)
            continue


def main():
    c = Client(n_workers=3, threads_per_worker=3)
    products = [#'L2__CH4___',
                #'L2__CO____',
                #'L2__HCHO__',
                'L2__NO2___',
                'L2__O3____',
                'L2__SO2___'
                ]
    begin = '2023-05-15T00:00:00.000Z'
    end = '2023-05-31T23:59:59.999Z'
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
        db.to_zarr(os.path.join(db_path, pro), mode='w', consolidated=True)

        delete_files = glob.glob(resized_path + '/*.nc')

        for file in delete_files:
            os.remove(file)


if __name__ == '__main__':
    main()
