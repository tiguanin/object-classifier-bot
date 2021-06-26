import os
import sys

script_dir = os.path.dirname(__file__)

for subdir, dirs, files in os.walk(script_dir):
    for DIR in dirs:
        print(subdir + " " + DIR)
        sys.path.insert(0, os.path.join(subdir, DIR))
