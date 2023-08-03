from sentinel5dl import search
from data_functions import *
from datetime import datetime, timedelta

def main():

    products = ['L2__CO____',
                'L2__HCHO__',
                'L2__NO2___',
                'L2__O3____',
                'L2__SO2___'
                ]

    begin = '2020-06-01T00:00:00.000Z'
    end = str(datetime.utcnow().isoformat() - timedelta(days=5)) + 'Z'


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
        try:
            multi_download(output_dir, result)
        except Exception as e:
            print(f"Error downloading {pro}")
            print(e)
            continue
        print(f"Download of {pro} finished.")
        try:
            process_db(output_dir, db_path, pro)
        except Exception as e:
            print(f"Error processing {pro}")
            print(e)


if __name__ == '__main__':
    main()
