import bpy
import os
import site
import subprocess
import sys


# Ensure pip is installed
subprocess.check_call([sys.executable, "-m", "ensurepip"])
# Install the module in user mode
subprocess.check_call([sys.executable, "-m", "pip",
                      "install", "--user", "pyyaml"])
# Get the user-specific site-packages path
user_site_packages_path = site.getusersitepackages()
# Add the user site-packages path to sys.path
if user_site_packages_path not in sys.path:
    sys.path.append(user_site_packages_path)

path = os.path.join(os.path.dirname(bpy.data.filepath), "scripts")
if path not in sys.path:
    sys.path.append(path)


path = os.path.join(os.path.dirname(bpy.data.filepath), "scripts")
sys.path.append(path)
