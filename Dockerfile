# Dockerfile

# pull the official docker image
FROM python:3.8

# set work directory
WORKDIR /app/src

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN chmod a+x docker/*.sh