# Import required libraries and functions
from sentinel5dl import search
from data_functions import *  # Assuming this file contains necessary functions
from datetime import datetime, timedelta


# Define the main function
def main():
    # Define a list of products (atmospheric composition measurements)
    products = ['L2__CO____', 'L2__HCHO__', 'L2__NO2___', 'L2__O3____', 'L2__SO2___']

    # Define the start and end time for data search
    begin = '2020-06-01T00:00:00.000Z'
    end = str(datetime.utcnow().isoformat() - timedelta(days=5)) + 'Z'

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
            processing_mode='Offline'
        )

        # Print information about the download process
        print(f"Download of {pro} started. {len(result.get('products'))} files will be downloaded.")

        # Attempt to download data for the current product
        try:
            multi_download(output_dir, result)
        except Exception as e:
            print(f"Error downloading {pro}")
            print(e)
            continue

        # Print download completion message
        print(f"Download of {pro} finished.")

        # Attempt to process the downloaded data and update the database
        try:
            process_db(output_dir, db_path, pro)
        except Exception as e:
            print(f"Error processing {pro}")
            print(e)


# Entry point of the script
if __name__ == '__main__':
    # Call the main function to start data retrieval and processing
    main()
