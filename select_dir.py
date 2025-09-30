import os
base_dir = '/home/USER/share/_PROJECTS/DB_TEST/DB_TEST-RTM-026'

def base_directory():
    for roots, dirs, files in os.walk(base_dir):
        return base_dir
    