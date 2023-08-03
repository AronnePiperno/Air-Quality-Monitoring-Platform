FROM continuumio/miniconda3:latest

WORKDIR /app

COPY ./environment.yml /app/environment.yml

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "big_data", "/bin/bash", "-c"]

COPY . /app

CMD ["./run.sh"]
