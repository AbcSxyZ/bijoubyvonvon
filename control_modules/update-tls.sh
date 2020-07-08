#!/bin/bash

APACHE_FOLDERS="./conf-apache/ ./matomo/apache2/"

# loadFile:
#
# Get the certificate and the private key within the container
# and save them in the apache configuration folder on the host.
loadFile()
{
    #Retrieve folder of certificate/key within the container.
    local certifDir="/etc/letsencrypt/live/"
    cmd="find $certifDir -type d -mindepth 1"
    certifDir=$(docker exec $DOCKER_CERTBOT_CONTAINER $cmd)

    # Get exact filename for the certif/key, both inside
    # the container, and on the host.
    local key cert hostKey hostCert

    key="$certifDir/privkey.pem"
    cert="$certifDir/cert.pem"
    for folder in $APACHE_FOLDERS
    do
        hostKey="${folder}/certif/key.pem"
        hostCert="${folder}/certif/certif.pem"

        # Finally cp container files to the host.
        docker cp -L $DOCKER_CERTBOT_CONTAINER:$key $hostKey
        docker cp -L $DOCKER_CERTBOT_CONTAINER:$cert $hostCert
    done
}

# Format -d options for certbot
# Get each domain (.fr/.com), with and without www.
formatCertbotDomainName()
{
    local domainOption;

    for domainName in $DOMAINS
    do
        domainOption="$domainOption -d $domainName -d www.$domainName "
    done
    echo $domainOption
}

#Couple of check before running prog

#Check if running with sudo
if [ "$(whoami)" != root ]
then
    echo "$0: Program must be launch with sudo." >&2
    exit 1
fi

#Remove apache to allow certbot creating the certificate
docker stop $DOCKER_APACHE_CONTAINER

#Launch certbot container
docker-compose up -d $DOCKER_CERTBOT_CONTAINER

# Command to create a new certificate
# CMD="certbot certonly --apache  $(formatCertbotDomainName)
#      -m $MAIL_USER --agree-tos --non-interactive"

# Command to update certificates
CMD="certbot renew"

# Add extra flag for tests (using letsencrypt sandbox)
[ "$TEST_MODE" = "True" ] && CMD="$CMD --staging"

# Generate certificate within the container
docker exec  $DOCKER_CERTBOT_CONTAINER $CMD

#Retrieve file within the container, and save them to the host
loadFile

# Remove certbot container and relaunch apache
docker stop $DOCKER_CERTBOT_CONTAINER
docker start $DOCKER_APACHE_CONTAINER
