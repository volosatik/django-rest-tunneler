# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
ENV PG_PASS=some_pass
ENV PG_NAME=some_name
ENV REMOTE_NAME=
ENV REMOTE_PASS=
WORKDIR /code
COPY requirements.txt /code/
# COPY ./packages/ /code/packages
# RUN python3 -m pip install --no-index --find-links=/code/packages/ -r requirements.txt
RUN pip3 install --proxy=http://msk-proxy.megafon.ru:3128 -r requirements.txt
COPY . /code/
