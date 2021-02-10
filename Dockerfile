FROM        python:3.8.1-alpine3.11
WORKDIR     /usr/src/app
ADD         requirements.txt .
RUN         apk add postgresql-dev \
                    build-base
RUN         pip install -r requirements.txt
ENV         FLASK_APP=manage.py
COPY        . .
CMD         python -m flask run -h 0.0.0.0 -p 8000 --debugger --reload

# FROM        python:3.8.1-alpine3.11 AS builder
# WORKDIR     /usr/src/app
# ADD         requirements.txt .
# RUN         apk add postgresql-dev \
#                     build-base
# RUN         pip install -r requirements.txt
#
# ###
# FROM        python:3.8.1-alpine3.11
# WORKDIR     /usr/src/app/
#
# ENV         FLASK_APP=manage.py
# COPY        --from=builder /usr/local /usr/local
# COPY        . .
