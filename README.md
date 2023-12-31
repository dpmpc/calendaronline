# pdfcalendar
A simple tool to create beautiful photo calendars as PDF for self printing.

You could see it in action on [k51.de](https://k51.de)

## Deploy with docker compose
Create a docker-compose.yml 

```
version: "3.9"

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
- [django 5.0](https://docs.djangoproject.com/en/4.2/)
- [Boostrap 5.3](https://getbootstrap.com/docs/5.3)
- [PyFPDF/fpdf2 2.7](https://pyfpdf.github.io/fpdf2/index.html)
- [Pillow (PIL Fork) 10.2](https://pillow.readthedocs.io/en/stable/installation.html)
- [Cropper.js 1.6.1](https://fengyuanchen.github.io/cropperjs/)
- [gunicorn 2.21](https://gunicorn.org/)
- [NGINX 1.25](https://www.nginx.com/)
- [Font Awesome 6.5](https://fontawesome.com/)

