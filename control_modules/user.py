import subprocess
import sys
import os
from control_modules.settings import DATABASE

class UserManager:
    """
    Control all about admin users.
    Have the ability to create, modify or delete an user.
    """
    @classmethod
    def launch(cls, action):
        """
        Perform the action expected by the controller.
        """
        if action == "create":
            cls.create_user()
        elif action == "change-password":
            cls.change_pass()
        elif action == "delete":
            cls.delete_user()
        elif action == "list":
            cls.list_users()

    @staticmethod
    def create_user():
        create_cmd = "docker exec -it {} ./manage.py createsuperuser"
        create_cmd = create_cmd.format(os.environ["DOCKER_APACHE_CONTAINER"])
        status = subprocess.Popen(create_cmd, shell=True).wait()
        if status == 0:
            print(f"{sys.argv[0]}: User created.")
        else:
            print(f"{sys.argv[0]}: User creation failed.",
                    file=sys.stderr)

    @staticmethod
    def change_pass():
        username = input("User to change password : ")
        change_cmd = "docker exec -it {} ./manage.py changepassword {}"
        change_cmd = change_cmd.format(os.environ["DOCKER_APACHE_CONTAINER"], username)
        status = subprocess.Popen(change_cmd, shell=True).wait()
        if status == 0:
            print(f"{sys.argv[0]}: {username} password changed")
        else:
            print(f"{sys.argv[0]}: Error to change {username} password",
                    file=sys.stderr)
        return status
    
    @staticmethod
    def delete_user():
        username = input("Name of the user to delete : ")
        deletion_script = """
from django.contrib.auth.models import User
try:
    User.objects.get(username='{}').delete()
    exit(0)
except User.DoesNotExist as error:
    exit(1)
        """.format(username)
        cmd = "docker exec {} ./manage.py shell -c \"{}\""
        cmd = cmd.format(os.environ["DOCKER_APACHE_CONTAINER"], deletion_script)
        status = subprocess.Popen(cmd, shell=True).wait()
        if status == 0:
            print(f"{sys.argv[0]}: User {username} deleted")
        else:
            print(f"{sys.argv[0]}: Error while deleting user {username}.")
        return status

    @staticmethod
    def list_users():
        listing_script = """
from django.contrib.auth.models import User

list_users = User.objects.all()
for user in list_users:
    print(user.username)
        """
        cmd = "docker exec {} ./manage.py shell -c \"{}\""
        cmd = cmd.format(os.environ["DOCKER_APACHE_CONTAINER"], listing_script)
        status = subprocess.Popen(cmd, shell=True).wait()
