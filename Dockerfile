FROM python:3.11

WORKDIR /app

ADD . .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "--no-capture-output" ,"-n", "big-data", "/bin/bash", "-c"]

CMD ["python", "main.py"]

