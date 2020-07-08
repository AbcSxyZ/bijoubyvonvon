import subprocess
import os

from .template import Template

class DockerManager:
    """
    Interface for manipulation of docker container.
    Getting standard container manipulation, indicated in SUBCOMMANDS.
    Is also an interface for Dockerfile + docker-compose to launch
    the website.
    """
    SUBCOMMANDS = ["start", "stop", "restart", "rm"]
    ALLOWED_COMMANDS = SUBCOMMANDS + ["setup"]

    def __init__(self, action):
        #Manager created once, with a single action of ALLOWED_COMMANDS
        self.action = action

        #store container names, get them from
        #environnement variables like DOCKER_XYZ_CONTAINER
        self.list_app = [
                'matomo',
                'apache',
                'mysql',
                ]
        for app_name in self.list_app:
            variable = "DOCKER_{}_CONTAINER".format(app_name.upper())
            setattr(self, app_name, os.environ[variable])

        #Create generic function for SUBCOMMANDS
        #DockerManager is getting one method for each command.
        for command in self.SUBCOMMANDS:
            setattr(self, command, self._generic_commands(command))

        #Perform the expected action of the created DockerManager
        self.manager_runner()

    def _generic_commands(self, command):
        """
        Create function to run docker with SUBCOMMANDS actions.
        Juste change the docker command for each of them.
        """
        cmd = "docker {} ".format(command) + "{}"

        def run_generic():
            for app_name in self.list_app:
                container_name = getattr(self, app_name)
                argv = cmd.format(container_name).split(" ")
                subprocess.Popen(argv).wait()

        return run_generic

    def setup(self):
        """
        Launch apache and mysql container for the first time.
        Retrieve static files structured by django to serve it.
        """
        # Launch container with "docker-compose up", avoid to launch
        # certbot, will be used independently.
        compose_up_cmd = "docker-compose up --scale certbot=0 -d"
        with Template("db_init.sql.template"):
            res = subprocess.Popen(compose_up_cmd.split(" "))
            res.wait()

        # Go to collect static files with django
        if res.returncode == 0:
            collect_cmd = "docker exec {} ./manage.py collectstatic " + \
                    "--noinput"
            collect_cmd = collect_cmd.format(self.apache)
            res = subprocess.Popen(collect_cmd.split(" "))
            res.wait()
        
        return res.returncode


    def manager_runner(self):
        # Run docker standard commands in SUBCOMMANDS
        if self.action in self.SUBCOMMANDS:
            cmd = getattr(self, self.action)
            cmd()

        # Launch for the first time servers with docker-compose
        elif self.action == "setup":
            self.setup()
