import glob
import os

import zarr
from sentinel5dl import search, download
import multiprocessing
import xarray as xr


def main():
    products = ['L2__CH4___', 'L2__CO____', 'L2__HCHO__', 'L2__NO2___', 'L2__O3____', 'L2__SO2___']
    begin = '2022-03-14T00:00:00.000Z'
    end = '2022-03-14T23:59:59.999Z'
    output_dir = './data'
    db_path = './db'

    for pro in products:
        result = search(
            begin_ts=begin,
            end_ts=end,
            product=pro,
            processing_level='L2',
            processing_mode='Offline'
            #per_request_limit=np.inf
        )
        print("debug")
        with multiprocessing.Pool(20) as pool:
            pool.starmap(download, map(
                 lambda product: ((product,), output_dir),
                 result.get('products')
             ))

        files = glob.glob(output_dir + '/*.nc')
        timestep_db = xr.open_dataset(files[0], group='PRODUCT')
        timestep_db.to_zarr(os.path.join(db_path, pro), mode='w', consolidated=True)
        os.remove(files[0])
        for file in files:
            if file == files[0]:
                continue
            timestep_db = xr.open_dataset(file, group='PRODUCT')
            timestep_db.to_zarr(os.path.join(db_path, pro), mode='a', consolidated=True, append_dim='scanline')
            os.remove(file)


if __name__ == '__main__':
    main()
