FROM debian:9

RUN apt update
RUN apt install -y certbot python-certbot-apache

EXPOSE 80

ENTRYPOINT ["bash", "-c"]
CMD ["apache2ctl -D FOREGROUND"]
