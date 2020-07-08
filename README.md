# README

**Website** : https://bijoubijoubyvonvon.com/

Information about the website configuration and manipulation.

## Default configurations

Configure an `env` file from the `env.template`:
- Change password/username settings for database
- Change django secret key
- Configure `MAIL_*` variables to send mail
- Change `DOMAINS` variable to match your domains name (local or not)

You must `source env` to export all variables to your shell environment.

**+ For the production, you must add some firewall, `ufw`, `fail2ban` etc.**

## Control with `control.py`

Main commands are grouped in control.py. See the help menu `--help` to list commands.
For more specific usage, please refer to the used tool (Docker, apache etc.).

`control.py` must be run as a root, and must have environnement variable
from `env` file. Think to `sudo -E` to herite your environnement as sudoer.

### Grant rights to django

Some folder/files must by owned by the django server, run :

`sudo chown -R www-data:www-data log-apache django-site/custom-media django-site/description.txt`

### Steps to run the server

1. `source env` : get your environnement variables.
2. `sudo -E ./control.py --servers setup`: Launch apache and mysql container.

__*Now, Wait a minute to let maria database perform his initialization.*__

3. `sudo -E ./control.py --setup` : Migrate django models.
4. `sudo -E ./control.py --user create` : Create a new admin

The website is ready to serve.

Use `sudo -E ./control.py --clean` to remove the website/containers/data.

### Different control type

- `./control.py` allow multiple action with the `--servers` option : start, stop, rm, restart. Each command correspond to a docker action.
- `./control.py` use `--user` option to create, delete or change password of a django admin.
- `./control.py` use `--update-tls` to manage the TLS certificate. Use `test` for testing purpose, and `production` so get certificate signed by Let's Encrypt.

### Data management

- To save the database and images of the website in zip format: : `./control.py --save  
- To load database and image from a zipfile : `./control.py --restore backup_file.zip`
