FROM python:3.8-alpine

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \ 
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /diary_app

COPY ./diary_app /diary_app

WORKDIR /diary_app
