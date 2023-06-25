from sentinel5dl import search
import schedule
from datetime import datetime, timedelta
import time
from data_functions import *

def batch():

    products = ['L2__CH4___',
                'L2__CO____',
                'L2__HCHO__',
                'L2__NO2___',
                'L2__O3____',
                'L2__SO2___'
                ]

    end = datetime.utcnow().isoformat()
    begin_datetime = datetime.utcnow() - timedelta(days=1)
    begin = str(begin_datetime.isoformat()) + 'Z'
    end = str(end) + 'Z'

    output_dir = './data'
    db_path = './db'


    for pro in products:
        erase_data_folder(output_dir)
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

    schedule.every().day.at("00:00").do(batch)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == '__main__':

    main()
