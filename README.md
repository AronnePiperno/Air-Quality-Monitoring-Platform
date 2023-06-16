# Air Quality Monitoring Platform

## Introduction

This is an air quality monitoring platform that leverages the Sentinel5P satellite and its API system. The platform allows users to retrieve historical air quality data, store it in a Zarr DB (a popular geospatial database), and implement batch processing to obtain the latest data. The platform utilizes Dask for efficient data retrieval and presents the results in a Streamlit dashboard. Additionally, the platform supports API calls to access the data.

## Features
Retrieve historical air quality data from Sentinel5P API
Store data in a Zarr DB
Implement batch processing for updating the latest data
Efficient data retrieval using Dask
Display data in a user-friendly Streamlit dashboard
Support API calls to access the data

## Files
- `historical_data.py`: Contains API calls to retrieve historical data from Sentinel5P and store it in the Zarr DB.
- `batch_processing.py`: Sets up batch processing to add the latest data to the Zarr DB.
- `data_retrieval.py`: Utilizes Dask to facilitate data searching within the DB.
- `dashboard.py`: Sets up the Streamlit dashboard using the Streamlit library and functions from data_retrieval.py.
- `requirements.txt`: Contains all the required libraries for running the platform, useful for Docker setups.
- `main.py`: Entry point to run the platform.

## Usage
1. Install the required libraries by running:

```python
   pip install -r requirements.txt
   ```

2. Run the `historical_data.py` script to retrieve historical data and populate the Zarr DB.

```python
python historical_data.py
   ```

3. Set up batch processing using the `batch_processing.py` script to keep the Zarr DB up to date with the latest data.

```python
python batch_processing.py
   ```

4. Run the `dashboard.py` script to start the Streamlit dashboard and visualize the air quality data. Inside it you could find some functions from `data_retrieval.py`

```python
streamlit run dashboard.py
   ```

5. Use the provided API calls to access the data programmatically.

## Contributing
Contributions to this project are welcome. If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request on the project's GitHub repository.

🌍🔍📊📈📉🌡️🌬️📡📅

Thank you for using our air quality monitoring platform! We hope you find it helpful in tracking and analyzing air quality data. If you have any questions or need assistance, please don't hesitate to contact us.

Happy monitoring! 🌍🌤️
