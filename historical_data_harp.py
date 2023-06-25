from sentinel5dl import search
from data_functions import *

def main():

    products = ['L2__CH4___',
                'L2__CO____',
                'L2__HCHO__',
                'L2__NO2___',
                'L2__O3____',
                'L2__SO2___'
                ]

    begin = '2023-06-01T00:00:00.000Z'
    end = '2023-06-15T23:59:59.999Z'

    output_dir = './data'
    db_path = './db'

    for pro in products:
        erase_data_folder(output_dir)
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



if __name__ == '__main__':
    main()
