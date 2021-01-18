FROM python:3.7.3-slim-stretch

RUN apt-get -y update && apt-get -y install gcc

COPY download_model.sh /nlp/download_model.sh 

RUN chmod +x /nlp/download_model.sh

WORKDIR /
COPY trained_model /trained_model

# Make changes to the requirements/app here.
# This Dockerfile order allows Docker to cache the checkpoint layer
# and improve build times if making changes.
RUN pip3 --no-cache-dir install --upgrade pip
RUN pip3 --no-cache-dir install transformers==2.9.1 aitextgen starlette==0.13.8 uvicorn ujson
COPY app.py /

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN sh ./download_model.sh 117M

ENTRYPOINT ["python3", "-X", "utf8", "app.py"]
