FROM python:3-alpine

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache linux-headers bash gcc \
    zlib-dev libmagic make libpq postgresql-dev musl-dev libxslt-dev libxml2-dev tzdata

WORKDIR /src
COPY ./src /src
RUN pip install -U -r requirements.txt
