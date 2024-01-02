FROM nginx:latest

COPY *conf /etc/nginx/
COPY ./static /static/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]