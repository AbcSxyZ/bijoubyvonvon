#!/usr/bin/python3

"""
    control.py:

    Manager for the website. Single interface to manipulate
    the site from the host.

    - Run, stop and delete the server
    - Save, restore or delete the database and jewel images.
    - Manage TLS certificate

    See --help for more details.
"""

import os
import sys

# Control if we are root before moving on. Needed before importing
# extra modules.
if os.getuid() != 0:
    err_msg = "{}: Program must be run as root".format(sys.argv[0])
    print(err_msg, file=sys.stderr)
    exit(1)

import argparse

#Custom modules
from control_modules.data import db_request, restore, \
         save_db, setup_site, delete_db, clean_site

from control_modules.settings import DATABASE
from control_modules.tls import update_tls
from control_modules import DockerManager, UserManager


def option_parse():
    """
    See -h for details with argparse:
    """

    description = "Save, restore or delete the database {}.".format(DATABASE)
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--delete", "-d", action="store_true", 
            help="Delete the database {}.".format(DATABASE))
    parser.add_argument("--save", "-s", action="store_true", 
            help="Save the db to perform a backup.")
    parser.add_argument("--restore", "-r", metavar="tar_file",
            help="Use backup in tar file to restore image and database.")
    parser.add_argument("--setup-db", "-S", action="store_true",
            help="Initialise the database for django models.")
    parser.add_argument("--update-tls", "-u", action="store",
            nargs=1, choices=["test", "production"],
            help="Update tls certificate for the website.")
    parser.add_argument("--servers", action="store",
            nargs=1, choices=DockerManager.ALLOWED_COMMANDS,
            help="Manage all containers simultaneously.")
    parser.add_argument("--clean", "-c", action="store_true",
            help="Remove all files managed by the website.")
    parser.add_argument("--user", action="store",
            choices=["create", "change-password", "delete", "list"],
            help="Create admin or change passwords.")
    args = parser.parse_args()

    options = vars(args).values()
    check = [opt for opt in options if opt]
    if len(check) != 1:
        error = "{}: Need a single option, see --help."
        print(error.format(sys.argv[0]), file=sys.stderr)
        exit(1)
    return args

def main():
    ARGS = option_parse()

    if ARGS.save:
        save_db()
    elif ARGS.restore:
        restore(ARGS)
    elif ARGS.delete:
        delete_db()
    elif ARGS.setup_db:
        setup_site()
    elif ARGS.update_tls:
        update_tls(ARGS.update_tls)
    elif ARGS.servers:
        DockerManager(ARGS.servers[0])
    elif ARGS.clean:
        clean_site()
    elif ARGS.user:
        UserManager.launch(ARGS.user)




if __name__ == "__main__":
    main()


