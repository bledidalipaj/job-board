FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

# Dependencies needed to build Pillow
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Remove dev dependencies
RUN apk del .build-deps

RUN mkdir /code
WORKDIR /code
COPY . .

RUN adduser -D user
USER user