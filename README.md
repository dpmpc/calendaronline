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
- [django 5.2](https://docs.djangoproject.com/en/5.2/)
- [Boostrap 5.3](https://getbootstrap.com/docs/5.3)
- [jQuery 3.7.1](https://api.jquery.com/category/version/3.7/)
- [PyFPDF/fpdf2 2.8](https://pyfpdf.github.io/fpdf2/index.html)
- [Pillow (PIL Fork) 11](https://pillow.readthedocs.io/en/stable/installation.html)
- [Cropper.js 1.6.2](https://fengyuanchen.github.io/cropperjs/)
- [gunicorn 2.23](https://gunicorn.org/)
- [NGINX 1.29](https://www.nginx.com/)
- [Font Awesome 6.5](https://fontawesome.com/)

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
