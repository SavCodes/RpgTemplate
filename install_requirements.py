import subprocess
import os
import sys


def install_requirements():
    # Check if the requirements.txt file exists
    if not os.path.isfile('requirements.txt'):
        print("requirements.txt not found. Please make sure the file is present.")
        sys.exit(1)

    # Install the packages listed in the requirements.txt file
    print("Installing dependencies from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


install_requirements()
