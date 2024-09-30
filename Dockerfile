# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
ENV PG_PASS=YWE5Yk12az9IP01iUVk5
ENV PG_NAME=c3NwX3Rtel91c3I=
ENV REMOTE_NAME=
ENV REMOTE_PASS=
WORKDIR /code
COPY requirements.txt /code/
# COPY ./packages/ /code/packages
# RUN python3 -m pip install --no-index --find-links=/code/packages/ -r requirements.txt
RUN pip3 install --proxy=http://msk-proxy.megafon.ru:3128 -r requirements.txt
COPY . /code/
