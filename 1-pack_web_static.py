#!/usr/bin/python3
""" Compress before sending """
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """ Fabric script that generates a .tgz archive from the contents of the web_static"""
    file_name = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
          .format(file_name))
        return "versions/web_static_{}.tgz".format(file_name)

    except Exception as e:
        return None
