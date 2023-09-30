#!/bin/sh
gunicorn calendaronline.wsgi:application --bind 0.0.0.0:8001