# pull official base image
FROM python:3.6

RUN apt-get update
RUN apt-get install -y wget vim git zip unzip less sqlite3 bsdmainutils bc
RUN echo "alias mypytest='python -m pytest --cov=. tests/ --cov-report term'" >> ~/.bashrc

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc sqlite3 \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .