FROM python:3.11-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc && \
    apt-get clean


COPY . .
RUN pip install --no-cache-dir -r requirements.txt



#ENTRYPOINT ["python", "manage.py"]
#CMD [ "runserver", "0.0.0.0:8000" ]
# CMD [ "collectstatic", "--noinput"]
# CMD ["uwsgi", "--ini", "/code/calendaronline.uwsgi.ini"]
CMD  ./startup.sh