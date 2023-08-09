# Air Quality Monitoring Platform

## Introduction

The project focuses on global air quality monitoring using ESA's Sentinel5P satellite. Through a detection frequency of about once a day, the satellite acquires crucial data on Formaldehyde (HCHO), Nitrogen Dioxide (NO2), Ozone (O3), Carbon Monoxide (CO) and Sulphur Dioxide (SO2), important air pollutants. Through the implementation of an API call system, data is stored in a dedicated database and batch processed to ensure up-to-date information is available. Using an intuitive dashboard, users can easily monitor air quality at any location on the planet and compare atmospheric conditions between different areas. With this solution, we provide useful tools to understand and assess global air quality efficiently and accurately.

## Requirements

The following specifications must be met in order to use and display the project:
- At least 4 cores
- 32GB RAM
- Have Docker installed on your device

## Demo Version Usage

1. Download the project:

```python
   clone https://github.com/AronnePiperno/Air-Quality-Monitoring-Platform
   ```
2. Download the demo data here and unzip it in the "zarr" folder:

3. Execute the following commands

```python
docker-compose build
   ```
```python
docker-compose up
   ```

4. To access the dashboard, use the link http://localhost:8501/. Whereas, if you want to access the API documentation use the link http://localhost:8000/docs

## Contributing
Contributions to this project are welcome. If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request on the project's GitHub repository.

🌍🔍📊📈📉🌡️🌬️📡📅

Thank you for using our air quality monitoring platform! We hope you find it helpful in tracking and analyzing air quality data. If you have any questions or need assistance, please don't hesitate to contact us.

Happy monitoring! 🌍🌤️
