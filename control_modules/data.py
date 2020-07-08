import os
import datetime
import subprocess
import shutil
import zipfile
import sys
from .settings import DATABASE, HOST_DATABASE, \
        SAVE_FOLDER, MEDIA_FOLDER, STATIC_FOLDER \
        

# Generic function(s), for all kind of mode (saving, restore, delete...)

def db_request():
    """
    Format command to be executed as subprocess.
    Add database settings into the query, and
    return the approriate string.
    """
    settings = {
        "USER" : os.environ["DJANGO_DB_USER"],
        "PASS" : os.environ["DJANGO_DB_PASS"],
        "PORT" : os.environ["DJANGO_DB_PORT"],
        "DATABASE" : DATABASE,
        "HOST" : HOST_DATABASE.strip(),
    }

    FORMAT_CONNEXION = "-u {USER} -p{PASS} -h {HOST} {DATABASE}"
    return (FORMAT_CONNEXION.format(**settings).split(" "))


# Save function(s)

def date_as_filename():
    #Retrieve and format current datetime
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y---%H-%M")

def save_images(save_zip):
    """
    Backup for website images. Store all generated images
    within the SAVE_FOLDER directory.
    """
    #Create the save directory if necessary
    save_dir_root = os.path.dirname(save_zip.filename)
    if os.path.exists(save_dir_root) is False:
        os.makedirs(save_dir_root)

    #Copy all files of the website in a new folder
    for directory, subdir, files in os.walk(MEDIA_FOLDER):
        for filename in files:
            filename = os.path.join(directory, filename)
            save_zip.write(filename, filename.replace(MEDIA_FOLDER, ""))

def save_db():
    """
    Save the database into the SAVE_FOLDER.
    Use the current time to generate filename.
    """
    #Isolated backup files in a zip files
    save_dir = os.path.join(SAVE_FOLDER, date_as_filename() + ".zip")

    with zipfile.ZipFile(save_dir, "w", compression=zipfile.ZIP_BZIP2) as save_zip:
        save_images(save_zip)

        #Get the database dumb and store it into the zipfile
        cmd = ["mysqldump"] + db_request()
        response = subprocess.check_output(cmd)

        #Format filename of sql backup
        save_file = "{}.sql".format(date_as_filename())
        #Save backup
        save_zip.writestr(save_file, response.decode())

        print("{}: Database and images saved".format(sys.argv[0]))

# Restore function(s)

def restore(args):
    """
    Delete current images of the website.
    Restore image and databases from a given zip file.
    """
    #Error verification for zip existance
    args.restore = os.path.abspath(args.restore)
    if not zipfile.is_zipfile(args.restore):
        err_msg = "{}: Please refer to a valid tar file."
        print(err_msg.format(sys.argv[0], file=sys.stderr))
        exit(1)

    #Remove current website folder for media
    if os.path.exists(MEDIA_FOLDER):
        shutil.rmtree(MEDIA_FOLDER)

    #Extract image from the zipfile
    with zipfile.ZipFile(args.restore) as zip_file:
        #Go through each filename available in the zipfile.
        #Skip sql files, retore the given filemane in MEDIA_FOLDER
        for zip_archive in zip_file.namelist():
            content = zip_file.read(zip_archive)
            if zip_archive.endswith(".sql"):
                restore_db(content)
                continue
            save_file = os.path.join(MEDIA_FOLDER, zip_archive)
            if not os.path.exists(os.path.dirname(save_file)):
                os.makedirs(os.path.dirname(save_file))
            with open(save_file, "wb") as Img:
                Img.write(content)
            new_file = MEDIA_FOLDER

    cmd = "chown -R www-data:www-data {}".format(MEDIA_FOLDER)
    subprocess.Popen(cmd, shell=True)

    print("{}: Images restaured.".format(sys.argv[0]))

def restore_db(content):
    """
    Use a given backup file to restore the database.
    Just load the given sql file into the db.
    """
    cmd = ["mysql"] + db_request()
    query = content.decode() + " ;"

    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    process.communicate(query.encode())
    process.wait()

    if process.returncode == 0:
        print("{}: Database restored.".format(sys.argv[0]))
    else:
        print("{}: Failure while loading database.".format(sys.argv[0]),
                file=sys.stderr)


# Deletion function(s)

def delete_db():
    """
    Delete all tables of the selected database.
    """
    cmd = ["mysql"] + db_request()
    query = "DROP DATABASE {0};CREATE DATABASE {0};".format(DATABASE)

    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    process.communicate(query.encode())
    process.wait()

    if process.returncode == 0:
        print("{}: Database {} deleted".format(sys.argv[0], DATABASE))
    else:
        print("{}: Failure while deleting database.".format(sys.argv[0]),
                file=sys.stderr)


# Setup function(s)

def setup_site():
    """
    Prepare the website to be deployed. Perform
    the first migration.
    """
    django_server = os.environ["DOCKER_APACHE_CONTAINER"]
    begin_cmd = "docker exec {} ./manage.py ".format(django_server)

    #Migration stuff
    cmd = begin_cmd + "makemigrations"
    subprocess.Popen(cmd.split(" ")).wait()
    cmd = begin_cmd + "migrate"
    subprocess.Popen(cmd.split(" ")).wait()

    msg = "{}: Website is ready to serve."
    print(msg.format(sys.argv[0]))

# Cleaning function(s)

def clean_site():
    if HOST_DATABASE:
        delete_db()
    rm_cmd = f"rm -rf {MEDIA_FOLDER}"
    subprocess.Popen(rm_cmd.split()).wait()

    rm_cmd = f"rm -rf {STATIC_FOLDER}"
    subprocess.Popen(rm_cmd.split()).wait()

    #Delete container
    docker_rm = "docker rm -f $(docker ps -qa)"
    subprocess.Popen(docker_rm, shell=True, stderr=subprocess.DEVNULL).wait()



