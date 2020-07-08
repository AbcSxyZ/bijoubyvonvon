FROM debian:9

RUN apt update

#Install apache
RUN apt install -y apache2 apache2-dev libapache2-mod-wsgi-py3 \
                    default-libmysqlclient-dev mariadb-client

#Install python3 and utils.
RUN apt install -y python3 python3-pip

#Install python packages
RUN pip3 install django==2.2.9 mysqlclient Pillow

#Setup mod_wsgi
WORKDIR /root/mod_wsgi
RUN curl -L https://github.com/GrahamDumpleton/mod_wsgi/archive/4.6.5.tar.gz -o mod_wsgi.tar.gz 
RUN tar -xvf mod_wsgi.tar.gz && \
    cd mod_wsgi-* && \
    ./configure --with-python=$(which python3) && \
    make && \
    make install

RUN a2enmod rewrite ssl http2

WORKDIR /var/www/

ENTRYPOINT ["apache2ctl", "-D", "FOREGROUND"]
