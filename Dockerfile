FROM python:3.13 AS server-base
WORKDIR /usr/src/backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt -y update && \
    apt install -y python3-dev libpq-dev python3-dev postgresql-client
RUN pip install -U pip uwsgi
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .