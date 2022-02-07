FROM python:3.8.3-slim

# set work directory
WORKDIR /ml-boilerplate/api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY requirements.txt /ml-boilerplate/api/requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# copy project
# COPY src /usr/app/src/
COPY . /ml-boilerplate/api

# set work directory
WORKDIR /ml-boilerplate