import subprocess
import os

def update_tls(mode):
    """
    Call update-tls.sh to update the tls certificate.
    Retrieve the filename and execute the script with
    the TEST_MODE variable set to True if it's for testing,
    False for real certificate.
    """
    module_dir = os.path.dirname(__file__)
    shell_script = os.path.join(module_dir, "update-tls.sh")
    test = mode[0] == "test"
    custom_env = {**os.environ, "TEST_MODE":str(test)}
    subprocess.Popen(shell_script, env=custom_env).wait()
