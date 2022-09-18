FROM python:3.7
COPY . /app
WORKDIR /app
RUN sudo apt-get update && sudo apt-get upgrade && pip3 install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD ["run_server.py"]