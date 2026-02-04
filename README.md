# pdfcalendar
A simple tool to create beautiful photo calendars as PDF for self printing.

You could see it in action on [k51.de](https://k51.de)

## Deploy with docker compose
Create a docker-compose.yml 

```
services:
  calendaronline-nginx:
    image: ghcr.io/dpmpc/calendaronline-nginx:latest
    restart: always
    ports:
      - "8000:80"
    depends_on: 
      - calendaronline

  calendaronline:
    image: ghcr.io/dpmpc/calendaronline:latest
    restart: always
    environment:
      - CSRF_TRUSTED_ORIGINS=https://localhost:8000
```

## Used libraries
- [Python 3](https://www.python.org/)

- [Boostrap 5.3](https://getbootstrap.com/docs/5.3)
- [Cropper.js 1.6.2](https://fengyuanchen.github.io/cropperjs/)
- [django 6.0](https://docs.djangoproject.com/en/6.0/)
- [gunicorn 2.25](https://gunicorn.org/)
- [icalevents 0.3](https://github.com/jazzband/icalevents)
- [jQuery 4.0](https://api.jquery.com/category/version/3.7/)
- [nginx 1.29](https://nginx.org/)
- [orjson 3.11](https://github.com/ijl/orjson)
- [Pillow (PIL Fork) 12](https://pillow.readthedocs.io/en/stable/installation.html)#
- [PyFPDF/fpdf2 2.8](https://pyfpdf.github.io/fpdf2/index.html)


### Used fonts
- [Font Awesome 6.5](https://fontawesome.com/)
- Monsieur La Doulaise - Copyright 2011 Alejandro Paul
- Noto Sans Display - Copyright 2012 Google Inc.
- [Pacifico](https://github.com/googlefonts/Pacifico) - Copyright 2018 The Pacifico Project Authors
- [Purisa](https://linux.thai.net/projects/fonts-tlwg) - Copyright 2003, 2004 Poonlap Veerathanabutr 
- [Sawasdee](https://linux.thai.net/projects/fonts-tlwg) - Copyright 2007 Pol Udomwittayanukul
- [Tippa](http://www.catfonts.de ) - Copyright (c) 2015, CAT-Fonts, Peter Wiegel


# Developemnt
Start a developemnt envrionment by the following commands:
```
cd web
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DEBUG=1
python manage.py runserver
```
