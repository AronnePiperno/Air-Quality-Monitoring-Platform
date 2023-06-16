import glob
import os
from sentinel5dl import search, download
import multiprocessing
import xarray as xr
import schedule
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
        time.sleep(10)
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
            os.remove(current_file)
            continue


def batch():

    resized_files = glob.glob('./resized' + '/*.nc')
    if len(resized_files) != 0:
        for file in resized_files:
            os.remove(file)
    data_files = glob.glob('./data' + '/*.nc')
    if len(data_files) != 0:
        for file in data_files:
            os.remove(file)

    c = Client(n_workers=3, threads_per_worker=3)
    products = [#'L2__CH4___',
                #'L2__CO____',
                #'L2__HCHO__',
                #'L2__NO2___',
                #'L2__O3____',
                'L2__SO2___'
                ]
    begin = '2023-06-10T00:00:00.000Z'
    end = '2023-06-10T01:59:59.999Z'
    output_dir = './data'
    db_path = './db'
    resized_path = './resized'

    for pro in products:
        result = search(
            begin_ts=begin,
            end_ts=end,
            product=pro,
            processing_level='L2',
            processing_mode='Near real time'
        )
        print(f"Download of {pro} started. {len(result.get('products'))} files will be downloaded.")

        t1 = threading.Thread(target=multi_download, args=(output_dir, result))
        t2 = threading.Thread(target=resize_db, args=(output_dir, resized_path))
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        resized_files = glob.glob(resized_path + '/*.nc')
        if len(resized_files) != 0:
            print('debug1')
            db = xr.open_zarr(os.path.join(db_path, pro+'.zarrBATCHTEST'), consolidated=True, drop_variables=['delta_time', 'time_utc'])
            print('debug2')
            f = xr.open_mfdataset(resized_path + '/*.nc', combine='nested', concat_dim='time', drop_variables=['delta_time', 'time_utc'])
            print('debug3')
            f = xr.concat([f, db], dim='time')
            print('debug4')
            f.to_zarr(os.path.join(db_path, pro+'.zarrBATCHTEST'), mode='w', consolidated=True)
            print('debug5')
            for file in resized_files:
                os.remove(file)

def main():

    schedule.every(10).seconds.do(batch)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
