import os
import subprocess
import shlex
import pwd

# Edit were storage for the sql database and images are made.

SAVE_FOLDER = "backup"
MEDIA_FOLDER = os.path.join(os.getcwd(), "django-site/media")
STATIC_FOLDER = os.path.join(os.getcwd(), "django-site/static")

# DO NOT EDIT CUSTOM CONFIG BELOW.
# Retrieve automatically some useful globals.
# Create expected folder in above settings to save data.

DATABASE = os.environ["DJANGO_DATABASE"]

def db_exist():
    """
    Depending whenever the program is launched, the container with
    sql database is running or not.
    """
    ps_query = f"name={os.environ['DOCKER_MYSQL_CONTAINER']}"
    ps_cmd = f'docker ps -q -f {ps_query}'
    ps_proc = subprocess.Popen(ps_cmd.split(), stdout=subprocess.PIPE)
    ps_proc.wait()
    res = ps_proc.stdout.read().decode().strip()
    return res

def create_media_folder():
    www_data_user = pwd.getpwnam("www-data")
    uid = www_data_user.pw_uid
    gid = www_data_user.pw_gid
    os.mkdir(MEDIA_FOLDER)
    os.chown(MEDIA_FOLDER, uid, gid)

#If the container with database already exists, retrieve
#his IP address
HOST_DATABASE = None
if HOST_DATABASE is None and db_exist():
    cmd = "docker inspect --format=" + \
            '"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" ' + \
            os.environ["DOCKER_MYSQL_CONTAINER"]

    HOST_DATABASE = subprocess.Popen(shlex.split(cmd), \
            stdout=subprocess.PIPE)
    HOST_DATABASE.wait()
    HOST_DATABASE = HOST_DATABASE.stdout.read().decode()

# Check if used folder exist, create them if necessary
if os.path.exists(SAVE_FOLDER) == False:
    os.system("mkdir -p " + SAVE_FOLDER)

if os.path.exists(MEDIA_FOLDER) is False:
    create_media_folder()

