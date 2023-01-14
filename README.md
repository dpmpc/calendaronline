# pdfcalendar
A simple tool to create beautiful photo calendars as PDF for self printing.

You could see it in action on [k51.de](https://k51.de)

## Deploy with docker compose
Create a docker-compose.yml 

```
version: "3.9"

services:
  calendaronline-nginx:
    image: dschlich/calendaronline-nginx:latest
    restart: always
    volumes:
      - uwsgi_data:/tmp/uwsgi/
      - web_static:/var/www/calendaronline/assets/:ro
    ports:
      - "8000:80"
    depends_on: 
      - calendaronlinie

  calendaronlinie:
    image: dschlich/calendaronline:latest
    restart: always
    volumes:
      - uwsgi_data:/tmp/uwsgi/
      - web_static:/static/

volumes:
  uwsgi_data:
  web_static:
```

## Used libraries
- [Python 3](https://www.python.org/)
- [django 4.1](https://docs.djangoproject.com/en/4.1/)
- [Boostrap 5.3](https://getbootstrap.com/docs/5.3)
- [PyFPDF/fpdf2 2.6](https://pyfpdf.github.io/fpdf2/index.html)
- [Pillow (PIL Fork)](https://pillow.readthedocs.io/en/stable/installation.html)
- [Cropper.js 1.5.13](https://fengyuanchen.github.io/cropperjs/)

