#!/bin/sh
python manage.py collectstatic --noinput  && uwsgi --ini calendaronline.uwsgi.ini