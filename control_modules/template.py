import os
import subprocess

class Template:
    """
    Hook for template file who need variable replacement
    from shell environnement.

    Create a rendered file from the given template.

    """
    EXTENSION = ".template"
    def __init__(self, template_filename):
        #Perform some check to get a valid template file.
        if not template_filename.endswith(self.EXTENSION):
            raise ValueError("Must have a file with .template extension")
        if not os.path.exists(template_filename):
            raise ValueError("Must have existing file")

        self.template_filename = template_filename

        #Get the filename of the rendered file, without
        #template extension.
        index_extension = len(template_filename) - len(self.EXTENSION)
        self.render_filename = template_filename[0:index_extension]

    def render(self):
        """
        Create rendered file from the template.
        """
        with open(self.render_filename, 'w') as stdout, \
                open(self.template_filename, 'r') as stdin:
            subprocess.check_call(["envsubst"], stdout=stdout,
                    stdin=stdin)

    @property
    def rendered_content(self):
        """
        Get content of the rendered file.
        """
        with open(self.render_filename) as rendered_file:
            return rendered_file.read()

    def __enter__(self):
        self.render()
        return self

    def __exit__(self, *args, **kwargs):
        pass
