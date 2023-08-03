#!/bin/bash

conda run -n big_data flask run --host 0.0.0.0 --port 5000 &

conda run -n big_data python -u historical_data.py
