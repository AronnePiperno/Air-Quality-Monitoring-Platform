FROM continuumio/miniconda3


#WORKDIR /

#ADD . .

RUN apt-get install libssl-dev

COPY environment.yml .
RUN pip install sentinel5dl
RUN conda env create -f environment.yml
ENV PATH /opt/conda/envs/big_data/bin:$PATH

SHELL ["conda", "run", "--no-capture-output" ,"-n", "big-data", "/bin/bash", "-c"]


RUN pip install sentinel5dl

CMD ["python", "main.py"]
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address"]
CMD ["python", "batch_processing.py"]
