# FROM        python:3.8.1-alpine3.11
# WORKDIR     /usr/src/app
# ADD         requirements.txt .
# RUN         apk add postgresql-dev \
#                     build-base
# RUN         pip install -r requirements.txt
# ENV         FLASK_APP=manage.py
# COPY        . .

FROM        python:3.8.1-alpine3.11 AS builder
WORKDIR     /usr/src/app
ADD         requirements.txt .
RUN         apk add postgresql-dev \
                    build-base
RUN         pip install -r requirements.txt

###
FROM        python:3.8.1-alpine3.11
WORKDIR     /usr/src/app/

ENV         FLASK_APP=manage.py
COPY        --from=builder /usr/local /usr/local
COPY        . .
