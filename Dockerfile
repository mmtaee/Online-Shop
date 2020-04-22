FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
ADD . /src/
RUN apt-get update && apt-get install -y python-pip python-dev libpq-dev postgresql postgresql-contrib
RUN pip install -r requirements.txt

