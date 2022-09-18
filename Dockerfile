FROM python:3.7
FROM continuumio/miniconda3
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip &&  pip3 install -r requirements.txt && pwd && ls  && conda update -n base -c defaults conda && conda env list \
&& pip freeze list && which mlflow 
RUN /bin/bash -c "run_mlflow.sh"
EXPOSE 5000
CMD mlflow server --host 0.0.0.0
ENTRYPOINT [ "python" ]
CMD ["run_server.py"]
