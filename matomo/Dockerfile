FROM debian:9

RUN apt update

#Custom software
RUN apt install -y wget unzip sudo gnupg

# Webserver related install
RUN apt install -y apache2 libapache2-mod-php

# apt dependency to install php 7.2
RUN wget -q https://packages.sury.org/php/apt.gpg -O- | apt-key add -
RUN echo "deb https://packages.sury.org/php/ stretch main" | tee /etc/apt/sources.list.d/php.list
RUN apt install -y ca-certificates apt-transport-https
RUN apt update

RUN apt install -y php7.2 php7.2-curl php7.2-gd \
    php 7.2-cli php7.2-mysql php7.2-xml php7.2-mbstring

RUN a2dismod php7.0
RUN a2enmod ssl http2

#Matomo installation

#Prepare matomo session
RUN mkdir /home/matomo && chown www-data:www-data /home/matomo

WORKDIR /home/matomo

RUN wget https://builds.matomo.org/matomo.zip && unzip matomo.zip
RUN chown -R www-data:www-data matomo

#clean matomo
RUN rm -rf matomo.zip 

RUN apt install -y curl git

#Fast fix to install matomo utils, to avoid rebuild img

RUN curl -s https://getcomposer.org/installer | php 

COPY entry.sh .

# ENTRYPOINT ["bash"]
ENTRYPOINT ["bash", "entry.sh"]
