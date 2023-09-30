###########
# BUILDER #
###########

# pull official base image
FROM python:3.11-slim-bookworm as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
RUN pip install flake8==6.0.0
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401 .

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

FROM python:3.11-slim-bookworm

# create directory for the app user
RUN mkdir -p /home/calendaronline

# create the app user
RUN addgroup --system clendaronline && adduser --system --group calendaronline

# create the appropriate directories
ENV HOME=/home/calendaronline
ENV APP_HOME=$HOME/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.prod.sh
#COPY ./entrypoint.prod.sh .
#RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
#RUN chmod +x  $APP_HOME/entrypoint.prod.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R calendaronline:calendaronline $APP_HOME

# change to the app user
USER calendaronline

# CMD  gunicorn calendaronline.wsgi:application --bind 0.0.0.0:8000
CMD ./startup.prod.sh

