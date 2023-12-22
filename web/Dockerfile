###########
# BUILDER #
###########

# pull official base image
FROM python:3.11-alpine as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apk add gcc

# lint
RUN pip install --upgrade pip
RUN pip install flake8==6.0.0
COPY . /usr/src/app/
RUN flake8 --ignore=E501 .

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

FROM python:3.11-alpine

ENV HOME=/home/calendaronline
ENV APP_HOME=$HOME/web

# create directory for the app user
RUN mkdir -p $APP_HOME && \
    addgroup --system calendaronline && \
    adduser --system -G calendaronline calendaronline

WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --upgrade pip && pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R calendaronline:calendaronline $APP_HOME && \
    chmod +x startup.prod.sh

# change to the app user
USER calendaronline

# CMD  gunicorn calendaronline.wsgi:application --bind 0.0.0.0:8000
CMD ./startup.prod.sh

