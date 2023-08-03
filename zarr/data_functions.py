import os
import glob
import multiprocessing
from sentinel5dl import download
import harp


def multi_download(output_dir: str, result: dict) -> None:
    with multiprocessing.Pool(10) as pool:
        pool.starmap(download, map(
            lambda product: ((product,), output_dir),
            result.get('products')
        ))


def process_db(path_in: str, path_out: str, product: str) -> None:

    match product:
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
            print("Error processing file", current_file)
            os.remove(current_file)

def erase_data_folder(path: str) -> None:

    files = glob.glob(path + '/*.nc')
    for file in files:
        os.remove(file)
