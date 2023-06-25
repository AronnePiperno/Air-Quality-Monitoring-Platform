from sentinel5dl import search
import schedule
import time
from data_functions import *

def batch(begin: str, end: str)-> None:

    products = ['L2__CH4___',
                'L2__CO____',
                'L2__HCHO__',
                'L2__NO2___',
                'L2__O3____',
                'L2__SO2___'
                ]
    #begin = '2023-06-01T00:00:00.000Z'
    #end = '2023-06-15T23:59:59.999Z'

    output_dir = './data'
    db_path = './db'


    for pro in products:
        result = search(
            begin_ts=begin,
            end_ts=end,
            product=pro,
            processing_level='L2',
            processing_mode='Near Real Time'
        )

        print(f"Download of {pro} started. {len(result.get('products'))} files will be downloaded.")
        multi_download(output_dir, result)
        print(f"Download of {pro} finished.")

        process_db(output_dir, db_path, pro)




def main():

    schedule.every(10).seconds.do(batch)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
