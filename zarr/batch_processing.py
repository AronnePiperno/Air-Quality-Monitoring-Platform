# Import necessary libraries and functions
from sentinel5dl import search
import schedule
from datetime import datetime, timedelta
import time
from data_functions import *


# Define a function to handle batch processing of data
def batch():
    # Define a list of products (atmospheric composition measurements)
    products = ['L2__CO____', 'L2__HCHO__', 'L2__NO2___', 'L2__O3____', 'L2__SO2___']

    # Calculate the time window for data search: from 24 hours ago to the current time
    end = datetime.utcnow().isoformat()
    begin_datetime = datetime.utcnow() - timedelta(days=1)
    begin = str(begin_datetime.isoformat()) + 'Z'
    end = str(end) + 'Z'

    # Specify output directory for downloaded files and path for the database
    output_dir = './data'
    db_path = './db'

    # Loop through each product and process the data
    for pro in products:
        # Clear the existing data folder
        erase_data_folder(output_dir)

        # Search for data products within the specified time window and processing parameters
        result = search(
            begin_ts=begin,
            end_ts=end,
            product=pro,
            processing_level='L2',
            processing_mode='Near Real Time'
        )

        # Print information about the download process
        print(f"Download of {pro} started. {len(result.get('products'))} files will be downloaded.")

        # Download the search results to the output directory
        multi_download(output_dir, result)

        # Print download completion message
        print(f"Download of {pro} finished.")

        # Process the downloaded data and update the database
        process_db(output_dir, db_path, pro)


# Define the main function to schedule batch processing
def main():
    # Schedule the batch function to run every day at midnight
    schedule.every().day.at("00:00").do(batch)

    # Continuously check for pending scheduled tasks and sleep between checks
    while True:
        schedule.run_pending()
        time.sleep(60)


# Entry point of the script
if __name__ == '__main__':
    # Call the main function to start the scheduled batch processing
    main()
