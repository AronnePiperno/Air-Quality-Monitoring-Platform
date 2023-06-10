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

4. Utilize the `data_retrieval.py` script to search and retrieve data from the Zarr DB using Dask.

```python
python data_retrieval.py
   ```

5. Run the `dashboard.py` script to start the Streamlit dashboard and visualize the air quality data.

```python
streamlit run dashboard.py
   ```

6. Use the provided API calls to access the data programmatically.

## Example API Calls
To retrieve air quality data for a specific location and time range, make a GET request to the following endpoint:

```console
GET /api/data?location={location}&start_date={start_date}&end_date={end_date}
```

- **location**: The geographical location to retrieve the data for.
- **start_date**: The start date of the time range to retrieve data from.
- **end_date**: The end date of the time range to retrieve data from.

The response will be in JSON format and contain the requested air quality data.

## Contributing
Contributions to this project are welcome. If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request on the project's GitHub repository.

🌍🔍📊📈📉🌡️🌬️📡📅

Thank you for using our air quality monitoring platform! We hope you find it helpful in tracking and analyzing air quality data. If you have any questions or need assistance, please don't hesitate to contact us.

Happy monitoring! 🌍🌤️
