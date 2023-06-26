from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.onprem.database import MongoDB
from diagrams.onprem.queue import Kafka

with Diagram("Air Quality Monitoring Platform", show=True):

    sentinel = Custom("Sentinel 5P", "img/sat.png")
    
    historical_data = Custom('Historical Data', 'https://icons.veryicon.com/png/o/miscellaneous/energy-consumption-management/historical-data-1.png')
    batch_processing = Kafka('Batch Processing')

    data_cleaning = Custom('Data Cleaning', 'img/clean.png')

    database = Custom('Zarr DB', "https://zarr.readthedocs.io/en/stable/_static/logo1.png")

    api = Custom('API', 'img/api.png')
    processing = Custom('Processing', 'img/processing.png')
    dashboard = Custom('Dashboard', 'img/dashboard.png')
    
    processing = Custom('Processing', 'img/processing.png')

    sentinel >> batch_processing >> data_cleaning
    sentinel >> historical_data >> data_cleaning

    data_cleaning >> database
    database >> api

    database >> processing >> dashboard
