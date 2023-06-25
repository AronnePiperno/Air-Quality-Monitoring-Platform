import glob
import os
from sentinel5dl import search, download
import multiprocessing
import xarray as xr
import threading
import time
from dask.distributed import Client
import harp

def multi_download(output_dir: str, result: dict) -> None:
    with multiprocessing.Pool(10) as pool:
        pool.starmap(download, map(
            lambda product: ((product,), output_dir),
            result.get('products')
        ))


def process_db(path_in: str, path_out: str, product: str) -> None:

    match product:
        case 'L2__CH4___':
            op_val = "CH4_column_volume_mixing_ratio_dry_air_validity"
            op_der = "CH4_column_volume_mixing_ratio_dry_air"
            op_measure = '[ppb]'
        case 'L2__CO____':
            op_val = "CO_column_number_density_validity"
            op_der = "CO_column_number_density"
            op_measure = '[mol/m^2]'
        case 'L2__HCHO__':
            op_val = "tropospheric_HCHO_column_number_density_validity"
            op_der = "tropospheric_HCHO_column_number_density"
            op_measure = '[mol/m^2]'
        case 'L2__NO2___':
            op_val = "tropospheric_NO2_column_number_density_validity"
            op_der = "tropospheric_NO2_column_number_density"
            op_measure = '[mol/m^2]'
        case 'L2__O3____':
            op_val = "O3_column_number_density_validity"
            op_der = "O3_column_number_density"
            op_measure = '[mol/m^2]'
        case 'L2__SO2___':
            op_val = "SO2_column_number_density_validity"
            op_der = "SO2_column_number_density"
            op_measure = '[mol/m^2]'
        case _:
            print("Invalid product")


    operations = ';'.join([
        f"{op_val}>50",
        f"derive({op_der} {op_measure})",
        "derive (datetime_stop {time})",
        "bin_spatial(1801,-90,0.1,3601,-180,0.1)",
        "derive(latitude {latitude})",
        "derive(longitude {longitude})",
        f"keep(datetime_start, latitude_bounds,longitude_bounds,{op_der})"
    ])

    reduce_operations = ";".join([
        "squash(time, (latitude, longitude)",
        "bin()"
    ])

    files = glob.glob(path_in + '/*.nc')

    print(f"Processing {len(files)} files")

    for file in files:
        current_file = file
        try:
            nc = harp.import_product(file, operations=operations, post_operations=reduce_operations)
            if os.path.exists(path_out + '/' + product + '.zarr'):
                nc.to_xarray().to_zarr(path_out + '/' + product + '.zarr', append_dim='time')
            else:
                nc.to_xarray().to_zarr(path_out + '/' + product + '.zarr')
            os.remove(file)
        except:
            print("Error resizing file")
            print('Current file', current_file)
            os.remove(current_file)


def main():
    #c = Client(n_workers=3, threads_per_worker=3)
    products = [#'L2__CH4___',
                #'L2__CO____',
                #'L2__HCHO__',
                #'L2__NO2___',
                'L2__O3____',
                'L2__SO2___'
                ]
    begin = '2023-06-01T00:00:00.000Z'
    end = '2023-06-15T23:59:59.999Z'
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

        print(f"Download of {pro} started. {len(result.get('products'))} files will be downloaded.")
        multi_download(output_dir, result)
        print(f"Download of {pro} finished.")

        process_db(output_dir, db_path, pro)
        #t1 = threading.Thread(target=multi_download, args=(output_dir, result))
        #t2 = threading.Thread(target=resize_db, args=('./data', './db', 'L2__CH4___'))
        #t1.start()
        #t2.start()

        #t1.join()
        #t2.join()

        #db = xr.open_mfdataset(resized_path + '/*.nc', combine='nested', concat_dim='time', drop_variables=['delta_time', 'time_utc'])

        #db.to_zarr(os.path.join(db_path, pro), mode='w', consolidated=True)

        #delete_files = glob.glob(resized_path + '/*.nc')

       # for file in delete_files:
        #    os.remove(file)


if __name__ == '__main__':
    main()
