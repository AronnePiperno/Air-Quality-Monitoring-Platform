FROM continuumio/miniconda3:latest

WORKDIR /app

COPY ./environment.yml /app/environment.yml

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "big_data", "/bin/bash", "-c"]

COPY . /app

CMD ["conda", "run", "-n", "big_data", "flask", "run", "--host", "0.0.0.0", "--port", "5000", "&&", "python", "historical_data.py"]