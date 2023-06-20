#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from genericpath import isdir
from fabric.api import *
import os
import re

env.hosts = ["54.226.54.247","18.205.246.150"]
env.user = "ubuntu"
env.key = "~/.ssh/id_rsa"


def do_deploy(file_name):
    """Function to distribute an archive to your web servers"""
    if not os.path.exists(file_name):
        return False

    put(file_name, "/tmp/")
    filename = re.search(r'[^/]+$', file_name).group(0)
    folder = "/data/web_static/releases/{}/".format(os.path.splitext(
        filename)[0])
    run("mkdir -p {}".format(folder))
    run("tar -xzf /tmp/{} -C {}".format(filename, folder))
    run("rm /tmp/{}".format(filename))
    run("mv {}web_static/* {}".format(folder, folder))
    run("rm -rf {}web_static".format(folder))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(folder))

    if not isdir("/var/www/html/hbnb_static"):
        run("mkdir -p /var/www/html/hbnb_static")

    run("sudo cp -r /data/web_static/current/* /var/www/html/hbnb_static/")
    print("New version deployed")
    return True
