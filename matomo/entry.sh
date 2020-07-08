mv composer.phar matomo/;
(cd matomo && php composer.phar install --no-dev)
apache2ctl -D FOREGROUND
