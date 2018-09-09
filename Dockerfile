FROM python:3-alpine

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache linux-headers bash gcc \
    zlib-dev libmagic make libpq postgresql-dev musl-dev libxslt-dev libxml2-dev tzdata libffi-dev

RUN rm -rf /src
COPY ./src /src
WORKDIR /src
RUN cp /usr/share/zoneinfo/Asia/Almaty /etc/localtime
RUN echo "Asia/Almaty" > /etc/timezone
RUN pip install -U -r requirements.txt